package com.kanemullett.model;

import static org.junit.Assert.assertEquals;

import org.junit.jupiter.api.Test;

import com.kanemullett.model.type.SqlDataType;

public class GroupRecordTest extends AbstractRecordTest {

    @Test
    void shouldReturnGroupTargetTable() {
        // When
        final String targetTable = GroupRecord.getTargetTable("tournamentId");

        // Then
        assertEquals("groups_tournamentId", targetTable);
    }

    @Test
    void shouldReturnGroupTableDefinition() {
        // When
        final TableDefinition tableDefinition = GroupRecord.getTableDefinition("tournamentId");

        // Then
        assertEquals("predictor", tableDefinition.getSchema());
        assertEquals("groups_tournamentId", tableDefinition.getTable());
        assertEquals(2, tableDefinition.getColumns().size());

        assertColumnDefinition("id", SqlDataType.VARCHAR, true, tableDefinition.getColumns().get(0));
        assertColumnDefinition("name", SqlDataType.VARCHAR, false, tableDefinition.getColumns().get(1));
    }
}
