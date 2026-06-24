package com.kanemullett.controller;

import static org.junit.Assert.assertEquals;
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

import com.kanemullett.model.ImmutableTeam;
import com.kanemullett.model.ImmutableTeamUpdate;
import com.kanemullett.model.Team;
import com.kanemullett.model.TeamUpdate;
import com.kanemullett.model.type.Confederation;
import com.kanemullett.service.TeamService;

public class TeamControllerTest {

    private final TeamService service = mock(TeamService.class);

    private final TeamController controller = new TeamController(service);

    private static final Team BOSNIA = ImmutableTeam.builder()
        .id("c08fd796-7fea-40d9-9a0a-cb3a49cce2e4")
        .name("Bosnia & Herzegovina")
        .imagePath("BIH.png")
        .confederation(Confederation.UEFA)
        .build();
    private static final Team BOTSWANA = ImmutableTeam.builder()
        .id("6ee28143-1286-4618-a8b9-ad86d348ead1")
        .name("Botswana")
        .imagePath("BOT.png")
        .confederation(Confederation.CAF)
        .build();
    private static final Team ENGLAND = ImmutableTeam.builder()
        .id("e107d069-b277-4902-bdad-7091a494a8b3")
        .name("England")
        .imagePath("ENG.png")
        .confederation(Confederation.UEFA)
        .build();

    @Test
    void shouldPassTeamsAsResponse() {
        // Given
        when(service.getTeams(null, null))
            .thenReturn(List.of(BOSNIA, BOTSWANA, ENGLAND));

        // When
        final List<Team> teams = controller.getTeams(null, null);

        // Then
        verify(service).getTeams(null, null);

        assertEquals(3, teams.size());
        
        assertTeam(BOSNIA, teams.get(0));
        assertTeam(BOTSWANA, teams.get(1));
        assertTeam(ENGLAND, teams.get(2));
    }

    @Test
    void shouldPassCreatedTeamsAsResponse() {
        // Given
        when(service.createTeams(anyList()))
            .thenReturn(List.of(BOSNIA, BOTSWANA));

        // When
        final List<Team> created = controller.createTeams(List.of(BOSNIA, BOTSWANA));

        // Then
        verify(service).createTeams(List.of(BOSNIA, BOTSWANA));

        assertEquals(2, created.size());

        assertTeam(BOSNIA, created.get(0));
        assertTeam(BOTSWANA, created.get(1));
    }

    @Test
    void shouldPassUpdatedTeamsAsResponse() {
        // Given
        final List<TeamUpdate> teamUpdates = List.of(
            ImmutableTeamUpdate.builder()
                .id("c08fd796-7fea-40d9-9a0a-cb3a49cce2e4")
                .confederation(Confederation.UEFA)
                .build(),
            ImmutableTeamUpdate.builder()
                .id("6ee28143-1286-4618-a8b9-ad86d348ead1")
                .imagePath("BOT.png")
                .build()
        );

        when(service.updateTeams(anyList()))
            .thenReturn(List.of(BOSNIA, BOTSWANA));

        // When
        final List<Team> updated = controller.updateTeams(teamUpdates);

        // Then
        verify(service).updateTeams(teamUpdates);

        assertEquals(2, updated.size());

        assertTeam(BOSNIA, updated.get(0));
        assertTeam(BOTSWANA, updated.get(1));
    }

    @Test
    void shouldPassTeamAsResponse() {
        // Given
        when(service.getTeamById(anyString()))
            .thenReturn(BOSNIA);

        // When
        final Team team = controller.getTeamById("c08fd796-7fea-40d9-9a0a-cb3a49cce2e4");

        // Then
        verify(service).getTeamById("c08fd796-7fea-40d9-9a0a-cb3a49cce2e4");

        assertTeam(BOSNIA, team);
    }

    @Test
    void shouldPassErrorIfTeamNotFound() {
        // Given
        when(service.getTeamById(anyString()))
            .thenThrow(new ResponseStatusException(HttpStatus.NOT_FOUND, "No teams found with a matching id."));

        // When
        final ResponseStatusException rse = assertThrows(ResponseStatusException.class, () -> controller.getTeamById("c08fd796-7fea-40d9-9a0a-cb3a49cce2e4"));

        // Then
        verify(service).getTeamById("c08fd796-7fea-40d9-9a0a-cb3a49cce2e4");

        assertEquals(HttpStatus.NOT_FOUND, rse.getStatusCode());
        assertEquals("No teams found with a matching id.", rse.getReason());
    }

    @Test
    void shouldDeleteTeamById() {
        // When
        controller.deleteTeamById("c08fd796-7fea-40d9-9a0a-cb3a49cce2e4");

        // Then
        verify(service).deleteTeamById("c08fd796-7fea-40d9-9a0a-cb3a49cce2e4");
    }

    private static void assertTeam(Team expected, Team actual) {
        assertEquals(expected.getId(), actual.getId());
        assertEquals(expected.getName(), actual.getName());
        assertEquals(expected.getImagePath(), actual.getImagePath());
        assertEquals(expected.getConfederation(), actual.getConfederation());
    }
}
