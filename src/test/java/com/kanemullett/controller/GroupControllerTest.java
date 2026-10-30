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

import com.kanemullett.model.Group;
import com.kanemullett.model.GroupRecord;
import com.kanemullett.model.ImmutableGroup;
import com.kanemullett.model.ImmutableGroupRecord;
import com.kanemullett.model.ImmutableTeam;
import com.kanemullett.model.Team;
import com.kanemullett.model.type.Confederation;
import com.kanemullett.service.GroupService;

public class GroupControllerTest {

    private final GroupService service = mock(GroupService.class);

    private final GroupController controller = new GroupController(service);

    private static final Team MEXICO = ImmutableTeam.builder()
        .id("295b5446-d81d-427e-8fcc-bae3576cb0c5")
        .name("Mexico")
        .imagePath("MEX.png")
        .confederation(Confederation.CONCACAF)
        .ranking(10)
        .build();
    private static final Team SOUTH_AFRICA = ImmutableTeam.builder()
        .id("77c8879b-2451-4fec-ba88-5d4d4e95ab1e")
        .name("South Africa")
        .imagePath("RSA.png")
        .confederation(Confederation.CAF)
        .ranking(54)
        .build();
    private static final Team SOUTH_KOREA = ImmutableTeam.builder()
        .id("81abc62d-5614-4b82-994b-62fa59b30949")
        .name("South Korea")
        .imagePath("KOR.png")
        .confederation(Confederation.AFC)
        .ranking(32)
        .build();
    private static final Team CZECHIA = ImmutableTeam.builder()
        .id("0d6319a1-2faa-4c98-8392-d700e78b57c2")
        .name("Czechia")
        .imagePath("CZE.png")
        .confederation(Confederation.UEFA)
        .ranking(48)
        .build();
    private static final Team CANADA = ImmutableTeam.builder()
        .id("179ebfc7-3672-4f15-9f5b-559a0fe2a57a")
        .name("Canada")
        .imagePath("CAN.png")
        .confederation(Confederation.CONCACAF)
        .ranking(30)
        .build();
    private static final Team BOSNIA_AND_HERZEGOVINA = ImmutableTeam.builder()
        .id("d6e08336-f4c6-458d-9483-95785ea4238e")
        .name("Bosnia and Herzegovina")
        .imagePath("BIH.png")
        .confederation(Confederation.UEFA)
        .ranking(61)
        .build();
    private static final Team QATAR = ImmutableTeam.builder()
        .id("e48f7922-94c5-4b01-9bd5-5a8846c8e583")
        .name("Qatar")
        .imagePath("QAT.png")
        .confederation(Confederation.AFC)
        .ranking(59)
        .build();
    private static final Team SWITZERLAND = ImmutableTeam.builder()
        .id("fa4c8cee-676d-4016-b10b-74d64d80a337")
        .name("Switzerland")
        .imagePath("SUI.png")
        .confederation(Confederation.UEFA)
        .ranking(14)
        .build();

    private static final Group GROUP_A = ImmutableGroup.builder()
        .id("5ffe2393-7717-43d4-860d-9fbd52775b5a")
        .name("Group A")
        .addTeams(MEXICO, SOUTH_AFRICA, SOUTH_KOREA, CZECHIA)
        .build();
    private static final Group GROUP_B = ImmutableGroup.builder()
        .id("9b60ac29-905a-437d-918f-b98b74ce3e1b")
        .name("Group B")
        .addTeams(CANADA, BOSNIA_AND_HERZEGOVINA, QATAR, SWITZERLAND)
        .build();

    @Test
    void shouldPassGroupsAsResponse() {
        // Given
        when(service.getGroups(anyString()))
            .thenReturn(List.of(GROUP_A, GROUP_B));

        // When
        final List<Group> groups = controller.getGroups("5341cff8-df9f-4068-8a42-4b4288ecba87");

        // Then
        assertGroup(GROUP_A, groups.get(0));
        assertGroup(GROUP_B, groups.get(1));
    }

    @Test
    void shouldPassErrorWhenRetrievingGroups() {
        // Given
        when(service.getGroups(anyString()))
            .thenThrow(new ResponseStatusException(HttpStatus.NOT_FOUND, "Not found"));

        // When
        final ResponseStatusException rse = assertThrows(ResponseStatusException.class, () -> controller.getGroups("5341cff8-df9f-4068-8a42-4b4288ecba87"));

        // Then
        assertEquals(HttpStatus.NOT_FOUND, rse.getStatusCode());
        assertEquals("Not found", rse.getReason());
    }

    @Test
    void shouldPassUpdatedGroupsAsResponse() {
        // Given
        final List<GroupRecord> updates = List.of(
            ImmutableGroupRecord.builder()
                .id("5ffe2393-7717-43d4-860d-9fbd52775b5a")
                .name("Group A")
                .build(),
            ImmutableGroupRecord.builder()
                .id("9b60ac29-905a-437d-918f-b98b74ce3e1b")
                .name("Group B")
                .build()
        );

        when(service.updateGroups(anyString(), anyList()))
            .thenReturn(List.of(GROUP_A, GROUP_B));

        // When
        final List<Group> updated = controller.updateGroups("5341cff8-df9f-4068-8a42-4b4288ecba87", updates);

        // Then
        assertGroup(GROUP_A, updated.get(0));
        assertGroup(GROUP_B, updated.get(1));
    }

