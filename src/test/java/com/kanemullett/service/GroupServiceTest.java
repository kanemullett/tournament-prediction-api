package com.kanemullett.service;

import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNull;
import static org.junit.jupiter.api.Assertions.assertThrows;
import org.junit.jupiter.api.Test;
import org.mockito.ArgumentCaptor;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.times;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;
import org.springframework.http.HttpStatus;
import org.springframework.web.server.ResponseStatusException;

import com.kanemullett.model.Column;
import com.kanemullett.model.DatabaseRecord;
import com.kanemullett.model.Group;
import com.kanemullett.model.GroupRecord;
import com.kanemullett.model.GroupTeam;
import com.kanemullett.model.ImmutableDatabaseRecord;
import com.kanemullett.model.ImmutableGroupRecord;
import com.kanemullett.model.ImmutableQueryResponse;
import com.kanemullett.model.ImmutableTeam;
import com.kanemullett.model.QueryCondition;
import com.kanemullett.model.QueryConditionGroup;
import com.kanemullett.model.QueryRequest;
import com.kanemullett.model.QueryResponse;
import com.kanemullett.model.Table;
import com.kanemullett.model.TableJoin;
import com.kanemullett.model.Team;
import com.kanemullett.model.UpdateRequest;
import com.kanemullett.model.type.ConditionOperator;
import com.kanemullett.model.type.Confederation;
import com.kanemullett.model.type.JoinType;
import com.kanemullett.model.type.SqlOperator;

import jakarta.annotation.Nullable;

public class GroupServiceTest {

    private final DatabaseQueryService queryService = mock(DatabaseQueryService.class);

    private final GroupService groupService = new GroupService(queryService);

    private static final DatabaseRecord MEXICO_RECORD = ImmutableDatabaseRecord.builder()
        .putData("groupId", "5ffe2393-7717-43d4-860d-9fbd52775b5a")
        .putData("groupName", "Group A")
        .putData("teamId", "295b5446-d81d-427e-8fcc-bae3576cb0c5")
        .putData("teamName", "Mexico")
        .putData("imagePath", "MEX.png")
        .putData("confederation", "CONCACAF")
        .putData("ranking", 10)
        .build();
    private static final DatabaseRecord SOUTH_AFRICA_RECORD = ImmutableDatabaseRecord.builder()
        .putData("groupId", "5ffe2393-7717-43d4-860d-9fbd52775b5a")
        .putData("groupName", "Group A")
        .putData("teamId", "77c8879b-2451-4fec-ba88-5d4d4e95ab1e")
        .putData("teamName", "South Africa")
        .putData("imagePath", "RSA.png")
        .putData("confederation", "CAF")
        .putData("ranking", 54)
        .build();
    private static final DatabaseRecord SOUTH_KOREA_RECORD = ImmutableDatabaseRecord.builder()
        .putData("groupId", "5ffe2393-7717-43d4-860d-9fbd52775b5a")
        .putData("groupName", "Group A")
        .putData("teamId", "81abc62d-5614-4b82-994b-62fa59b30949")
        .putData("teamName", "South Korea")
        .putData("imagePath", "KOR.png")
        .putData("confederation", "AFC")
        .putData("ranking", 32)
        .build();
    private static final DatabaseRecord CZECHIA_RECORD = ImmutableDatabaseRecord.builder()
        .putData("groupId", "5ffe2393-7717-43d4-860d-9fbd52775b5a")
        .putData("groupName", "Group A")
        .putData("teamId", "0d6319a1-2faa-4c98-8392-d700e78b57c2")
        .putData("teamName", "Czechia")
        .putData("imagePath", "CZE.png")
        .putData("confederation", "UEFA")
        .putData("ranking", 48)
        .build();
    private static final DatabaseRecord CANADA_RECORD = ImmutableDatabaseRecord.builder()
        .putData("groupId", "9b60ac29-905a-437d-918f-b98b74ce3e1b")
        .putData("groupName", "Group B")
        .putData("teamId", "179ebfc7-3672-4f15-9f5b-559a0fe2a57a")
        .putData("teamName", "Canada")
        .putData("imagePath", "CAN.png")
        .putData("confederation", "CONCACAF")
        .putData("ranking", 30)
        .build();
    private static final DatabaseRecord BOSNIA_AND_HERZEGOVINA_RECORD = ImmutableDatabaseRecord.builder()
        .putData("groupId", "9b60ac29-905a-437d-918f-b98b74ce3e1b")
        .putData("groupName", "Group B")
        .putData("teamId", "d6e08336-f4c6-458d-9483-95785ea4238e")
        .putData("teamName", "Bosnia and Herzegovina")
        .putData("imagePath", "BIH.png")
        .putData("confederation", "UEFA")
        .putData("ranking", 61)
        .build();
    private static final DatabaseRecord QATAR_RECORD = ImmutableDatabaseRecord.builder()
        .putData("groupId", "9b60ac29-905a-437d-918f-b98b74ce3e1b")
        .putData("groupName", "Group B")
        .putData("teamId", "e48f7922-94c5-4b01-9bd5-5a8846c8e583")
        .putData("teamName", "Qatar")
        .putData("imagePath", "QAT.png")
        .putData("confederation", "AFC")
        .putData("ranking", 59)
        .build();
    private static final DatabaseRecord SWITZERLAND_RECORD = ImmutableDatabaseRecord.builder()
        .putData("groupId", "9b60ac29-905a-437d-918f-b98b74ce3e1b")
        .putData("groupName", "Group B")
        .putData("teamId", "fa4c8cee-676d-4016-b10b-74d64d80a337")
        .putData("teamName", "Switzerland")
        .putData("imagePath", "SUI.png")
        .putData("confederation", "UEFA")
        .putData("ranking", 14)
        .build();

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

