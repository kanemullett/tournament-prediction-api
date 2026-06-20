package com.kanemullett.service;

import java.util.List;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertThrows;
import org.junit.jupiter.api.Test;
import org.mockito.ArgumentCaptor;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.times;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;
import org.springframework.http.HttpStatus;
import org.springframework.web.server.ResponseStatusException;

import com.kanemullett.model.Competition;
import com.kanemullett.model.CompetitionUpdate;
import com.kanemullett.model.CompetitionUser;
import com.kanemullett.model.DatabaseRecord;
import com.kanemullett.model.ImmutableCompetition;
import com.kanemullett.model.ImmutableCompetitionUpdate;
import com.kanemullett.model.ImmutableCompetitionUser;
import com.kanemullett.model.ImmutableUser;
import com.kanemullett.model.QueryCondition;
import com.kanemullett.model.QueryRequest;
import com.kanemullett.model.QueryResponse;
import com.kanemullett.model.Table;
import com.kanemullett.model.UpdateRequest;
import com.kanemullett.model.User;
import com.kanemullett.model.type.ConditionJoin;
import com.kanemullett.model.type.ConditionOperator;
import com.kanemullett.model.type.SqlOperator;

public class CompetitionServiceTest {

    private final DatabaseQueryService queryService = mock(DatabaseQueryService.class);

    private final CompetitionService service = new CompetitionService(queryService);

    @Test
    void shouldReturnCompetitions() {
        // Give
        final QueryResponse<DatabaseRecord> queryResponse = mock(QueryResponse.class);
        when(queryResponse.getRecordCount())
            .thenReturn(2);
        when(queryResponse.getRecords())
            .thenReturn(List.of(
                ImmutableCompetition.builder()
                    .id("71d14fb4-ba29-47f7-a235-d2675028d700")
                    .name("The Boys")
                    .tournamentId("72ed614f-06a3-41b4-9d50-52e1f8fd9e58")
                    .build(),
                ImmutableCompetition.builder()
                    .id("4cb9e47c-722d-4de0-b63a-ee5f9b9f2900")
                    .name("Meine Familie")
                    .tournamentId("72ed614f-06a3-41b4-9d50-52e1f8fd9e58")
                    .build()
            ));

        when(queryService.retrieveRecords(any()))
            .thenReturn(queryResponse);

        // When
        final List<Competition> competitions = service.getCompetitions();

        // Then
        final ArgumentCaptor<QueryRequest<Competition>> requestCaptor = ArgumentCaptor.forClass(QueryRequest.class);
        verify(queryService).retrieveRecords(requestCaptor.capture());
        final QueryRequest<Competition> request = requestCaptor.getValue();
        
        final Table requestTable = request.getTable();
        assertEquals("predictor", requestTable.getSchema());
        assertEquals("competitions", requestTable.getTable());

        assertEquals(2, competitions.size());

        final Competition competition1 = competitions.get(0);
        assertEquals("71d14fb4-ba29-47f7-a235-d2675028d700", competition1.getId());
        assertEquals("The Boys", competition1.getName());
        assertEquals("72ed614f-06a3-41b4-9d50-52e1f8fd9e58", competition1.getTournamentId());

        final Competition competition2 = competitions.get(1);
        assertEquals("4cb9e47c-722d-4de0-b63a-ee5f9b9f2900", competition2.getId());
        assertEquals("Meine Familie", competition2.getName());
        assertEquals("72ed614f-06a3-41b4-9d50-52e1f8fd9e58", competition2.getTournamentId());
    }

