package com.kanemullett.controller;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.mockito.ArgumentMatchers.anyList;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.when;

import java.util.List;

import org.junit.jupiter.api.Test;
import org.springframework.http.HttpStatus;
import org.springframework.web.server.ResponseStatusException;

import com.kanemullett.model.ImmutableRound;
import com.kanemullett.model.ImmutableRoundUpdate;
import com.kanemullett.model.Round;
import com.kanemullett.model.RoundUpdate;
import com.kanemullett.service.RoundService;

public class RoundControllerTest {

    private final RoundService service = mock(RoundService.class);

    private final RoundController controller = new RoundController(service);

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
    void shouldPassRoundsAsResponse() {
        // Given
        when(service.getRounds(anyString()))
            .thenReturn(List.of(ROUND_ONE, ROUND_TWO));

        // When
        final List<Round> rounds = controller.getRounds(TOURNAMENT_ID);

        // Then
        assertRound(ROUND_ONE, rounds.get(0));
        assertRound(ROUND_TWO, rounds.get(1));
    }

    @Test
    void shouldPassErrorInGetRounds() {
        // Given
        when(service.getRounds(anyString()))
            .thenThrow(new ResponseStatusException(HttpStatus.NOT_FOUND, "Not found"));

        // When
        final ResponseStatusException rse = assertThrows(ResponseStatusException.class, () -> controller.getRounds(TOURNAMENT_ID));

        // Then
        assertEquals(HttpStatus.NOT_FOUND, rse.getStatusCode());
        assertEquals("Not found", rse.getReason());
    }

    @Test
    void shouldPassUpdatedRoundsAsResponse() {
        // Given
        when(service.updateRounds(anyString(), anyList()))
            .thenReturn(List.of(ROUND_ONE, ROUND_TWO));

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
        final List<Round> updated = controller.updateRounds(TOURNAMENT_ID, updates);

        // Then
        assertRound(ROUND_ONE, updated.get(0));
        assertRound(ROUND_TWO, updated.get(1));
    }

    @Test
    void shouldPassErrorInUpdateRounds() {
        // Given
        when(service.updateRounds(anyString(), anyList()))
            .thenThrow(new ResponseStatusException(HttpStatus.NOT_FOUND, "Not found"));

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
        final ResponseStatusException rse = assertThrows(ResponseStatusException.class, () -> controller.updateRounds(TOURNAMENT_ID, updates));

        // Then
        assertEquals(HttpStatus.NOT_FOUND, rse.getStatusCode());
        assertEquals("Not found", rse.getReason());
    }

    @Test
    void shouldPassRoundAsResponse() {
        // Given
        when(service.getRoundById(anyString(), anyString()))
            .thenReturn(ROUND_ONE);

        // When
        final Round round = controller.getRoundById(TOURNAMENT_ID, ROUND_ONE.getId());

        // Then
        assertRound(ROUND_ONE, round);
    }

    @Test
    void shouldPassErrorInGetRound() {
        // Given
        when(service.getRoundById(anyString(), anyString()))
            .thenThrow(new ResponseStatusException(HttpStatus.NOT_FOUND, "Not found"));

        // When
        final ResponseStatusException rse = assertThrows(ResponseStatusException.class, () -> controller.getRoundById(TOURNAMENT_ID, ROUND_ONE.getId()));

        // Then
        assertEquals(HttpStatus.NOT_FOUND, rse.getStatusCode());
        assertEquals("Not found", rse.getReason());
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
}
