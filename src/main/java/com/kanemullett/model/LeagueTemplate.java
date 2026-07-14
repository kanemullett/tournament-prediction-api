package com.kanemullett.model;

import org.immutables.value.Value.Immutable;

import com.fasterxml.jackson.databind.annotation.JsonDeserialize;
import com.fasterxml.jackson.databind.annotation.JsonSerialize;

@Immutable
@JsonSerialize(as = ImmutableLeagueTemplate.class)
@JsonDeserialize(as = ImmutableLeagueTemplate.class)
public interface LeagueTemplate extends DatabaseRecord {

    static String TARGET_TABLE = "league-templates";

    static String NAME_COLUMN = "name";
    static String GROUP_COUNT_COLUMN = "groupCount";
    static String TEAMS_PER_GROUP_COLUMN = "teamsPerGroup";
    static String HOME_AND_AWAY_COLUMN = "homeAndAway";

    String getName();

    int getGroupCount();

    int getTeamsPerGroup();

    boolean getHomeAndAway();
}
