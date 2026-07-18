package com.kanemullett.service;

import java.util.LinkedHashMap;
import java.util.List;
import java.util.stream.Collectors;

import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Service;
import org.springframework.web.server.ResponseStatusException;

import com.kanemullett.model.Column;
import com.kanemullett.model.DatabaseRecord;
import com.kanemullett.model.Group;
import com.kanemullett.model.GroupRecord;
import com.kanemullett.model.GroupTeam;
import com.kanemullett.model.ImmutableGroup;
import com.kanemullett.model.ImmutableGroupTeam;
import com.kanemullett.model.ImmutableQueryCondition;
import com.kanemullett.model.ImmutableQueryRequest;
import com.kanemullett.model.ImmutableTableJoin;
import com.kanemullett.model.ImmutableTeam;
import com.kanemullett.model.ImmutableUpdateRequest;
import com.kanemullett.model.LeagueTemplate;
import com.kanemullett.model.QueryCondition;
import com.kanemullett.model.QueryConditionGroup;
import com.kanemullett.model.QueryRequest;
import com.kanemullett.model.QueryResponse;
import com.kanemullett.model.Table;
import com.kanemullett.model.TableJoin;
import com.kanemullett.model.Team;
import com.kanemullett.model.Tournament;
import com.kanemullett.model.TournamentTemplateRecord;
import com.kanemullett.model.UpdateRequest;
import com.kanemullett.model.type.ConditionOperator;
import com.kanemullett.model.type.Confederation;
import com.kanemullett.model.type.JoinType;
import com.kanemullett.model.type.SqlOperator;
import com.kanemullett.util.DatabaseConstants;
import com.kanemullett.util.PredictorConstants;

import jakarta.annotation.Nullable;

@Service
public class GroupService {

    private final DatabaseQueryService queryService;

    private static final String GROUPS_TABLE_ALIAS = "gr";
    private static final String GROUP_TEAMS_TABLE_ALIAS = "gt";
    private static final String LEAGUE_TEMPLATES_TABLE_ALIAS = "lt";
    private static final String TEAMS_TABLE_ALIAS = "te";
    private static final String TOURNAMENTS_TABLE_ALIAS = "to";
    private static final String TOURNAMENT_TEMPLATES_TABLE_ALIAS = "tt";

    public GroupService(DatabaseQueryService queryService) {
        this.queryService = queryService;
    }

    public List<Group> getGroups(String tournamentId) {

        verifyTournament(tournamentId);
        return retrieveAndBuildGroups(tournamentId, null);
    }

    public List<Group> updateGroups(String tournamentId, List<GroupRecord> groupUpdates) {
        verifyTournament(tournamentId);

        final UpdateRequest<GroupRecord> updateRequest = ImmutableUpdateRequest.<GroupRecord>builder()
            .operation(SqlOperator.UPDATE)
            .table(Table.of(PredictorConstants.PREDICTOR_SCHEMA, GroupRecord.getTargetTable(tournamentId)))
            .records(groupUpdates)
            .build();

        queryService.updateRecords(updateRequest);

        final QueryCondition queryCondition = ImmutableQueryCondition.builder()
            .column(Column.of(GROUP_TEAMS_TABLE_ALIAS, GroupTeam.GROUP_ID_COLUMN))
            .operator(ConditionOperator.IN)
            .value(groupUpdates.stream()
                .map(GroupRecord::getId)
                .toList())
            .build();

        return retrieveAndBuildGroups(tournamentId, QueryConditionGroup.of(queryCondition));
    }

    public Group getGroupById(String tournamentId, String groupId) {
        verifyTournament(tournamentId);
        verifyGroup(tournamentId, groupId);

        return retrieveAndBuildGroup(tournamentId, groupId);
    }

