package com.kanemullett.service;

import java.util.List;
import java.util.Map;
import java.util.function.Function;
import java.util.stream.Collectors;
import java.util.stream.IntStream;
import java.util.stream.Stream;

import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Service;
import org.springframework.web.server.ResponseStatusException;

import com.kanemullett.model.Column;
import com.kanemullett.model.GroupRecord;
import com.kanemullett.model.GroupTeam;
import com.kanemullett.model.ImmutableGroupRecord;
import com.kanemullett.model.ImmutableMatchRecord;
import com.kanemullett.model.ImmutableQueryCondition;
import com.kanemullett.model.ImmutableQueryRequest;
import com.kanemullett.model.ImmutableUpdateRequest;
import com.kanemullett.model.KnockoutTemplate;
import com.kanemullett.model.LeagueTemplate;
import com.kanemullett.model.MatchRecord;
import com.kanemullett.model.QueryCondition;
import com.kanemullett.model.QueryConditionGroup;
import com.kanemullett.model.QueryRequest;
import com.kanemullett.model.QueryResponse;
import com.kanemullett.model.Result;
import com.kanemullett.model.Round;
import com.kanemullett.model.Table;
import com.kanemullett.model.TableDefinition;
import com.kanemullett.model.Tournament;
import com.kanemullett.model.TournamentTemplate;
import com.kanemullett.model.TournamentUpdate;
import com.kanemullett.model.UpdateRequest;
import com.kanemullett.model.type.ConditionOperator;
import com.kanemullett.model.type.SqlOperator;
import com.kanemullett.util.DatabaseConstants;
import com.kanemullett.util.PredictorConstants;

@Service
public class TournamentService {

    private final DatabaseQueryService queryService;
    private final DatabaseTableService tableService;
    private final TournamentTemplateService tournamentTemplateService;

    public TournamentService(
            DatabaseQueryService queryService,
            DatabaseTableService tableService,
            TournamentTemplateService tournamentTemplateService) {
        this.queryService = queryService;
        this.tableService = tableService;
        this.tournamentTemplateService = tournamentTemplateService;
    }

    public List<Tournament> getTournaments() {
        final QueryRequest<Tournament> queryRequest = ImmutableQueryRequest.<Tournament>builder()
            .table(Table.of(PredictorConstants.PREDICTOR_SCHEMA, Tournament.TARGET_TABLE))
            .recordClass(Tournament.class)
            .build();

        final QueryResponse<Tournament> queryResponse = queryService.retrieveRecords(queryRequest);

        return queryResponse.getRecords();
    }

    public List<Tournament> createTournaments(List<Tournament> tournaments) {
        final UpdateRequest<Tournament> updateRequest = ImmutableUpdateRequest.<Tournament>builder()
            .operation(SqlOperator.INSERT)
            .table(Table.of(PredictorConstants.PREDICTOR_SCHEMA, Tournament.TARGET_TABLE))
            .records(tournaments)
            .build();

        queryService.updateRecords(updateRequest);

        final List<String> templateIds = tournaments.stream()
            .map(Tournament::getTemplateId)
            .distinct()
            .toList();

        final Map<String, TournamentTemplate> templatesById = tournamentTemplateService.getTournamentTemplates().stream()
            .filter(template -> templateIds.contains(template.getId()))
            .collect(Collectors.toMap(TournamentTemplate::getId, Function.identity()));

        final Map<String, TournamentTemplate> tournamentTemplateMap = tournaments.stream()
            .collect(Collectors.toMap(
                Tournament::getId,
                tournament -> templatesById.get(tournament.getTemplateId())
            ));

        tournamentTemplateMap.forEach((tournamentId, tournamentTemplate) -> {
            final TableDefinition matchTable = MatchRecord.getTableDefinition(tournamentId);
            tableService.createTable(matchTable);

            final TableDefinition resultTable = Result.getTableDefinition(tournamentId);
            tableService.createTable(resultTable);

            if (tournamentTemplate.getLeague() != null) {
                createGroupTables(tournamentId, tournamentTemplate.getLeague());
            }

            if (tournamentTemplate.getKnockout() != null) {
                createRoundTables(tournamentId, tournamentTemplate.getKnockout());
            }
        });

        return tournaments;
    }

