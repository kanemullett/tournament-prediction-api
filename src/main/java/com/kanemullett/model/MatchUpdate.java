package com.kanemullett.model;

import java.time.LocalDateTime;

import org.immutables.value.Value.Immutable;

import com.fasterxml.jackson.databind.annotation.JsonDeserialize;
import com.fasterxml.jackson.databind.annotation.JsonSerialize;

import jakarta.annotation.Nullable;

@Immutable
@JsonSerialize(as = ImmutableMatchUpdate.class)
@JsonDeserialize(as = ImmutableMatchUpdate.class)
public interface MatchUpdate extends DatabaseRecord {

    @Nullable
    LocalDateTime getKickoff();

    @Nullable
    String getHomeTeamId();

    @Nullable
    String getAwayTeamId();
}