    @Test
    void shouldReturnGroups() {
        // Given
        final QueryResponse<DatabaseRecord> existsResponse = buildTournamentExistsResponse();

        final List<DatabaseRecord> teamRecords = List.of(
                MEXICO_RECORD,
                SOUTH_AFRICA_RECORD,
                SOUTH_KOREA_RECORD,
                CZECHIA_RECORD,
                CANADA_RECORD,
                BOSNIA_AND_HERZEGOVINA_RECORD,
                QATAR_RECORD,
                SWITZERLAND_RECORD
        );
        final QueryResponse<DatabaseRecord> groupTeamsResponse = buildGroupTeamsResponse(teamRecords);

        when(queryService.retrieveRecords(any()))
            .thenReturn(existsResponse, groupTeamsResponse);

        // When
        final List<Group> groups = groupService.getGroups("2c299156-dd35-4791-8684-eca54a433042");

        // Then
        final ArgumentCaptor<QueryRequest> requestCaptor = ArgumentCaptor.forClass(QueryRequest.class);
        verify(queryService, times(2)).retrieveRecords(requestCaptor.capture());
        final List<QueryRequest> queryRequests = requestCaptor.getAllValues();

        assertTournamentExistsRequest(queryRequests.get(0), "2c299156-dd35-4791-8684-eca54a433042");
        assertGroupRequest(queryRequests.get(1), "2c299156-dd35-4791-8684-eca54a433042");

        assertEquals(2, groups.size());

        final Group group1 = groups.get(0);
        assertEquals("5ffe2393-7717-43d4-860d-9fbd52775b5a", group1.getId());
        assertEquals("Group A", group1.getName());
        assertEquals(4, group1.getTeams().size());

        assertTeam(MEXICO, group1.getTeams().get(0));
        assertTeam(SOUTH_AFRICA, group1.getTeams().get(1));
        assertTeam(SOUTH_KOREA, group1.getTeams().get(2));
        assertTeam(CZECHIA, group1.getTeams().get(3));

        final Group group2 = groups.get(1);
        assertEquals("9b60ac29-905a-437d-918f-b98b74ce3e1b", group2.getId());
        assertEquals("Group B", group2.getName());
        assertEquals(4, group2.getTeams().size());

        assertTeam(CANADA, group2.getTeams().get(0));
        assertTeam(BOSNIA_AND_HERZEGOVINA, group2.getTeams().get(1));
        assertTeam(QATAR, group2.getTeams().get(2));
        assertTeam(SWITZERLAND, group2.getTeams().get(3));
    }

    @Test
    void shouldErrorIfTournamentDoesNotExistWhileRetrievingGroups() {
        // Given
        final QueryResponse<DatabaseRecord> existsResponse = mock(QueryResponse.class);
        when(existsResponse.getRecordCount())
            .thenReturn(0);

        when(queryService.retrieveRecords(any()))
            .thenReturn(existsResponse);

        // When
        final ResponseStatusException rse = assertThrows(ResponseStatusException.class, () -> groupService.getGroups("5341cff8-df9f-4068-8a42-4b4288ecba87"));

        // Then
        assertEquals(HttpStatus.NOT_FOUND, rse.getStatusCode());
        assertEquals("No tournaments found with a matching id.", rse.getReason());
    }

    @Test
    void shouldErrorIfTournamentHasNoGroupStage() {
        // Given
        final QueryResponse<DatabaseRecord> existsResponse = mock(QueryResponse.class);
        when(existsResponse.getRecordCount())
            .thenReturn(1);
        when(existsResponse.getRecords())
            .thenReturn(List.of(
                ImmutableDatabaseRecord.builder()
                    .id("2c299156-dd35-4791-8684-eca54a433042")
                    .putData("knockoutTemplateId", "53a09cc5-859b-482d-9d37-99217a11fcb5")
                    .build()
            ));

        when(queryService.retrieveRecords(any()))
            .thenReturn(existsResponse);

        // When
        final ResponseStatusException rse = assertThrows(ResponseStatusException.class, () -> groupService.getGroups("2c299156-dd35-4791-8684-eca54a433042"));

        // Then
        assertEquals(HttpStatus.NOT_FOUND, rse.getStatusCode());
        assertEquals("The tournament with the supplied id does not have a group stage.", rse.getReason());
    }

