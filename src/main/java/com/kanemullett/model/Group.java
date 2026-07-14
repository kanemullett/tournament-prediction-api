package com.kanemullett.model;

import java.util.List;

import org.immutables.value.Value.Default;
import org.immutables.value.Value.Immutable;

import com.fasterxml.jackson.databind.annotation.JsonDeserialize;
import com.fasterxml.jackson.databind.annotation.JsonSerialize;

@Immutable
@JsonSerialize(as = ImmutableGroup.class)
@JsonDeserialize(as = ImmutableGroup.class)
public interface Group {

    String getId();

    String getName();

    @Default
    default List<Team> getTeams() {
        return List.of();
    }
}
