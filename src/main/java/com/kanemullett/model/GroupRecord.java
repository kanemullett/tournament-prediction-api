package com.kanemullett.model;

import java.util.List;

import org.immutables.value.Value.Immutable;

import com.fasterxml.jackson.databind.annotation.JsonDeserialize;
import com.fasterxml.jackson.databind.annotation.JsonSerialize;
import com.kanemullett.model.type.SqlDataType;
import com.kanemullett.util.DatabaseConstants;
import com.kanemullett.util.PredictorConstants;

@Immutable
@JsonSerialize(as = ImmutableGroupRecord.class)
@JsonDeserialize(as = ImmutableGroupRecord.class)
public interface GroupRecord extends DatabaseRecord {

    static String getTargetTable(String tournamentId) {
        return "groups_" + tournamentId;
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
                ColumnDefinition.of(NAME_COLUMN, SqlDataType.VARCHAR)
            ))
            .build();
    }

    static String NAME_COLUMN = "name";

    String getName();
}
