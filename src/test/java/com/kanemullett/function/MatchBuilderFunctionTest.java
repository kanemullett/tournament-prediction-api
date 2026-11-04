package com.kanemullett.function;

import static org.junit.Assert.assertNull;
import static org.junit.jupiter.api.Assertions.assertEquals;

import java.sql.Timestamp;
import java.time.LocalDateTime;
import java.util.stream.Stream;

import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.Arguments;
import org.junit.jupiter.params.provider.MethodSource;

import com.kanemullett.model.DatabaseRecord;
import com.kanemullett.model.Group;
import com.kanemullett.model.ImmutableDatabaseRecord;
import com.kanemullett.model.ImmutableGroup;
import com.kanemullett.model.ImmutableMatch;
import com.kanemullett.model.ImmutableRound;
import com.kanemullett.model.ImmutableTeam;
import com.kanemullett.model.Match;
import com.kanemullett.model.Round;
import com.kanemullett.model.Team;
import com.kanemullett.model.type.Confederation;

public class MatchBuilderFunctionTest {

    private final MatchBuilderFunction matchBuilderFunction = new MatchBuilderFunction();

    private static final DatabaseRecord BIH_NGA_RECORD = ImmutableDatabaseRecord.builder()
        .putData("matchId", "8efaf853-980e-4607-9b45-d854460ec5e0")
        .putData("homeId", "bbec1707-7ea3-49cb-9791-7a1358a2b894")
        .putData("homeName", "Bosnia & Herzegovina")
        .putData("homeImagePath", "BIH.png")
        .putData("homeConfederation", "UEFA")
        .putData("awayId", "463de8d9-8520-4fa4-b30c-5aac0f3b363c")
        .putData("awayName", "Nigeria")
        .putData("awayImagePath", "NGA.png")
        .putData("awayConfederation", "CAF")
        .putData("kickoff", Timestamp.valueOf(LocalDateTime.of(2025, 6, 1, 14, 0, 0)))
        .putData("groupMatchDay", 1)
        .putData("groupId", "4c2c8046-0007-48db-a76a-865f9048d9de")
        .putData("homeGoals", 2)
        .putData("awayGoals", 1)
        .putData("afterExtraTime", false)
        .putData("afterPenalties", false)
        .putData("groupName", "Group A")
        .build();
    private static final DatabaseRecord ARG_IRI_RECORD = ImmutableDatabaseRecord.builder()
        .putData("matchId", "d8b3685b-3749-438d-9d85-da29c97ebaef")
        .putData("homeId", "977f3f69-0149-43fd-adb0-7c524aea37aa")
        .putData("homeName", "Argentina")
        .putData("homeImagePath", "ARG.png")
        .putData("homeConfederation", "CONMEBOL")
        .putData("awayId", "58adea3b-bdda-496a-be74-64501e34622b")
        .putData("awayName", "Iran")
        .putData("awayImagePath", "IRI.png")
        .putData("awayConfederation", "AFC")
        .putData("kickoff", Timestamp.valueOf(LocalDateTime.of(2025, 6, 1, 17, 30, 0)))
        .putData("roundId", "322ab9d0-ae46-49ac-89b3-c789a0d9d889")
        .putData("homeGoals", 2)
        .putData("awayGoals", 1)
        .putData("afterExtraTime", false)
        .putData("afterPenalties", false)
        .putData("roundName", "Round of 16")
        .putData("teamCount", 16)
        .putData("roundOrder", 1)
        .putData("twoLegs", false)
        .putData("extraTime", true)
        .putData("awayGoalsDecider", false)
        .build();

