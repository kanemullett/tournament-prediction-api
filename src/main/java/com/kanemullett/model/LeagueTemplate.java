package com.kanemullett.model;

import org.immutables.value.Value.Immutable;

import com.fasterxml.jackson.databind.annotation.JsonDeserialize;
import com.fasterxml.jackson.databind.annotation.JsonSerialize;

@Immutable
@JsonSerialize(as = ImmutableLeagueTemplate.class)
@JsonDeserialize(as = ImmutableLeagueTemplate.class)
public interface LeagueTemplate extends DatabaseRecord {

    static String TARGET_TABLE = "league-templates";

    String getName();

    int getGroupCount();

    int getTeamsPerGroup();

    boolean getHomeAndAway();
}