    @Test
    void shouldCreateCompetitions() {
        // Given
        final List<Competition> competitions = List.of(
            ImmutableCompetition.builder()
                .name("The Boys")
                .tournamentId("72ed614f-06a3-41b4-9d50-52e1f8fd9e58")
                .build(),
            ImmutableCompetition.builder()
                .name("Meine Familie")
                .tournamentId("72ed614f-06a3-41b4-9d50-52e1f8fd9e58")
                .build()
        );

        // When
        final List<Competition> created = service.createCompetitions(competitions);

        // Then
        final ArgumentCaptor<UpdateRequest<Competition>> updateCaptor = ArgumentCaptor.forClass(UpdateRequest.class);
        verify(queryService).updateRecords(updateCaptor.capture());
        final UpdateRequest<Competition> request = updateCaptor.getValue();

        assertEquals(SqlOperator.INSERT, request.getOperation());

        final Table requestTable = request.getTable();
        assertEquals("predictor", requestTable.getSchema());
        assertEquals("competitions", requestTable.getTable());

        assertEquals(2, request.getRecords().size());

        final Competition record1 = request.getRecords().get(0);
        assertNotNull(record1.getId());
        assertEquals("The Boys", record1.getName());
        assertEquals("72ed614f-06a3-41b4-9d50-52e1f8fd9e58", record1.getTournamentId());

        final Competition record2 = request.getRecords().get(1);
        assertNotNull(record2.getId());
        assertEquals("Meine Familie", record2.getName());
        assertEquals("72ed614f-06a3-41b4-9d50-52e1f8fd9e58", record2.getTournamentId());

        assertEquals(2, created.size());

        final Competition competition1 = created.get(0);
        assertNotNull(competition1.getId());
        assertEquals("The Boys", competition1.getName());
        assertEquals("72ed614f-06a3-41b4-9d50-52e1f8fd9e58", competition1.getTournamentId());

        final Competition competition2 = created.get(1);
        assertNotNull(competition2.getId());
        assertEquals("Meine Familie", competition2.getName());
        assertEquals("72ed614f-06a3-41b4-9d50-52e1f8fd9e58", competition2.getTournamentId());
    }

    @Test
    void shouldUpdateCompetitions() {
        // Given
        final List<CompetitionUpdate> competitionUpdates = List.of(
            ImmutableCompetitionUpdate.builder()
                .id("71d14fb4-ba29-47f7-a235-d2675028d700")
                .name("The Boys")
                .build(),
            ImmutableCompetitionUpdate.builder()
                .id("4cb9e47c-722d-4de0-b63a-ee5f9b9f2900")
                .name("Meine Familie")
                .build()
        );

        final QueryResponse<DatabaseRecord> queryResponse = mock(QueryResponse.class);
        when(queryResponse.getRecordCount())
            .thenReturn(2);
        when(queryResponse.getRecords())
            .thenReturn(List.of(
                ImmutableCompetition.builder()
                    .id("71d14fb4-ba29-47f7-a235-d2675028d700")
                    .name("The Boys")
                    .tournamentId("72ed614f-06a3-41b4-9d50-52e1f8fd9e58")
                    .build(),
                ImmutableCompetition.builder()
                    .id("4cb9e47c-722d-4de0-b63a-ee5f9b9f2900")
                    .name("Meine Familie")
                    .tournamentId("72ed614f-06a3-41b4-9d50-52e1f8fd9e58")
                    .build()
            ));

        when(queryService.retrieveRecords(any()))
            .thenReturn(queryResponse);

        // When
        final List<Competition> updated = service.updateCompetitions(competitionUpdates);

        // Then
        final ArgumentCaptor<UpdateRequest<CompetitionUpdate>> updateCaptor = ArgumentCaptor.forClass(UpdateRequest.class);
        verify(queryService).updateRecords(updateCaptor.capture());
        final UpdateRequest<CompetitionUpdate> updateRequest = updateCaptor.getValue();

        assertEquals(SqlOperator.UPDATE, updateRequest.getOperation());

        final Table updateTable = updateRequest.getTable();
        assertEquals("predictor", updateTable.getSchema());
        assertEquals("competitions", updateTable.getTable());

        assertEquals(2, updateRequest.getRecords().size());

        final CompetitionUpdate update1 = updateRequest.getRecords().get(0);
        assertEquals("71d14fb4-ba29-47f7-a235-d2675028d700", update1.getId());
        assertEquals("The Boys", update1.getName());

        final CompetitionUpdate update2 = updateRequest.getRecords().get(1);
        assertEquals("4cb9e47c-722d-4de0-b63a-ee5f9b9f2900", update2.getId());
        assertEquals("Meine Familie", update2.getName());

        final ArgumentCaptor<QueryRequest<Competition>> queryCaptor = ArgumentCaptor.forClass(QueryRequest.class);
        verify(queryService).retrieveRecords(queryCaptor.capture());
        final QueryRequest<Competition> queryRequest = queryCaptor.getValue();

        final Table queryTable = queryRequest.getTable();
        assertEquals("predictor", queryTable.getSchema());
        assertEquals("competitions", queryTable.getTable());

        assertEquals(1, queryRequest.getConditionGroup().getConditions().size());

        final QueryCondition queryCondition = queryRequest.getConditionGroup().getConditions().get(0);
        assertEquals(List.of("id"), queryCondition.getColumn().getParts());
        assertEquals(ConditionOperator.IN, queryCondition.getOperator());
        assertEquals(List.of("71d14fb4-ba29-47f7-a235-d2675028d700", "4cb9e47c-722d-4de0-b63a-ee5f9b9f2900"), queryCondition.getValue());

        assertEquals(2, updated.size());

        final Competition competition1 = updated.get(0);
        assertEquals("71d14fb4-ba29-47f7-a235-d2675028d700", competition1.getId());
        assertEquals("The Boys", competition1.getName());
        assertEquals("72ed614f-06a3-41b4-9d50-52e1f8fd9e58", competition1.getTournamentId());

        final Competition competition2 = updated.get(1);
        assertEquals("4cb9e47c-722d-4de0-b63a-ee5f9b9f2900", competition2.getId());
        assertEquals("Meine Familie", competition2.getName());
        assertEquals("72ed614f-06a3-41b4-9d50-52e1f8fd9e58", competition1.getTournamentId());
    }

