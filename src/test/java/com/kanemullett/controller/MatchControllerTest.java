package com.kanemullett.controller;

import static org.junit.Assert.assertNull;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.mockito.ArgumentMatchers.anyList;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.when;

import java.time.LocalDateTime;
import java.util.List;

import org.junit.jupiter.api.Test;
import org.springframework.http.HttpStatus;
import org.springframework.web.server.ResponseStatusException;

import com.kanemullett.model.Group;
import com.kanemullett.model.ImmutableGroup;
import com.kanemullett.model.ImmutableMatch;
import com.kanemullett.model.ImmutableMatchUpdate;
import com.kanemullett.model.ImmutableRound;
import com.kanemullett.model.ImmutableTeam;
import com.kanemullett.model.Match;
import com.kanemullett.model.MatchUpdate;
import com.kanemullett.model.Round;
import com.kanemullett.model.Team;
import com.kanemullett.model.type.Confederation;
import com.kanemullett.service.MatchService;

public class MatchControllerTest {

    private final MatchService service = mock(MatchService.class);

    private final MatchController controller = new MatchController(service);

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

    @Test
    void shouldPassMatchesAsResponse() {
        // Given
        when(service.getMatches(anyString(), eq(null), eq(null), eq(null)))
            .thenReturn(List.of(BIH_NGA_MATCH, ARG_IRI_MATCH));

        // When
        final List<Match> matches = controller.getMatches("5341cff8-df9f-4068-8a42-4b4288ecba87", null, null, null);

        // Then
        assertEquals(2, matches.size());
        assertMatch(BIH_NGA_MATCH, matches.get(0));
        assertMatch(ARG_IRI_MATCH, matches.get(1));
    }

    @Test
    void shouldPassErrorForGetMatches() {
        // Given
        when(service.getMatches(anyString(), eq(null), eq(null), eq(null)))
            .thenThrow(new ResponseStatusException(HttpStatus.NOT_FOUND, "Not found"));

        // When
        final ResponseStatusException rse = assertThrows(ResponseStatusException.class, () -> controller.getMatches("5341cff8-df9f-4068-8a42-4b4288ecba87", null, null, null));

        // Then
        assertEquals(HttpStatus.NOT_FOUND, rse.getStatusCode());
        assertEquals("Not found", rse.getReason());
    }

    @Test
    void shouldPassUpdatedMatchesAsResponse() {
        // Given
        final List<MatchUpdate> updates = List.of(
            ImmutableMatchUpdate.builder()
                .id("8efaf853-980e-4607-9b45-d854460ec5e0")
                .kickoff(LocalDateTime.of(2025, 6, 1, 14, 0, 0))
                .build(),
            ImmutableMatchUpdate.builder()
                .id("d8b3685b-3749-438d-9d85-da29c97ebaef")
                .kickoff(LocalDateTime.of(2025, 6, 1, 17, 30, 0))
                .build()
        );

        when(service.updateMatches(anyString(), anyList()))
            .thenReturn(List.of(BIH_NGA_MATCH, ARG_IRI_MATCH));

        // When
        final List<Match> matches = controller.updateMatches("5341cff8-df9f-4068-8a42-4b4288ecba87", updates);

        // Then
        assertEquals(2, matches.size());
        assertMatch(BIH_NGA_MATCH, matches.get(0));
        assertMatch(ARG_IRI_MATCH, matches.get(1));
    }

    @Test
    void shouldPassErrorForUpdateMatches() {
        // Given
        final List<MatchUpdate> updates = List.of(
            ImmutableMatchUpdate.builder()
                .id("8efaf853-980e-4607-9b45-d854460ec5e0")
                .kickoff(LocalDateTime.of(2025, 6, 1, 14, 0, 0))
                .build(),
            ImmutableMatchUpdate.builder()
                .id("d8b3685b-3749-438d-9d85-da29c97ebaef")
                .kickoff(LocalDateTime.of(2025, 6, 1, 17, 30, 0))
                .build()
        );

        when(service.updateMatches(anyString(), anyList()))
            .thenThrow(new ResponseStatusException(HttpStatus.NOT_FOUND, "Not found"));

        // When
        final ResponseStatusException rse = assertThrows(ResponseStatusException.class, () -> controller.updateMatches("5341cff8-df9f-4068-8a42-4b4288ecba87", updates));

        // Then
        assertEquals(HttpStatus.NOT_FOUND, rse.getStatusCode());
        assertEquals("Not found", rse.getReason());
    }

    @Test
    void shouldPassMatchAsResponse() {
        // Given
        when(service.getMatchById(anyString(), anyString()))
            .thenReturn(BIH_NGA_MATCH);

        // When
        final Match match = controller.getMatchById("5341cff8-df9f-4068-8a42-4b4288ecba87", "8efaf853-980e-4607-9b45-d854460ec5e0");

        // Then
        assertMatch(BIH_NGA_MATCH, match);
    }

    @Test
    void shouldPassErrorForGetMatchById() {
        // Given
        when(service.getMatchById(anyString(), anyString()))
            .thenThrow(new ResponseStatusException(HttpStatus.NOT_FOUND, "Not found"));

        // When
        final ResponseStatusException rse = assertThrows(ResponseStatusException.class, () -> controller.getMatchById("5341cff8-df9f-4068-8a42-4b4288ecba87", "8efaf853-980e-4607-9b45-d854460ec5e0"));

        // Then
        assertEquals(HttpStatus.NOT_FOUND, rse.getStatusCode());
        assertEquals("Not found", rse.getReason());
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
