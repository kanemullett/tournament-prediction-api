package com.kanemullett.service;

import java.util.List;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertNotNull;
import static org.junit.Assert.assertTrue;
import static org.junit.jupiter.api.Assertions.assertThrows;

import org.junit.jupiter.api.Test;
import org.mockito.ArgumentCaptor;
import org.springframework.http.HttpStatus;
import org.springframework.web.server.ResponseStatusException;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

import com.kanemullett.model.Column;
import com.kanemullett.model.DatabaseRecord;
import com.kanemullett.model.GroupTeam;
import com.kanemullett.model.ImmutableTeam;
import com.kanemullett.model.ImmutableTeamUpdate;
import com.kanemullett.model.MatchRecord;
import com.kanemullett.model.OrderBy;
import com.kanemullett.model.QueryCondition;
import com.kanemullett.model.QueryJoin;
import com.kanemullett.model.QueryRequest;
import com.kanemullett.model.QueryResponse;
import com.kanemullett.model.Table;
import com.kanemullett.model.Team;
import com.kanemullett.model.TeamUpdate;
import com.kanemullett.model.UpdateRequest;
import com.kanemullett.model.type.ConditionOperator;
import com.kanemullett.model.type.Confederation;
import com.kanemullett.model.type.JoinType;
import com.kanemullett.model.type.OrderDirection;
import com.kanemullett.model.type.SqlOperator;

public class TeamServiceTest {

    private final DatabaseQueryService queryService = mock(DatabaseQueryService.class);

    private final TeamService service = new TeamService(queryService);

    private static final Team BOSNIA = ImmutableTeam.builder()
        .id("c08fd796-7fea-40d9-9a0a-cb3a49cce2e4")
        .name("Bosnia & Herzegovina")
        .imagePath("BIH.png")
        .confederation(Confederation.UEFA)
        .build();
    private static final Team BOTSWANA = ImmutableTeam.builder()
        .id("6ee28143-1286-4618-a8b9-ad86d348ead1")
        .name("Botswana")
        .imagePath("BOT.png")
        .confederation(Confederation.CAF)
        .build();
    private static final Team ENGLAND = ImmutableTeam.builder()
        .id("e107d069-b277-4902-bdad-7091a494a8b3")
        .name("England")
        .imagePath("ENG.png")
        .confederation(Confederation.UEFA)
        .build();

    @Test
    void shouldReturnAllTeamsWithNoParameters() {
        // Given
        final QueryResponse<DatabaseRecord> queryResponse = mock(QueryResponse.class);
        when(queryResponse.getRecordCount())
            .thenReturn(3);
        when(queryResponse.getRecords())
            .thenReturn(List.of(BOSNIA, BOTSWANA, ENGLAND));

        when(queryService.retrieveRecords(any()))
            .thenReturn(queryResponse);

        // When
        final List<Team> teams = service.getTeams(null, null);

        // Then
        final ArgumentCaptor<QueryRequest<Team>> requestCaptor = ArgumentCaptor.forClass(QueryRequest.class);
        verify(queryService).retrieveRecords(requestCaptor.capture());
        final QueryRequest<Team> request = requestCaptor.getValue();

        final Table table = request.getTable();
        assertEquals("predictor", table.getSchema());
        assertEquals("teams", table.getTable());

        final OrderBy orderBy = request.getOrderBy();
        assertEquals(List.of("name"), orderBy.getColumn().getParts());
        assertEquals(OrderDirection.ASCENDING, orderBy.getDirection());

        assertEquals(3, teams.size());

        final Team team1 = teams.get(0);
        assertEquals("c08fd796-7fea-40d9-9a0a-cb3a49cce2e4", team1.getId());
        assertEquals("Bosnia & Herzegovina", team1.getName());
        assertEquals("BIH.png", team1.getImagePath());
        assertEquals(Confederation.UEFA, team1.getConfederation());

        final Team team2 = teams.get(1);
        assertEquals("6ee28143-1286-4618-a8b9-ad86d348ead1", team2.getId());
        assertEquals("Botswana", team2.getName());
        assertEquals("BOT.png", team2.getImagePath());
        assertEquals(Confederation.CAF, team2.getConfederation());

        final Team team3 = teams.get(2);
        assertEquals("e107d069-b277-4902-bdad-7091a494a8b3", team3.getId());
        assertEquals("England", team3.getName());
        assertEquals("ENG.png", team3.getImagePath());
        assertEquals(Confederation.UEFA, team3.getConfederation());
    }

