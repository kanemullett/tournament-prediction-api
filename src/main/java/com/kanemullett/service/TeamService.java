package com.kanemullett.service;

import java.util.List;

import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Service;
import org.springframework.web.server.ResponseStatusException;

import com.kanemullett.model.Column;
import com.kanemullett.model.GroupTeam;
import com.kanemullett.model.ImmutableQueryCondition;
import com.kanemullett.model.ImmutableQueryConditionGroup;
import com.kanemullett.model.ImmutableQueryJoin;
import com.kanemullett.model.ImmutableQueryRequest;
import com.kanemullett.model.ImmutableUpdateRequest;
import com.kanemullett.model.MatchRecord;
import com.kanemullett.model.OrderBy;
import com.kanemullett.model.QueryCondition;
import com.kanemullett.model.QueryConditionGroup;
import com.kanemullett.model.QueryRequest;
import com.kanemullett.model.QueryResponse;
import com.kanemullett.model.Table;
import com.kanemullett.model.Team;
import com.kanemullett.model.TeamUpdate;
import com.kanemullett.model.UpdateRequest;
import com.kanemullett.model.type.ConditionOperator;
import com.kanemullett.model.type.Confederation;
import com.kanemullett.model.type.JoinType;
import com.kanemullett.model.type.SqlOperator;
import com.kanemullett.util.DatabaseConstants;
import com.kanemullett.util.PredictorConstants;

import jakarta.annotation.Nullable;

@Service
public class TeamService {

    private final DatabaseQueryService queryService;

    private static final String TEAM_ALIAS = "team";

    public TeamService(DatabaseQueryService queryService) {
        this.queryService = queryService;
    }

    public List<Team> getTeams(@Nullable Confederation confederation, @Nullable String tournamentId) {
        final ImmutableQueryConditionGroup.Builder conditionGroup = ImmutableQueryConditionGroup.builder();
        
        if (confederation != null) {
            conditionGroup.addConditions(QueryCondition.of(
                Column.of(Team.CONFEDERATION_COLUMN),
                confederation
            ));
        }

        final QueryConditionGroup queryConditionGroup = conditionGroup.build();

        final ImmutableQueryRequest.Builder<Team> requestBuilder = ImmutableQueryRequest.<Team>builder()
            .conditionGroup(queryConditionGroup)
            .orderBy(OrderBy.of(Column.of(Team.NAME_COLUMN)))
            .recordClass(Team.class);

        if (tournamentId == null) {
            requestBuilder
                .table(Table.of(PredictorConstants.PREDICTOR_SCHEMA, Team.TARGET_TABLE));
        } else {
            requestBuilder
                .distinct(true)
                .columns(List.of(
                    Column.of(TEAM_ALIAS, DatabaseConstants.ID),
                    Column.of(TEAM_ALIAS, Team.NAME_COLUMN),
                    Column.of(TEAM_ALIAS, Team.IMAGE_PATH_COLUMN),
                    Column.of(TEAM_ALIAS, Team.CONFEDERATION_COLUMN)
                ))
                .table(Table.of(PredictorConstants.PREDICTOR_SCHEMA, Team.TARGET_TABLE, TEAM_ALIAS))
                .joins(List.of(
                    ImmutableQueryJoin.<GroupTeam>builder()
                        .query(ImmutableQueryRequest.<GroupTeam>builder()
                            .distinct(true)
                            .columns(List.of(Column.of(GroupTeam.TEAM_ID_COLUMN)))
                            .table(Table.of(PredictorConstants.PREDICTOR_SCHEMA, GroupTeam.getTargetTable(tournamentId)))
                            .joins(List.of(
                                ImmutableQueryJoin.<MatchRecord>builder()
                                    .query(ImmutableQueryRequest.<MatchRecord>builder()
                                        .distinct(true)
                                        .columns(List.of(Column.of(MatchRecord.HOME_TEAM_ID_COLUMN)))
                                        .table(Table.of(PredictorConstants.PREDICTOR_SCHEMA, MatchRecord.getTargetTable(tournamentId)))
                                        .recordClass(MatchRecord.class)
                                        .build())
                                    .joinType(JoinType.UNION)
                                    .build(),
                                ImmutableQueryJoin.<MatchRecord>builder()
                                    .query(ImmutableQueryRequest.<MatchRecord>builder()
                                        .distinct(true)
                                        .columns(List.of(Column.of(MatchRecord.AWAY_TEAM_ID_COLUMN)))
                                        .table(Table.of(PredictorConstants.PREDICTOR_SCHEMA, MatchRecord.getTargetTable(tournamentId)))
                                        .recordClass(MatchRecord.class)
                                        .build())
                                    .joinType(JoinType.UNION)
                                    .build()
                            ))
                            .recordClass(GroupTeam.class)
                            .build())
                        .alias("teamIds")
                        .joinType(JoinType.INNER)
                        .joinCondition(QueryCondition.of(
                            Column.of(TEAM_ALIAS, DatabaseConstants.ID),
                            Column.of("teamIds", GroupTeam.TEAM_ID_COLUMN)
                        ))
                        .build()
                ));
        }

        final QueryRequest<Team> queryRequest = requestBuilder.build();
        final QueryResponse<Team> queryResponse = queryService.retrieveRecords(queryRequest);
        
        return queryResponse.getRecords();
    }

