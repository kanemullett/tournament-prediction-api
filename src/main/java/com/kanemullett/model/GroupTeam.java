package com.kanemullett.model;

import java.util.List;

import org.immutables.value.Value.Immutable;

import com.fasterxml.jackson.databind.annotation.JsonDeserialize;
import com.fasterxml.jackson.databind.annotation.JsonSerialize;
import com.kanemullett.model.type.SqlDataType;
import com.kanemullett.util.DatabaseConstants;
import com.kanemullett.util.PredictorConstants;

@Immutable
@JsonSerialize(as = ImmutableGroupTeam.class)
@JsonDeserialize(as = ImmutableGroupTeam.class)
public interface GroupTeam extends DatabaseRecord {

    static String getTargetTable(String tournamentId) {
        return "group-teams_" + tournamentId;
    }

    static TableDefinition getTableDefinition(String tournamentId) {
        return ImmutableTableDefinition.builder()
            .schema(PredictorConstants.PREDICTOR_SCHEMA)
            .table(getTargetTable(tournamentId))
            .columns(List.of(
                ImmutableColumnDefinition.builder()
                    .name(DatabaseConstants.ID)
                    .dataType(SqlDataType.VARCHAR)
                    .primaryKey(true)
                    .build(),
                ColumnDefinition.of(GROUP_ID_COLUMN, SqlDataType.VARCHAR),
                ColumnDefinition.of(TEAM_ID_COLUMN, SqlDataType.VARCHAR)
            ))
            .build();
    }

    static String GROUP_ID_COLUMN = "groupId";
    static String TEAM_ID_COLUMN = "teamId";

    String getGroupId();

    String getTeamId();
}