    @Test
    void shouldReturnTeamsInConfederation() {
        // Given
        final QueryResponse<DatabaseRecord> queryResponse = mock(QueryResponse.class);
        when(queryResponse.getRecordCount())
            .thenReturn(2);
        when(queryResponse.getRecords())
            .thenReturn(List.of(BOSNIA, ENGLAND));

        when(queryService.retrieveRecords(any()))
            .thenReturn(queryResponse);

        // When
        final List<Team> teams = service.getTeams(Confederation.UEFA, null);

        // Then
        final ArgumentCaptor<QueryRequest<Team>> requestCaptor = ArgumentCaptor.forClass(QueryRequest.class);
        verify(queryService).retrieveRecords(requestCaptor.capture());
        final QueryRequest<Team> request = requestCaptor.getValue();

        final Table table = request.getTable();
        assertEquals("predictor", table.getSchema());
        assertEquals("teams", table.getTable());

        assertEquals(1, request.getConditionGroup().getConditions().size());

        final QueryCondition condition = request.getConditionGroup().getConditions().get(0);
        assertEquals(List.of("confederation"), condition.getColumn().getParts());
        assertEquals(ConditionOperator.EQUAL, condition.getOperator());
        assertEquals(Confederation.UEFA, condition.getValue());

        final OrderBy orderBy = request.getOrderBy();
        assertEquals(List.of("name"), orderBy.getColumn().getParts());
        assertEquals(OrderDirection.ASCENDING, orderBy.getDirection());

        assertEquals(2, teams.size());

        final Team team1 = teams.get(0);
        assertEquals("c08fd796-7fea-40d9-9a0a-cb3a49cce2e4", team1.getId());
        assertEquals("Bosnia & Herzegovina", team1.getName());
        assertEquals("BIH.png", team1.getImagePath());
        assertEquals(Confederation.UEFA, team1.getConfederation());

        final Team team2 = teams.get(1);
        assertEquals("e107d069-b277-4902-bdad-7091a494a8b3", team2.getId());
        assertEquals("England", team2.getName());
        assertEquals("ENG.png", team2.getImagePath());
        assertEquals(Confederation.UEFA, team2.getConfederation());
    }

