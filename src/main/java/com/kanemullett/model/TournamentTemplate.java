package com.kanemullett.model;

import org.immutables.value.Value.Immutable;

import com.fasterxml.jackson.databind.annotation.JsonDeserialize;
import com.fasterxml.jackson.databind.annotation.JsonSerialize;

import jakarta.annotation.Nullable;

@Immutable
@JsonSerialize(as=ImmutableTournamentTemplate.class)
@JsonDeserialize(as=ImmutableTournamentTemplate.class)
public interface TournamentTemplate {

    String getId();

    String getName();

    @Nullable
    LeagueTemplate getLeague();
    
    @Nullable
    KnockoutTemplate getKnockout();
}
