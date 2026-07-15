package com.kanemullett.model;

import java.time.LocalDateTime;
import java.util.List;

import org.immutables.value.Value.Immutable;

import com.fasterxml.jackson.databind.annotation.JsonDeserialize;
import com.fasterxml.jackson.databind.annotation.JsonSerialize;
import com.kanemullett.model.type.SqlDataType;
import com.kanemullett.util.DatabaseConstants;
import com.kanemullett.util.PredictorConstants;

import jakarta.annotation.Nullable;

@Immutable
@JsonSerialize(as = ImmutableMatchRecord.class)
@JsonDeserialize(as = ImmutableMatchRecord.class)
public interface MatchRecord extends DatabaseRecord {

    static String getTargetTable(String tournamentId) {
        return "matches_" + tournamentId;
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
                ColumnDefinition.of(HOME_TEAM_ID_COLUMN, SqlDataType.VARCHAR),
                ColumnDefinition.of(AWAY_TEAM_ID_COLUMN, SqlDataType.VARCHAR),
                ColumnDefinition.of(KICKOFF_COLUMN, SqlDataType.TIMESTAMP_WITHOUT_TIME_ZONE),
                ColumnDefinition.of(GROUP_MATCH_DAY_COLUMN, SqlDataType.INTEGER),
                ColumnDefinition.of(GROUP_ID_COLUMN, SqlDataType.VARCHAR),
                ColumnDefinition.of(ROUND_ID_COLUMN, SqlDataType.VARCHAR)
            ))
            .build();
    } 

    static String HOME_TEAM_ID_COLUMN = "homeTeamId";
    static String AWAY_TEAM_ID_COLUMN = "awayTeamId";
    static String KICKOFF_COLUMN = "kickoff";
    static String GROUP_MATCH_DAY_COLUMN = "groupMatchDay";
    static String GROUP_ID_COLUMN = "groupId";
    static String ROUND_ID_COLUMN = "roundId";

    @Nullable
    String getHomeTeamId();

    @Nullable
    String getAwayTeamId();

    @Nullable
    LocalDateTime getKickoff();

    @Nullable
    Integer getGroupMatchDay();

    @Nullable
    String getGroupId();

    @Nullable
    String getRoundId();
}
