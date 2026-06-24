package com.kanemullett.model;

import java.time.LocalDateTime;

import org.immutables.value.Value.Immutable;

import com.fasterxml.jackson.databind.annotation.JsonDeserialize;
import com.fasterxml.jackson.databind.annotation.JsonSerialize;

import jakarta.annotation.Nullable;

@Immutable
@JsonSerialize(as = ImmutableMatchRecord.class)
@JsonDeserialize(as = ImmutableMatchRecord.class)
public interface MatchRecord extends DatabaseRecord {

    static String getTargetTable(String tournamentId) {
        return "matches_" + tournamentId;
    }

    static String HOME_TEAM_ID_COLUMN = "homeTeamId";
    static String AWAY_TEAM_ID_COLUMN = "awayTeamId";

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