    @Test
    void shouldPassErrorWhenUpdatingGroups() {
        // Given
        final List<GroupRecord> updates = List.of(
            ImmutableGroupRecord.builder()
                .id("5ffe2393-7717-43d4-860d-9fbd52775b5a")
                .name("Group A")
                .build(),
            ImmutableGroupRecord.builder()
                .id("9b60ac29-905a-437d-918f-b98b74ce3e1b")
                .name("Group B")
                .build()
        );

        when(service.updateGroups(anyString(), anyList()))
            .thenThrow(new ResponseStatusException(HttpStatus.NOT_FOUND, "Not found"));

        // When
        final ResponseStatusException rse = assertThrows(ResponseStatusException.class, () -> controller.updateGroups("5341cff8-df9f-4068-8a42-4b4288ecba87", updates));

        // Then
        assertEquals(HttpStatus.NOT_FOUND, rse.getStatusCode());
        assertEquals("Not found", rse.getReason());
    }

    @Test
    void shouldPassGroupAsResponse() {
        // Given
        when(service.getGroupById(anyString(), anyString()))
            .thenReturn(GROUP_A);

        // When
        final Group group = controller.getGroupById("5341cff8-df9f-4068-8a42-4b4288ecba87", "5ffe2393-7717-43d4-860d-9fbd52775b5a");

        // Then
        assertGroup(GROUP_A, group);
    }

    @Test
    void shouldPassErrorWhenRetrievingGroup() {
        // Given
        when(service.getGroupById(anyString(), anyString()))
            .thenThrow(new ResponseStatusException(HttpStatus.NOT_FOUND, "Not found"));

        // When
        final ResponseStatusException rse = assertThrows(ResponseStatusException.class, () -> controller.getGroupById("5341cff8-df9f-4068-8a42-4b4288ecba87", "5ffe2393-7717-43d4-860d-9fbd52775b5a"));

        // Then
        assertEquals(HttpStatus.NOT_FOUND, rse.getStatusCode());
        assertEquals("Not found", rse.getReason());
    }

    @Test
    void shouldPassUpdatedGroupAfterInsert() {
        // Given
        when(service.addTeamsToGroup(anyString(), anyString(), anyList()))
            .thenReturn(GROUP_A);

        // When
        final Group updated = controller.addTeamsToGroup("5341cff8-df9f-4068-8a42-4b4288ecba87", "5ffe2393-7717-43d4-860d-9fbd52775b5a", List.of("295b5446-d81d-427e-8fcc-bae3576cb0c5"));

        // Then
        assertGroup(GROUP_A, updated);
    }

    @Test
    void shouldPassErrorFromInsert() {
        // Given
        when(service.addTeamsToGroup(anyString(), anyString(), anyList()))
            .thenThrow(new ResponseStatusException(HttpStatus.NOT_FOUND, "Not found"));

        // When
        final ResponseStatusException rse = assertThrows(ResponseStatusException.class, () -> controller.addTeamsToGroup("5341cff8-df9f-4068-8a42-4b4288ecba87", "5ffe2393-7717-43d4-860d-9fbd52775b5a", List.of("295b5446-d81d-427e-8fcc-bae3576cb0c5")));

        // Then
        assertEquals(HttpStatus.NOT_FOUND, rse.getStatusCode());
        assertEquals("Not found", rse.getReason());
    }

    @Test
    void shouldPassUpdatedGroupAfterRemove() {
        // Given
        final Group group = ImmutableGroup.copyOf(GROUP_A)
            .withTeams(SOUTH_AFRICA, SOUTH_KOREA, CZECHIA);

        when(service.removeTeamFromGroup(anyString(), anyString(), anyString()))
            .thenReturn(group);

        // When
        final Group updated = controller.removeTeamFromGroup("5341cff8-df9f-4068-8a42-4b4288ecba87", "5ffe2393-7717-43d4-860d-9fbd52775b5a", "295b5446-d81d-427e-8fcc-bae3576cb0c5");

        // Then
        assertGroup(group, updated);
    }

    @Test
    void shouldPassErrorFromRemove() {
        // Given
        when(service.removeTeamFromGroup(anyString(), anyString(), anyString()))
            .thenThrow(new ResponseStatusException(HttpStatus.NOT_FOUND, "Not found"));

        // When
        final ResponseStatusException rse = assertThrows(ResponseStatusException.class, () -> controller.removeTeamFromGroup("5341cff8-df9f-4068-8a42-4b4288ecba87", "5ffe2393-7717-43d4-860d-9fbd52775b5a", "295b5446-d81d-427e-8fcc-bae3576cb0c5"));

        // Then
        assertEquals(HttpStatus.NOT_FOUND, rse.getStatusCode());
        assertEquals("Not found", rse.getReason());
    }

    private static void assertGroup(Group expected, Group actual) {
        assertEquals(expected.getId(), actual.getId());
        assertEquals(expected.getName(), actual.getName());
        assertEquals(expected.getTeams().size(), actual.getTeams().size());

        for (int i = 0; i < actual.getTeams().size(); i++) {
            assertTeam(expected.getTeams().get(i), actual.getTeams().get(i));
        }
    }

    private static void assertTeam(Team expected, Team actual) {
        assertEquals(expected.getId(), actual.getId());
        assertEquals(expected.getName(), actual.getName());
        assertEquals(expected.getImagePath(), actual.getImagePath());
        assertEquals(expected.getConfederation(), actual.getConfederation());
        assertEquals(expected.getRanking(), actual.getRanking());
    }
}
