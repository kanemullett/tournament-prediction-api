package com.kanemullett.service;

import java.util.List;

import static org.junit.Assert.assertEquals;
import org.junit.jupiter.api.Test;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.when;

import com.kanemullett.model.DatabaseRecord;
import com.kanemullett.model.Group;
import com.kanemullett.model.ImmutableDatabaseRecord;
import com.kanemullett.model.QueryResponse;

public class GroupServiceTest {

    private final DatabaseQueryService queryService = mock(DatabaseQueryService.class);

    private final GroupService groupService = new GroupService(queryService);

    @Test
    void shouldReturnGroups() {
        // Given
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

        final QueryResponse<DatabaseRecord> groupTeamsResponse = mock(QueryResponse.class);
        when(groupTeamsResponse.getRecordCount())
            .thenReturn(8);
        when(groupTeamsResponse.getRecords())
            .thenReturn(List.of(
                ImmutableDatabaseRecord.builder()
                    .putData("groupId", "5ffe2393-7717-43d4-860d-9fbd52775b5a")
                    .putData("groupName", "Group A")
                    .putData("teamId", "295b5446-d81d-427e-8fcc-bae3576cb0c5")
                    .putData("teamName", "Mexico")
                    .putData("imagePath", "MEX.png")
                    .putData("confederation", "CONCACAF")
                    .putData("ranking", 10)
                    .build(),
                ImmutableDatabaseRecord.builder()
                    .putData("groupId", "5ffe2393-7717-43d4-860d-9fbd52775b5a")
                    .putData("groupName", "Group A")
                    .putData("teamId", "77c8879b-2451-4fec-ba88-5d4d4e95ab1e")
                    .putData("teamName", "South Africa")
                    .putData("imagePath", "RSA.png")
                    .putData("confederation", "CAF")
                    .putData("ranking", 54)
                    .build(),
                ImmutableDatabaseRecord.builder()
                    .putData("groupId", "5ffe2393-7717-43d4-860d-9fbd52775b5a")
                    .putData("groupName", "Group A")
                    .putData("teamId", "81abc62d-5614-4b82-994b-62fa59b30949")
                    .putData("teamName", "South Korea")
                    .putData("imagePath", "KOR.png")
                    .putData("confederation", "AFC")
                    .putData("ranking", 32)
                    .build(),
                ImmutableDatabaseRecord.builder()
                    .putData("groupId", "5ffe2393-7717-43d4-860d-9fbd52775b5a")
                    .putData("groupName", "Group A")
                    .putData("teamId", "0d6319a1-2faa-4c98-8392-d700e78b57c2")
                    .putData("teamName", "Czechia")
                    .putData("imagePath", "CZE.png")
                    .putData("confederation", "UEFA")
                    .putData("ranking", 48)
                    .build(),
                ImmutableDatabaseRecord.builder()
                    .putData("groupId", "9b60ac29-905a-437d-918f-b98b74ce3e1b")
                    .putData("groupName", "Group B")
                    .putData("teamId", "179ebfc7-3672-4f15-9f5b-559a0fe2a57a")
                    .putData("teamName", "Canada")
                    .putData("imagePath", "CAN.png")
                    .putData("confederation", "CONCACAF")
                    .putData("ranking", 30)
                    .build(),
                ImmutableDatabaseRecord.builder()
                    .putData("groupId", "9b60ac29-905a-437d-918f-b98b74ce3e1b")
                    .putData("groupName", "Group B")
                    .putData("teamId", "d6e08336-f4c6-458d-9483-95785ea4238e")
                    .putData("teamName", "Bosnia and Herzegovina")
                    .putData("imagePath", "BIH.png")
                    .putData("confederation", "UEFA")
                    .putData("ranking", 61)
                    .build(),
                ImmutableDatabaseRecord.builder()
                    .putData("groupId", "9b60ac29-905a-437d-918f-b98b74ce3e1b")
                    .putData("groupName", "Group B")
                    .putData("teamId", "e48f7922-94c5-4b01-9bd5-5a8846c8e583")
                    .putData("teamName", "Qatar")
                    .putData("imagePath", "QAT.png")
                    .putData("confederation", "AFC")
                    .putData("ranking", 59)
                    .build(),
                ImmutableDatabaseRecord.builder()
                    .putData("groupId", "9b60ac29-905a-437d-918f-b98b74ce3e1b")
                    .putData("groupName", "Group B")
                    .putData("teamId", "fa4c8cee-676d-4016-b10b-74d64d80a337")
                    .putData("teamName", "Switzerland")
                    .putData("imagePath", "SUI.png")
                    .putData("confederation", "UEFA")
                    .putData("ranking", 14)
                    .build()
            ));

        when(queryService.retrieveRecords(any()))
            .thenReturn(existsResponse, groupTeamsResponse);

        // When
        final List<Group> groups = groupService.getGroups("2c299156-dd35-4791-8684-eca54a433042");

        // Then
        assertEquals(2, groups.size());
    }
}