    @Test
    void shouldUpdateGroups() {
        // Given
        final QueryResponse<DatabaseRecord> existsResponse = buildTournamentExistsResponse();

        final QueryResponse<DatabaseRecord> groupsResponse = ImmutableQueryResponse.builder()
            .recordCount(8)
            .records(List.of(
                MEXICO_RECORD,
                SOUTH_AFRICA_RECORD,
                SOUTH_KOREA_RECORD,
                CZECHIA_RECORD,
                CANADA_RECORD,
                BOSNIA_AND_HERZEGOVINA_RECORD,
                QATAR_RECORD,
                SWITZERLAND_RECORD
            ))
            .referenceId("")
            .build();

        when(queryService.retrieveRecords(any()))
            .thenReturn(existsResponse, groupsResponse);

        final List<GroupRecord> groupUpdates = List.of(
            ImmutableGroupRecord.builder()
                .id("5ffe2393-7717-43d4-860d-9fbd52775b5a")
                .name("Group A")
                .build(),
            ImmutableGroupRecord.builder()
                .id("9b60ac29-905a-437d-918f-b98b74ce3e1b")
                .name("Group B")
                .build()
        );

        // When
        final List<Group> updates = groupService.updateGroups("5341cff8-df9f-4068-8a42-4b4288ecba87", groupUpdates);

        // Then
        final ArgumentCaptor<UpdateRequest> updateCaptor = ArgumentCaptor.forClass(UpdateRequest.class);
        verify(queryService).updateRecords(updateCaptor.capture());
        final UpdateRequest<DatabaseRecord> updateRequest = updateCaptor.getValue();

        assertEquals(SqlOperator.UPDATE, updateRequest.getOperation());
        assertTable("predictor", "groups_5341cff8-df9f-4068-8a42-4b4288ecba87", updateRequest.getTable());

        assertEquals(2, updateRequest.getRecords().size());
        assertGroupRecord("5ffe2393-7717-43d4-860d-9fbd52775b5a", "Group A", (GroupRecord) updateRequest.getRecords().get(0));
        assertGroupRecord("9b60ac29-905a-437d-918f-b98b74ce3e1b", "Group B", (GroupRecord) updateRequest.getRecords().get(1));

        assertEquals(2, updates.size());

        final Group group1 = updates.get(0);
        assertEquals("5ffe2393-7717-43d4-860d-9fbd52775b5a", group1.getId());
        assertEquals("Group A", group1.getName());
        assertEquals(4, group1.getTeams().size());

        assertTeam(MEXICO, group1.getTeams().get(0));
        assertTeam(SOUTH_AFRICA, group1.getTeams().get(1));
        assertTeam(SOUTH_KOREA, group1.getTeams().get(2));
        assertTeam(CZECHIA, group1.getTeams().get(3));

        final Group group2 = updates.get(1);
        assertEquals("9b60ac29-905a-437d-918f-b98b74ce3e1b", group2.getId());
        assertEquals("Group B", group2.getName());
        assertEquals(4, group2.getTeams().size());

        assertTeam(CANADA, group2.getTeams().get(0));
        assertTeam(BOSNIA_AND_HERZEGOVINA, group2.getTeams().get(1));
        assertTeam(QATAR, group2.getTeams().get(2));
        assertTeam(SWITZERLAND, group2.getTeams().get(3));
    }

    @Test
    void shouldErrorIfTournamentDoesNotExistWhileUpdatingGroups() {
        // Given
        final QueryResponse<DatabaseRecord> existsResponse = mock(QueryResponse.class);
        when(existsResponse.getRecordCount())
            .thenReturn(0);

        when(queryService.retrieveRecords(any()))
            .thenReturn(existsResponse);

        final List<GroupRecord> groupUpdates = List.of(
            ImmutableGroupRecord.builder()
                .id("5ffe2393-7717-43d4-860d-9fbd52775b5a")
                .name("Group A")
                .build(),
            ImmutableGroupRecord.builder()
                .id("9b60ac29-905a-437d-918f-b98b74ce3e1b")
                .name("Group B")
                .build()
        );

        // When
        final ResponseStatusException rse = assertThrows(ResponseStatusException.class, () -> groupService.updateGroups("5341cff8-df9f-4068-8a42-4b4288ecba87", groupUpdates));

        // Then
        assertEquals(HttpStatus.NOT_FOUND, rse.getStatusCode());
        assertEquals("No tournaments found with a matching id.", rse.getReason());
    }

    @Test
    void shouldErrorIfTournamentHasNoGroupStageWhileUpdatingGroups() {
        // Given
        final QueryResponse<DatabaseRecord> existsResponse = mock(QueryResponse.class);
        when(existsResponse.getRecordCount())
            .thenReturn(1);
        when(existsResponse.getRecords())
            .thenReturn(List.of(
                ImmutableDatabaseRecord.builder()
                    .id("2c299156-dd35-4791-8684-eca54a433042")
                    .putData("knockoutTemplateId", "53a09cc5-859b-482d-9d37-99217a11fcb5")
                    .build()
            ));

        when(queryService.retrieveRecords(any()))
            .thenReturn(existsResponse);

        final List<GroupRecord> groupUpdates = List.of(
            ImmutableGroupRecord.builder()
                .id("5ffe2393-7717-43d4-860d-9fbd52775b5a")
                .name("Group A")
                .build(),
            ImmutableGroupRecord.builder()
                .id("9b60ac29-905a-437d-918f-b98b74ce3e1b")
                .name("Group B")
                .build()
        );

        // When
        final ResponseStatusException rse = assertThrows(ResponseStatusException.class, () -> groupService.updateGroups("5341cff8-df9f-4068-8a42-4b4288ecba87", groupUpdates));

        // Then
        assertEquals(HttpStatus.NOT_FOUND, rse.getStatusCode());
        assertEquals("The tournament with the supplied id does not have a group stage.", rse.getReason());
    }

