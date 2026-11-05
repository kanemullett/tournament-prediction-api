package com.kanemullett.service;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

import java.util.List;

import org.junit.jupiter.api.Test;
import org.mockito.ArgumentCaptor;
import org.springframework.http.HttpStatus;
import org.springframework.web.server.ResponseStatusException;

import com.kanemullett.model.Column;
import com.kanemullett.model.DatabaseRecord;
import com.kanemullett.model.ImmutableQueryCondition;
import com.kanemullett.model.ImmutableResult;
import com.kanemullett.model.MatchRecord;
import com.kanemullett.model.QueryCondition;
import com.kanemullett.model.QueryConditionGroup;
import com.kanemullett.model.QueryRequest;
import com.kanemullett.model.QueryResponse;
import com.kanemullett.model.Result;
import com.kanemullett.model.Table;
import com.kanemullett.model.UpdateRequest;
import com.kanemullett.model.type.ConditionOperator;
import com.kanemullett.model.type.SqlOperator;
import com.kanemullett.model.type.Winner;

public class ResultServiceTest {

    private final DatabaseQueryService queryService = mock(DatabaseQueryService.class);
    private final TournamentService tournamentService = mock(TournamentService.class);

    private final ResultService resultService = new ResultService(queryService, tournamentService);

    private static final Result RESULT_ONE = ImmutableResult.builder()
        .id("1db1fe5c-97d4-42e9-974f-633edb1dc0c4")
        .homeGoals(2)
        .awayGoals(1)
        .afterExtraTime(true)
        .afterPenalties(false)
        .build();
    private static final Result RESULT_TWO = ImmutableResult.builder()
        .id("a1212f49-534f-4d36-90f4-f3ec9f0d9735")
        .homeGoals(3)
        .awayGoals(3)
        .afterExtraTime(true)
        .afterPenalties(true)
        .penaltiesWinner(Winner.AWAY)
        .build();

    @Test
    void shouldCreateResults() {
        // Given
        final List<Result> results = List.of(RESULT_ONE, RESULT_TWO);

        final QueryResponse<DatabaseRecord> matchResponse = mock(QueryResponse.class);
        when(matchResponse.getRecordCount())
            .thenReturn(2);

        when(queryService.retrieveRecords(any()))
            .thenReturn(matchResponse);

        // When
        final List<Result> created = resultService.createResults("5341cff8-df9f-4068-8a42-4b4288ecba87", results);

        // Then
        verify(tournamentService).getTournamentById("5341cff8-df9f-4068-8a42-4b4288ecba87");

        final ArgumentCaptor<QueryRequest<MatchRecord>> requestCaptor = ArgumentCaptor.forClass(QueryRequest.class);
        verify(queryService).retrieveRecords(requestCaptor.capture());
        final QueryRequest<MatchRecord> queryRequest = requestCaptor.getValue();

        assertTable("predictor", "matches_5341cff8-df9f-4068-8a42-4b4288ecba87", queryRequest.getTable());

        assertConditionGroup(
            QueryConditionGroup.of(
                ImmutableQueryCondition.builder()
                    .column(Column.of("id"))
                    .operator(ConditionOperator.IN)
                    .value(List.of("1db1fe5c-97d4-42e9-974f-633edb1dc0c4", "a1212f49-534f-4d36-90f4-f3ec9f0d9735"))
                    .build()
            ), 
            queryRequest.getConditionGroup()
        );

        final ArgumentCaptor<UpdateRequest<Result>> updateCaptor = ArgumentCaptor.forClass(UpdateRequest.class);
        verify(queryService).updateRecords(updateCaptor.capture());
        final UpdateRequest<Result> updateRequest = updateCaptor.getValue();

        assertEquals(SqlOperator.INSERT, updateRequest.getOperation());
        assertTable("predictor", "results_5341cff8-df9f-4068-8a42-4b4288ecba87", updateRequest.getTable());
        
        assertEquals(2, updateRequest.getRecords().size());
        assertResult(RESULT_ONE, updateRequest.getRecords().get(0));
        assertResult(RESULT_TWO, updateRequest.getRecords().get(1));

        assertEquals(2, created.size());
        assertResult(RESULT_ONE, created.get(0));
        assertResult(RESULT_TWO, created.get(1));
    }

