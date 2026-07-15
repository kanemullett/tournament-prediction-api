package com.kanemullett.model;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertFalse;
import static org.junit.Assert.assertNotNull;
import static org.junit.Assert.assertTrue;

import org.junit.jupiter.api.Test;

public class RoundTest {

    @Test
    void shouldReturnRoundFromRoundTemplate() {
        // Given
        final RoundTemplate roundTemplate = ImmutableRoundTemplate.builder()
            .name("Final")
            .teamCount(2)
            .roundOrder(1)
            .twoLegs(false)
            .extraTime(true)
            .awayGoals(false)
            .build();

        // When
        final Round round = Round.of(roundTemplate);

        // Then
        assertNotNull(round.getId());
        assertEquals("Final", round.getName());
        assertEquals(2, round.getTeamCount());
        assertEquals(1, round.getRoundOrder());
        assertFalse(round.getTwoLegs());
        assertTrue(round.getExtraTime());
        assertFalse(round.getAwayGoals());
    }
}
