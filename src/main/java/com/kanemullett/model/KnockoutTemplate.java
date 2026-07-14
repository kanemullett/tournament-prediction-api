package com.kanemullett.model;

import java.util.List;

import org.immutables.value.Value.Immutable;

import com.fasterxml.jackson.databind.annotation.JsonDeserialize;
import com.fasterxml.jackson.databind.annotation.JsonSerialize;

import jakarta.annotation.Nullable;

@Immutable
@JsonSerialize(as=ImmutableKnockoutTemplate.class)
@JsonDeserialize(as=ImmutableKnockoutTemplate.class)
public interface KnockoutTemplate extends DatabaseRecord {

    static String TARGET_TABLE = "knockout-templates";

    static String NAME_COLUMN = "name";
    static String ROUNDS_COLUMN = "rounds";

    String getName();

    @Nullable
    List<RoundTemplate> getRounds();
}
