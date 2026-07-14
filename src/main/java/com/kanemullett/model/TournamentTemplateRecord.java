package com.kanemullett.model;

import org.immutables.value.Value.Immutable;

import com.fasterxml.jackson.databind.annotation.JsonDeserialize;
import com.fasterxml.jackson.databind.annotation.JsonSerialize;

import jakarta.annotation.Nullable;

@Immutable
@JsonSerialize(as = ImmutableTournamentTemplateRecord.class)
@JsonDeserialize(as = ImmutableTournamentTemplateRecord.class)
public interface TournamentTemplateRecord extends DatabaseRecord {

    static String TARGET_TABLE = "tournament-templates";

    static String NAME_COLUMN = "name";
    static String LEAGUE_TEMPLATE_ID_COLUMN = "leagueTemplateId";
    static String KNOCKOUT_TEMPLATE_ID_COLUMN = "knockoutTemplateId";

    String getName();

    @Nullable
    String getLeagueTemplateId();

    @Nullable
    String getKnockoutTemplateId();
}