    public List<Tournament> updateTournaments(List<TournamentUpdate> tournamentUpdates) {
        final UpdateRequest<TournamentUpdate> updateRequest = ImmutableUpdateRequest.<TournamentUpdate>builder()
            .operation(SqlOperator.UPDATE)
            .table(Table.of(PredictorConstants.PREDICTOR_SCHEMA, Tournament.TARGET_TABLE))
            .records(tournamentUpdates)
            .build();

        queryService.updateRecords(updateRequest);

        final List<String> includedIds = tournamentUpdates.stream()
            .map(TournamentUpdate::getId)
            .toList();

        final QueryRequest<Tournament> queryRequest = ImmutableQueryRequest.<Tournament>builder()
            .table(Table.of(PredictorConstants.PREDICTOR_SCHEMA, Tournament.TARGET_TABLE))
            .conditionGroup(QueryConditionGroup.of(
                ImmutableQueryCondition.builder()
                    .column(Column.of(DatabaseConstants.ID))
                    .operator(ConditionOperator.IN)
                    .value(includedIds)
                    .build()
            ))
            .recordClass(Tournament.class)
            .build();

        final QueryResponse<Tournament> queryResponse = queryService.retrieveRecords(queryRequest);

        return queryResponse.getRecords();
    }

    public Tournament getTournamentById(String tournamentId) {
        final QueryRequest<Tournament> queryRequest = ImmutableQueryRequest.<Tournament>builder()
            .table(Table.of(PredictorConstants.PREDICTOR_SCHEMA, Tournament.TARGET_TABLE))
            .conditionGroup(QueryConditionGroup.of(
                QueryCondition.of(
                    Column.of(DatabaseConstants.ID),
                    tournamentId
                )
            ))
            .recordClass(Tournament.class)
            .build();

        final QueryResponse<Tournament> queryResponse = queryService.retrieveRecords(queryRequest);

        if (queryResponse.getRecordCount() == 0) {
            throw new ResponseStatusException(HttpStatus.NOT_FOUND, "No tournaments found with a matching id.");
        }

        return queryResponse.getRecords().get(0);
    }

    public void deleteTournamentById(String tournamentId) {
        deleteTournamentTables(tournamentId);

        final UpdateRequest<Tournament> updateRequest = ImmutableUpdateRequest.<Tournament>builder()
            .operation(SqlOperator.DELETE)
            .table(Table.of(PredictorConstants.PREDICTOR_SCHEMA, Tournament.TARGET_TABLE))
            .conditionGroup(QueryConditionGroup.of(
                QueryCondition.of(
                    Column.of(DatabaseConstants.ID),
                    tournamentId
                )
            ))
            .build();

        queryService.updateRecords(updateRequest);
    }

    private void createGroupTables(String tournamentId, LeagueTemplate leagueTemplate) {
        final TableDefinition groupTable = GroupRecord.getTableDefinition(tournamentId);
        tableService.createTable(groupTable);

        final TableDefinition groupTeamTable = GroupTeam.getTableDefinition(tournamentId);
        tableService.createTable(groupTeamTable);

        createGroups(tournamentId, leagueTemplate);
    }

    private void createGroups(String tournamentId, LeagueTemplate leagueTemplate) {
        final List<GroupRecord> generatedGroups = generateGroups(leagueTemplate.getGroupCount());

        final UpdateRequest<GroupRecord> groupUpdateRequest = ImmutableUpdateRequest.<GroupRecord>builder()
            .operation(SqlOperator.INSERT)
            .table(Table.of(PredictorConstants.PREDICTOR_SCHEMA, GroupRecord.getTargetTable(tournamentId)))
            .records(generatedGroups)
            .build();

        queryService.updateRecords(groupUpdateRequest);

        final List<MatchRecord> generatedMatches = generatedGroups.stream()
            .flatMap(group -> generateGroupMatches(group.getId(), leagueTemplate.getTeamsPerGroup(), leagueTemplate.getHomeAndAway()))
            .toList();

        final UpdateRequest<MatchRecord> matchUpdateRequest = ImmutableUpdateRequest.<MatchRecord>builder()
            .operation(SqlOperator.INSERT)
            .table(Table.of(PredictorConstants.PREDICTOR_SCHEMA, MatchRecord.getTargetTable(tournamentId)))
            .records(generatedMatches)
            .build();

        queryService.updateRecords(matchUpdateRequest);
    }

