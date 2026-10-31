package com.kanemullett.service;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.times;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

import java.util.List;

import org.junit.jupiter.api.Test;
import org.mockito.ArgumentCaptor;
import org.springframework.http.HttpStatus;
import org.springframework.web.server.ResponseStatusException;

import com.kanemullett.model.Column;
import com.kanemullett.model.DatabaseRecord;
import com.kanemullett.model.ImmutableDatabaseRecord;
import com.kanemullett.model.ImmutableQueryCondition;
import com.kanemullett.model.ImmutableRound;
import com.kanemullett.model.ImmutableRoundUpdate;
import com.kanemullett.model.QueryCondition;
import com.kanemullett.model.QueryConditionGroup;
import com.kanemullett.model.QueryRequest;
import com.kanemullett.model.QueryResponse;
import com.kanemullett.model.Round;
import com.kanemullett.model.RoundUpdate;
import com.kanemullett.model.Table;
import com.kanemullett.model.TableJoin;
import com.kanemullett.model.UpdateRequest;
import com.kanemullett.model.type.ConditionOperator;
import com.kanemullett.model.type.JoinType;
import com.kanemullett.model.type.SqlOperator;

import jakarta.annotation.Nullable;

public class RoundServiceTest {

    private final DatabaseQueryService queryService = mock(DatabaseQueryService.class);

    private final RoundService roundService = new RoundService(queryService);

    private static final String TOURNAMENT_ID = "dc51daad-bf1a-43ea-a109-2b53d30de357";
    private static final Round ROUND_ONE = ImmutableRound.builder()
        .id("96074478-23c4-4b6f-a8a4-1abe9fac2659")
        .name("Round 1")
        .teamCount(32)
        .roundOrder(1)
        .twoLegs(true)
        .extraTime(true)
        .awayGoals(true)
        .build();
    private static final Round ROUND_TWO = ImmutableRound.builder()
        .id("e0ee5d0e-9d57-4c74-b938-0aa306a2313e")
        .name("Round 2")
        .teamCount(16)
        .roundOrder(2)
        .twoLegs(true)
        .extraTime(true)
        .awayGoals(true)
        .build();

    @Test
    void shouldReturnRounds() {
        // Given
        final QueryResponse<DatabaseRecord> existsResponse = buildTournamentExistsResponse();
        final QueryResponse<DatabaseRecord> roundsResponse = buildRoundsResponse(List.of(ROUND_ONE, ROUND_TWO));

        when(queryService.retrieveRecords(any()))
            .thenReturn(existsResponse, roundsResponse);

        // When
        final List<Round> rounds = roundService.getRounds(TOURNAMENT_ID);

        // Then
        final ArgumentCaptor<QueryRequest<DatabaseRecord>> requestCaptor = ArgumentCaptor.forClass(QueryRequest.class);
        verify(queryService, times(2)).retrieveRecords(requestCaptor.capture());
        final List<QueryRequest<DatabaseRecord>> requests = requestCaptor.getAllValues();

        assertTournamentExistsRequest(requests.get(0));
        assertRetrieveRoundsRequest(requests.get(1), null);

        assertEquals(2, rounds.size());
        assertRound(ROUND_ONE, rounds.get(0));
        assertRound(ROUND_TWO, rounds.get(1));
    }

    @Test
    void shouldErrorIfTournamentDoesNotExistWhileRetrievingRounds() {
        // Given
        final QueryResponse<DatabaseRecord> existsResponse = mock(QueryResponse.class);
        when(existsResponse.getRecordCount())
            .thenReturn(0);

        when(queryService.retrieveRecords(any()))
            .thenReturn(existsResponse);

        // When
        final ResponseStatusException rse = assertThrows(ResponseStatusException.class, () -> roundService.getRounds(TOURNAMENT_ID));

        // Then
        assertEquals(HttpStatus.NOT_FOUND, rse.getStatusCode());
        assertEquals("No tournaments found with a matching id.", rse.getReason());
    }

    @Test
    void shouldErrorIfTournamentHasNoKnockoutTemplateWhileRetrievingRounds() {
        // Given
        final QueryResponse<DatabaseRecord> existsResponse = mock(QueryResponse.class);
        when(existsResponse.getRecordCount())
            .thenReturn(1);
        when(existsResponse.getRecords())
            .thenReturn(List.of(
                ImmutableDatabaseRecord.builder()
                    .id(TOURNAMENT_ID)
                    .build()
            ));

        when(queryService.retrieveRecords(any()))
            .thenReturn(existsResponse);

        // When
        final ResponseStatusException rse = assertThrows(ResponseStatusException.class, () -> roundService.getRounds(TOURNAMENT_ID));

        // Then
        assertEquals(HttpStatus.NOT_FOUND, rse.getStatusCode());
        assertEquals("The tournament with the supplied id does not have a knockout stage.", rse.getReason());
    }

