package com.kanemullett.controller;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.mockito.ArgumentMatchers.anyList;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.Mockito.doThrow;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.when;

import java.util.List;

import org.junit.jupiter.api.Test;
import org.springframework.http.HttpStatus;
import org.springframework.web.server.ResponseStatusException;

import com.kanemullett.model.ImmutableKnockoutTemplate;
import com.kanemullett.model.ImmutableLeagueTemplate;
import com.kanemullett.model.ImmutableRoundTemplate;
import com.kanemullett.model.ImmutableTournamentTemplate;
import com.kanemullett.model.ImmutableTournamentTemplateRecord;
import com.kanemullett.model.KnockoutTemplate;
import com.kanemullett.model.LeagueTemplate;
import com.kanemullett.model.RoundTemplate;
import com.kanemullett.model.TournamentTemplate;
import com.kanemullett.model.TournamentTemplateRecord;
import com.kanemullett.service.TournamentTemplateService;

public class TournamentTemplateControllerTest {

    private final TournamentTemplateService service = mock(TournamentTemplateService.class);

    private final TournamentTemplateController controller = new TournamentTemplateController(service);

    private static final LeagueTemplate LEAGUE_TEMPLATE_ONE = ImmutableLeagueTemplate.builder()
        .id("0ca3adf1-f5a5-43e9-9c82-5619340739be")
        .name("league1")
        .groupCount(8)
        .teamsPerGroup(4)
        .homeAndAway(true)
        .build();
    private static final LeagueTemplate LEAGUE_TEMPLATE_TWO = ImmutableLeagueTemplate.builder()
        .id("508c8b55-2e0c-415b-8078-2dcb2065c7ca")
        .name("league2")
        .groupCount(6)
        .teamsPerGroup(4)
        .homeAndAway(false)
        .build();
    private static final RoundTemplate ROUND_TEMPLATE_ONE = ImmutableRoundTemplate.builder()
        .name("round1")
        .teamCount(4)
        .roundOrder(1)
        .twoLegs(true)
        .extraTime(true)
        .awayGoals(true)
        .build();
    private static final RoundTemplate ROUND_TEMPLATE_TWO = ImmutableRoundTemplate.builder()
        .name("round2")
        .teamCount(2)
        .roundOrder(2)
        .twoLegs(false)
        .extraTime(true)
        .awayGoals(false)
        .build();
    private static final RoundTemplate ROUND_TEMPLATE_THREE = ImmutableRoundTemplate.builder()
        .name("round3")
        .teamCount(4)
        .roundOrder(1)
        .twoLegs(true)
        .extraTime(true)
        .awayGoals(true)
        .build();
    private static final RoundTemplate ROUND_TEMPLATE_FOUR = ImmutableRoundTemplate.builder()
        .name("round4")
        .teamCount(2)
        .roundOrder(2)
        .twoLegs(false)
        .extraTime(true)
        .awayGoals(false)
        .build();
    private static final KnockoutTemplate KNOCKOUT_TEMPLATE_ONE = ImmutableKnockoutTemplate.builder()
        .id("80e9c164-637d-400f-a3cf-bf922073bc9b")
        .name("knockout1")
        .rounds(List.of(ROUND_TEMPLATE_ONE, ROUND_TEMPLATE_TWO))
        .build();
    private static final KnockoutTemplate KNOCKOUT_TEMPLATE_TWO = ImmutableKnockoutTemplate.builder()
        .id("1a4d1cc8-f035-439a-b274-fe739b8fcfa5")
        .name("knockout2")
        .rounds(List.of(ROUND_TEMPLATE_THREE, ROUND_TEMPLATE_FOUR))
        .build();
    private static final TournamentTemplate TOURNAMENT_TEMPLATE_ONE = ImmutableTournamentTemplate.builder()
        .id("c08fd796-7fea-40d9-9a0a-cb3a49cce2e4")
        .name("tournament1")
        .knockout(KNOCKOUT_TEMPLATE_ONE)
        .build();
    private static final TournamentTemplate TOURNAMENT_TEMPLATE_TWO = ImmutableTournamentTemplate.builder()
        .id("6ee28143-1286-4618-a8b9-ad86d348ead1")
        .name("tournament2")
        .league(LEAGUE_TEMPLATE_ONE)
        .build();
    private static final TournamentTemplate TOURNAMENT_TEMPLATE_THREE = ImmutableTournamentTemplate.builder()
        .id("d15956ef-d199-40b1-b7d7-850a9add97e7")
        .name("tournament3")
        .league(LEAGUE_TEMPLATE_TWO)
        .knockout(KNOCKOUT_TEMPLATE_TWO)
        .build();

    @Test
    void shouldPassTournamentTemplatesAsResponse() {
        // Given
        when(service.getTournamentTemplates())
            .thenReturn(List.of(TOURNAMENT_TEMPLATE_ONE, TOURNAMENT_TEMPLATE_TWO, TOURNAMENT_TEMPLATE_THREE));

        // When
        final List<TournamentTemplate> tournamentTemplates = controller.getTournamentTemplates();

        // Then
        assertEquals(3, tournamentTemplates.size());

        assertTournamentTemplate(TOURNAMENT_TEMPLATE_ONE, tournamentTemplates.get(0));
        assertTournamentTemplate(TOURNAMENT_TEMPLATE_TWO, tournamentTemplates.get(1));
        assertTournamentTemplate(TOURNAMENT_TEMPLATE_THREE, tournamentTemplates.get(2));
    }

