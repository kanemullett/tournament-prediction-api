package com.kanemullett.model;

import org.immutables.value.Value.Immutable;

import com.fasterxml.jackson.databind.annotation.JsonDeserialize;
import com.fasterxml.jackson.databind.annotation.JsonSerialize;

import jakarta.annotation.Nullable;

@Immutable
@JsonSerialize(as=ImmutableCompetitionUpdate.class)
@JsonDeserialize(as=ImmutableCompetitionUpdate.class)
public interface CompetitionUpdate extends DatabaseRecord {

    @Nullable
    String getName();

    @Nullable
    String getTournamentId();
}