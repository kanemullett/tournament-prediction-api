package com.kanemullett.controller;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.mockito.ArgumentMatchers.anyList;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.Mockito.doThrow;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

import java.util.List;

import org.junit.jupiter.api.Test;
import org.springframework.http.HttpStatus;
import org.springframework.web.server.ResponseStatusException;

import com.kanemullett.model.ImmutableResult;
import com.kanemullett.model.Result;
import com.kanemullett.model.type.Winner;
import com.kanemullett.service.ResultService;

public class ResultControllerTest {

    private final ResultService service = mock(ResultService.class);

    private final ResultController controller = new ResultController(service);

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
    void shouldPassCreatedResults() {
        // Given
        final List<Result> results = List.of(RESULT_ONE, RESULT_TWO);

        when(service.createResults(anyString(), anyList()))
            .thenReturn(List.of(RESULT_ONE, RESULT_TWO));

        // When
        final List<Result> created = controller.createResults("1c29f6c3-9f98-41a8-ba0f-e07013742797", results);

        // Then
        assertEquals(2, created.size());
        assertResult(RESULT_ONE, created.get(0));
        assertResult(RESULT_TWO, created.get(1));
    }

    @Test
    void shouldPassErrorWhenCreatingResults() {
        // Given
        final List<Result> results = List.of(RESULT_ONE, RESULT_TWO);

        when(service.createResults(anyString(), anyList()))
            .thenThrow(new ResponseStatusException(HttpStatus.NOT_FOUND, "Not found"));

        // When
        final ResponseStatusException rse = assertThrows(ResponseStatusException.class, () -> controller.createResults("1c29f6c3-9f98-41a8-ba0f-e07013742797", results));

        // Then
        assertEquals(HttpStatus.NOT_FOUND, rse.getStatusCode());
        assertEquals("Not found", rse.getReason());
    }

    @Test
    void shouldPassUpdatedResults() {
        // Given
        final List<Result> updates = List.of(RESULT_ONE, RESULT_TWO);

        when(service.updateResults(anyString(), anyList()))
            .thenReturn(List.of(RESULT_ONE, RESULT_TWO));

        // When
        final List<Result> updated = controller.updateResults("1c29f6c3-9f98-41a8-ba0f-e07013742797", updates);

        // Then
        assertEquals(2, updated.size());
        assertResult(RESULT_ONE, updated.get(0));
        assertResult(RESULT_TWO, updated.get(1));
    }

    @Test
    void shouldPassErrorWhenUpdatingResults() {
        // Given
        final List<Result> updates = List.of(RESULT_ONE, RESULT_TWO);

        when(service.updateResults(anyString(), anyList()))
            .thenThrow(new ResponseStatusException(HttpStatus.NOT_FOUND, "Not found"));

        // When
        final ResponseStatusException rse = assertThrows(ResponseStatusException.class, () -> controller.updateResults("1c29f6c3-9f98-41a8-ba0f-e07013742797", updates));

        // Then
        assertEquals(HttpStatus.NOT_FOUND, rse.getStatusCode());
        assertEquals("Not found", rse.getReason());
    }

    @Test
    void shouldDeleteResultById() {
        // When
        controller.deleteResultById("1c29f6c3-9f98-41a8-ba0f-e07013742797", "1db1fe5c-97d4-42e9-974f-633edb1dc0c4");

        // Then
        verify(service).deleteResultById("1c29f6c3-9f98-41a8-ba0f-e07013742797", "1db1fe5c-97d4-42e9-974f-633edb1dc0c4");
    }

    @Test
    void shouldPassErrorWhenDeletingResultById() {
        // Given
        doThrow(new ResponseStatusException(HttpStatus.NOT_FOUND, "Not found"))
            .when(service).deleteResultById(anyString(), anyString());

        // When
        final ResponseStatusException rse = assertThrows(ResponseStatusException.class, () -> controller.deleteResultById("1c29f6c3-9f98-41a8-ba0f-e07013742797", "1db1fe5c-97d4-42e9-974f-633edb1dc0c4"));

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
}
