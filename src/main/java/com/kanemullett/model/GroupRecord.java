package com.kanemullett.model;

import org.immutables.value.Value.Immutable;

import com.fasterxml.jackson.databind.annotation.JsonDeserialize;
import com.fasterxml.jackson.databind.annotation.JsonSerialize;

@Immutable
@JsonSerialize(as = ImmutableGroupRecord.class)
@JsonDeserialize(as = ImmutableGroupRecord.class)
public interface GroupRecord extends DatabaseRecord {

    static String getTargetTable(String tournamentId) {
        return "groups_" + tournamentId;
    }

    String getName();
}
