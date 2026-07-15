package com.kanemullett.model;

import static org.junit.jupiter.api.Assertions.assertEquals;

import org.junit.jupiter.api.Test;

import com.kanemullett.model.type.SqlDataType;

public class MatchRecordTest extends AbstractRecordTest {

    @Test
    void shouldReturnMatchTargetTable() {
        // When
        final String targetTable = MatchRecord.getTargetTable("tournamentId");

        // Then
        assertEquals("matches_tournamentId", targetTable);
    }

    @Test
    void shouldReturnMatchTableDefinition() {
        // When
        final TableDefinition tableDefinition = MatchRecord.getTableDefinition("tournamentId");

        // Then
        assertEquals("predictor", tableDefinition.getSchema());
        assertEquals("matches_tournamentId", tableDefinition.getTable());
        assertEquals(7, tableDefinition.getColumns().size());

        assertColumnDefinition("id", SqlDataType.VARCHAR, true, tableDefinition.getColumns().get(0));
        assertColumnDefinition("homeTeamId", SqlDataType.VARCHAR, false, tableDefinition.getColumns().get(1));
        assertColumnDefinition("awayTeamId", SqlDataType.VARCHAR, false, tableDefinition.getColumns().get(2));
        assertColumnDefinition("kickoff", SqlDataType.TIMESTAMP_WITHOUT_TIME_ZONE, false, tableDefinition.getColumns().get(3));
        assertColumnDefinition("groupMatchDay", SqlDataType.INTEGER, false, tableDefinition.getColumns().get(4));
        assertColumnDefinition("groupId", SqlDataType.VARCHAR, false, tableDefinition.getColumns().get(5));
        assertColumnDefinition("roundId", SqlDataType.VARCHAR, false, tableDefinition.getColumns().get(6));
    }
}
