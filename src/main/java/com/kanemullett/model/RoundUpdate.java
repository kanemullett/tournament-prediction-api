package com.kanemullett.model;

import org.immutables.value.Value.Immutable;

import com.fasterxml.jackson.databind.annotation.JsonDeserialize;
import com.fasterxml.jackson.databind.annotation.JsonSerialize;

import jakarta.annotation.Nullable;

@Immutable
@JsonSerialize(as = ImmutableRoundUpdate.class)
@JsonDeserialize(as = ImmutableRoundUpdate.class)
public interface RoundUpdate extends DatabaseRecord {

    @Nullable
    String getName();

    @Nullable
    Boolean isTwoLegs();

    @Nullable
    Boolean getExtraTime();

    @Nullable
    Boolean getAwayGoals();
}
