package com.kanemullett.service;

import java.util.List;

import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Service;
import org.springframework.web.server.ResponseStatusException;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.kanemullett.model.Column;
import com.kanemullett.model.DatabaseRecord;
import com.kanemullett.model.ImmutableColumn;
import com.kanemullett.model.ImmutableKnockoutTemplate;
import com.kanemullett.model.ImmutableLeagueTemplate;
import com.kanemullett.model.ImmutableQueryCondition;
import com.kanemullett.model.ImmutableQueryRequest;
import com.kanemullett.model.ImmutableTournamentTemplate;
import com.kanemullett.model.ImmutableUpdateRequest;
import com.kanemullett.model.KnockoutTemplate;
import com.kanemullett.model.LeagueTemplate;
import com.kanemullett.model.QueryCondition;
import com.kanemullett.model.QueryConditionGroup;
import com.kanemullett.model.QueryRequest;
import com.kanemullett.model.QueryResponse;
import com.kanemullett.model.RoundTemplate;
import com.kanemullett.model.Table;
import com.kanemullett.model.TableJoin;
import com.kanemullett.model.Tournament;
import com.kanemullett.model.TournamentTemplate;
import com.kanemullett.model.TournamentTemplateRecord;
import com.kanemullett.model.UpdateRequest;
import com.kanemullett.model.type.ConditionOperator;
import com.kanemullett.model.type.JoinType;
import com.kanemullett.model.type.SqlOperator;
import com.kanemullett.util.DatabaseConstants;
import com.kanemullett.util.PredictorConstants;

import jakarta.annotation.Nullable;

@Service
public class TournamentTemplateService {

    private final DatabaseQueryService queryService;

    private final ObjectMapper mapper = new ObjectMapper();

    private static final String TOURNAMENT_TEMPLATES_TABLE_ALIAS = "tt";
    private static final String LEAGUE_TEMPLATES_TABLE_ALIAS = "lt";
    private static final String KNOCKOUT_TEMPLATES_TABLE_ALIAS = "kt";

    private static final String TOURNAMENT_TEMPLATE_NAME_COLUMN = "tournamentTemplateName";
    private static final String LEAGUE_TEMPLATE_NAME_COLUMN = "leagueTemplateName";
    private static final String KNOCKOUT_TEMPLATE_NAME_COLUMN = "knockoutTemplateName";

    public TournamentTemplateService(DatabaseQueryService queryService) {
        this.queryService = queryService;
    }

    public List<TournamentTemplate> getTournamentTemplates() {
        return getTournamentTemplates(null);
    }

    public List<TournamentTemplate> createTournamentTemplates(List<TournamentTemplateRecord> tournamentTemplates) {
        final UpdateRequest<TournamentTemplateRecord> updateRequest = ImmutableUpdateRequest.<TournamentTemplateRecord>builder()
            .operation(SqlOperator.INSERT)
            .table(Table.of(PredictorConstants.PREDICTOR_SCHEMA, TournamentTemplateRecord.TARGET_TABLE))
            .records(tournamentTemplates)
            .build();

        queryService.updateRecords(updateRequest);

        return getTournamentTemplates(QueryConditionGroup.of(
            ImmutableQueryCondition.builder()
                .column(Column.of(DatabaseConstants.ID))
                .operator(ConditionOperator.IN)
                .value(tournamentTemplates.stream()
                    .map(TournamentTemplateRecord::getId)
                    .toList())
                .build()
        ));
    }

    public TournamentTemplate getTournamentTemplateById(String tournamentTemplateId) {
        final QueryConditionGroup conditionGroup = QueryConditionGroup.of(
            QueryCondition.of(
                Column.of(DatabaseConstants.ID),
                tournamentTemplateId
            )
        );

        final List<TournamentTemplate> tournamentTemplates = getTournamentTemplates(conditionGroup);

        if (tournamentTemplates.isEmpty()) {
            throw new ResponseStatusException(HttpStatus.NOT_FOUND, "No tournament templates found with a matching id.");
        }

        return tournamentTemplates.get(0);
    }

    public void deleteTournamentTemplateById(String tournamentTemplateId) {
        final QueryRequest<Tournament> queryRequest = ImmutableQueryRequest.<Tournament>builder()
            .table(Table.of(PredictorConstants.PREDICTOR_SCHEMA, Tournament.TARGET_TABLE))
            .conditionGroup(QueryConditionGroup.of(
                QueryCondition.of(
                    Column.of(Tournament.TEMPLATE_ID_COLUMN),
                    tournamentTemplateId
                )
            ))
            .recordClass(Tournament.class)
            .build();
        
        final QueryResponse<Tournament> response = queryService.retrieveRecords(queryRequest);

        if (response.getRecordCount() > 0) {
            throw new ResponseStatusException(HttpStatus.CONFLICT, "Cannot delete tournament template as it is part of an existing tournament.");
        }

        final UpdateRequest<TournamentTemplateRecord> updateRequest = ImmutableUpdateRequest.<TournamentTemplateRecord>builder()
            .operation(SqlOperator.DELETE)
            .table(Table.of(PredictorConstants.PREDICTOR_SCHEMA, TournamentTemplateRecord.TARGET_TABLE))
            .conditionGroup(QueryConditionGroup.of(
                QueryCondition.of(
                    Column.of(DatabaseConstants.ID),
                    tournamentTemplateId
                )
            ))
            .build();

        queryService.updateRecords(updateRequest);

    }