    @Test
    void shouldErrorIfTournamentDoesNotExistWhenCreatingResults() {
        // Given
        final List<Result> results = List.of(RESULT_ONE, RESULT_TWO);

        when(tournamentService.getTournamentById(anyString()))
            .thenThrow(new ResponseStatusException(HttpStatus.NOT_FOUND, "Not found"));

        // When
        final ResponseStatusException rse = assertThrows(ResponseStatusException.class, () -> resultService.createResults("5341cff8-df9f-4068-8a42-4b4288ecba87", results));

        // Then
        assertEquals(HttpStatus.NOT_FOUND, rse.getStatusCode());
        assertEquals("Not found", rse.getReason());
    }

    @Test
    void shouldErrorIfMatchDoesNotExistWhenCreatingResults() {
        // Given
        final List<Result> results = List.of(RESULT_ONE, RESULT_TWO);

        final QueryResponse<DatabaseRecord> matchResponse = mock(QueryResponse.class);
        when(matchResponse.getRecordCount())
            .thenReturn(1);

        when(queryService.retrieveRecords(any()))
            .thenReturn(matchResponse);

        // When
        final ResponseStatusException rse = assertThrows(ResponseStatusException.class, () -> resultService.createResults("5341cff8-df9f-4068-8a42-4b4288ecba87", results));

        // Then
        assertEquals(HttpStatus.BAD_REQUEST, rse.getStatusCode());
        assertEquals("One or more results do not have a corresponding match record.", rse.getReason());
    }

    @Test
    void shouldUpdateResults() {
        // Given
        final List<Result> updates = List.of(RESULT_ONE, RESULT_TWO);

        final QueryResponse<DatabaseRecord> resultResponse = mock(QueryResponse.class);
        when(resultResponse.getRecords())
            .thenReturn(List.of(RESULT_ONE, RESULT_TWO));

        when(queryService.retrieveRecords(any()))
            .thenReturn(resultResponse);

        // When
        final List<Result> updated = resultService.updateResults("5341cff8-df9f-4068-8a42-4b4288ecba87", updates);

        // Then
        verify(tournamentService).getTournamentById("5341cff8-df9f-4068-8a42-4b4288ecba87");

        final ArgumentCaptor<UpdateRequest<Result>> updateCaptor = ArgumentCaptor.forClass(UpdateRequest.class);
        verify(queryService).updateRecords(updateCaptor.capture());
        final UpdateRequest<Result> updateRequest = updateCaptor.getValue();

        assertEquals(SqlOperator.UPDATE, updateRequest.getOperation());
        assertTable("predictor", "results_5341cff8-df9f-4068-8a42-4b4288ecba87", updateRequest.getTable());
        
        assertEquals(2, updateRequest.getRecords().size());
        assertResult(RESULT_ONE, updateRequest.getRecords().get(0));
        assertResult(RESULT_TWO, updateRequest.getRecords().get(1));

        final ArgumentCaptor<QueryRequest<Result>> requestCaptor = ArgumentCaptor.forClass(QueryRequest.class);
        verify(queryService).retrieveRecords(requestCaptor.capture());
        final QueryRequest<Result> queryRequest = requestCaptor.getValue();

        assertTable("predictor", "results_5341cff8-df9f-4068-8a42-4b4288ecba87", queryRequest.getTable());

        assertConditionGroup(
            QueryConditionGroup.of(
                ImmutableQueryCondition.builder()
                    .column(Column.of("id"))
                    .operator(ConditionOperator.IN)
                    .value(List.of("1db1fe5c-97d4-42e9-974f-633edb1dc0c4", "a1212f49-534f-4d36-90f4-f3ec9f0d9735"))
                    .build()
            ), 
            queryRequest.getConditionGroup()
        );

        assertEquals(2, updated.size());
        assertResult(RESULT_ONE, updated.get(0));
        assertResult(RESULT_TWO, updated.get(1));
    }

