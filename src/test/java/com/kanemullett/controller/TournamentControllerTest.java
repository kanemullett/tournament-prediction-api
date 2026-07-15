package com.kanemullett.controller;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.mockito.ArgumentMatchers.anyList;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

import java.util.List;

import org.junit.jupiter.api.Test;
import org.springframework.http.HttpStatus;
import org.springframework.web.server.ResponseStatusException;

import com.kanemullett.model.ImmutableTournament;
import com.kanemullett.model.ImmutableTournamentUpdate;
import com.kanemullett.model.Tournament;
import com.kanemullett.model.TournamentUpdate;
import com.kanemullett.model.type.Confederation;
import com.kanemullett.service.TournamentService;

public class TournamentControllerTest {

    private final TournamentService service = mock(TournamentService.class);

    private final TournamentController controller = new TournamentController(service);

    private static final Tournament EUROS = ImmutableTournament.builder()
        .id("c08fd796-7fea-40d9-9a0a-cb3a49cce2e4")
        .name("UEFA Euro 2024")
        .year(2024)
        .confederation(Confederation.UEFA)
        .templateId("ef0f7ca7-20c5-44ba-97be-f4e7d96cd114")
        .build();
    private static final Tournament WORLD_CUP = ImmutableTournament.builder()
        .id("6ee28143-1286-4618-a8b9-ad86d348ead1")
        .name("2026 FIFA World Cup")
        .year(2026)
        .templateId("ccf688ac-a331-45de-b7cb-bf8b24f8fffb")
        .build();

    @Test
    void shouldPassTournamentsAsResponse() {
        // Given
        when(service.getTournaments())
            .thenReturn(List.of(EUROS, WORLD_CUP));

        // When
        final List<Tournament> tournaments = controller.getTournaments();

        // Then
        assertTournament(EUROS, tournaments.get(0));
        assertTournament(WORLD_CUP, tournaments.get(1));
        
    }

    @Test
    void shouldPassCreatedTournamentsAsResponse() {
        // Given
        when(service.createTournaments(anyList()))
            .thenReturn(List.of(EUROS, WORLD_CUP));

        // When
        final List<Tournament> created = controller.createTournaments(List.of(EUROS, WORLD_CUP));

        // Then
        assertTournament(EUROS, created.get(0));
        assertTournament(WORLD_CUP, created.get(1));
    }

    @Test
    void shouldPassUpdatedTournamentsAsResponse() {
        // Given
        final List<TournamentUpdate> updates = List.of(
            ImmutableTournamentUpdate.builder()
                .id("c08fd796-7fea-40d9-9a0a-cb3a49cce2e4")
                .confederation(Confederation.UEFA)
                .build(),
            ImmutableTournamentUpdate.builder()
                .id("6ee28143-1286-4618-a8b9-ad86d348ead1")
                .year(2026)
                .build()
        );

        when(service.updateTournaments(updates))
            .thenReturn(List.of(EUROS, WORLD_CUP));

        // When
        final List<Tournament> updated = controller.updateTournaments(updates);

        // Then
        assertTournament(EUROS, updated.get(0));
        assertTournament(WORLD_CUP, updated.get(1));
    }

    @Test
    void shouldPassFoundTournamentAsResponse() {
        // Given
        when(service.getTournamentById(anyString()))
            .thenReturn(EUROS);

        // When
        final Tournament tournament = controller.getTournamentById("c08fd796-7fea-40d9-9a0a-cb3a49cce2e4");

        // Then
        assertTournament(EUROS, tournament);
    }

    @Test
    void shouldPassErrorIfTournamentNotFound() {
        // Given
        when(service.getTournamentById(anyString()))
            .thenThrow(new ResponseStatusException(HttpStatus.NOT_FOUND, "No tournaments found with a matching id."));

        // When
        final ResponseStatusException rse = assertThrows(ResponseStatusException.class, () -> controller.getTournamentById("c08fd796-7fea-40d9-9a0a-cb3a49cce2e4"));

        // Then
        assertEquals(HttpStatus.NOT_FOUND, rse.getStatusCode());
        assertEquals("No tournaments found with a matching id.", rse.getReason());
    }

    @Test
    void shouldDeleteTournamentById() {
        // When
        controller.deleteTournamentById("c08fd796-7fea-40d9-9a0a-cb3a49cce2e4");

        // Then
        verify(service).deleteTournamentById("c08fd796-7fea-40d9-9a0a-cb3a49cce2e4");
    }

    private static void assertTournament(Tournament expected, Tournament actual) {
        assertEquals(expected.getId(), actual.getId());
        assertEquals(expected.getYear(), expected.getYear());
        assertEquals(expected.getConfederation(), actual.getConfederation());
    }
}