    @Test
    void shouldReturnCompetitionById() {
        // Given
        final QueryResponse<DatabaseRecord> queryResponse = mock(QueryResponse.class);
        when(queryResponse.getRecordCount())
            .thenReturn(1);
        when(queryResponse.getRecords())
            .thenReturn(List.of(
                ImmutableCompetition.builder()
                    .id("71d14fb4-ba29-47f7-a235-d2675028d700")
                    .name("The Boys")
                    .tournamentId("72ed614f-06a3-41b4-9d50-52e1f8fd9e58")
                    .build()
            ));

        when(queryService.retrieveRecords(any()))
            .thenReturn(queryResponse);

        // When
        final Competition competition = service.getCompetitionById("71d14fb4-ba29-47f7-a235-d2675028d700");

        // Then
        final ArgumentCaptor<QueryRequest<Competition>> queryCaptor = ArgumentCaptor.forClass(QueryRequest.class);
        verify(queryService).retrieveRecords(queryCaptor.capture());
        final QueryRequest<Competition> queryRequest = queryCaptor.getValue();

        final Table queryTable = queryRequest.getTable();
        assertEquals("predictor", queryTable.getSchema());
        assertEquals("competitions", queryTable.getTable());

        assertEquals(1, queryRequest.getConditionGroup().getConditions().size());

        final QueryCondition queryCondition = queryRequest.getConditionGroup().getConditions().get(0);
        assertEquals(List.of("id"), queryCondition.getColumn().getParts());
        assertEquals(ConditionOperator.EQUAL, queryCondition.getOperator());
        assertEquals("71d14fb4-ba29-47f7-a235-d2675028d700", queryCondition.getValue());

        assertEquals("71d14fb4-ba29-47f7-a235-d2675028d700", competition.getId());
        assertEquals("The Boys", competition.getName());
        assertEquals("72ed614f-06a3-41b4-9d50-52e1f8fd9e58", competition.getTournamentId());
    }

    @Test
    void shouldErrorIfCompetitionNotFound() {
        // Given
        final QueryResponse<DatabaseRecord> queryResponse = mock(QueryResponse.class);
        when(queryResponse.getRecordCount())
            .thenReturn(0);

        when(queryService.retrieveRecords(any()))
            .thenReturn(queryResponse);

        // When
        final ResponseStatusException rse = assertThrows(ResponseStatusException.class, () -> service.getCompetitionById("71d14fb4-ba29-47f7-a235-d2675028d700"));

        // Then
        assertEquals(HttpStatus.NOT_FOUND, rse.getStatusCode());
        assertEquals("No competitions found with a matching id.", rse.getReason());
    }