    private static List<GroupRecord> generateGroups(int groupCount) {
        return IntStream.range(0, groupCount)
            .mapToObj(i -> (GroupRecord) ImmutableGroupRecord.builder()
                .name("Group " + (char) ('A' + i))
                .build())
            .toList();
    }

    private Stream<MatchRecord> generateGroupMatches(String groupId, int teamsPerGroup, boolean homeAndAway) {
        return IntStream.rangeClosed(1, calculateTotalGameDays(teamsPerGroup, homeAndAway))
            .boxed()
            .flatMap(gameDay -> Stream.generate(() -> (MatchRecord) ImmutableMatchRecord.builder()
                    .groupMatchDay(gameDay)
                    .groupId(groupId)
                    .build())
                .limit(calculateMatchesPerGameDay(teamsPerGroup)));
    }

    private static int calculateMatchesPerGameDay(int teamCount) {
        return teamCount / 2;
    }

    private static int calculateTotalGameDays(int teamCount, boolean homeAndAway) {
        final int multiplier = homeAndAway ? 2 : 1;

        return (teamCount - 1) * multiplier;
    }

    private void createRoundTables(String tournamentId, KnockoutTemplate knockoutTemplate) {
        final TableDefinition roundTable = Round.getTableDefinition(tournamentId);
        tableService.createTable(roundTable);

        createRounds(tournamentId, knockoutTemplate);
    }

    private void createRounds(String tournamentId, KnockoutTemplate knockoutTemplate) {
        final List<Round> rounds = knockoutTemplate.getRounds().stream()
            .map(Round::of)
            .toList();

        final UpdateRequest<Round> roundUpdateRequest = ImmutableUpdateRequest.<Round>builder()
            .operation(SqlOperator.INSERT)
            .table(Table.of(PredictorConstants.PREDICTOR_SCHEMA, Round.getTargetTable(tournamentId)))
            .records(rounds)
            .build();

        queryService.updateRecords(roundUpdateRequest);

        final List<MatchRecord> generatedMatches = rounds.stream()
            .flatMap(round -> generateRoundMatches(round.getId(), round.getTeamCount()))
            .toList();

        final UpdateRequest<MatchRecord> matchUpdateRequest = ImmutableUpdateRequest.<MatchRecord>builder()
            .operation(SqlOperator.INSERT)
            .table(Table.of(PredictorConstants.PREDICTOR_SCHEMA, MatchRecord.getTargetTable(tournamentId)))
            .records(generatedMatches)
            .build();

        queryService.updateRecords(matchUpdateRequest);
    }

    private Stream<MatchRecord> generateRoundMatches(String roundId, int teamCount) {
        return Stream.generate(() -> (MatchRecord) ImmutableMatchRecord.builder()
                .roundId(roundId)
                .build())
            .limit(calculateMatchesPerGameDay(teamCount));
    }

    private void deleteTournamentTables(String tournamentId) {
        tableService.deleteTable(Table.of(PredictorConstants.PREDICTOR_SCHEMA, MatchRecord.getTargetTable(tournamentId)));
        tableService.deleteTable(Table.of(PredictorConstants.PREDICTOR_SCHEMA, Result.getTargetTable(tournamentId)));
        tableService.deleteTable(Table.of(PredictorConstants.PREDICTOR_SCHEMA, GroupRecord.getTargetTable(tournamentId)));
        tableService.deleteTable(Table.of(PredictorConstants.PREDICTOR_SCHEMA, GroupTeam.getTargetTable(tournamentId)));
        tableService.deleteTable(Table.of(PredictorConstants.PREDICTOR_SCHEMA, Round.getTargetTable(tournamentId)));
    }
}
