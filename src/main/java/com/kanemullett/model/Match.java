package com.kanemullett.model;

import java.time.LocalDateTime;

import org.immutables.value.Value.Immutable;

import com.fasterxml.jackson.databind.annotation.JsonDeserialize;
import com.fasterxml.jackson.databind.annotation.JsonSerialize;

import jakarta.annotation.Nullable;

@Immutable
@JsonSerialize(as = ImmutableMatch.class)
@JsonDeserialize(as = ImmutableMatch.class)
public interface Match extends DatabaseRecord {

    @Nullable
    LocalDateTime getKickoff();

    @Nullable
    Team getHomeTeam();

    @Nullable
    Team getAwayTeam();

    @Nullable
    Integer getGroupMatchDay();

    @Nullable
    Group getGroup();

    @Nullable
    Round getRound();

    @Nullable
    MatchOutcome getResult();
}