    @Test
    void shouldDeleteCompetition() {
        // When
        service.deleteCompetitionById("71d14fb4-ba29-47f7-a235-d2675028d700");

        // Then
        final ArgumentCaptor<UpdateRequest<Competition>> updateCaptor = ArgumentCaptor.forClass(UpdateRequest.class);
        verify(queryService).updateRecords(updateCaptor.capture());
        final UpdateRequest<Competition> updateRequest = updateCaptor.getValue();

        assertEquals(SqlOperator.DELETE, updateRequest.getOperation());

        final Table updateTable = updateRequest.getTable();
        assertEquals("predictor", updateTable.getSchema());
        assertEquals("competitions", updateTable.getTable());

        assertEquals(1, updateRequest.getConditionGroup().getConditions().size());

        final QueryCondition updateCondition = updateRequest.getConditionGroup().getConditions().get(0);
        assertEquals(List.of("id"), updateCondition.getColumn().getParts());
        assertEquals(ConditionOperator.EQUAL, updateCondition.getOperator());
        assertEquals("71d14fb4-ba29-47f7-a235-d2675028d700", updateCondition.getValue());
    }

    @Test
    void shouldAddUsersToCompetition() {
        // Given
        final List<String> usernames = List.of("user1", "user2");

        final QueryResponse<DatabaseRecord> competitionResponse = mock(QueryResponse.class);
        when(competitionResponse.getRecordCount())
            .thenReturn(1);
        when(competitionResponse.getRecords())
            .thenReturn(List.of(
                ImmutableCompetition.builder()
                    .id("6407ed54-6fc7-4a88-9033-047472f34611")
                    .name("Test Competition")
                    .tournamentId("f6d32424-fee4-41e3-8973-4741beeed161")
                    .build()
            ));

        final QueryResponse<DatabaseRecord> userResponse = mock(QueryResponse.class);
        when(userResponse.getRecordCount())
            .thenReturn(2);
        when(userResponse.getRecords())
            .thenReturn(List.of(
                ImmutableUser.builder()
                    .id("user1")
                    .displayName("User 1")
                    .build(),
                ImmutableUser.builder()
                    .id("user2")
                    .displayName("User 2")
                    .build()
            ));

        final QueryResponse<DatabaseRecord> existsResponse = mock(QueryResponse.class);
        when(existsResponse.getRecordCount())
            .thenReturn(0);

        when(queryService.retrieveRecords(any()))
            .thenReturn(competitionResponse, userResponse, existsResponse);

        // When
        service.addUsersToCompetition("6407ed54-6fc7-4a88-9033-047472f34611", usernames);

        // Then
        final ArgumentCaptor<QueryRequest<?>> requestCaptor = ArgumentCaptor.forClass(QueryRequest.class);
        verify(queryService, times(3)).retrieveRecords(requestCaptor.capture());
        final List<QueryRequest<?>> requests = requestCaptor.getAllValues();

        final QueryRequest<Competition> competitionRequest = (QueryRequest<Competition>) requests.get(0);

        final Table competitionTable = competitionRequest.getTable();
        assertEquals("predictor", competitionTable.getSchema());
        assertEquals("competitions", competitionTable.getTable());

        assertEquals(1, competitionRequest.getConditionGroup().getConditions().size());

        final QueryCondition competitionCondition = competitionRequest.getConditionGroup().getConditions().get(0);
        assertEquals(List.of("id"), competitionCondition.getColumn().getParts());
        assertEquals(ConditionOperator.EQUAL, competitionCondition.getOperator());
        assertEquals("6407ed54-6fc7-4a88-9033-047472f34611", competitionCondition.getValue());

        final QueryRequest<User> userRequest = (QueryRequest<User>) requests.get(1);

        final Table userTable = userRequest.getTable();
        assertEquals("predictor", userTable.getSchema());
        assertEquals("users", userTable.getTable());

        assertEquals(1, userRequest.getConditionGroup().getConditions().size());

        final QueryCondition userCondition = userRequest.getConditionGroup().getConditions().get(0);
        assertEquals(List.of("id"), userCondition.getColumn().getParts());
        assertEquals(ConditionOperator.IN, userCondition.getOperator());
        assertEquals(List.of("user1", "user2"), userCondition.getValue());

        final QueryRequest<CompetitionUser> competitionUserRequest = (QueryRequest<CompetitionUser>) requests.get(2);

        final Table competitionUserTable = competitionUserRequest.getTable();
        assertEquals("predictor", competitionUserTable.getSchema());
        assertEquals("competition-users", competitionUserTable.getTable());

        assertEquals(2, competitionUserRequest.getConditionGroup().getConditions().size());

        final QueryCondition competitionUserCondition1 = competitionUserRequest.getConditionGroup().getConditions().get(0);
        assertEquals(List.of("competitionId"), competitionUserCondition1.getColumn().getParts());
        assertEquals(ConditionOperator.EQUAL, competitionUserCondition1.getOperator());
        assertEquals("6407ed54-6fc7-4a88-9033-047472f34611", competitionUserCondition1.getValue());

        final QueryCondition competitionUserCondition2 = competitionUserRequest.getConditionGroup().getConditions().get(1);
        assertEquals(List.of("username"), competitionUserCondition2.getColumn().getParts());
        assertEquals(ConditionOperator.IN, competitionUserCondition2.getOperator());
        assertEquals(List.of("user1", "user2"), competitionUserCondition2.getValue());

        final ArgumentCaptor<UpdateRequest<CompetitionUser>> updateCaptor = ArgumentCaptor.forClass(UpdateRequest.class);
        verify(queryService).updateRecords(updateCaptor.capture());
        final UpdateRequest<CompetitionUser> updateRequest = updateCaptor.getValue();

        assertEquals(SqlOperator.INSERT, updateRequest.getOperation());

        final Table updateTable = updateRequest.getTable();
        assertEquals("predictor", updateTable.getSchema());
        assertEquals("competition-users", updateTable.getTable());

        assertEquals(2, updateRequest.getRecords().size());

        final CompetitionUser record1 = updateRequest.getRecords().get(0);
        assertEquals("6407ed54-6fc7-4a88-9033-047472f34611", record1.getCompetitionId());
        assertEquals("user1", record1.getUsername());

        final CompetitionUser record2 = updateRequest.getRecords().get(1);
        assertEquals("6407ed54-6fc7-4a88-9033-047472f34611", record2.getCompetitionId());
        assertEquals("user2", record2.getUsername());
    }