    public List<Team> createTeams(List<Team> teams) {
        final UpdateRequest<Team> updateRequest = ImmutableUpdateRequest.<Team>builder()
            .operation(SqlOperator.INSERT)
            .table(Table.of(PredictorConstants.PREDICTOR_SCHEMA, Team.TARGET_TABLE))
            .records(teams)
            .build();

        queryService.updateRecords(updateRequest);

        return teams;
    }

    public List<Team> updateTeams(List<TeamUpdate> teams) {
        final UpdateRequest<TeamUpdate> updateRequest = ImmutableUpdateRequest.<TeamUpdate>builder()
            .operation(SqlOperator.UPDATE)
            .table(Table.of(PredictorConstants.PREDICTOR_SCHEMA, Team.TARGET_TABLE))
            .records(teams)
            .build();

        queryService.updateRecords(updateRequest);

        final QueryRequest<Team> queryRequest = ImmutableQueryRequest.<Team>builder()
            .table(Table.of(PredictorConstants.PREDICTOR_SCHEMA, Team.TARGET_TABLE))
            .conditionGroup(QueryConditionGroup.of(
                ImmutableQueryCondition.builder()
                    .column(Column.of(DatabaseConstants.ID))
                    .operator(ConditionOperator.IN)
                    .value(teams.stream()
                        .map(TeamUpdate::getId)
                        .toList())
                    .build()
            ))
            .recordClass(Team.class)
            .build();

        final QueryResponse<Team> queryResponse = queryService.retrieveRecords(queryRequest);

        return queryResponse.getRecords();
    }

    public Team getTeamById(String teamId) {
        final QueryRequest<Team> queryRequest = ImmutableQueryRequest.<Team>builder()
            .table(Table.of(PredictorConstants.PREDICTOR_SCHEMA, Team.TARGET_TABLE))
            .conditionGroup(QueryConditionGroup.of(
                QueryCondition.of(
                    Column.of(DatabaseConstants.ID),
                    teamId
                )
            ))
            .recordClass(Team.class)
            .build();

        final QueryResponse<Team> queryResponse = queryService.retrieveRecords(queryRequest);

        if (queryResponse.getRecordCount() == 0) {
            throw new ResponseStatusException(HttpStatus.NOT_FOUND, "No teams found with a matching id.");
        }

        return queryResponse.getRecords().get(0);
    }

    public void deleteTeamById(String teamId) {
        final UpdateRequest<Team> updateRequest = ImmutableUpdateRequest.<Team>builder()
            .operation(SqlOperator.DELETE)
            .table(Table.of(PredictorConstants.PREDICTOR_SCHEMA, Team.TARGET_TABLE))
            .conditionGroup(QueryConditionGroup.of(
                QueryCondition.of(
                    Column.of(DatabaseConstants.ID),
                    teamId
                )
            ))
            .build();

        queryService.updateRecords(updateRequest);
    }
    // football>java.spi(nuilder)controller
    // jennifer.buckley>kane.mullett<will be together for ever. sticking out toungue 
    // i love you: return.com :)
}
