package com.kanemullett.model;

import org.immutables.value.Value.Default;
import org.immutables.value.Value.Immutable;

import com.fasterxml.jackson.databind.annotation.JsonDeserialize;
import com.fasterxml.jackson.databind.annotation.JsonSerialize;
import com.kanemullett.model.type.Winner;

import jakarta.annotation.Nullable;

@Immutable
@JsonSerialize(as = ImmutableMatchOutcome.class)
@JsonDeserialize(as = ImmutableMatchOutcome.class)
public interface MatchOutcome {

    int getHomeGoals();

    int getAwayGoals();

    @Default
    default Boolean isAfterExtraTime() {
        return false;
    }

    @Default
    default Boolean isAfterPenalties() {
        return false;
    }

    @Nullable
    Winner getWinner();
}