    @Test
    void shouldReturnGroupById() {
        // Given
        final QueryResponse<DatabaseRecord> existsResponse = buildTournamentExistsResponse();

        final List<DatabaseRecord> teamRecords = List.of(
                MEXICO_RECORD,
                SOUTH_AFRICA_RECORD,
                SOUTH_KOREA_RECORD,
                CZECHIA_RECORD
        );
        final QueryResponse<DatabaseRecord> groupTeamsResponse = buildGroupTeamsResponse(teamRecords);

        when(queryService.retrieveRecords(any()))
            .thenReturn(existsResponse, groupTeamsResponse);

        // When
        final Group group = groupService.getGroupById("5341cff8-df9f-4068-8a42-4b4288ecba87", "5ffe2393-7717-43d4-860d-9fbd52775b5a");

        // Then
        final ArgumentCaptor<QueryRequest<DatabaseRecord>> requestCaptor = ArgumentCaptor.forClass(QueryRequest.class);
        verify(queryService, times(3)).retrieveRecords(requestCaptor.capture());
        final List<QueryRequest<DatabaseRecord>> requests = requestCaptor.getAllValues();

        assertTournamentExistsRequest(requests.get(0), "5341cff8-df9f-4068-8a42-4b4288ecba87");
        assertGroupExistsRequest(requests.get(1), "5341cff8-df9f-4068-8a42-4b4288ecba87", "5ffe2393-7717-43d4-860d-9fbd52775b5a");
        
        final QueryConditionGroup expectedConditionGroup = QueryConditionGroup.of(
            QueryCondition.of(
                Column.of("gt", "groupId"), "5ffe2393-7717-43d4-860d-9fbd52775b5a"
            )
        );
        assertGroupRequest(expectedConditionGroup, requests.get(2), "5341cff8-df9f-4068-8a42-4b4288ecba87");

        assertEquals("5ffe2393-7717-43d4-860d-9fbd52775b5a", group.getId());
        assertEquals("Group A", group.getName());
        assertEquals(4, group.getTeams().size());

        assertTeam(MEXICO, group.getTeams().get(0));
        assertTeam(SOUTH_AFRICA, group.getTeams().get(1));
        assertTeam(SOUTH_KOREA, group.getTeams().get(2));
        assertTeam(CZECHIA, group.getTeams().get(3));
    }

    @Test
    void shouldErrorIfTournamentDoesNotExistWhileRetrievingGroup() {
        // Given
        final QueryResponse<DatabaseRecord> existsResponse = mock(QueryResponse.class);
        when(existsResponse.getRecordCount())
            .thenReturn(0);

        when(queryService.retrieveRecords(any()))
            .thenReturn(existsResponse);

        // When
        final ResponseStatusException rse = assertThrows(ResponseStatusException.class, () -> groupService.getGroupById("5341cff8-df9f-4068-8a42-4b4288ecba87", "5ffe2393-7717-43d4-860d-9fbd52775b5a"));

        // Then
        assertEquals(HttpStatus.NOT_FOUND, rse.getStatusCode());
        assertEquals("No tournaments found with a matching id.", rse.getReason());
    }

    @Test
    void shouldErrorIfTournamentHasNoGroupStageWhileRetrievingGroup() {
        // Given
        final QueryResponse<DatabaseRecord> existsResponse = mock(QueryResponse.class);
        when(existsResponse.getRecordCount())
            .thenReturn(1);
        when(existsResponse.getRecords())
            .thenReturn(List.of(
                ImmutableDatabaseRecord.builder()
                    .id("2c299156-dd35-4791-8684-eca54a433042")
                    .putData("knockoutTemplateId", "53a09cc5-859b-482d-9d37-99217a11fcb5")
                    .build()
            ));

        when(queryService.retrieveRecords(any()))
            .thenReturn(existsResponse);

        // When
        final ResponseStatusException rse = assertThrows(ResponseStatusException.class, () -> groupService.getGroupById("5341cff8-df9f-4068-8a42-4b4288ecba87", "5ffe2393-7717-43d4-860d-9fbd52775b5a"));

        // Then
        assertEquals(HttpStatus.NOT_FOUND, rse.getStatusCode());
        assertEquals("The tournament with the supplied id does not have a group stage.", rse.getReason());
    }

    @Test
    void shouldErrorIfGroupDoesNotExist() {
        // Given
        final QueryResponse<DatabaseRecord> tournamentExistsResponse = mock(QueryResponse.class);
        when(tournamentExistsResponse.getRecordCount())
            .thenReturn(1);
        when(tournamentExistsResponse.getRecords())
            .thenReturn(List.of(
                ImmutableDatabaseRecord.builder()
                    .id("2c299156-dd35-4791-8684-eca54a433042")
                    .putData("leagueTemplateId", "53a09cc5-859b-482d-9d37-99217a11fcb5")
                    .build()
            ));

        final QueryResponse<DatabaseRecord> groupExistsResponse = mock(QueryResponse.class);
        when(groupExistsResponse.getRecordCount())
            .thenReturn(0);

        when(queryService.retrieveRecords(any()))
            .thenReturn(tournamentExistsResponse, groupExistsResponse);

        // When
        final ResponseStatusException rse = assertThrows(ResponseStatusException.class, () -> groupService.getGroupById("5341cff8-df9f-4068-8a42-4b4288ecba87", "5ffe2393-7717-43d4-860d-9fbd52775b5a"));

        // Then
        assertEquals(HttpStatus.NOT_FOUND, rse.getStatusCode());
        assertEquals("No groups found with a matching id.", rse.getReason());
    }

