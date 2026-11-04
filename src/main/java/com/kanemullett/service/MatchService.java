package com.kanemullett.service;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Service;
import org.springframework.web.server.ResponseStatusException;

import com.kanemullett.function.MatchBuilderFunction;
import com.kanemullett.model.Column;
import com.kanemullett.model.DatabaseRecord;
import com.kanemullett.model.GroupRecord;
import com.kanemullett.model.ImmutableColumn;
import com.kanemullett.model.ImmutableQueryCondition;
import com.kanemullett.model.ImmutableQueryConditionGroup;
import com.kanemullett.model.ImmutableQueryRequest;
import com.kanemullett.model.ImmutableUpdateRequest;
import com.kanemullett.model.Match;
import com.kanemullett.model.MatchRecord;
import com.kanemullett.model.MatchUpdate;
import com.kanemullett.model.OrderBy;
import com.kanemullett.model.QueryCondition;
import com.kanemullett.model.QueryRequest;
import com.kanemullett.model.QueryResponse;
import com.kanemullett.model.Result;
import com.kanemullett.model.Round;
import com.kanemullett.model.Table;
import com.kanemullett.model.TableJoin;
import com.kanemullett.model.Team;
import com.kanemullett.model.UpdateRequest;
import com.kanemullett.model.type.ConditionJoin;
import com.kanemullett.model.type.ConditionOperator;
import com.kanemullett.model.type.JoinType;
import com.kanemullett.model.type.SqlOperator;
import com.kanemullett.util.DatabaseConstants;
import com.kanemullett.util.PredictorConstants;

import jakarta.annotation.Nullable;

@Service
public class MatchService {

    private final DatabaseQueryService queryService;
    private final TournamentService tournamentService;
    private final GroupService groupService;
    private final RoundService roundService;
    private final MatchBuilderFunction matchBuilderFunction;

    private static final String AWAY_ALIAS = "away";
    private static final String GROUP_ALIAS = "group";
    private static final String HOME_ALIAS = "home";
    private static final String MATCH_ALIAS = "match";
    private static final String ROUND_ALIAS = "round";
    private static final String RESULT_ALIAS = "result";

    public MatchService(
        DatabaseQueryService queryService,
        TournamentService tournamentService,
        GroupService groupService,
        RoundService roundService,
        MatchBuilderFunction matchBuilderFunction
    ) {
        this.queryService = queryService;
        this.tournamentService = tournamentService;
        this.groupService = groupService;
        this.roundService = roundService;
        this.matchBuilderFunction = matchBuilderFunction;
    }

    public List<Match> getMatches(
            String tournamentId,
            @Nullable String groupId,
            @Nullable Integer groupMatchDay,
            @Nullable String roundId) {

        tournamentService.getTournamentById(tournamentId);
        return retrieveMatches(tournamentId, groupId, groupMatchDay, roundId);
    }

    public List<Match> updateMatches(String tournamentId, List<MatchUpdate> updates) {
        tournamentService.getTournamentById(tournamentId);

        final UpdateRequest<MatchUpdate> updateRequest = ImmutableUpdateRequest.<MatchUpdate>builder()
            .operation(SqlOperator.UPDATE)
            .table(Table.of(
                PredictorConstants.PREDICTOR_SCHEMA,
                MatchRecord.getTargetTable(tournamentId)
            ))
            .records(updates)
            .build();

        queryService.updateRecords(updateRequest);

        return retrieveMatches(
            tournamentId,
            updates.stream()
                .map(MatchUpdate::getId)
                .toList()
        );
    }

    public Match getMatchById(String tournamentId, String matchId) {
        
        tournamentService.getTournamentById(tournamentId);
        final Optional<Match> match = retrieveMatch(tournamentId, matchId);

        if (match.isEmpty()) {
            throw new ResponseStatusException(HttpStatus.NOT_FOUND, "No matches found with a matching id.");
        }

        return match.get();
    }

    private Optional<Match> retrieveMatch(String tournamentId, String matchId) {
        final List<Match> matches = retrieveMatches(tournamentId, List.of(matchId));

        return matches.stream().findFirst();
    }

    private List<Match> retrieveMatches(String tournamentId, List<String> matchIds) {
        return retrieveMatches(tournamentId, null, null, null, matchIds);
    }

    private List<Match> retrieveMatches(
            String tournamentId,
            @Nullable String groupId,
            @Nullable Integer groupMatchDay,
            @Nullable String roundId) {
        return retrieveMatches(tournamentId, groupId, groupMatchDay, roundId, null);
    }

