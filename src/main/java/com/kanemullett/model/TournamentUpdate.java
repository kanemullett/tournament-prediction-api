package com.kanemullett.model;

import org.immutables.value.Value.Immutable;

import com.fasterxml.jackson.databind.annotation.JsonDeserialize;
import com.fasterxml.jackson.databind.annotation.JsonSerialize;
import com.kanemullett.model.type.Confederation;

import jakarta.annotation.Nullable;

@Immutable
@JsonSerialize(as = ImmutableTournamentUpdate.class)
@JsonDeserialize(as = ImmutableTournamentUpdate.class)
public interface TournamentUpdate extends DatabaseRecord {

    @Nullable
    String getName();

    @Nullable
    Integer getYear();

    @Nullable
    Confederation getConfederation();

    @Nullable
    String getTemplateId();
}