    @Test
    void shouldAssignTeamsToGroup() {
        // Given
        final QueryResponse<DatabaseRecord> tournamentExistsResponse = buildTournamentExistsResponse();
        final QueryResponse<DatabaseRecord> groupExistsResponse = buildGroupExistsResponse();

        final QueryResponse<DatabaseRecord> teamsResponse = mock(QueryResponse.class);
        when(teamsResponse.getRecords())
            .thenReturn(List.of(MEXICO, CZECHIA));

        final QueryResponse<DatabaseRecord> groupTeamsResponse = mock(QueryResponse.class);
        when(groupTeamsResponse.getRecordCount())
            .thenReturn(2);

        final QueryResponse<DatabaseRecord> teamsPerGroupResponse = mock(QueryResponse.class);
        when(teamsPerGroupResponse.getRecords())
            .thenReturn(List.of(
                ImmutableDatabaseRecord.builder()
                    .putData("teamsPerGroup", 4)
                    .build()
            ));

        final QueryResponse<DatabaseRecord> groupResponse = mock(QueryResponse.class);
        when(groupResponse.getRecordCount())
            .thenReturn(4);
        when(groupResponse.getRecords())
            .thenReturn(List.of(
                MEXICO_RECORD,
                SOUTH_AFRICA_RECORD,
                SOUTH_KOREA_RECORD,
                CZECHIA_RECORD
            ));


        when(queryService.retrieveRecords(any()))
            .thenReturn(tournamentExistsResponse, groupExistsResponse, teamsResponse, groupTeamsResponse, teamsPerGroupResponse, groupResponse);

        // When
        final Group group = groupService.addTeamsToGroup("5341cff8-df9f-4068-8a42-4b4288ecba87", "5ffe2393-7717-43d4-860d-9fbd52775b5a", List.of("295b5446-d81d-427e-8fcc-bae3576cb0c5", "0d6319a1-2faa-4c98-8392-d700e78b57c2"));

        // Then
        final ArgumentCaptor<UpdateRequest<GroupTeam>> updateCaptor = ArgumentCaptor.forClass(UpdateRequest.class);
        verify(queryService).updateRecords(updateCaptor.capture());
        final UpdateRequest<GroupTeam> updateRequest = updateCaptor.getValue();

        assertEquals(SqlOperator.INSERT, updateRequest.getOperation());
        assertTable("predictor", "group-teams_5341cff8-df9f-4068-8a42-4b4288ecba87", updateRequest.getTable());
        assertEquals(2, updateRequest.getRecords().size());

        assertGroupTeam("5ffe2393-7717-43d4-860d-9fbd52775b5a", "295b5446-d81d-427e-8fcc-bae3576cb0c5", updateRequest.getRecords().get(0));
        assertGroupTeam("5ffe2393-7717-43d4-860d-9fbd52775b5a", "0d6319a1-2faa-4c98-8392-d700e78b57c2", updateRequest.getRecords().get(1));

        assertEquals("5ffe2393-7717-43d4-860d-9fbd52775b5a", group.getId());
        assertEquals("Group A", group.getName());
        assertEquals(4, group.getTeams().size());

        assertTeam(MEXICO, group.getTeams().get(0));
        assertTeam(SOUTH_AFRICA, group.getTeams().get(1));
        assertTeam(SOUTH_KOREA, group.getTeams().get(2));
        assertTeam(CZECHIA, group.getTeams().get(3));
    }

    @Test
    void shouldErrorWhenTeamsNotFound() {
        // Given
        final QueryResponse<DatabaseRecord> tournamentExistsResponse = buildTournamentExistsResponse();
        final QueryResponse<DatabaseRecord> groupExistsResponse = buildGroupExistsResponse();

        final QueryResponse<DatabaseRecord> teamsResponse = mock(QueryResponse.class);
        when(teamsResponse.getRecordCount())
            .thenReturn(0);
        when(teamsResponse.getRecords())
            .thenReturn(List.of());


        when(queryService.retrieveRecords(any()))
            .thenReturn(tournamentExistsResponse, groupExistsResponse, teamsResponse);

        // When
        final ResponseStatusException rse = assertThrows(ResponseStatusException.class, () -> groupService.addTeamsToGroup("5341cff8-df9f-4068-8a42-4b4288ecba87", "5ffe2393-7717-43d4-860d-9fbd52775b5a", List.of("295b5446-d81d-427e-8fcc-bae3576cb0c5", "0d6319a1-2faa-4c98-8392-d700e78b57c2")));

        // Then
        assertEquals(HttpStatus.BAD_REQUEST, rse.getStatusCode());
        assertEquals("No teams found with ids: 295b5446-d81d-427e-8fcc-bae3576cb0c5, 0d6319a1-2faa-4c98-8392-d700e78b57c2", rse.getReason());
    }

    @Test
    void shouldErrorWhenTournamentNotFoundDuringAssign() {
        // Given
        final QueryResponse<DatabaseRecord> tournamentExistsResponse = mock(QueryResponse.class);
        when(tournamentExistsResponse.getRecordCount())
            .thenReturn(0);

        when(queryService.retrieveRecords(any()))
            .thenReturn(tournamentExistsResponse);

        // When
        final ResponseStatusException rse = assertThrows(ResponseStatusException.class, () -> groupService.addTeamsToGroup("5341cff8-df9f-4068-8a42-4b4288ecba87", "5ffe2393-7717-43d4-860d-9fbd52775b5a", List.of("295b5446-d81d-427e-8fcc-bae3576cb0c5", "0d6319a1-2faa-4c98-8392-d700e78b57c2")));

        // Then
        assertEquals(HttpStatus.NOT_FOUND, rse.getStatusCode());
        assertEquals("No tournaments found with a matching id.", rse.getReason());
    }

    @Test
    void shouldErrorWhenTournamentHasNoGroupStageDuringAssign() {
        // Given
        final QueryResponse<DatabaseRecord> tournamentExistsResponse = mock(QueryResponse.class);
        when(tournamentExistsResponse.getRecordCount())
            .thenReturn(1);
        when(tournamentExistsResponse.getRecords())
            .thenReturn(List.of(
                ImmutableDatabaseRecord.builder()
                    .id("5341cff8-df9f-4068-8a42-4b4288ecba87")
                    .build()
            ));

        when(queryService.retrieveRecords(any()))
            .thenReturn(tournamentExistsResponse);

        // When
        final ResponseStatusException rse = assertThrows(ResponseStatusException.class, () -> groupService.addTeamsToGroup("5341cff8-df9f-4068-8a42-4b4288ecba87", "5ffe2393-7717-43d4-860d-9fbd52775b5a", List.of("295b5446-d81d-427e-8fcc-bae3576cb0c5", "0d6319a1-2faa-4c98-8392-d700e78b57c2")));

        // Then
        assertEquals(HttpStatus.NOT_FOUND, rse.getStatusCode());
        assertEquals("The tournament with the supplied id does not have a group stage.", rse.getReason());
    }

