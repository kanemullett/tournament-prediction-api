package com.kanemullett.controller;

import static org.junit.Assert.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.mockito.ArgumentMatchers.anyList;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.when;

import java.util.List;

import org.junit.jupiter.api.Test;
import org.springframework.http.HttpStatus;
import org.springframework.web.server.ResponseStatusException;

import com.kanemullett.model.ImmutableLeagueTemplate;
import com.kanemullett.model.LeagueTemplate;
import com.kanemullett.service.LeagueTemplateService;

public class LeagueTemplateControllerTest {

    private final LeagueTemplateService service = mock(LeagueTemplateService.class);

    private final LeagueTemplateController controller = new LeagueTemplateController(service);

    private static final LeagueTemplate EIGHT_BY_FOUR = ImmutableLeagueTemplate.builder()
        .id("c08fd796-7fea-40d9-9a0a-cb3a49cce2e4")
        .name("8x4 Group-Stage Single-Game")
        .groupCount(8)
        .teamsPerGroup(4)
        .homeAndAway(false)
        .build();
    private static final LeagueTemplate SIX_BY_FOUR = ImmutableLeagueTemplate.builder()
        .id("6ee28143-1286-4618-a8b9-ad86d348ead1")
        .name("6x4 Group-Stage Single-Game")
        .groupCount(6)
        .teamsPerGroup(4)
        .homeAndAway(false)
        .build();

    @Test
    void shouldPassLeagueTemplatesAsResponse() {
        // Given
        when(service.getLeagueTemplates())
            .thenReturn(List.of(EIGHT_BY_FOUR, SIX_BY_FOUR));

        // When
        final List<LeagueTemplate> leagueTemplates = controller.getLeagueTemplates();

        // Then
        assertEquals(2, leagueTemplates.size());

        assertLeagueTemplate(EIGHT_BY_FOUR, leagueTemplates.get(0));
        assertLeagueTemplate(SIX_BY_FOUR, leagueTemplates.get(1));
    }

    @Test
    void shouldPassCreatedLeagueTemplatesAsResponse() {
        // Given
        final List<LeagueTemplate> leagueTemplates = List.of(EIGHT_BY_FOUR, SIX_BY_FOUR);

        when(service.createLeagueTemplates(anyList()))
            .thenReturn(List.of(EIGHT_BY_FOUR, SIX_BY_FOUR));

        // When
        final List<LeagueTemplate> created = controller.createLeagueTemplates(leagueTemplates);

        // Then
        assertEquals(2, created.size());

        assertLeagueTemplate(EIGHT_BY_FOUR, created.get(0));
        assertLeagueTemplate(SIX_BY_FOUR, created.get(1));
    }

    @Test
    void shouldPassFoundLeagueTemplateAsResponse() {
        // Given
        when(service.getLeagueTemplateById(anyString()))
            .thenReturn(EIGHT_BY_FOUR);

        // When
        final LeagueTemplate leagueTemplate = controller.getLeagueTemplateById("c08fd796-7fea-40d9-9a0a-cb3a49cce2e4");

        // Then
        assertLeagueTemplate(EIGHT_BY_FOUR, leagueTemplate);
    }

    @Test
    void shouldPassErrorIfLeagueTemplateNotFound() {
        // Given
        when(service.getLeagueTemplateById(anyString()))
            .thenThrow(new ResponseStatusException(HttpStatus.NOT_FOUND, "No league templates found with a matching id."));

        // When
        final ResponseStatusException rse = assertThrows(ResponseStatusException.class, () -> controller.getLeagueTemplateById("c08fd796-7fea-40d9-9a0a-cb3a49cce2e4"));

        // Then
        assertEquals(HttpStatus.NOT_FOUND, rse.getStatusCode());
        assertEquals("No league templates found with a matching id.", rse.getReason());
    }

    @Test
    void shouldPassErrorIfLeagueTemplateBeingUsed() {
        // Given
        when(service.getLeagueTemplateById(anyString()))
            .thenThrow(new ResponseStatusException(HttpStatus.CONFLICT, "Cannot delete league template as it is part of an existing tournament template."));

        // When
        final ResponseStatusException rse = assertThrows(ResponseStatusException.class, () -> controller.getLeagueTemplateById("c08fd796-7fea-40d9-9a0a-cb3a49cce2e4"));

        // Then
        assertEquals(HttpStatus.CONFLICT, rse.getStatusCode());
        assertEquals("Cannot delete league template as it is part of an existing tournament template.", rse.getReason());
    }

    private static void assertLeagueTemplate(LeagueTemplate expected, LeagueTemplate actual) {
        assertEquals(expected.getId(), actual.getId());
        assertEquals(expected.getName(), actual.getName());
        assertEquals(expected.getGroupCount(), actual.getGroupCount());
        assertEquals(expected.getTeamsPerGroup(), actual.getTeamsPerGroup());
        assertEquals(expected.getHomeAndAway(), actual.getHomeAndAway());
    }
}