    @Test
    void shouldReturnTeamsInTournament() {
        // Given
        final QueryResponse<DatabaseRecord> queryResponse = mock(QueryResponse.class);
        when(queryResponse.getRecordCount())
            .thenReturn(2);
        when(queryResponse.getRecords())
            .thenReturn(List.of(BOSNIA, ENGLAND));

        when(queryService.retrieveRecords(any()))
            .thenReturn(queryResponse);

        // When
        final List<Team> teams = service.getTeams(null, "7a5d1149-7be0-4cdd-a651-e54ee8cd4051");

        // Then
        final ArgumentCaptor<QueryRequest<Team>> requestCaptor = ArgumentCaptor.forClass(QueryRequest.class);
        verify(queryService).retrieveRecords(requestCaptor.capture());
        final QueryRequest<Team> request = requestCaptor.getValue();

        assertTrue(request.getDistinct());
        assertEquals(4, request.getColumns().size());

        final Column column1 = request.getColumns().get(0);
        assertEquals(List.of("team", "id"), column1.getParts());

        final Column column2 = request.getColumns().get(1);
        assertEquals(List.of("team", "name"), column2.getParts());

        final Column column3 = request.getColumns().get(2);
        assertEquals(List.of("team", "imagePath"), column3.getParts());

        final Column column4 = request.getColumns().get(3);
        assertEquals(List.of("team", "confederation"), column4.getParts());

        final Table table = request.getTable();
        assertEquals("predictor", table.getSchema());
        assertEquals("teams", table.getTable());
        assertEquals("team", table.getAlias());

        assertEquals(1, request.getJoins().size());

        final QueryJoin<GroupTeam> queryJoin = (QueryJoin<GroupTeam>) request.getJoins().get(0);
        assertEquals("teamIds", queryJoin.getAlias());
        assertEquals(JoinType.INNER, queryJoin.getJoinType());

        final QueryRequest<GroupTeam> joinQuery = queryJoin.getQuery();
        assertTrue(joinQuery.getDistinct());
        assertEquals(1, joinQuery.getColumns().size());

        final Column joinQueryColumn = joinQuery.getColumns().get(0);
        assertEquals(List.of("teamId"), joinQueryColumn.getParts());

        final Table joinQueryTable = joinQuery.getTable();
        assertEquals("predictor", joinQueryTable.getSchema());
        assertEquals("group-teams_7a5d1149-7be0-4cdd-a651-e54ee8cd4051", joinQueryTable.getTable());

        assertEquals(2, joinQuery.getJoins().size());

        final QueryJoin<MatchRecord> joinQueryJoin1 = (QueryJoin<MatchRecord>) joinQuery.getJoins().get(0);
        assertEquals(JoinType.UNION, joinQueryJoin1.getJoinType());

        final QueryRequest<MatchRecord> joinQueryJoin1Query = joinQueryJoin1.getQuery();
        assertTrue(joinQueryJoin1Query.getDistinct());
        assertEquals(1, joinQueryJoin1Query.getColumns().size());

        final Column joinQueryJoin1QueryColumn = joinQueryJoin1Query.getColumns().get(0);
        assertEquals(List.of("homeTeamId"), joinQueryJoin1QueryColumn.getParts());

        final Table joinQueryJoin1QueryTable = joinQueryJoin1Query.getTable();
        assertEquals("predictor", joinQueryJoin1QueryTable.getSchema());
        assertEquals("matches_7a5d1149-7be0-4cdd-a651-e54ee8cd4051", joinQueryJoin1QueryTable.getTable());

        final QueryJoin<MatchRecord> joinQueryJoin2 = (QueryJoin<MatchRecord>) joinQuery.getJoins().get(1);
        assertEquals(JoinType.UNION, joinQueryJoin2.getJoinType());

        final QueryRequest<MatchRecord> joinQueryJoin2Query = joinQueryJoin2.getQuery();
        assertTrue(joinQueryJoin2Query.getDistinct());
        assertEquals(1, joinQueryJoin2Query.getColumns().size());

        final Column joinQueryJoin2QueryColumn = joinQueryJoin2Query.getColumns().get(0);
        assertEquals(List.of("awayTeamId"), joinQueryJoin2QueryColumn.getParts());

        final Table joinQueryJoin2QueryTable = joinQueryJoin2Query.getTable();
        assertEquals("predictor", joinQueryJoin2QueryTable.getSchema());
        assertEquals("matches_7a5d1149-7be0-4cdd-a651-e54ee8cd4051", joinQueryJoin2QueryTable.getTable());

        final QueryCondition queryJoinCondition = queryJoin.getJoinCondition();
        assertEquals(List.of("team", "id"), queryJoinCondition.getColumn().getParts());

        final Column queryJoinConditionValue = (Column) queryJoinCondition.getValue();
        assertEquals(List.of("teamIds", "teamId"), queryJoinConditionValue.getParts());

        final OrderBy orderBy = request.getOrderBy();
        assertEquals(List.of("name"), orderBy.getColumn().getParts());
        assertEquals(OrderDirection.ASCENDING, orderBy.getDirection());

        assertEquals(2, teams.size());

        assertEquals(2, teams.size());

        final Team team1 = teams.get(0);
        assertEquals("c08fd796-7fea-40d9-9a0a-cb3a49cce2e4", team1.getId());
        assertEquals("Bosnia & Herzegovina", team1.getName());
        assertEquals("BIH.png", team1.getImagePath());
        assertEquals(Confederation.UEFA, team1.getConfederation());

        final Team team2 = teams.get(1);
        assertEquals("e107d069-b277-4902-bdad-7091a494a8b3", team2.getId());
        assertEquals("England", team2.getName());
        assertEquals("ENG.png", team2.getImagePath());
        assertEquals(Confederation.UEFA, team2.getConfederation());
    }