    @Test
    void shouldUpdateRounds() {
        // Given
        final QueryResponse<DatabaseRecord> existsResponse = buildTournamentExistsResponse();
        final QueryResponse<DatabaseRecord> roundsResponse = buildRoundsResponse(List.of(ROUND_ONE, ROUND_TWO));

        when(queryService.retrieveRecords(any()))
            .thenReturn(existsResponse, roundsResponse);

        final List<RoundUpdate> updates = List.of(
            ImmutableRoundUpdate.builder()
                .id("96074478-23c4-4b6f-a8a4-1abe9fac2659")
                .name("Round 1")
                .build(),
            ImmutableRoundUpdate.builder()
                .id("e0ee5d0e-9d57-4c74-b938-0aa306a2313e")
                .extraTime(true)
                .build()
        );

        // When
        final List<Round> updated = roundService.updateRounds(TOURNAMENT_ID, updates);

        // Then
        final ArgumentCaptor<QueryRequest<DatabaseRecord>> requestCaptor = ArgumentCaptor.forClass(QueryRequest.class);
        verify(queryService, times(2)).retrieveRecords(requestCaptor.capture());
        final List<QueryRequest<DatabaseRecord>> requests = requestCaptor.getAllValues();

        assertTournamentExistsRequest(requests.get(0));

        final QueryConditionGroup expectedConditionGroup = QueryConditionGroup.of(
            ImmutableQueryCondition.builder()
                .column(Column.of("id"))
                .operator(ConditionOperator.IN)
                .value(List.of("96074478-23c4-4b6f-a8a4-1abe9fac2659", "e0ee5d0e-9d57-4c74-b938-0aa306a2313e"))
                .build()
        );
        assertRetrieveRoundsRequest(requests.get(1), expectedConditionGroup);

        final ArgumentCaptor<UpdateRequest<RoundUpdate>> updateCaptor = ArgumentCaptor.forClass(UpdateRequest.class);
        verify(queryService).updateRecords(updateCaptor.capture());
        final UpdateRequest<RoundUpdate> updateRequest = updateCaptor.getValue();

        assertEquals(SqlOperator.UPDATE, updateRequest.getOperation());
        assertTable("predictor", "rounds_dc51daad-bf1a-43ea-a109-2b53d30de357", updateRequest.getTable());

        assertEquals(2, updateRequest.getRecords().size());
        assertRoundUpdate(updates.get(0), updateRequest.getRecords().get(0));
        assertRoundUpdate(updates.get(1), updateRequest.getRecords().get(1));

        assertEquals(RoundUpdate.class, updateRequest.getRecordClass());

        assertEquals(2, updated.size());
        assertRound(ROUND_ONE, updated.get(0));
        assertRound(ROUND_TWO, updated.get(1));
    }

    @Test
    void shouldErrorIfTournamentDoesNotExistWhileUpdatingRounds() {
        // Given
        final QueryResponse<DatabaseRecord> existsResponse = mock(QueryResponse.class);
        when(existsResponse.getRecordCount())
            .thenReturn(0);

        when(queryService.retrieveRecords(any()))
            .thenReturn(existsResponse);

        final List<RoundUpdate> updates = List.of(
            ImmutableRoundUpdate.builder()
                .id("96074478-23c4-4b6f-a8a4-1abe9fac2659")
                .name("Round 1")
                .build(),
            ImmutableRoundUpdate.builder()
                .id("e0ee5d0e-9d57-4c74-b938-0aa306a2313e")
                .extraTime(true)
                .build()
        );

        // When
        final ResponseStatusException rse = assertThrows(ResponseStatusException.class, () -> roundService.updateRounds(TOURNAMENT_ID, updates));

        // Then
        assertEquals(HttpStatus.NOT_FOUND, rse.getStatusCode());
        assertEquals("No tournaments found with a matching id.", rse.getReason());
    }

    @Test
    void shouldErrorIfTournamentHasNoKnockoutTemplateWhileUpdatingRounds() {
        // Given
        final QueryResponse<DatabaseRecord> existsResponse = mock(QueryResponse.class);
        when(existsResponse.getRecordCount())
            .thenReturn(1);
        when(existsResponse.getRecords())
            .thenReturn(List.of(
                ImmutableDatabaseRecord.builder()
                    .id(TOURNAMENT_ID)
                    .build()
            ));

        when(queryService.retrieveRecords(any()))
            .thenReturn(existsResponse);

        final List<RoundUpdate> updates = List.of(
            ImmutableRoundUpdate.builder()
                .id("96074478-23c4-4b6f-a8a4-1abe9fac2659")
                .name("Round 1")
                .build(),
            ImmutableRoundUpdate.builder()
                .id("e0ee5d0e-9d57-4c74-b938-0aa306a2313e")
                .extraTime(true)
                .build()
        );

        // When
        final ResponseStatusException rse = assertThrows(ResponseStatusException.class, () -> roundService.updateRounds(TOURNAMENT_ID, updates));

        // Then
        assertEquals(HttpStatus.NOT_FOUND, rse.getStatusCode());
        assertEquals("The tournament with the supplied id does not have a knockout stage.", rse.getReason());
    }

