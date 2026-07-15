package com.kanemullett.model;

import static org.junit.jupiter.api.Assertions.assertEquals;

import org.junit.jupiter.api.Test;

import com.kanemullett.model.type.SqlDataType;

public class GroupTeamTest extends AbstractRecordTest {

    @Test
    void shouldReturnGroupTeamTargetTable() {
        // When
        final String targetTable = GroupTeam.getTargetTable("tournamentId");

        // Then
        assertEquals("group-teams_tournamentId", targetTable);
    }

    @Test
    void shouldReturnGroupTeamTableDefinition() {
        // When
        final TableDefinition tableDefinition = GroupTeam.getTableDefinition("tournamentId");

        // Then
        assertEquals("predictor", tableDefinition.getSchema());
        assertEquals("group-teams_tournamentId", tableDefinition.getTable());
        assertEquals(3, tableDefinition.getColumns().size());

        assertColumnDefinition("id", SqlDataType.VARCHAR, true, tableDefinition.getColumns().get(0));
        assertColumnDefinition("groupId", SqlDataType.VARCHAR, false, tableDefinition.getColumns().get(1));
        assertColumnDefinition("teamId", SqlDataType.VARCHAR, false, tableDefinition.getColumns().get(2));
    }
}