    @Test
    void shouldPassCreatedTournamentTemplatesAsResponse() {
        // Given
        final List<TournamentTemplateRecord> tournamentTemplates = List.of(
            ImmutableTournamentTemplateRecord.builder()
                .name("tournament1")
                .knockoutTemplateId("80e9c164-637d-400f-a3cf-bf922073bc9b")
                .build(),
            ImmutableTournamentTemplateRecord.builder()
                .name("tournament2")
                .leagueTemplateId("0ca3adf1-f5a5-43e9-9c82-5619340739be")
                .build(),
            ImmutableTournamentTemplateRecord.builder()
                .name("tournament3")
                .leagueTemplateId("508c8b55-2e0c-415b-8078-2dcb2065c7ca")
                .knockoutTemplateId("1a4d1cc8-f035-439a-b274-fe739b8fcfa5")
                .build()
        );

        when(service.createTournamentTemplates(anyList()))
            .thenReturn(List.of(TOURNAMENT_TEMPLATE_ONE, TOURNAMENT_TEMPLATE_TWO, TOURNAMENT_TEMPLATE_THREE));

        // When
        final List<TournamentTemplate> created = controller.createTournamentTemplates(tournamentTemplates);

        // Then
        assertEquals(3, created.size());

        assertTournamentTemplate(TOURNAMENT_TEMPLATE_ONE, created.get(0));
        assertTournamentTemplate(TOURNAMENT_TEMPLATE_TWO, created.get(1));
        assertTournamentTemplate(TOURNAMENT_TEMPLATE_THREE, created.get(2));
    }

    @Test
    void shouldPassFoundTournamentTemplateAsResponse() {
        // Given
        when(service.getTournamentTemplateById(anyString()))
            .thenReturn(TOURNAMENT_TEMPLATE_THREE);

        // When
        final TournamentTemplate tournamentTemplate = controller.getTournamentTemplateById("d15956ef-d199-40b1-b7d7-850a9add97e7");

        // Then
        assertTournamentTemplate(TOURNAMENT_TEMPLATE_THREE, tournamentTemplate);
    }

    @Test
    void shouldPassErrorIfTournamentTemplateNotFound() {
        // Given
        when(service.getTournamentTemplateById(anyString()))
            .thenThrow(new ResponseStatusException(HttpStatus.NOT_FOUND, "No tournament templates found with a matching id."));

        // When
        final ResponseStatusException rse = assertThrows(ResponseStatusException.class, () -> controller.getTournamentTemplateById("c08fd796-7fea-40d9-9a0a-cb3a49cce2e4"));

        // Then
        assertEquals(HttpStatus.NOT_FOUND, rse.getStatusCode());
        assertEquals("No tournament templates found with a matching id.", rse.getReason());
    }

    @Test
    void shouldPassErrorIfTournamentTemplateIsBeingUsed() {
        // Given
        doThrow(new ResponseStatusException(HttpStatus.CONFLICT, "Cannot delete tournament template as it is part of an existing tournament."))
            .when(service)
                .deleteTournamentTemplateById(anyString());

        // When
        final ResponseStatusException rse = assertThrows(ResponseStatusException.class, () -> controller.deleteTournamentTemplateById("c08fd796-7fea-40d9-9a0a-cb3a49cce2e4"));

        // Then
        assertEquals(HttpStatus.CONFLICT, rse.getStatusCode());
        assertEquals("Cannot delete tournament template as it is part of an existing tournament.", rse.getReason());
    }

    private static void assertTournamentTemplate(TournamentTemplate expected, TournamentTemplate actual) {
        assertEquals(expected.getId(), actual.getId());
        assertEquals(expected.getName(), actual.getName());

        if (expected.getLeague() != null) {
            assertLeagueTemplate(expected.getLeague(), actual.getLeague());
        }

        if (expected.getKnockout() != null) {
            assertKnockoutTemplate(expected.getKnockout(), actual.getKnockout());
        }
    }

    private static void assertLeagueTemplate(LeagueTemplate expected, LeagueTemplate actual) {
        assertEquals(expected.getId(), actual.getId());
        assertEquals(expected.getName(), actual.getName());
        assertEquals(expected.getGroupCount(), actual.getGroupCount());
        assertEquals(expected.getTeamsPerGroup(), actual.getTeamsPerGroup());
        assertEquals(expected.getHomeAndAway(), actual.getHomeAndAway());
    }

    private static void assertKnockoutTemplate(KnockoutTemplate expected, KnockoutTemplate actual) {
        assertEquals(expected.getId(), actual.getId());
        assertEquals(expected.getName(), actual.getName());

        for (int i = 0; i < expected.getRounds().size(); i++) {
            assertRoundTemplate(expected.getRounds().get(i), actual.getRounds().get(i));
        }
    }

    private static void assertRoundTemplate(RoundTemplate expected, RoundTemplate actual) {
        assertEquals(expected.getName(), actual.getName());
        assertEquals(expected.getTeamCount(), actual.getTeamCount());
        assertEquals(expected.getRoundOrder(), actual.getRoundOrder());
        assertEquals(expected.getTwoLegs(), actual.getTwoLegs());
        assertEquals(expected.getExtraTime(), actual.getExtraTime());
        assertEquals(expected.getAwayGoals(), actual.getAwayGoals());
    }
}