    @Test
    void shouldReturnRoundById() {
        // Given
        final QueryResponse<DatabaseRecord> tournamentExistsResponse = buildTournamentExistsResponse();
        final QueryResponse<DatabaseRecord> roundsResponse = buildRoundsResponse(List.of(ROUND_ONE));

        when(queryService.retrieveRecords(any()))
            .thenReturn(tournamentExistsResponse, roundsResponse);

        // When
        final Round round = roundService.getRoundById(TOURNAMENT_ID, ROUND_ONE.getId());

        // Then
        final ArgumentCaptor<QueryRequest<DatabaseRecord>> requestCaptor = ArgumentCaptor.forClass(QueryRequest.class);
        verify(queryService, times(2)).retrieveRecords(requestCaptor.capture());
        final List<QueryRequest<DatabaseRecord>> requests = requestCaptor.getAllValues();

        assertTournamentExistsRequest(requests.get(0));

        final QueryConditionGroup expectedConditionGroup = QueryConditionGroup.of(
            ImmutableQueryCondition.builder()
                .column(Column.of("id"))
                .operator(ConditionOperator.EQUAL)
                .value("96074478-23c4-4b6f-a8a4-1abe9fac2659")
                .build()
        );
        assertRetrieveRoundsRequest(requests.get(1), expectedConditionGroup);

        assertRound(ROUND_ONE, round);
    }

    @Test
    void shouldErrorIfTournamentDoesNotExistWhileRetrievingRound() {
        // Given
        final QueryResponse<DatabaseRecord> existsResponse = mock(QueryResponse.class);
        when(existsResponse.getRecordCount())
            .thenReturn(0);

        when(queryService.retrieveRecords(any()))
            .thenReturn(existsResponse);

        // When
        final ResponseStatusException rse = assertThrows(ResponseStatusException.class, () -> roundService.getRoundById(TOURNAMENT_ID, ROUND_ONE.getId()));

        // Then
        assertEquals(HttpStatus.NOT_FOUND, rse.getStatusCode());
        assertEquals("No tournaments found with a matching id.", rse.getReason());
    }

    @Test
    void shouldErrorIfTournamentHasNoKnockoutTemplateWhileRetrievingRound() {
        // Given
        final QueryResponse<DatabaseRecord> existsResponse = mock(QueryResponse.class);
        when(existsResponse.getRecordCount())
            .thenReturn(1);
        when(existsResponse.getRecords())
            .thenReturn(List.of(
                ImmutableDatabaseRecord.builder()
                    .id(TOURNAMENT_ID)
                    .build()
            ));

        when(queryService.retrieveRecords(any()))
            .thenReturn(existsResponse);

        // When
        final ResponseStatusException rse = assertThrows(ResponseStatusException.class, () -> roundService.getRoundById(TOURNAMENT_ID, ROUND_ONE.getId()));

        // Then
        assertEquals(HttpStatus.NOT_FOUND, rse.getStatusCode());
        assertEquals("The tournament with the supplied id does not have a knockout stage.", rse.getReason());
    }

    @Test
    void shouldErrorIfRoundNotFound() {
        // Given
        final QueryResponse<DatabaseRecord> tournamentExistsResponse = buildTournamentExistsResponse();
        final QueryResponse<DatabaseRecord> roundsResponse = buildRoundsResponse(List.of());

        when(queryService.retrieveRecords(any()))
            .thenReturn(tournamentExistsResponse, roundsResponse);

        // When
        final ResponseStatusException rse = assertThrows(ResponseStatusException.class, () -> roundService.getRoundById(TOURNAMENT_ID, ROUND_ONE.getId()));

        // Then
        assertEquals(HttpStatus.NOT_FOUND, rse.getStatusCode());
        assertEquals("No rounds found with a matching id.", rse.getReason());
    }