    @Test
    void shouldCreateNewTeams() {
        // Given
        final List<Team> teams = List.of(BOSNIA, BOTSWANA);

        // When
        final List<Team> created = service.createTeams(teams);

        // Then
        final ArgumentCaptor<UpdateRequest<Team>> updateCaptor = ArgumentCaptor.forClass(UpdateRequest.class);
        verify(queryService).updateRecords(updateCaptor.capture());
        final UpdateRequest<Team> updateRequest = updateCaptor.getValue();

        assertEquals(SqlOperator.INSERT, updateRequest.getOperation());

        final Table table = updateRequest.getTable();
        assertEquals("predictor", table.getSchema());
        assertEquals("teams", table.getTable());

        assertEquals(2, updateRequest.getRecords().size());

        final Team record1 = updateRequest.getRecords().get(0);
        assertNotNull(record1.getId());
        assertEquals("Bosnia & Herzegovina", record1.getName());
        assertEquals("BIH.png", record1.getImagePath());
        assertEquals(Confederation.UEFA, record1.getConfederation());

        final Team record2 = updateRequest.getRecords().get(1);
        assertNotNull(record2.getId());
        assertEquals("Botswana", record2.getName());
        assertEquals("BOT.png", record2.getImagePath());
        assertEquals(Confederation.CAF, record2.getConfederation());

        assertEquals(2, created.size());

        final Team team1 = created.get(0);
        assertNotNull(team1.getId());
        assertEquals("Bosnia & Herzegovina", team1.getName());
        assertEquals("BIH.png", team1.getImagePath());
        assertEquals(Confederation.UEFA, team1.getConfederation());

        final Team team2 = created.get(1);
        assertNotNull(team2.getId());
        assertEquals("Botswana", team2.getName());
        assertEquals("BOT.png", team2.getImagePath());
        assertEquals(Confederation.CAF, team2.getConfederation());
    }

    @Test
    void shouldUpdateExistingTeams() {
        // Given
        final List<TeamUpdate> teamUpdates = List.of(
            ImmutableTeamUpdate.builder()
                .id("c08fd796-7fea-40d9-9a0a-cb3a49cce2e4")
                .confederation(Confederation.UEFA)
                .build(),
            ImmutableTeamUpdate.builder()
                .id("6ee28143-1286-4618-a8b9-ad86d348ead1")
                .imagePath("BOT.png")
                .build()
        );

        final QueryResponse<DatabaseRecord> response = mock(QueryResponse.class);
        when(response.getRecordCount())
            .thenReturn(2);
        when(response.getRecords())
            .thenReturn(List.of(BOSNIA, BOTSWANA));

        when(queryService.retrieveRecords(any()))
            .thenReturn(response);

        // When
        final List<Team> updated = service.updateTeams(teamUpdates);

        // Then
        final ArgumentCaptor<UpdateRequest<TeamUpdate>> updateCaptor = ArgumentCaptor.forClass(UpdateRequest.class);
        verify(queryService).updateRecords(updateCaptor.capture());
        final UpdateRequest<TeamUpdate> updateRequest = updateCaptor.getValue();

        assertEquals(SqlOperator.UPDATE, updateRequest.getOperation());

        final Table updateTable = updateRequest.getTable();
        assertEquals("predictor", updateTable.getSchema());
        assertEquals("teams", updateTable.getTable());

        assertEquals(2, updateRequest.getRecords().size());

        final TeamUpdate record1 = updateRequest.getRecords().get(0);
        assertEquals("c08fd796-7fea-40d9-9a0a-cb3a49cce2e4", record1.getId());
        assertEquals(Confederation.UEFA, record1.getConfederation());

        final TeamUpdate record2 = updateRequest.getRecords().get(1);
        assertEquals("6ee28143-1286-4618-a8b9-ad86d348ead1", record2.getId());
        assertEquals("BOT.png", record2.getImagePath());

        final ArgumentCaptor<QueryRequest<Team>> requestCaptor = ArgumentCaptor.forClass(QueryRequest.class);
        verify(queryService).retrieveRecords(requestCaptor.capture());
        final QueryRequest<Team> queryRequest = requestCaptor.getValue();

        final Table requestTable = queryRequest.getTable();
        assertEquals("predictor", requestTable.getSchema());
        assertEquals("teams", requestTable.getTable());

        assertEquals(1, queryRequest.getConditionGroup().getConditions().size());

        final QueryCondition queryCondition = queryRequest.getConditionGroup().getConditions().get(0);
        assertEquals(List.of("id"), queryCondition.getColumn().getParts());
        assertEquals(ConditionOperator.IN, queryCondition.getOperator());
        assertEquals(List.of("c08fd796-7fea-40d9-9a0a-cb3a49cce2e4", "6ee28143-1286-4618-a8b9-ad86d348ead1"), queryCondition.getValue());

        final OrderBy queryOrderBy = queryRequest.getOrderBy();
        assertEquals(List.of("name"), queryOrderBy.getColumn().getParts());
        assertEquals(OrderDirection.ASCENDING, queryOrderBy.getDirection());

        assertEquals(2, updated.size());

        final Team team1 = updated.get(0);
        assertEquals("c08fd796-7fea-40d9-9a0a-cb3a49cce2e4", team1.getId());
        assertEquals("Bosnia & Herzegovina", team1.getName());
        assertEquals("BIH.png", team1.getImagePath());
        assertEquals(Confederation.UEFA, team1.getConfederation());

        final Team team2 = updated.get(1);
        assertEquals("6ee28143-1286-4618-a8b9-ad86d348ead1", team2.getId());
        assertEquals("Botswana", team2.getName());
        assertEquals("BOT.png", team2.getImagePath());
        assertEquals(Confederation.CAF, team2.getConfederation());
    }