    private List<TournamentTemplate> getTournamentTemplates(@Nullable QueryConditionGroup conditionGroup) {
        final ImmutableQueryRequest.Builder<DatabaseRecord> queryRequest = ImmutableQueryRequest.builder()
            .columns(List.of(
                Column.of(TOURNAMENT_TEMPLATES_TABLE_ALIAS, DatabaseConstants.ID),
                ImmutableColumn.builder()
                    .parts(List.of(TOURNAMENT_TEMPLATES_TABLE_ALIAS, TournamentTemplateRecord.NAME_COLUMN))
                    .alias(TOURNAMENT_TEMPLATE_NAME_COLUMN)
                    .build(),
                Column.of(TOURNAMENT_TEMPLATES_TABLE_ALIAS, TournamentTemplateRecord.LEAGUE_TEMPLATE_ID_COLUMN),
                ImmutableColumn.builder()
                    .parts(List.of(LEAGUE_TEMPLATES_TABLE_ALIAS, LeagueTemplate.NAME_COLUMN))
                    .alias(LEAGUE_TEMPLATE_NAME_COLUMN)
                    .build(),
                Column.of(LEAGUE_TEMPLATES_TABLE_ALIAS, LeagueTemplate.GROUP_COUNT_COLUMN),
                Column.of(LEAGUE_TEMPLATES_TABLE_ALIAS, LeagueTemplate.TEAMS_PER_GROUP_COLUMN),
                Column.of(LEAGUE_TEMPLATES_TABLE_ALIAS, LeagueTemplate.HOME_AND_AWAY_COLUMN),
                ImmutableColumn.builder()
                    .parts(List.of(KNOCKOUT_TEMPLATES_TABLE_ALIAS, KnockoutTemplate.NAME_COLUMN))
                    .alias(KNOCKOUT_TEMPLATE_NAME_COLUMN)
                    .build(),
                Column.of(KNOCKOUT_TEMPLATES_TABLE_ALIAS, KnockoutTemplate.ROUNDS_COLUMN)
            ))
            .table(Table.of(PredictorConstants.PREDICTOR_SCHEMA, TournamentTemplateRecord.TARGET_TABLE, TOURNAMENT_TEMPLATES_TABLE_ALIAS))
            .joins(List.of(
                TableJoin.of(
                    Table.of(PredictorConstants.PREDICTOR_SCHEMA, LeagueTemplate.TARGET_TABLE, LEAGUE_TEMPLATES_TABLE_ALIAS),
                    QueryCondition.of(
                        Column.of(TOURNAMENT_TEMPLATES_TABLE_ALIAS, TournamentTemplateRecord.LEAGUE_TEMPLATE_ID_COLUMN),
                        Column.of(LEAGUE_TEMPLATES_TABLE_ALIAS, DatabaseConstants.ID)
                    ),
                    JoinType.LEFT
                ),
                TableJoin.of(
                    Table.of(PredictorConstants.PREDICTOR_SCHEMA, KnockoutTemplate.TARGET_TABLE, KNOCKOUT_TEMPLATES_TABLE_ALIAS), 
                    QueryCondition.of(
                        Column.of(TOURNAMENT_TEMPLATES_TABLE_ALIAS, TournamentTemplateRecord.KNOCKOUT_TEMPLATE_ID_COLUMN),
                        Column.of(KNOCKOUT_TEMPLATES_TABLE_ALIAS, DatabaseConstants.ID)
                    ),
                    JoinType.LEFT
                )
            ))
            .recordClass(DatabaseRecord.class);

        if (conditionGroup != null) {
            queryRequest.conditionGroup(conditionGroup);
        }

        final QueryResponse<DatabaseRecord> queryResponse = queryService.retrieveRecords(queryRequest.build());

        return queryResponse.getRecords().stream()
            .map(this::buildTournamentTemplate)
            .toList();
    }

    private TournamentTemplate buildTournamentTemplate(DatabaseRecord databaseRecord) {
        final ImmutableTournamentTemplate.Builder builder = ImmutableTournamentTemplate.builder()
            .id(databaseRecord.getId())
            .name((String) databaseRecord.getData().get(TOURNAMENT_TEMPLATE_NAME_COLUMN));

        final String leagueId = (String) databaseRecord.getData().get(TournamentTemplateRecord.LEAGUE_TEMPLATE_ID_COLUMN);
        if (leagueId != null) {
            builder.league(ImmutableLeagueTemplate.builder()
                .id(leagueId)
                .name((String) databaseRecord.getData().get(LEAGUE_TEMPLATE_NAME_COLUMN))
                .groupCount((Integer) databaseRecord.getData().get(LeagueTemplate.GROUP_COUNT_COLUMN))
                .teamsPerGroup((Integer) databaseRecord.getData().get(LeagueTemplate.TEAMS_PER_GROUP_COLUMN))
                .homeAndAway((Boolean) databaseRecord.getData().get(LeagueTemplate.HOME_AND_AWAY_COLUMN))
                .build());
        }

        final String knockoutId = (String) databaseRecord.getData().get(TournamentTemplateRecord.KNOCKOUT_TEMPLATE_ID_COLUMN);
        if (knockoutId != null) {
            builder.knockout(ImmutableKnockoutTemplate.builder()
                .id(knockoutId)
                .name((String) databaseRecord.getData().get(KNOCKOUT_TEMPLATE_NAME_COLUMN))
                .rounds(parseRounds(databaseRecord.getData().get(KnockoutTemplate.ROUNDS_COLUMN)))
                .build());
        }

        return builder.build();
    }

    private List<RoundTemplate> parseRounds(Object rawValue) {
        if (rawValue == null) {
            return null;
        }
        try {
            return mapper.readValue(rawValue.toString(), new TypeReference<List<RoundTemplate>>() {});
        } catch (JsonProcessingException e) {
            throw new IllegalStateException("Unable to parse rounds JSON: " + rawValue, e);
        }
    }
}