    private static QueryResponse<DatabaseRecord> buildTournamentExistsResponse() {
        final QueryResponse<DatabaseRecord> existsResponse = mock(QueryResponse.class);
        when(existsResponse.getRecordCount())
            .thenReturn(1);
        when(existsResponse.getRecords())
            .thenReturn(List.of(
                ImmutableDatabaseRecord.builder()
                    .id(TOURNAMENT_ID)
                    .putData("knockoutTemplateId", "72119bfa-212b-443c-b992-7dc6983c6a1a")
                    .build()
            ));

        return existsResponse;
    }

    private static QueryResponse<DatabaseRecord> buildRoundsResponse(List<DatabaseRecord> rounds) {
        final QueryResponse<DatabaseRecord> roundsResponse = mock(QueryResponse.class);
        when(roundsResponse.getRecordCount())
            .thenReturn(rounds.size());
        when(roundsResponse.getRecords())
            .thenReturn(rounds);

        return roundsResponse;
    }

    private static void assertTournamentExistsRequest(QueryRequest<DatabaseRecord> request) {
        assertEquals(2, request.getColumns().size());
        assertEquals(Column.of("to", "id"), request.getColumns().get(0));
        assertEquals(Column.of("tt", "knockoutTemplateId"), request.getColumns().get(1));

        assertTable("predictor", "tournaments", "to", request.getTable());

        assertEquals(1, request.getJoins().size());
        assertTableJoin(
            Table.of("predictor", "tournament-templates", "tt"),
            JoinType.INNER,
            QueryCondition.of(
                Column.of("to", "templateId"),
                Column.of("tt", "id")
            ),
            (TableJoin) request.getJoins().get(0)
        );

        assertEquals(1, request.getConditionGroup().getConditions().size());
        assertCondition(
            QueryCondition.of(
                Column.of("to", "id"),
                TOURNAMENT_ID
            ),
            request.getConditionGroup().getConditions().get(0)
        );

        assertEquals(DatabaseRecord.class, request.getRecordClass());
    }

    private static void assertRetrieveRoundsRequest(QueryRequest<DatabaseRecord> request, @Nullable QueryConditionGroup expectedConditionGroup) {
        assertTable("predictor", "rounds_dc51daad-bf1a-43ea-a109-2b53d30de357", request.getTable());

        if (expectedConditionGroup != null) {
            assertConditionGroup(expectedConditionGroup, request.getConditionGroup());
        }

        assertEquals(Round.class, request.getRecordClass());
    }

    private static void assertRound(Round expected, Round actual) {
        assertEquals(expected.getId(), actual.getId());
        assertEquals(expected.getName(), actual.getName());
        assertEquals(expected.getTeamCount(), actual.getTeamCount());
        assertEquals(expected.getRoundOrder(), actual.getRoundOrder());
        assertEquals(expected.getTwoLegs(), actual.getTwoLegs());
        assertEquals(expected.getExtraTime(), actual.getExtraTime());
        assertEquals(expected.getAwayGoals(), actual.getAwayGoals());
    }

    private static void assertRoundUpdate(RoundUpdate expected, RoundUpdate actual) {
        assertEquals(expected.getId(), actual.getId());
        assertEquals(expected.getName(), actual.getName());
        assertEquals(expected.isTwoLegs(), actual.isTwoLegs());
        assertEquals(expected.getExtraTime(), actual.getExtraTime());
        assertEquals(expected.getAwayGoals(), actual.getAwayGoals());
    }

    private static void assertTable(String expectedSchema, String expectedTable, Table actual) {
        assertTable(expectedSchema, expectedTable, null, actual);
    }

    private static void assertTable(String expectedSchema, String expectedTable, @Nullable String expectedAlias, Table actual) {
        assertEquals(expectedSchema, actual.getSchema());
        assertEquals(expectedTable, actual.getTable());
        assertEquals(expectedAlias, actual.getAlias());
    }

    private static void assertTable(Table expected, Table actual) {
        assertTable(expected.getSchema(), expected.getTable(), expected.getAlias(), actual);
    }

    private static void assertTableJoin(Table expectedTable, JoinType expectedJoinType, QueryCondition expectedCondition, TableJoin actual) {
        assertTable(expectedTable, actual.getTable());
        assertEquals(expectedJoinType, actual.getJoinType());
        assertCondition(expectedCondition, actual.getJoinCondition());
    }

    private static void assertCondition(QueryCondition expected, QueryCondition actual) {
        assertEquals(expected.getColumn(), actual.getColumn());
        assertEquals(expected.getOperator(), actual.getOperator());
        assertEquals(expected.getValue(), actual.getValue());
    }

    private static void assertConditionGroup(QueryConditionGroup expected, QueryConditionGroup actual) {
        assertEquals(expected.getJoin(), actual.getJoin());
        
        for (int i = 0; i < actual.getConditions().size(); i++) {
            assertCondition(expected.getConditions().get(i), actual.getConditions().get(i));
        }
    }
}
