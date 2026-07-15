package com.kanemullett.model;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertFalse;
import static org.junit.Assert.assertNotNull;
import static org.junit.Assert.assertTrue;

import org.junit.jupiter.api.Test;

import com.kanemullett.model.type.SqlDataType;

public class RoundTest extends AbstractRecordTest {

    @Test
    void shouldReturnRoundTargetTable() {
        // When
        final String targetTable = Round.getTargetTable("tournamentId");

        // Then
        assertEquals("rounds_tournamentId", targetTable);
    }

    @Test
    void shouldReturnRoundTableDefinition() {
        // When
        final TableDefinition tableDefinition = Round.getTableDefinition("tournamentId");

        // Then
        assertEquals("predictor", tableDefinition.getSchema());
        assertEquals("rounds_tournamentId", tableDefinition.getTable());
        assertEquals(7, tableDefinition.getColumns().size());

        assertColumnDefinition("id", SqlDataType.VARCHAR, true, tableDefinition.getColumns().get(0));
        assertColumnDefinition("name", SqlDataType.VARCHAR, false, tableDefinition.getColumns().get(1));
        assertColumnDefinition("teamCount", SqlDataType.INTEGER, false, tableDefinition.getColumns().get(2));
        assertColumnDefinition("roundOrder", SqlDataType.INTEGER, false, tableDefinition.getColumns().get(3));
        assertColumnDefinition("twoLegs", SqlDataType.BOOLEAN, false, tableDefinition.getColumns().get(4));
        assertColumnDefinition("extraTime", SqlDataType.BOOLEAN, false, tableDefinition.getColumns().get(5));
        assertColumnDefinition("awayGoals", SqlDataType.BOOLEAN, false, tableDefinition.getColumns().get(6));
    }

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
