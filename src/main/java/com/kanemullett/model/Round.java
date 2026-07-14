package com.kanemullett.model;

import java.util.List;

import org.immutables.value.Value.Immutable;

import com.fasterxml.jackson.databind.annotation.JsonDeserialize;
import com.fasterxml.jackson.databind.annotation.JsonSerialize;
import com.kanemullett.model.type.SqlDataType;
import com.kanemullett.util.DatabaseConstants;
import com.kanemullett.util.PredictorConstants;

@Immutable
@JsonSerialize(as = ImmutableRound.class)
@JsonDeserialize(as = ImmutableRound.class)
public interface Round extends DatabaseRecord {

    static String getTargetTable(String tournamentId) {
        return "rounds_" + tournamentId;
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
                ColumnDefinition.of(NAME_COLUMN, SqlDataType.VARCHAR),
                ColumnDefinition.of(TEAM_COUNT_COLUMN, SqlDataType.INTEGER),
                ColumnDefinition.of(ROUND_ORDER_COLUMN, SqlDataType.INTEGER),
                ColumnDefinition.of(TWO_LEGS_COLUMN, SqlDataType.BOOLEAN),
                ColumnDefinition.of(EXTRA_TIME_COLUMN, SqlDataType.BOOLEAN),
                ColumnDefinition.of(AWAY_GOALS_COLUMN, SqlDataType.BOOLEAN)
            ))
            .build();
    }

    static String NAME_COLUMN = "name";
    static String TEAM_COUNT_COLUMN = "teamCount";
    static String ROUND_ORDER_COLUMN = "roundOrder";
    static String TWO_LEGS_COLUMN = "twoLegs";
    static String EXTRA_TIME_COLUMN = "extraTime";
    static String AWAY_GOALS_COLUMN = "awayGoals";

    String getName();

    int getTeamCount();

    int getRoundOrder();

    boolean getTwoLegs();

    boolean getExtraTime();

    boolean getAwayGoals();

    static Round of(RoundTemplate roundTemplate) {
        return ImmutableRound.builder()
            .name(roundTemplate.getName())
            .teamCount(roundTemplate.getTeamCount())
            .roundOrder(roundTemplate.getTeamCount())
            .twoLegs(roundTemplate.getTwoLegs())
            .extraTime(roundTemplate.getExtraTime())
            .awayGoals(roundTemplate.getAwayGoals())
            .build();
    }
}
