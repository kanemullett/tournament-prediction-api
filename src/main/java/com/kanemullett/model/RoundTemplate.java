package com.kanemullett.model;

import org.immutables.value.Value.Immutable;

import com.fasterxml.jackson.databind.annotation.JsonDeserialize;
import com.fasterxml.jackson.databind.annotation.JsonSerialize;

@Immutable
@JsonSerialize(as=ImmutableRoundTemplate.class)
@JsonDeserialize(as=ImmutableRoundTemplate.class)
public interface RoundTemplate {

    String getName();

    int getTeamCount();

    int getRoundOrder();

    boolean getTwoLegs();

    boolean getExtraTime();

    boolean getAwayGoals();
}
