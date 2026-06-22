package com.kanemullett.model;

import org.immutables.value.Value.Immutable;

import com.fasterxml.jackson.databind.annotation.JsonDeserialize;
import com.fasterxml.jackson.databind.annotation.JsonSerialize;
import com.kanemullett.model.type.Confederation;

import jakarta.annotation.Nullable;

@Immutable
@JsonSerialize(as=ImmutableTeam.class)
@JsonDeserialize(as=ImmutableTeam.class)
public interface Team extends DatabaseRecord {

    static String TARGET_TABLE = "teams";

    static String NAME_COLUMN = "name";
    static String IMAGE_PATH_COLUMN = "imagePath";
    static String CONFEDERATION_COLUMN = "confederation";

    String getName();

    String getImagePath();

    Confederation getConfederation();

    @Nullable
    Integer getRanking();
}
