package com.kanemullett.model;

import static org.junit.jupiter.api.Assertions.assertEquals;

import org.junit.jupiter.api.Test;

import com.kanemullett.model.type.SqlDataType;

public class ResultTest extends AbstractRecordTest {

    @Test
    void shouldReturnResultTargetTable() {
        // When
        final String targetTable = Result.getTargetTable("tournamentId");

        // Then
        assertEquals("results_tournamentId", targetTable);
    }

    @Test
    void shouldReturnResultTableDefinition() {
        // When
        final TableDefinition tableDefinition = Result.getTableDefinition("tournamentId");

        // Then
        assertEquals("predictor", tableDefinition.getSchema());
        assertEquals("results_tournamentId", tableDefinition.getTable());
        assertEquals(6, tableDefinition.getColumns().size());

        assertColumnDefinition("id", SqlDataType.VARCHAR, true, tableDefinition.getColumns().get(0));
        assertColumnDefinition("homeGoals", SqlDataType.INTEGER, false, tableDefinition.getColumns().get(1));
        assertColumnDefinition("awayGoals", SqlDataType.INTEGER, false, tableDefinition.getColumns().get(2));
        assertColumnDefinition("afterExtraTime", SqlDataType.BOOLEAN, false, tableDefinition.getColumns().get(3));
        assertColumnDefinition("afterPenalties", SqlDataType.BOOLEAN, false, tableDefinition.getColumns().get(4));
        assertColumnDefinition("penaltiesWinner", SqlDataType.VARCHAR, false, tableDefinition.getColumns().get(5));
    }
}