    @Test
    void shouldErrorIfTournamentDoesNotExistWhenUpdatingResults() {
        // Given
        final List<Result> updates = List.of(RESULT_ONE, RESULT_TWO);

        when(tournamentService.getTournamentById(anyString()))
            .thenThrow(new ResponseStatusException(HttpStatus.NOT_FOUND, "Not found"));

        // When
        final ResponseStatusException rse = assertThrows(ResponseStatusException.class, () -> resultService.updateResults("5341cff8-df9f-4068-8a42-4b4288ecba87", updates));

        // Then
        assertEquals(HttpStatus.NOT_FOUND, rse.getStatusCode());
        assertEquals("Not found", rse.getReason());
    }

    @Test
    void shouldDeleteResultById() {
        // When
        resultService.deleteResultById("5341cff8-df9f-4068-8a42-4b4288ecba87", "1db1fe5c-97d4-42e9-974f-633edb1dc0c4");

        // Then
        verify(tournamentService).getTournamentById("5341cff8-df9f-4068-8a42-4b4288ecba87");

        final ArgumentCaptor<UpdateRequest<Result>> updateCaptor = ArgumentCaptor.forClass(UpdateRequest.class);
        verify(queryService).updateRecords(updateCaptor.capture());
        final UpdateRequest<Result> updateRequest = updateCaptor.getValue();

        assertEquals(SqlOperator.DELETE, updateRequest.getOperation());
        assertTable("predictor", "results_5341cff8-df9f-4068-8a42-4b4288ecba87", updateRequest.getTable());
        assertConditionGroup(
            QueryConditionGroup.of(
                QueryCondition.of(
                    Column.of("id"),
                    "1db1fe5c-97d4-42e9-974f-633edb1dc0c4"
                )
            ),
            updateRequest.getConditionGroup()
        );
    }

    @Test
    void shouldErrorIfTournamentDoesNotExistWhenDeletingResult() {
        // Given
        when(tournamentService.getTournamentById(anyString()))
            .thenThrow(new ResponseStatusException(HttpStatus.NOT_FOUND, "Not found"));

        // When
        final ResponseStatusException rse = assertThrows(ResponseStatusException.class, () -> resultService.deleteResultById("5341cff8-df9f-4068-8a42-4b4288ecba87", "1db1fe5c-97d4-42e9-974f-633edb1dc0c4"));

        // Then
        assertEquals(HttpStatus.NOT_FOUND, rse.getStatusCode());
        assertEquals("Not found", rse.getReason());
    }

    private static void assertResult(Result expected, Result actual) {
        assertEquals(expected.getId(), actual.getId());
        assertEquals(expected.getHomeGoals(), actual.getHomeGoals());
        assertEquals(expected.getAwayGoals(), actual.getAwayGoals());
        assertEquals(expected.getAfterExtraTime(), actual.getAfterExtraTime());
        assertEquals(expected.getAfterPenalties(), actual.getAfterPenalties());
        assertEquals(expected.getPenaltiesWinner(), actual.getPenaltiesWinner());
    }

    private static void assertColumn(Column expected, Column actual) {
        assertEquals(expected.getParts(), actual.getParts());
        assertEquals(expected.getAlias(), actual.getAlias());
    }

    private static void assertTable(String expectedSchema, String expectedTable, Table actual) {
        assertEquals(expectedSchema, actual.getSchema());
        assertEquals(expectedTable, actual.getTable());
    }

    private static void assertCondition(QueryCondition expected, QueryCondition actual) {
        assertColumn(expected.getColumn(), actual.getColumn());
        assertEquals(expected.getOperator(), actual.getOperator());
        assertEquals(expected.getValue(), actual.getValue());
    }

    private static void assertConditionGroup(QueryConditionGroup expected, QueryConditionGroup actual) {
        assertEquals(expected.getJoin(), actual.getJoin());

        for (int i = 0; i < expected.getConditions().size(); i++) {
            assertCondition(expected.getConditions().get(i), actual.getConditions().get(i));
        }
    }
}