    public Group addTeamsToGroup(String tournamentId, String groupId, List<String> teamIds) {
        verifyTournament(tournamentId);
        verifyGroup(tournamentId, groupId);

        final QueryRequest<Team> teamRequest = ImmutableQueryRequest.<Team>builder()
            .table(Table.of(PredictorConstants.PREDICTOR_SCHEMA, Team.TARGET_TABLE))
            .conditionGroup(QueryConditionGroup.of(
                ImmutableQueryCondition.builder()
                    .column(Column.of(DatabaseConstants.ID))
                    .operator(ConditionOperator.IN)
                    .value(teamIds)
                    .build()
            ))
            .recordClass(Team.class)
            .build();

        final QueryResponse<Team> teamResponse = queryService.retrieveRecords(teamRequest);

        final List<String> existingIds = teamResponse.getRecords().stream()
            .map(Team::getId)
            .toList();

        final List<String> invalidIds = teamIds.stream()
            .filter(teamId -> !existingIds.contains(teamId))
            .toList();

        if (!invalidIds.isEmpty()) {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "No teams found with ids: " + String.join(", ", invalidIds));
        }

        final QueryRequest<GroupTeam> groupTeamsRequest = ImmutableQueryRequest.<GroupTeam>builder()
            .table(Table.of(PredictorConstants.PREDICTOR_SCHEMA, GroupTeam.getTargetTable(tournamentId)))
            .conditionGroup(QueryConditionGroup.of(
                QueryCondition.of(
                    Column.of(GroupTeam.GROUP_ID_COLUMN),
                    groupId
                )
            ))
            .recordClass(GroupTeam.class)
            .build();

        final QueryResponse<GroupTeam> groupTeamsResponse = queryService.retrieveRecords(groupTeamsRequest);
        final int teamsInGroup = groupTeamsResponse.getRecordCount();

        final QueryRequest<DatabaseRecord> teamsPerGroupRequest = ImmutableQueryRequest.<DatabaseRecord>builder()
            .columns(List.of(
                Column.of(LEAGUE_TEMPLATES_TABLE_ALIAS, LeagueTemplate.TEAMS_PER_GROUP_COLUMN)
            ))
            .table(Table.of(PredictorConstants.PREDICTOR_SCHEMA, Tournament.TARGET_TABLE, TOURNAMENTS_TABLE_ALIAS))
            .joins(List.of(
                TableJoin.of(
                    Table.of(PredictorConstants.PREDICTOR_SCHEMA, TournamentTemplateRecord.TARGET_TABLE, TOURNAMENT_TEMPLATES_TABLE_ALIAS),
                    QueryCondition.of(
                        Column.of(TOURNAMENTS_TABLE_ALIAS, Tournament.TEMPLATE_ID_COLUMN),
                        Column.of(TOURNAMENT_TEMPLATES_TABLE_ALIAS, DatabaseConstants.ID)
                    ),
                    JoinType.INNER
                ),
                TableJoin.of(
                    Table.of(PredictorConstants.PREDICTOR_SCHEMA, LeagueTemplate.TARGET_TABLE, LEAGUE_TEMPLATES_TABLE_ALIAS),
                    QueryCondition.of(
                        Column.of(TOURNAMENT_TEMPLATES_TABLE_ALIAS, TournamentTemplateRecord.LEAGUE_TEMPLATE_ID_COLUMN),
                        Column.of(LEAGUE_TEMPLATES_TABLE_ALIAS, DatabaseConstants.ID)
                    ),
                    JoinType.INNER
                )
            ))
            .conditionGroup(QueryConditionGroup.of(
                QueryCondition.of(
                    Column.of(TOURNAMENTS_TABLE_ALIAS, DatabaseConstants.ID),
                    tournamentId
                )
            ))
            .recordClass(DatabaseRecord.class)
            .build();

        final QueryResponse<DatabaseRecord> teamsPerGroupResponse = queryService.retrieveRecords(teamsPerGroupRequest);
        final int teamsPerGroup = teamsPerGroupResponse.getRecordCount();

        if (teamsInGroup + teamIds.size() > teamsPerGroup) {
            throw new ResponseStatusException(HttpStatus.CONFLICT, "Adding teams to the specified group will exceed its maximum team count.");
        }

        final UpdateRequest<GroupTeam> updateRequest = ImmutableUpdateRequest.<GroupTeam>builder()
            .operation(SqlOperator.INSERT)
            .table(Table.of(PredictorConstants.PREDICTOR_SCHEMA, GroupTeam.getTargetTable(tournamentId)))
            .records(teamIds.stream()
                .map(teamId -> ImmutableGroupTeam.builder()
                    .groupId(groupId)
                    .teamId(teamId)
                    .build())
                .toList())
            .build();

