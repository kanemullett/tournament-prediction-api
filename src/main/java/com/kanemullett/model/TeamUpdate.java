package com.kanemullett.model;

import org.immutables.value.Value.Immutable;

import com.fasterxml.jackson.databind.annotation.JsonDeserialize;
import com.fasterxml.jackson.databind.annotation.JsonSerialize;
import com.kanemullett.model.type.Confederation;

import jakarta.annotation.Nullable;

@Immutable
@JsonSerialize(as = ImmutableTeamUpdate.class)
@JsonDeserialize(as = ImmutableTeamUpdate.class)
public interface TeamUpdate extends DatabaseRecord {

    @Nullable
    String getName();

    @Nullable
    String getImagePath();

    @Nullable
    Confederation getConfederation();

    @Nullable
    Integer getRanking();
}