    @Test
    void shouldErrorIfCompetitionNotFoundWhenAddingUsers() {
        // Given
        final List<String> usernames = List.of("user1", "user2");

        final QueryResponse<DatabaseRecord> queryResponse = mock(QueryResponse.class);
        when(queryResponse.getRecordCount())
            .thenReturn(0);
        when(queryResponse.getRecords())
            .thenReturn(List.of());

        when(queryService.retrieveRecords(any()))
            .thenReturn(queryResponse);

        // When
        final ResponseStatusException rse = assertThrows(ResponseStatusException.class, () -> service.addUsersToCompetition("6407ed54-6fc7-4a88-9033-047472f34611", usernames));

        // Then
        assertEquals(HttpStatus.NOT_FOUND, rse.getStatusCode());
        assertEquals("No competitions found with a matching id.", rse.getReason());
    }

    @Test
    void shouldErrorIfUserNotFoundWhenAddingUsersToCompetition() {
        // Given
        final List<String> usernames = List.of("user1", "user2");

        final Competition competition = mock(Competition.class);

        final QueryResponse<DatabaseRecord> competitionResponse = mock(QueryResponse.class);
        when(competitionResponse.getRecordCount())
            .thenReturn(1);
        when(competitionResponse.getRecords())
            .thenReturn(List.of(competition));

        final User user = mock(User.class);
        when(user.getId())
            .thenReturn("user1");

        final QueryResponse<DatabaseRecord> userResponse = mock(QueryResponse.class);
        when(userResponse.getRecordCount())
            .thenReturn(1);
        when(userResponse.getRecords())
            .thenReturn(List.of(user));

        when(queryService.retrieveRecords(any()))
            .thenReturn(competitionResponse, userResponse);

        // When
        final ResponseStatusException rse = assertThrows(ResponseStatusException.class, () -> service.addUsersToCompetition("6407ed54-6fc7-4a88-9033-047472f34611", usernames));

        // Then
        assertEquals(HttpStatus.BAD_REQUEST, rse.getStatusCode());
        assertEquals("No users found with usernames: [user2]", rse.getReason());
    }

