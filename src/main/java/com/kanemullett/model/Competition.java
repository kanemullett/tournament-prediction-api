package com.kanemullett.model;

import org.immutables.value.Value.Immutable;

import com.fasterxml.jackson.databind.annotation.JsonDeserialize;
import com.fasterxml.jackson.databind.annotation.JsonSerialize;

import jakarta.annotation.Nullable;

@Immutable
@JsonSerialize(as=ImmutableCompetition.class)
@JsonDeserialize(as=ImmutableCompetition.class)
public interface Competition extends DatabaseRecord {

    static String TARGET_TABLE = "competitions";

    String getName();

    @Nullable
    String getTournamentId();
}
