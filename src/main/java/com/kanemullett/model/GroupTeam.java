package com.kanemullett.model;

import org.immutables.value.Value.Immutable;

import com.fasterxml.jackson.databind.annotation.JsonDeserialize;
import com.fasterxml.jackson.databind.annotation.JsonSerialize;

@Immutable
@JsonSerialize(as = ImmutableGroupTeam.class)
@JsonDeserialize(as = ImmutableGroupTeam.class)
public interface GroupTeam extends DatabaseRecord {

    static String getTargetTable(String tournamentId) {
        return "group-teams_" + tournamentId;
    }

    static String GROUP_ID_COLUMN = "groupId";
    static String TEAM_ID_COLUMN = "teamId";

    String getGroupId();

    String getTeamId();
}