    @Test
    void shouldErrorIfAddingUserAlreadyAssignedToCompetition() {
        // Given
        final List<String> usernames = List.of("user1", "user2");

        final Competition competition = mock(Competition.class);

        final QueryResponse<DatabaseRecord> competitionResponse = mock(QueryResponse.class);
        when(competitionResponse.getRecordCount())
            .thenReturn(1);
        when(competitionResponse.getRecords())
            .thenReturn(List.of(competition));

        final User user1 = mock(User.class);
        final User user2 = mock(User.class);

        final QueryResponse<DatabaseRecord> userResponse = mock(QueryResponse.class);
        when(userResponse.getRecordCount())
            .thenReturn(2);
        when(userResponse.getRecords())
            .thenReturn(List.of(user1, user2));

        final CompetitionUser competitionUser = ImmutableCompetitionUser.builder()
            .competitionId("6407ed54-6fc7-4a88-9033-047472f34611")
            .username("user1")
            .build();

        final QueryResponse<DatabaseRecord> competitionUserResponse = mock(QueryResponse.class);
        when(competitionUserResponse.getRecordCount())
            .thenReturn(1);
        when(competitionUserResponse.getRecords())
            .thenReturn(List.of(competitionUser));

        when(queryService.retrieveRecords(any()))
            .thenReturn(competitionResponse, userResponse, competitionUserResponse);

        // When
        final ResponseStatusException rse = assertThrows(ResponseStatusException.class, () -> service.addUsersToCompetition("6407ed54-6fc7-4a88-9033-047472f34611", usernames));

        // Then
        assertEquals(HttpStatus.CONFLICT, rse.getStatusCode());
        assertEquals("Users already assigned to this competition: [user1]", rse.getReason());
    }

