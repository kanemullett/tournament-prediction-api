package com.kanemullett.model;

import java.util.List;

import org.immutables.value.Value.Immutable;

import com.fasterxml.jackson.databind.annotation.JsonDeserialize;
import com.fasterxml.jackson.databind.annotation.JsonSerialize;
import com.kanemullett.model.type.SqlDataType;
import com.kanemullett.model.type.Winner;
import com.kanemullett.util.DatabaseConstants;
import com.kanemullett.util.PredictorConstants;

import jakarta.annotation.Nullable;

@Immutable
@JsonSerialize(as = ImmutableResult.class)
@JsonDeserialize(as = ImmutableResult.class)
public interface Result extends DatabaseRecord {

    static String getTargetTable(String tournamentId) {
        return "results_" + tournamentId;
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
                ColumnDefinition.of(HOME_GOALS_COLUMN, SqlDataType.INTEGER),
                ColumnDefinition.of(AWAY_GOALS_COLUMN, SqlDataType.INTEGER),
                ColumnDefinition.of(AFTER_EXTRA_TIME_COLUMN, SqlDataType.BOOLEAN),
                ColumnDefinition.of(AFTER_PENALTIES_COLUMN, SqlDataType.BOOLEAN),
                ColumnDefinition.of(PENALTIES_WINNER_COLUMN, SqlDataType.VARCHAR)
            ))
            .build();
    }

    static String HOME_GOALS_COLUMN = "homeGoals";
    static String AWAY_GOALS_COLUMN = "awayGoals";
    static String AFTER_EXTRA_TIME_COLUMN = "afterExtraTime";
    static String AFTER_PENALTIES_COLUMN = "afterPenalties";
    static String PENALTIES_WINNER_COLUMN = "penaltiesWinner";

    int getHomeGoals();

    int getAwayGoals();

    boolean getAfterExtraTime();

    boolean getAfterPenalties();

    @Nullable
    Winner getPenaltiesWinner();
}
