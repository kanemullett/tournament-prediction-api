package com.kanemullett.model;

import org.immutables.value.Value.Immutable;

import com.fasterxml.jackson.databind.annotation.JsonDeserialize;
import com.fasterxml.jackson.databind.annotation.JsonSerialize;

@Immutable
@JsonSerialize(as=ImmutableCompetitionUser.class)
@JsonDeserialize(as=ImmutableCompetitionUser.class)
public interface CompetitionUser extends DatabaseRecord {

    static String TARGET_TABLE = "competition-users";

    static String COMPETITION_ID_COLUMN = "competitionId";
    static String USERNAME_COLUMN = "username";

    String getCompetitionId();

    String getUsername();
}