    @Test
    void shouldErrorWhenGroupNotFoundDuringAssign() {
        // Given
        final QueryResponse<DatabaseRecord> tournamentExistsResponse = buildTournamentExistsResponse();

        final QueryResponse<DatabaseRecord> groupExistsResponse = mock(QueryResponse.class);
        when(groupExistsResponse.getRecordCount())
            .thenReturn(0);

        when(queryService.retrieveRecords(any()))
            .thenReturn(tournamentExistsResponse, groupExistsResponse);

        // When
        final ResponseStatusException rse = assertThrows(ResponseStatusException.class, () -> groupService.addTeamsToGroup("5341cff8-df9f-4068-8a42-4b4288ecba87", "5ffe2393-7717-43d4-860d-9fbd52775b5a", List.of("295b5446-d81d-427e-8fcc-bae3576cb0c5", "0d6319a1-2faa-4c98-8392-d700e78b57c2")));

        // Then
        assertEquals(HttpStatus.NOT_FOUND, rse.getStatusCode());
        assertEquals("No groups found with a matching id.", rse.getReason());
    }

    @Test
    void shouldErrorWhenAssigningTooManyTeamsToGroup() {
        // Given
        final QueryResponse<DatabaseRecord> tournamentExistsResponse = buildTournamentExistsResponse();
        final QueryResponse<DatabaseRecord> groupExistsResponse = buildGroupExistsResponse();

        final QueryResponse<DatabaseRecord> teamsResponse = mock(QueryResponse.class);
        when(teamsResponse.getRecords())
            .thenReturn(List.of(MEXICO, CZECHIA));

        final QueryResponse<DatabaseRecord> groupTeamsResponse = mock(QueryResponse.class);
        when(groupTeamsResponse.getRecordCount())
            .thenReturn(3);

        final QueryResponse<DatabaseRecord> teamsPerGroupResponse = mock(QueryResponse.class);
        when(teamsPerGroupResponse.getRecords())
            .thenReturn(List.of(
                ImmutableDatabaseRecord.builder()
                    .putData("teamsPerGroup", 4)
                    .build()
            ));


        when(queryService.retrieveRecords(any()))
            .thenReturn(tournamentExistsResponse, groupExistsResponse, teamsResponse, groupTeamsResponse, teamsPerGroupResponse);

        // When
        final ResponseStatusException rse = assertThrows(ResponseStatusException.class, () -> groupService.addTeamsToGroup("5341cff8-df9f-4068-8a42-4b4288ecba87", "5ffe2393-7717-43d4-860d-9fbd52775b5a", List.of("295b5446-d81d-427e-8fcc-bae3576cb0c5", "0d6319a1-2faa-4c98-8392-d700e78b57c2")));

        // Then
        assertEquals(HttpStatus.CONFLICT, rse.getStatusCode());
        assertEquals("Adding teams to the specified group will exceed its maximum team count.", rse.getReason());
    }

    @Test
    void shouldRemoveTeamFromGroup() {
        // Given
        final QueryResponse<DatabaseRecord> tournamentExistsResponse = buildTournamentExistsResponse();
        final QueryResponse<DatabaseRecord> groupExistsResponse = buildGroupExistsResponse();

        final QueryResponse<DatabaseRecord> groupResponse = mock(QueryResponse.class);
        when(groupResponse.getRecordCount())
            .thenReturn(3);
        when(groupResponse.getRecords())
            .thenReturn(List.of(
                SOUTH_AFRICA_RECORD,
                SOUTH_KOREA_RECORD,
                CZECHIA_RECORD
            ));

        when(queryService.retrieveRecords(any()))
            .thenReturn(tournamentExistsResponse, groupExistsResponse, groupResponse);

        // When
        final Group group = groupService.removeTeamFromGroup("5341cff8-df9f-4068-8a42-4b4288ecba87", "5ffe2393-7717-43d4-860d-9fbd52775b5a", "295b5446-d81d-427e-8fcc-bae3576cb0c5");

        // Then
        final ArgumentCaptor<UpdateRequest<GroupTeam>> updateCaptor = ArgumentCaptor.forClass(UpdateRequest.class);
        verify(queryService).updateRecords(updateCaptor.capture());
        final UpdateRequest<GroupTeam> updateRequest = updateCaptor.getValue();

        assertEquals(SqlOperator.DELETE, updateRequest.getOperation());
        assertTable("predictor", "group-teams_5341cff8-df9f-4068-8a42-4b4288ecba87", updateRequest.getTable());
        assertEquals(2, updateRequest.getConditionGroup().getConditions().size());

        final QueryCondition queryCondition1 = updateRequest.getConditionGroup().getConditions().get(0);
        assertCondition(QueryCondition.of(Column.of("groupId"), "5ffe2393-7717-43d4-860d-9fbd52775b5a"), queryCondition1);

        final QueryCondition queryCondition2 = updateRequest.getConditionGroup().getConditions().get(1);
        assertCondition(QueryCondition.of(Column.of("teamId"), "295b5446-d81d-427e-8fcc-bae3576cb0c5"), queryCondition2);

        assertEquals("5ffe2393-7717-43d4-860d-9fbd52775b5a", group.getId());
        assertEquals("Group A", group.getName());
        assertEquals(3, group.getTeams().size());

        assertTeam(SOUTH_AFRICA, group.getTeams().get(0));
        assertTeam(SOUTH_KOREA, group.getTeams().get(1));
        assertTeam(CZECHIA, group.getTeams().get(2));
    }

