package com.kanemullett.model;

import org.immutables.value.Value.Immutable;

import com.fasterxml.jackson.databind.annotation.JsonDeserialize;
import com.fasterxml.jackson.databind.annotation.JsonSerialize;
import com.kanemullett.model.type.Confederation;

import jakarta.annotation.Nullable;

@Immutable
@JsonSerialize(as=ImmutableTournament.class)
@JsonDeserialize(as=ImmutableTournament.class)
public interface Tournament extends DatabaseRecord {

    static String TARGET_TABLE = "tournaments";

    static String TEMPLATE_ID_COLUMN = "templateId";

    String getName();

    Integer getYear();

    @Nullable
    Confederation getConfederation();

    String getTemplateId();
}
