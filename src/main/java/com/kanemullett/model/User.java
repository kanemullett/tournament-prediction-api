package com.kanemullett.model;

import org.immutables.value.Value.Immutable;

import com.fasterxml.jackson.databind.annotation.JsonDeserialize;
import com.fasterxml.jackson.databind.annotation.JsonSerialize;

@Immutable
@JsonSerialize(as=ImmutableUser.class)
@JsonDeserialize(as=ImmutableUser.class)
public interface User extends DatabaseRecord {

    static String TARGET_TABLE = "users";

    String getDisplayName();
}