    @Test
    void shouldErrorWhenTournamentNotFoundDuringRemove() {
        // Given
        final QueryResponse<DatabaseRecord> tournamentExistsResponse = mock(QueryResponse.class);
        when(tournamentExistsResponse.getRecordCount())
            .thenReturn(0);

        when(queryService.retrieveRecords(any()))
            .thenReturn(tournamentExistsResponse);

        // When
        final ResponseStatusException rse = assertThrows(ResponseStatusException.class, () -> groupService.removeTeamFromGroup("5341cff8-df9f-4068-8a42-4b4288ecba87", "5ffe2393-7717-43d4-860d-9fbd52775b5a", "295b5446-d81d-427e-8fcc-bae3576cb0c5"));

        // Then
        assertEquals(HttpStatus.NOT_FOUND, rse.getStatusCode());
        assertEquals("No tournaments found with a matching id.", rse.getReason());
    }

    @Test
    void shouldErrorWhenTournamentHasNoGroupStageDuringRemove() {
        // Given
        final QueryResponse<DatabaseRecord> tournamentExistsResponse = mock(QueryResponse.class);
        when(tournamentExistsResponse.getRecordCount())
            .thenReturn(1);
        when(tournamentExistsResponse.getRecords())
            .thenReturn(List.of(
                ImmutableDatabaseRecord.builder()
                    .id("5341cff8-df9f-4068-8a42-4b4288ecba87")
                    .build()
            ));

        when(queryService.retrieveRecords(any()))
            .thenReturn(tournamentExistsResponse);

        // When
        final ResponseStatusException rse = assertThrows(ResponseStatusException.class, () -> groupService.removeTeamFromGroup("5341cff8-df9f-4068-8a42-4b4288ecba87", "5ffe2393-7717-43d4-860d-9fbd52775b5a", "295b5446-d81d-427e-8fcc-bae3576cb0c5"));

        // Then
        assertEquals(HttpStatus.NOT_FOUND, rse.getStatusCode());
        assertEquals("The tournament with the supplied id does not have a group stage.", rse.getReason());
    }

    @Test
    void shouldErrorWhenGroupNotFoundDuringRemove() {
        // Given
        final QueryResponse<DatabaseRecord> tournamentExistsResponse = buildTournamentExistsResponse();

        final QueryResponse<DatabaseRecord> groupExistsResponse = mock(QueryResponse.class);
        when(groupExistsResponse.getRecordCount())
            .thenReturn(0);

        when(queryService.retrieveRecords(any()))
            .thenReturn(tournamentExistsResponse, groupExistsResponse);

        // When
        final ResponseStatusException rse = assertThrows(ResponseStatusException.class, () -> groupService.removeTeamFromGroup("5341cff8-df9f-4068-8a42-4b4288ecba87", "5ffe2393-7717-43d4-860d-9fbd52775b5a", "295b5446-d81d-427e-8fcc-bae3576cb0c5"));

        // Then
        assertEquals(HttpStatus.NOT_FOUND, rse.getStatusCode());
        assertEquals("No groups found with a matching id.", rse.getReason());
    }

    private static QueryResponse<DatabaseRecord> buildTournamentExistsResponse() {
        final QueryResponse<DatabaseRecord> existsResponse = mock(QueryResponse.class);
        when(existsResponse.getRecordCount())
            .thenReturn(1);
        when(existsResponse.getRecords())
            .thenReturn(List.of(
                ImmutableDatabaseRecord.builder()
                    .id("2c299156-dd35-4791-8684-eca54a433042")
                    .putData("leagueTemplateId", "53a09cc5-859b-482d-9d37-99217a11fcb5")
                    .build()
            ));

        return existsResponse;
    }

    private static QueryResponse<DatabaseRecord> buildGroupExistsResponse() {
        final QueryResponse<DatabaseRecord> existsResponse = mock(QueryResponse.class);
        when(existsResponse.getRecordCount())
            .thenReturn(1);

        return existsResponse;
    }

    private static QueryResponse<DatabaseRecord> buildGroupTeamsResponse(List<DatabaseRecord> teamRecords) {
        final QueryResponse<DatabaseRecord> groupTeamsResponse = mock(QueryResponse.class);
        when(groupTeamsResponse.getRecordCount())
            .thenReturn(teamRecords.size());
        when(groupTeamsResponse.getRecords())
            .thenReturn(teamRecords);

        return groupTeamsResponse;
    }

    private static void assertTournamentExistsRequest(QueryRequest<DatabaseRecord> actual, String tournamentId) {
        final List<Column> tournamentColumns = actual.getColumns();
        assertEquals(2, tournamentColumns.size());
        assertColumn("to", "id", tournamentColumns.get(0));
        assertColumn("tt", "leagueTemplateId", tournamentColumns.get(1));

        assertTable("predictor", "tournaments", "to", actual.getTable());

        assertEquals(1, actual.getJoins().size());
        
        final TableJoin tournamentJoin = (TableJoin) actual.getJoins().get(0);
        assertTable("predictor", "tournament-templates", "tt", tournamentJoin.getTable());
        assertEquals(JoinType.INNER, tournamentJoin.getJoinType());

        final QueryCondition tournamentJoinCondition = tournamentJoin.getJoinCondition();
        assertColumn("to", "templateId", tournamentJoinCondition.getColumn());
        assertColumn("tt", "id", (Column) tournamentJoinCondition.getValue());

        assertEquals(1, actual.getConditionGroup().getConditions().size());

        final QueryCondition tournamentCondition = actual.getConditionGroup().getConditions().get(0);
        assertColumn("to", "id", tournamentCondition.getColumn());
        assertEquals(ConditionOperator.EQUAL, tournamentCondition.getOperator());
        assertEquals(tournamentId, tournamentCondition.getValue());
    }