    @Test
    void shouldReturnTeamById() {
        // Given
        final QueryResponse<DatabaseRecord> response = mock(QueryResponse.class);
        when(response.getRecordCount())
            .thenReturn(1);
        when(response.getRecords())
            .thenReturn(List.of(BOSNIA));

        when(queryService.retrieveRecords(any()))
            .thenReturn(response);

        // When
        final Team team = service.getTeamById("c08fd796-7fea-40d9-9a0a-cb3a49cce2e4");

        // Then
        final ArgumentCaptor<QueryRequest<Team>> requestCaptor = ArgumentCaptor.forClass(QueryRequest.class);
        verify(queryService).retrieveRecords(requestCaptor.capture());
        final QueryRequest<Team> request = requestCaptor.getValue();

        final Table table = request.getTable();
        assertEquals("predictor", table.getSchema());
        assertEquals("teams", table.getTable());

        assertEquals(1, request.getConditionGroup().getConditions().size());

        final QueryCondition condition = request.getConditionGroup().getConditions().get(0);
        assertEquals(List.of("id"), condition.getColumn().getParts());
        assertEquals(ConditionOperator.EQUAL, condition.getOperator());
        assertEquals("c08fd796-7fea-40d9-9a0a-cb3a49cce2e4", condition.getValue());

        assertEquals("c08fd796-7fea-40d9-9a0a-cb3a49cce2e4", team.getId());
        assertEquals("Bosnia & Herzegovina", team.getName());
        assertEquals("BIH.png", team.getImagePath());
        assertEquals(Confederation.UEFA, team.getConfederation());
    }

    @Test
    void shouldRaiseExceptionIfTeamNotFound() {
        // Given
        final QueryResponse<DatabaseRecord> response = mock(QueryResponse.class);
        when(response.getRecordCount())
            .thenReturn(0);

        when(queryService.retrieveRecords(any()))
            .thenReturn(response);

        // When
        final ResponseStatusException rse = assertThrows(ResponseStatusException.class, () -> service.getTeamById("c08fd796-7fea-40d9-9a0a-cb3a49cce2e4"));

        // Then
        assertEquals(HttpStatus.NOT_FOUND, rse.getStatusCode());
        assertEquals("No teams found with a matching id.", rse.getReason());
    }

    @Test
    void shouldDeleteTeamById() {
        // When
        service.deleteTeamById("c08fd796-7fea-40d9-9a0a-cb3a49cce2e4");

        // Then
        final ArgumentCaptor<UpdateRequest<Team>> updateCaptor = ArgumentCaptor.forClass(UpdateRequest.class);
        verify(queryService).updateRecords(updateCaptor.capture());
        final UpdateRequest<Team> updateRequest = updateCaptor.getValue();

        assertEquals(SqlOperator.DELETE, updateRequest.getOperation());

        final Table table = updateRequest.getTable();
        assertEquals("predictor", table.getSchema());
        assertEquals("teams", table.getTable());

        assertEquals(1, updateRequest.getConditionGroup().getConditions().size());

        final QueryCondition condition = updateRequest.getConditionGroup().getConditions().get(0);
        assertEquals(List.of("id"), condition.getColumn().getParts());
        assertEquals(ConditionOperator.EQUAL, condition.getOperator());
        assertEquals("c08fd796-7fea-40d9-9a0a-cb3a49cce2e4", condition.getValue());
    }
}