        queryService.updateRecords(updateRequest);

        return retrieveAndBuildGroup(tournamentId, groupId);
    }

    public Group removeTeamFromGroup(String tournamentId, String groupId, String teamId) {
        verifyTournament(tournamentId);
        verifyGroup(tournamentId, groupId);

        final UpdateRequest<GroupTeam> updateRequest = ImmutableUpdateRequest.<GroupTeam>builder()
            .operation(SqlOperator.DELETE)
            .table(Table.of(PredictorConstants.PREDICTOR_SCHEMA, GroupTeam.getTargetTable(tournamentId)))
            .conditionGroup(QueryConditionGroup.of(
                QueryCondition.of(
                    Column.of(GroupTeam.GROUP_ID_COLUMN),
                    groupId
                ),
                QueryCondition.of(
                    Column.of(GroupTeam.TEAM_ID_COLUMN),
                    teamId
                )
            ))
            .build();

        queryService.updateRecords(updateRequest);

        return retrieveAndBuildGroup(tournamentId, groupId);
    }

    private void verifyTournament(String tournamentId) {
        final QueryRequest<DatabaseRecord> queryRequest = ImmutableQueryRequest.<DatabaseRecord>builder()
            .columns(List.of(
                Column.of(TOURNAMENTS_TABLE_ALIAS, DatabaseConstants.ID),
                Column.of(TOURNAMENT_TEMPLATES_TABLE_ALIAS, TournamentTemplateRecord.LEAGUE_TEMPLATE_ID_COLUMN)
            ))
            .table(Table.of(PredictorConstants.PREDICTOR_SCHEMA, Tournament.TARGET_TABLE, TOURNAMENTS_TABLE_ALIAS))
            .joins(List.of(ImmutableTableJoin.builder()
                    .table(Table.of(
                        PredictorConstants.PREDICTOR_SCHEMA,
                        TournamentTemplateRecord.TARGET_TABLE,
                        TOURNAMENT_TEMPLATES_TABLE_ALIAS
                    ))
                    .joinType(JoinType.INNER)
                    .joinCondition(QueryCondition.of(
                        Column.of(TOURNAMENTS_TABLE_ALIAS, Tournament.TEMPLATE_ID_COLUMN),
                        Column.of(TOURNAMENT_TEMPLATES_TABLE_ALIAS, DatabaseConstants.ID)
                    ))
                    .build()
            ))
            .conditionGroup(QueryConditionGroup.of(
                QueryCondition.of(
                    Column.of(TOURNAMENTS_TABLE_ALIAS, DatabaseConstants.ID),
                    tournamentId
                )
            ))
            .recordClass(DatabaseRecord.class)
            .build();

        final QueryResponse<DatabaseRecord> queryResponse = queryService.retrieveRecords(queryRequest);

        if (queryResponse.getRecordCount() == 0) {
            throw new ResponseStatusException(HttpStatus.NOT_FOUND, "No tournaments found with a matching id.");
        }

        final DatabaseRecord tournamentRecord = queryResponse.getRecords().get(0);

        if (tournamentRecord.getData().get(TournamentTemplateRecord.LEAGUE_TEMPLATE_ID_COLUMN) == null) {
            throw new ResponseStatusException(HttpStatus.NOT_FOUND, "The tournament with the supplied id does not have a group stage.");
        }
    }

    private void verifyGroup(String tournamentId, String groupId) {
        final QueryRequest<GroupRecord> queryRequest = ImmutableQueryRequest.<GroupRecord>builder()
            .table(Table.of(PredictorConstants.PREDICTOR_SCHEMA, GroupRecord.getTargetTable(tournamentId)))
            .conditionGroup(QueryConditionGroup.of(
                QueryCondition.of(
                    Column.of(DatabaseConstants.ID),
                    groupId
                )
            ))
            .recordClass(GroupRecord.class)
            .build();

        final QueryResponse<GroupRecord> queryResponse = queryService.retrieveRecords(queryRequest);

        if (queryResponse.getRecordCount() == 0) {
            throw new ResponseStatusException(HttpStatus.NOT_FOUND, "No groups found with a matching id.");
        }
    }

    private Group retrieveAndBuildGroup(String tournamentId, String groupId) {
        final QueryConditionGroup conditionGroup = QueryConditionGroup.of(
            QueryCondition.of(
                Column.of(GROUP_TEAMS_TABLE_ALIAS, GroupTeam.GROUP_ID_COLUMN),
                groupId
            )
        );

        return retrieveAndBuildGroups(tournamentId, conditionGroup).get(0);
    }

    private List<Group> retrieveAndBuildGroups(String tournamentId, @Nullable QueryConditionGroup conditionGroup) {

        final QueryRequest<DatabaseRecord> queryRequest = ImmutableQueryRequest.<DatabaseRecord>builder()
            .columns(List.of(
                Column.of(GROUP_TEAMS_TABLE_ALIAS, GroupTeam.GROUP_ID_COLUMN),
                Column.of(GROUPS_TABLE_ALIAS, GroupRecord.NAME_COLUMN, "groupName"),
                Column.of(GROUP_TEAMS_TABLE_ALIAS, GroupTeam.TEAM_ID_COLUMN),
                Column.of(TEAMS_TABLE_ALIAS, Team.NAME_COLUMN, "teamName"),
                Column.of(TEAMS_TABLE_ALIAS, Team.IMAGE_PATH_COLUMN),
                Column.of(TEAMS_TABLE_ALIAS, Team.CONFEDERATION_COLUMN),
                Column.of(TEAMS_TABLE_ALIAS, Team.RANKING_COLUMN)
            ))
            .table(Table.of(PredictorConstants.PREDICTOR_SCHEMA, GroupTeam.getTargetTable(tournamentId), GROUP_TEAMS_TABLE_ALIAS))
            .joins(List.of(
                ImmutableTableJoin.builder()
                    .table(Table.of(PredictorConstants.PREDICTOR_SCHEMA, GroupRecord.getTargetTable(tournamentId), GROUPS_TABLE_ALIAS))
                    .joinType(JoinType.INNER)
                    .joinCondition(QueryCondition.of(
                        Column.of(GROUP_TEAMS_TABLE_ALIAS, GroupTeam.GROUP_ID_COLUMN),
                        Column.of(GROUPS_TABLE_ALIAS, DatabaseConstants.ID)
                    ))
                    .build(),
                ImmutableTableJoin.builder()
                    .table(Table.of(PredictorConstants.PREDICTOR_SCHEMA, Team.TARGET_TABLE, TEAMS_TABLE_ALIAS))
                    .joinType(JoinType.INNER)
                    .joinCondition(QueryCondition.of(
                        Column.of(GROUP_TEAMS_TABLE_ALIAS, GroupTeam.TEAM_ID_COLUMN),
                        Column.of(TEAMS_TABLE_ALIAS, DatabaseConstants.ID)
                    ))
                    .build()
            ))
            .conditionGroup(conditionGroup)
            .recordClass(DatabaseRecord.class)
            .build();

        final QueryResponse<DatabaseRecord> queryResponse = queryService.retrieveRecords(queryRequest);

        return queryResponse.getRecords().stream()
            .collect(Collectors.groupingBy(record -> (String) record.getData().get(GroupTeam.GROUP_ID_COLUMN), LinkedHashMap::new, Collectors.toList()))
            .entrySet().stream()
            .map(entry -> buildGroup(entry.getKey(), entry.getValue()))
            .collect(Collectors.toList());
    }

    private Group buildGroup(String groupId, List<DatabaseRecord> groupRecords) {
        final String groupName = (String) groupRecords.get(0).getData().get("groupName");

        final List<Team> teams = groupRecords.stream()
            .map(record -> ImmutableTeam.builder()
                .id((String) record.getData().get(GroupTeam.TEAM_ID_COLUMN))
                .name((String) record.getData().get("teamName"))
                .imagePath((String) record.getData().get(Team.IMAGE_PATH_COLUMN))
                .confederation(Enum.valueOf(Confederation.class, (String) record.getData().get(Team.CONFEDERATION_COLUMN)))
                .ranking((Integer) record.getData().get(Team.RANKING_COLUMN))
                .build())
            .collect(Collectors.toList());

        return ImmutableGroup.builder()
            .id(groupId)
            .name(groupName)
            .teams(teams)
            .build();
    }
}