    private static final Match BIH_NGA_MATCH = ImmutableMatch.builder()
        .id("8efaf853-980e-4607-9b45-d854460ec5e0")
        .kickoff(LocalDateTime.of(2025, 6, 1, 14, 0, 0))
        .groupMatchDay(1)
        .homeTeam(ImmutableTeam.builder()
            .id("bbec1707-7ea3-49cb-9791-7a1358a2b894")
            .name("Bosnia & Herzegovina")
            .imagePath("BIH.png")
            .confederation(Confederation.UEFA)
            .build())
        .awayTeam(ImmutableTeam.builder()
            .id("463de8d9-8520-4fa4-b30c-5aac0f3b363c")
            .name("Nigeria")
            .imagePath("NGA.png")
            .confederation(Confederation.CAF)
            .build())
        .group(ImmutableGroup.builder()
            .id("4c2c8046-0007-48db-a76a-865f9048d9de")
            .name("Group A")
            .build())
        .build();
    private static final Match ARG_IRI_MATCH = ImmutableMatch.builder()
        .id("d8b3685b-3749-438d-9d85-da29c97ebaef")
        .kickoff(LocalDateTime.of(2025, 6, 1, 17, 30, 0))
        .homeTeam(ImmutableTeam.builder()
            .id("977f3f69-0149-43fd-adb0-7c524aea37aa")
            .name("Argentina")
            .imagePath("ARG.png")
            .confederation(Confederation.CONMEBOL)
            .build())
        .awayTeam(ImmutableTeam.builder()
            .id("58adea3b-bdda-496a-be74-64501e34622b")
            .name("Iran")
            .imagePath("IRI.png")
            .confederation(Confederation.AFC)
            .build())
        .round(ImmutableRound.builder()
            .id("322ab9d0-ae46-49ac-89b3-c789a0d9d889")
            .name("Round of 16")
            .teamCount(16)
            .roundOrder(1)
            .twoLegs(false)
            .extraTime(true)
            .awayGoals(false)
            .build())
        .build();

    private static Stream<Arguments> recordsAndMatches() {
        return Stream.of(
            Arguments.of(BIH_NGA_RECORD, BIH_NGA_MATCH),
            Arguments.of(ARG_IRI_RECORD, ARG_IRI_MATCH)
        );
    }

    @ParameterizedTest
    @MethodSource("recordsAndMatches")
    void shouldBuildMatchFromRecord(DatabaseRecord dbRecord, Match match) {
        // When
        final Match built = matchBuilderFunction.apply(dbRecord);

        // Then
        assertMatch(match, built);
    }

    private static void assertMatch(Match expected, Match actual) {
        assertEquals(expected.getId(), actual.getId());
        assertEquals(expected.getKickoff(), actual.getKickoff());
        assertEquals(expected.getGroupMatchDay(), actual.getGroupMatchDay());
        assertTeam(expected.getHomeTeam(), actual.getHomeTeam());
        assertTeam(expected.getAwayTeam(), actual.getAwayTeam());

        if (actual.getGroup() != null) {
            assertGroup(expected.getGroup(), actual.getGroup());
        } else {
            assertNull(expected.getGroup());
        }

        if (actual.getRound() != null) {
            assertRound(expected.getRound(), actual.getRound());
        } else {
            assertNull(expected.getRound());
        }
    }

    private static void assertTeam(Team expected, Team actual) {
        assertEquals(expected.getId(), actual.getId());
        assertEquals(expected.getName(), actual.getName());
        assertEquals(expected.getImagePath(), actual.getImagePath());
        assertEquals(expected.getConfederation(), actual.getConfederation());
    }

    private static void assertGroup(Group expected, Group actual) {
        assertEquals(expected.getId(), actual.getId());
        assertEquals(expected.getName(), actual.getName());
    }

    private static void assertRound(Round expected, Round actual) {
        assertEquals(expected.getId(), actual.getId());
        assertEquals(expected.getName(), actual.getName());
        assertEquals(expected.getTeamCount(), actual.getTeamCount());
        assertEquals(expected.getRoundOrder(), actual.getRoundOrder());
        assertEquals(expected.getTwoLegs(), actual.getTwoLegs());
        assertEquals(expected.getExtraTime(), actual.getExtraTime());
        assertEquals(expected.getAwayGoals(), actual.getAwayGoals());
    }
}
