package com.kanemullett.controller;

import static org.junit.Assert.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.mockito.ArgumentMatchers.anyList;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.Mockito.doThrow;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

import java.util.List;

import org.junit.jupiter.api.Test;
import org.springframework.http.HttpStatus;
import org.springframework.web.server.ResponseStatusException;

import com.kanemullett.model.Competition;
import com.kanemullett.model.CompetitionUpdate;
import com.kanemullett.service.CompetitionService;

public class CompetitionControllerTest {

    private final CompetitionService service = mock(CompetitionService.class);

    private final CompetitionController controller = new CompetitionController(service);

    @Test
    void shouldPassCompetitionsAsResponse() {
        // Given
        final Competition competition1 = mock(Competition.class);
        final Competition competition2 = mock(Competition.class);

        when(service.getCompetitions())
            .thenReturn(List.of(competition1, competition2));

        // When
        final List<Competition> competitions = controller.getCompetitions();

        // Then
        assertEquals(2, competitions.size());
        assertEquals(competition1, competitions.get(0));
        assertEquals(competition2, competitions.get(1));
    }

    @Test
    void shouldPassCreatedCompetitionsAsResponse() {
        // Given
        final Competition competition1 = mock(Competition.class);
        final Competition competition2 = mock(Competition.class);

        when(service.createCompetitions(anyList()))
            .thenReturn(List.of(competition1, competition2));

        // When
        final List<Competition> created = controller.createCompetitions(List.of(competition1, competition2));

        // Then
        assertEquals(2, created.size());
        assertEquals(competition1, created.get(0));
        assertEquals(competition2, created.get(1));
    }

    @Test
    void shouldPassUpdatedCompetitionsAsResponse() {
        // Given
        final CompetitionUpdate competition1 = mock(CompetitionUpdate.class);
        final CompetitionUpdate competition2 = mock(CompetitionUpdate.class);

        final Competition updated1 = mock(Competition.class);
        final Competition updated2 = mock(Competition.class);

        when(service.updateCompetitions(anyList()))
            .thenReturn(List.of(updated1, updated2));

        // When
        final List<Competition> updated = controller.updateCompetitions(List.of(competition1, competition2));

        // Then
        assertEquals(2, updated.size());
        assertEquals(updated1, updated.get(0));
        assertEquals(updated2, updated.get(1));
    }

    @Test
    void shouldPassCompetitionAsResponse() {
        // Given
        final Competition competition = mock(Competition.class);

        when(service.getCompetitionById(anyString()))
            .thenReturn(competition);

        // When
        final Competition response = controller.getCompetitionById("test-id");

        // Then
        assertEquals(competition, response);
    }

    @Test
    void shouldDeleteCompetition() {
        // When
        controller.deleteCompetitionById("test-id");

        // Then
        verify(service).deleteCompetitionById("test-id");
    }

    @Test
    void shouldAddUsersToCompetition() {
        // When
        controller.addUsersToCompetition("test-id", List.of("user1", "user2"));

        // Then
        verify(service).addUsersToCompetition("test-id", List.of("user1", "user2"));
    }

    @Test
    void shouldRemoveUserFromCompetition() {
        // When
        controller.removeUserFromCompetition("test-id", "user");

        // Then
        verify(service).removeUserFromCompetition("test-id", "user");
    }

    @Test
    void shouldPassErrorFromGetCompetitionById() {
        // Given
        when(service.getCompetitionById(anyString()))
            .thenThrow(new ResponseStatusException(HttpStatus.I_AM_A_TEAPOT, "I am a teapot."));

        // When
        final ResponseStatusException rse = assertThrows(ResponseStatusException.class, () -> controller.getCompetitionById("test-id"));

        // Then
        assertEquals(HttpStatus.I_AM_A_TEAPOT, rse.getStatusCode());
        assertEquals("I am a teapot.", rse.getReason());
    }

    @Test
    void shouldPassErrorFromDeleteCompetitionById() {
        // Given
        doThrow(new ResponseStatusException(HttpStatus.I_AM_A_TEAPOT, "I am a teapot."))
            .when(service).deleteCompetitionById(anyString());

        // When
        final ResponseStatusException rse = assertThrows(ResponseStatusException.class, () -> controller.deleteCompetitionById("test-id"));

        // Then
        assertEquals(HttpStatus.I_AM_A_TEAPOT, rse.getStatusCode());
        assertEquals("I am a teapot.", rse.getReason());
    }

    @Test
    void shouldPassErrorFromAddUsersToCompetition() {
        // Given
        doThrow(new ResponseStatusException(HttpStatus.I_AM_A_TEAPOT, "I am a teapot."))
            .when(service).addUsersToCompetition(anyString(), anyList());

        // When
        final ResponseStatusException rse = assertThrows(ResponseStatusException.class, () -> controller.addUsersToCompetition("test-id", List.of("user1", "user2")));

        // Then
        assertEquals(HttpStatus.I_AM_A_TEAPOT, rse.getStatusCode());
        assertEquals("I am a teapot.", rse.getReason());
    }

    @Test
    void shouldPassErrorFromRemoveUserFromCompetition() {
        // Given
        doThrow(new ResponseStatusException(HttpStatus.I_AM_A_TEAPOT, "I am a teapot."))
            .when(service).removeUserFromCompetition(anyString(), anyString());

        // When
        final ResponseStatusException rse = assertThrows(ResponseStatusException.class, () -> controller.removeUserFromCompetition("test-id", "user"));

        // Then
        assertEquals(HttpStatus.I_AM_A_TEAPOT, rse.getStatusCode());
        assertEquals("I am a teapot.", rse.getReason());
    }
}