    private static void assertGroupExistsRequest(QueryRequest<DatabaseRecord> actual, String tournamentId, String groupId) {
        assertTable("predictor", "groups_" + tournamentId, actual.getTable());

        final QueryCondition groupCondition = actual.getConditionGroup().getConditions().get(0);
        assertColumn(Column.of("id"), groupCondition.getColumn());
        assertEquals(ConditionOperator.EQUAL, groupCondition.getOperator());
        assertEquals(groupId, groupCondition.getValue());
    }

    private static void assertGroupRequest(QueryRequest<DatabaseRecord> actual, String tournamentId) {
        assertGroupRequest(null, actual, tournamentId);
    }

    private static void assertGroupRequest(@Nullable QueryConditionGroup expectedConditionGroup, QueryRequest<DatabaseRecord> actual, String tournamentId) {
        final List<Column> columns = actual.getColumns();
        assertEquals(7, columns.size());
        assertColumn("gt", "groupId", columns.get(0));
        assertColumn("gr", "name", "groupName", columns.get(1));
        assertColumn("gt", "teamId", columns.get(2));
        assertColumn("te", "name", "teamName", columns.get(3));
        assertColumn("te", "imagePath", columns.get(4));
        assertColumn("te", "confederation", columns.get(5));
        assertColumn("te", "ranking", columns.get(6));

        assertTable("predictor", "group-teams_" + tournamentId, "gt", actual.getTable());

        assertEquals(2, actual.getJoins().size());

        final TableJoin join1 = (TableJoin) actual.getJoins().get(0);
        assertTable("predictor", "groups_" + tournamentId, "gr", join1.getTable());
        assertEquals(JoinType.INNER, join1.getJoinType());

        final QueryCondition join1Condition = join1.getJoinCondition();
        assertColumn("gt", "groupId", join1Condition.getColumn());
        assertEquals(ConditionOperator.EQUAL, join1Condition.getOperator());
        assertColumn("gr", "id", (Column) join1Condition.getValue());

        final TableJoin join2 = (TableJoin) actual.getJoins().get(1);
        assertTable("predictor", "teams", "te", join2.getTable());
        assertEquals(JoinType.INNER, join2.getJoinType());

        final QueryCondition join2Condition = join2.getJoinCondition();
        assertColumn("gt", "teamId", join2Condition.getColumn());
        assertEquals(ConditionOperator.EQUAL, join2Condition.getOperator());
        assertColumn("te", "id", (Column) join2Condition.getValue());

        if (expectedConditionGroup == null) {
            assertNull(actual.getConditionGroup());
        } else {
            assertConditionGroup(expectedConditionGroup, actual.getConditionGroup());
        }
    }

    private static void assertGroupTeam(String groupId, String teamId, GroupTeam actual) {
        assertEquals(groupId, actual.getGroupId());
        assertEquals(teamId, actual.getTeamId());
    }

    private static void assertGroupRecord(String expectedId, String expectedName, GroupRecord actual) {
        assertEquals(expectedId, actual.getId());
        assertEquals(expectedName, actual.getName());
    }

    private static void assertTeam(Team expected, Team actual) {
        assertEquals(expected.getId(), actual.getId());
        assertEquals(expected.getName(), actual.getName());
        assertEquals(expected.getImagePath(), actual.getImagePath());
        assertEquals(expected.getConfederation(), actual.getConfederation());
        assertEquals(expected.getRanking(), actual.getRanking());
    }

    private static void assertColumn(String expectedTableAlias, String expectedColumn, Column actual) {
        assertColumn(expectedTableAlias, expectedColumn, null, actual);
    }

    private static void assertColumn(String expectedTableAlias, String expectedColumn, @Nullable String expectedColumnAlias, Column actual) {
        assertEquals(expectedTableAlias, actual.getParts().get(0));
        assertEquals(expectedColumn, actual.getParts().get(1));
        assertEquals(expectedColumnAlias, actual.getAlias());
    }

    private static void assertColumn(Column expected, Column actual) {
        assertEquals(expected.getParts(), actual.getParts());
        assertEquals(expected.getAlias(), actual.getAlias());
    }

    private static void assertTable(String expectedSchema, String expectedTable, Table actual) {
        assertTable(expectedSchema, expectedTable, null, actual);
    }

    private static void assertTable(String expectedSchema, String expectedTable, @Nullable String expectedAlias, Table actual) {
        assertEquals(expectedSchema, actual.getSchema());
        assertEquals(expectedTable, actual.getTable());
        assertEquals(expectedAlias, actual.getAlias());
    }

    private static void assertConditionGroup(QueryConditionGroup expected, QueryConditionGroup actual) {
        assertEquals(expected.getJoin(), actual.getJoin());
        assertEquals(expected.getConditions().size(), actual.getConditions().size());
        
        for (int i = 0; i < expected.getConditions().size(); i++) {
            assertCondition(expected.getConditions().get(i), actual.getConditions().get(i));
        }
    }

    private static void assertCondition(QueryCondition expected, QueryCondition actual) {
        assertColumn(expected.getColumn(), actual.getColumn());
        assertEquals(expected.getOperator(), actual.getOperator());
        assertEquals(expected.getValue(), actual.getValue());
    }
}