    private List<Match> retrieveMatches(
        String tournamentId,
        @Nullable String groupId,
        @Nullable Integer groupMatchDay,
        @Nullable String roundId,
        @Nullable List<String> matchIds) {

        final List<Column> columns = new ArrayList<>(
            List.of(
                ImmutableColumn.builder()
                    .addParts(MATCH_ALIAS, DatabaseConstants.ID)
                    .alias("matchId")
                    .build(),
                ImmutableColumn.builder()
                    .addParts(HOME_ALIAS, DatabaseConstants.ID)
                    .alias("homeId")
                    .build(),
                ImmutableColumn.builder()
                    .addParts(HOME_ALIAS, Team.NAME_COLUMN)
                    .alias("homeName")
                    .build(),
                ImmutableColumn.builder()
                    .addParts(HOME_ALIAS, Team.IMAGE_PATH_COLUMN)
                    .alias("homeImagePath")
                    .build(),
                ImmutableColumn.builder()
                    .addParts(HOME_ALIAS, Team.CONFEDERATION_COLUMN)
                    .alias("homeConfederation")
                    .build(),
                ImmutableColumn.builder()
                    .addParts(AWAY_ALIAS, DatabaseConstants.ID)
                    .alias("awayId")
                    .build(),
                ImmutableColumn.builder()
                    .addParts(AWAY_ALIAS, Team.NAME_COLUMN)
                    .alias("awayName")
                    .build(),
                ImmutableColumn.builder()
                    .addParts(AWAY_ALIAS, Team.IMAGE_PATH_COLUMN)
                    .alias("awayImagePath")
                    .build(),
                ImmutableColumn.builder()
                    .addParts(AWAY_ALIAS, Team.CONFEDERATION_COLUMN)
                    .alias("awayConfederation")
                    .build(),
                Column.of(MATCH_ALIAS, MatchRecord.KICKOFF_COLUMN),
                Column.of(MATCH_ALIAS, MatchRecord.GROUP_MATCH_DAY_COLUMN),
                Column.of(MATCH_ALIAS, MatchRecord.GROUP_ID_COLUMN),
                Column.of(MATCH_ALIAS, MatchRecord.ROUND_ID_COLUMN),
                Column.of(RESULT_ALIAS, Result.HOME_GOALS_COLUMN),
                Column.of(RESULT_ALIAS, Result.AWAY_GOALS_COLUMN),
                Column.of(RESULT_ALIAS, Result.AFTER_EXTRA_TIME_COLUMN),
                Column.of(RESULT_ALIAS, Result.AFTER_PENALTIES_COLUMN),
                Column.of(RESULT_ALIAS, Result.PENALTIES_WINNER_COLUMN)
            )
        );

        final List<TableJoin> tableJoins = new ArrayList<>(
            List.of(
                TableJoin.of(
                    Table.of(
                        PredictorConstants.PREDICTOR_SCHEMA,
                        Team.TARGET_TABLE,
                        HOME_ALIAS
                    ),
                    QueryCondition.of(
                        Column.of(MATCH_ALIAS, MatchRecord.HOME_TEAM_ID_COLUMN),
                        Column.of(HOME_ALIAS, DatabaseConstants.ID)
                    ),
                    JoinType.LEFT
                ),
                TableJoin.of(
                    Table.of(
                        PredictorConstants.PREDICTOR_SCHEMA,
                        Team.TARGET_TABLE,
                        AWAY_ALIAS
                    ),
                    QueryCondition.of(
                        Column.of(MATCH_ALIAS, MatchRecord.AWAY_TEAM_ID_COLUMN),
                        Column.of(AWAY_ALIAS, DatabaseConstants.ID)
                    ),
                    JoinType.LEFT
                ),
                TableJoin.of(
                    Table.of(
                        PredictorConstants.PREDICTOR_SCHEMA,
                        Result.getTargetTable(tournamentId),
                        RESULT_ALIAS
                    ),
                    QueryCondition.of(
                        Column.of(MATCH_ALIAS, DatabaseConstants.ID),
                        Column.of(RESULT_ALIAS, DatabaseConstants.ID)
                    ),
                    JoinType.LEFT
                )
            )
        );

        final List<OrderBy> orderBy = new ArrayList<>(
            List.of(
                OrderBy.of(
                    Column.of(MATCH_ALIAS, MatchRecord.KICKOFF_COLUMN)
                ),
                OrderBy.of(
                    Column.of(MATCH_ALIAS, MatchRecord.GROUP_MATCH_DAY_COLUMN)
                )
            )
        );

        if (groupService.tournamentHasGroupStage(tournamentId)) {
            columns.add(
                ImmutableColumn.builder()
                    .addParts(GROUP_ALIAS, GroupRecord.NAME_COLUMN)
                    .alias("groupName")
                    .build()
            );

            tableJoins.add(
                TableJoin.of(
                    Table.of(
                        PredictorConstants.PREDICTOR_SCHEMA,
                        GroupRecord.getTargetTable(tournamentId),
                        GROUP_ALIAS
                    ),
                    QueryCondition.of(
                        Column.of(MATCH_ALIAS, MatchRecord.GROUP_ID_COLUMN),
                        Column.of(GROUP_ALIAS, DatabaseConstants.ID)
                    ),
                    JoinType.LEFT
                )
            );

            orderBy.add(
                1,
                OrderBy.of(
                    Column.of(GROUP_ALIAS, GroupRecord.NAME_COLUMN)
                )
            );
        }

        if (roundService.tournamentHasKnockoutStage(tournamentId)) {
            columns.addAll(List.of(
                ImmutableColumn.builder()
                    .addParts(ROUND_ALIAS, Round.NAME_COLUMN)
                    .alias("roundName")
                    .build(),
                Column.of(ROUND_ALIAS, Round.TEAM_COUNT_COLUMN),
                Column.of(ROUND_ALIAS, Round.ROUND_ORDER_COLUMN),
                Column.of(ROUND_ALIAS, Round.TWO_LEGS_COLUMN),
                Column.of(ROUND_ALIAS, Round.EXTRA_TIME_COLUMN),
                ImmutableColumn.builder()
                    .addParts(ROUND_ALIAS, Round.AWAY_GOALS_COLUMN)
                    .alias("awayGoalsDecider")
                    .build()
            ));

            tableJoins.add(
                TableJoin.of(
                    Table.of(
                        PredictorConstants.PREDICTOR_SCHEMA,
                        Round.getTargetTable(tournamentId),
                        ROUND_ALIAS
                    ),
                    QueryCondition.of(
                        Column.of(MATCH_ALIAS, MatchRecord.ROUND_ID_COLUMN),
                        Column.of(ROUND_ALIAS, DatabaseConstants.ID)
                    ),
                    JoinType.LEFT
                )
            );

            orderBy.add(
                OrderBy.of(
                    Column.of(ROUND_ALIAS, Round.ROUND_ORDER_COLUMN)
                )
            );
        }

        final List<QueryCondition> conditions = new ArrayList<>();

        if (groupId != null) {
            conditions.add(
                QueryCondition.of(
                    Column.of(MATCH_ALIAS, MatchRecord.GROUP_ID_COLUMN),
                    groupId
                )
            );
        }

        if (groupMatchDay != null) {
            conditions.add(
                QueryCondition.of(
                    Column.of(MATCH_ALIAS, MatchRecord.GROUP_MATCH_DAY_COLUMN),
                    groupMatchDay
                )
            );
        }

        if (roundId != null) {
            conditions.add(
                QueryCondition.of(
                    Column.of(MATCH_ALIAS, MatchRecord.ROUND_ID_COLUMN),
                    roundId
                )
            );
        }

        if (matchIds != null) {
            conditions.add(
                ImmutableQueryCondition.builder()
                    .column(Column.of(MATCH_ALIAS, DatabaseConstants.ID))
                    .operator(ConditionOperator.IN)
                    .value(matchIds)
                    .build()
            );
        }

        final QueryRequest<DatabaseRecord> queryRequest = ImmutableQueryRequest.builder()
            .columns(columns)
            .table(Table.of(
                PredictorConstants.PREDICTOR_SCHEMA,
                MatchRecord.getTargetTable(tournamentId),
                MATCH_ALIAS
            ))
            .joins(tableJoins)
            .conditionGroup(!conditions.isEmpty() ?
                ImmutableQueryConditionGroup.builder()
                    .conditions(conditions)
                    .join(ConditionJoin.AND)
                    .build() : null)
            .orderBy(orderBy)
            .recordClass(DatabaseRecord.class)
            .build();

        final QueryResponse<DatabaseRecord> response = queryService.retrieveRecords(queryRequest);

        return response.getRecords().stream()
            .map(matchBuilderFunction)
            .toList();
    }
}