    @Test
    void shouldRemoveUserFromCompetition() {
        // Given
        final QueryResponse<DatabaseRecord> competitionResponse = mock(QueryResponse.class);
        when(competitionResponse.getRecordCount())
            .thenReturn(1);
        when(competitionResponse.getRecords())
            .thenReturn(List.of(
                ImmutableCompetition.builder()
                    .id("6407ed54-6fc7-4a88-9033-047472f34611")
                    .name("Test Competition")
                    .tournamentId("f6d32424-fee4-41e3-8973-4741beeed161")
                    .build()
            ));

        final QueryResponse<DatabaseRecord> userResponse = mock(QueryResponse.class);
        when(userResponse.getRecordCount())
            .thenReturn(1);
        when(userResponse.getRecords())
            .thenReturn(List.of(
                ImmutableUser.builder()
                    .id("user1")
                    .displayName("User 1")
                    .build()
            ));

        when(queryService.retrieveRecords(any()))
            .thenReturn(competitionResponse, userResponse);

        // When
        service.removeUserFromCompetition("6407ed54-6fc7-4a88-9033-047472f34611", "user1");

        // Then
        final ArgumentCaptor<QueryRequest<?>> requestCaptor = ArgumentCaptor.forClass(QueryRequest.class);
        verify(queryService, times(2)).retrieveRecords(requestCaptor.capture());
        final List<QueryRequest<?>> requests = requestCaptor.getAllValues();

        final QueryRequest<Competition> competitionRequest = (QueryRequest<Competition>) requests.get(0);

        final Table competitionTable = competitionRequest.getTable();
        assertEquals("predictor", competitionTable.getSchema());
        assertEquals("competitions", competitionTable.getTable());

        assertEquals(1, competitionRequest.getConditionGroup().getConditions().size());

        final QueryCondition competitionCondition = competitionRequest.getConditionGroup().getConditions().get(0);
        assertEquals(List.of("id"), competitionCondition.getColumn().getParts());
        assertEquals(ConditionOperator.EQUAL, competitionCondition.getOperator());
        assertEquals("6407ed54-6fc7-4a88-9033-047472f34611", competitionCondition.getValue());

        final QueryRequest<User> userRequest = (QueryRequest<User>) requests.get(1);

        final Table userTable = userRequest.getTable();
        assertEquals("predictor", userTable.getSchema());
        assertEquals("users", userTable.getTable());

        assertEquals(1, userRequest.getConditionGroup().getConditions().size());

        final QueryCondition userCondition = userRequest.getConditionGroup().getConditions().get(0);
        assertEquals(List.of("id"), userCondition.getColumn().getParts());
        assertEquals(ConditionOperator.EQUAL, userCondition.getOperator());
        assertEquals("user1", userCondition.getValue());

        final ArgumentCaptor<UpdateRequest<CompetitionUser>> updateCaptor = ArgumentCaptor.forClass(UpdateRequest.class);
        verify(queryService).updateRecords(updateCaptor.capture());
        final UpdateRequest<CompetitionUser> updateRequest = updateCaptor.getValue();

        assertEquals(SqlOperator.DELETE, updateRequest.getOperation());

        final Table updateTable = updateRequest.getTable();
        assertEquals("predictor", updateTable.getSchema());
        assertEquals("competition-users", updateTable.getTable());

        assertEquals(ConditionJoin.AND, updateRequest.getConditionGroup().getJoin());
        assertEquals(2, updateRequest.getConditionGroup().getConditions().size());

        final QueryCondition queryCondition1 = updateRequest.getConditionGroup().getConditions().get(0);
        assertEquals(List.of("competitionId"), queryCondition1.getColumn().getParts());
        assertEquals(ConditionOperator.EQUAL, queryCondition1.getOperator());
        assertEquals("6407ed54-6fc7-4a88-9033-047472f34611", queryCondition1.getValue());

        final QueryCondition queryCondition2 = updateRequest.getConditionGroup().getConditions().get(1);
        assertEquals(List.of("username"), queryCondition2.getColumn().getParts());
        assertEquals(ConditionOperator.EQUAL, queryCondition2.getOperator());
        assertEquals("user1", queryCondition2.getValue());
    }

    @Test
    void shouldErrorIfCompetitionNotFoundWhenRemovingUser() {
        // Given
        final QueryResponse<DatabaseRecord> queryResponse = mock(QueryResponse.class);
        when(queryResponse.getRecordCount())
            .thenReturn(0);
        when(queryResponse.getRecords())
            .thenReturn(List.of());

        when(queryService.retrieveRecords(any()))
            .thenReturn(queryResponse);

        // When
        final ResponseStatusException rse = assertThrows(ResponseStatusException.class, () -> service.removeUserFromCompetition("6407ed54-6fc7-4a88-9033-047472f34611", "user1"));

        // Then
        assertEquals(HttpStatus.NOT_FOUND, rse.getStatusCode());
        assertEquals("No competitions found with a matching id.", rse.getReason());
    }

    @Test
    void shouldErrorIfUserNotFoundWhenRemovingUserFromCompetition() {
        // Given
        final Competition competition = mock(Competition.class);

        final QueryResponse<DatabaseRecord> competitionResponse = mock(QueryResponse.class);
        when(competitionResponse.getRecordCount())
            .thenReturn(1);
        when(competitionResponse.getRecords())
            .thenReturn(List.of(competition));

        final QueryResponse<DatabaseRecord> userResponse = mock(QueryResponse.class);
        when(userResponse.getRecordCount())
            .thenReturn(0);
        when(userResponse.getRecords())
            .thenReturn(List.of());

        when(queryService.retrieveRecords(any()))
            .thenReturn(competitionResponse, userResponse);

        // When
        final ResponseStatusException rse = assertThrows(ResponseStatusException.class, () -> service.removeUserFromCompetition("6407ed54-6fc7-4a88-9033-047472f34611", "user1"));

        // Then
        assertEquals(HttpStatus.NOT_FOUND, rse.getStatusCode());
        assertEquals("No users found with a matching username.", rse.getReason());
    }
}
