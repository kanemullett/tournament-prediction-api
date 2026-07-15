package com.kanemullett.service;

import static org.junit.Assert.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.times;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

import java.util.List;

import org.junit.jupiter.api.Test;
import org.mockito.ArgumentCaptor;
import org.springframework.http.HttpStatus;
import org.springframework.web.server.ResponseStatusException;

import com.kanemullett.model.DatabaseRecord;
import com.kanemullett.model.GroupRecord;
import com.kanemullett.model.ImmutableKnockoutTemplate;
import com.kanemullett.model.ImmutableLeagueTemplate;
import com.kanemullett.model.ImmutableRoundTemplate;
import com.kanemullett.model.ImmutableTournament;
import com.kanemullett.model.ImmutableTournamentTemplate;
import com.kanemullett.model.ImmutableTournamentUpdate;
import com.kanemullett.model.MatchRecord;
import com.kanemullett.model.QueryCondition;
import com.kanemullett.model.QueryRequest;
import com.kanemullett.model.QueryResponse;
import com.kanemullett.model.Round;
import com.kanemullett.model.Table;
import com.kanemullett.model.TableDefinition;
import com.kanemullett.model.Tournament;
import com.kanemullett.model.TournamentTemplate;
import com.kanemullett.model.TournamentUpdate;
import com.kanemullett.model.UpdateRequest;
import com.kanemullett.model.type.ConditionOperator;
import com.kanemullett.model.type.Confederation;
import com.kanemullett.model.type.SqlOperator;

public class TournamentServiceTest {

    private final DatabaseQueryService queryService = mock(DatabaseQueryService.class);
    private final DatabaseTableService tableService = mock(DatabaseTableService.class);
    private final TournamentTemplateService tournamentTemplateService = mock(TournamentTemplateService.class);

    private final TournamentService service = new TournamentService(queryService, tableService, tournamentTemplateService);

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
    private static final TournamentTemplate TEMPLATE_ONE = ImmutableTournamentTemplate.builder()
        .id("ef0f7ca7-20c5-44ba-97be-f4e7d96cd114")
        .name("6x4 Group Stage, 16-Team Single-Leg Knockout")
        .league(ImmutableLeagueTemplate.builder()
            .id("641276e0-4ea6-4142-9775-63d94660ccac")
            .name("6x4 Group Stage")
            .groupCount(6)
            .teamsPerGroup(4)
            .homeAndAway(false)
            .build())
        .knockout(ImmutableKnockoutTemplate.builder()
            .id("e14d4ef4-b231-4d0d-9844-361c105ba5e0")
            .name("16-Team Single-Leg Knockout")
            .rounds(List.of(
                ImmutableRoundTemplate.builder()
                    .name("Round of 16")
                    .teamCount(16)
                    .roundOrder(1)
                    .twoLegs(false)
                    .extraTime(true)
                    .awayGoals(false)
                    .build(),
                ImmutableRoundTemplate.builder()
                    .name("Quarter-Finals")
                    .teamCount(8)
                    .roundOrder(2)
                    .twoLegs(false)
                    .extraTime(true)
                    .awayGoals(false)
                    .build(),
                ImmutableRoundTemplate.builder()
                    .name("Semi-Finals")
                    .teamCount(4)
                    .roundOrder(3)
                    .twoLegs(false)
                    .extraTime(true)
                    .awayGoals(false)
                    .build(),
                ImmutableRoundTemplate.builder()
                    .name("Final")
                    .teamCount(2)
                    .roundOrder(4)
                    .twoLegs(false)
                    .extraTime(true)
                    .awayGoals(false)
                    .build()
            ))
            .build())
        .build();
    private static final TournamentTemplate TEMPLATE_TWO = ImmutableTournamentTemplate.builder()
        .id("ccf688ac-a331-45de-b7cb-bf8b24f8fffb")
        .name("12x4 Group Stage, 32-Team Single-Leg Knockout")
        .league(ImmutableLeagueTemplate.builder()
            .id("641276e0-4ea6-4142-9775-63d94660ccac")
            .name("12x4 Group Stage")
            .groupCount(12)
            .teamsPerGroup(4)
            .homeAndAway(false)
            .build())
        .knockout(ImmutableKnockoutTemplate.builder()
            .id("e14d4ef4-b231-4d0d-9844-361c105ba5e0")
            .name("32-Team Single-Leg Knockout")
            .rounds(List.of(
                ImmutableRoundTemplate.builder()
                    .name("Round of 32")
                    .teamCount(32)
                    .roundOrder(1)
                    .twoLegs(false)
                    .extraTime(true)
                    .awayGoals(false)
                    .build(),
                ImmutableRoundTemplate.builder()
                    .name("Round of 16")
                    .teamCount(16)
                    .roundOrder(2)
                    .twoLegs(false)
                    .extraTime(true)
                    .awayGoals(false)
                    .build(),
                ImmutableRoundTemplate.builder()
                    .name("Quarter-Finals")
                    .teamCount(8)
                    .roundOrder(3)
                    .twoLegs(false)
                    .extraTime(true)
                    .awayGoals(false)
                    .build(),
                ImmutableRoundTemplate.builder()
                    .name("Semi-Finals")
                    .teamCount(4)
                    .roundOrder(4)
                    .twoLegs(false)
                    .extraTime(true)
                    .awayGoals(false)
                    .build(),
                ImmutableRoundTemplate.builder()
                    .name("Third-Place Playoff")
                    .teamCount(2)
                    .roundOrder(5)
                    .twoLegs(false)
                    .extraTime(true)
                    .awayGoals(false)
                    .build(),
                ImmutableRoundTemplate.builder()
                    .name("Final")
                    .teamCount(2)
                    .roundOrder(6)
                    .twoLegs(false)
                    .extraTime(true)
                    .awayGoals(false)
                    .build()
            ))
            .build())
        .build();
    private static final TournamentTemplate TEMPLATE_THREE = ImmutableTournamentTemplate.builder()
        .id("8742f36d-ee4f-4a8a-8620-adec8ea3e5a3")
        .name("20-Team League")
        .league(ImmutableLeagueTemplate.builder()
            .id("641276e0-4ea6-4142-9775-63d94660ccac")
            .name("20-Team League")
            .groupCount(20)
            .teamsPerGroup(1)
            .homeAndAway(true)
            .build())
        .build();

    @Test
    void shouldReturnTournaments() {
        // Given
        final QueryResponse<DatabaseRecord> queryResponse = mock(QueryResponse.class);
        when(queryResponse.getRecordCount())
            .thenReturn(2);
        when(queryResponse.getRecords())
            .thenReturn(List.of(EUROS, WORLD_CUP));

        when(queryService.retrieveRecords(any()))
            .thenReturn(queryResponse);

        // When
        final List<Tournament> tournaments = service.getTournaments();

        // Then
        final ArgumentCaptor<QueryRequest<Tournament>> requestCaptor = ArgumentCaptor.forClass(QueryRequest.class);
        verify(queryService).retrieveRecords(requestCaptor.capture());
        final QueryRequest<Tournament> queryRequest = requestCaptor.getValue();

        assertTable("predictor", "tournaments", queryRequest.getTable());

        assertEquals(2, tournaments.size());
        assertTournament(EUROS, tournaments.get(0));
        assertTournament(WORLD_CUP, tournaments.get(1));
    }

    @Test
    void shouldCreateTournaments() {
        // Given
        final List<Tournament> tournaments = List.of(EUROS, WORLD_CUP);

        when(tournamentTemplateService.getTournamentTemplates())
            .thenReturn(List.of(TEMPLATE_ONE, TEMPLATE_TWO, TEMPLATE_THREE));


        // When
        final List<Tournament> created = service.createTournaments(tournaments);

        // Then
        final ArgumentCaptor<TableDefinition> definitionCaptor = ArgumentCaptor.forClass(TableDefinition.class);
        verify(tableService, times(10)).createTable(definitionCaptor.capture());
        final List<TableDefinition> tableDefinitions = definitionCaptor.getAllValues();

        assertTableDefinition("predictor", "matches_c08fd796-7fea-40d9-9a0a-cb3a49cce2e4", tableDefinitions.get(0));
        assertTableDefinition("predictor", "results_c08fd796-7fea-40d9-9a0a-cb3a49cce2e4", tableDefinitions.get(1));
        assertTableDefinition("predictor", "groups_c08fd796-7fea-40d9-9a0a-cb3a49cce2e4", tableDefinitions.get(2));
        assertTableDefinition("predictor", "group-teams_c08fd796-7fea-40d9-9a0a-cb3a49cce2e4", tableDefinitions.get(3));
        assertTableDefinition("predictor", "rounds_c08fd796-7fea-40d9-9a0a-cb3a49cce2e4", tableDefinitions.get(4));
        assertTableDefinition("predictor", "matches_6ee28143-1286-4618-a8b9-ad86d348ead1", tableDefinitions.get(5));
        assertTableDefinition("predictor", "results_6ee28143-1286-4618-a8b9-ad86d348ead1", tableDefinitions.get(6));
        assertTableDefinition("predictor", "groups_6ee28143-1286-4618-a8b9-ad86d348ead1", tableDefinitions.get(7));
        assertTableDefinition("predictor", "group-teams_6ee28143-1286-4618-a8b9-ad86d348ead1", tableDefinitions.get(8));
        assertTableDefinition("predictor", "rounds_6ee28143-1286-4618-a8b9-ad86d348ead1", tableDefinitions.get(9));

        final ArgumentCaptor<UpdateRequest<?>> updateCaptor = ArgumentCaptor.forClass(UpdateRequest.class);
        verify(queryService, times(9)).updateRecords(updateCaptor.capture());
        final List<UpdateRequest<?>> updates = updateCaptor.getAllValues();

        final UpdateRequest<Tournament> tournamentInsert = (UpdateRequest<Tournament>) updates.get(0);
        assertInsertRequest("predictor", "tournaments", 2, tournamentInsert);
        assertTournament(EUROS, tournamentInsert.getRecords().get(0));
        assertTournament(WORLD_CUP, tournamentInsert.getRecords().get(1));

        final UpdateRequest<GroupRecord> groupInsert1 = (UpdateRequest<GroupRecord>) updates.get(1);
        assertInsertRequest("predictor", "groups_c08fd796-7fea-40d9-9a0a-cb3a49cce2e4", 6, groupInsert1);

        final UpdateRequest<MatchRecord> groupMatchInsert1 = (UpdateRequest<MatchRecord>) updates.get(2);
        assertInsertRequest("predictor", "matches_c08fd796-7fea-40d9-9a0a-cb3a49cce2e4", 36, groupMatchInsert1);

        final UpdateRequest<Round> roundInsert1 = (UpdateRequest<Round>) updates.get(3);
        assertInsertRequest("predictor", "rounds_c08fd796-7fea-40d9-9a0a-cb3a49cce2e4", 4, roundInsert1);

        final UpdateRequest<MatchRecord> roundMatchInsert1 = (UpdateRequest<MatchRecord>) updates.get(4);
        assertInsertRequest("predictor", "matches_c08fd796-7fea-40d9-9a0a-cb3a49cce2e4", 15, roundMatchInsert1);

        final UpdateRequest<GroupRecord> groupInsert2 = (UpdateRequest<GroupRecord>) updates.get(5);
        assertInsertRequest("predictor", "groups_6ee28143-1286-4618-a8b9-ad86d348ead1", 12, groupInsert2);

        final UpdateRequest<MatchRecord> groupMatchInsert2 = (UpdateRequest<MatchRecord>) updates.get(6);
        assertInsertRequest("predictor", "matches_6ee28143-1286-4618-a8b9-ad86d348ead1", 72, groupMatchInsert2);

        final UpdateRequest<Round> roundInsert2 = (UpdateRequest<Round>) updates.get(7);
        assertInsertRequest("predictor", "rounds_6ee28143-1286-4618-a8b9-ad86d348ead1", 6, roundInsert2);

        final UpdateRequest<MatchRecord> roundMatchInsert2 = (UpdateRequest<MatchRecord>) updates.get(8);
        assertInsertRequest("predictor", "matches_6ee28143-1286-4618-a8b9-ad86d348ead1", 32, roundMatchInsert2);

        assertTournament(EUROS, created.get(0));
        assertTournament(WORLD_CUP, created.get(1));
    }

    @Test
    void shouldUpdateTournaments() {
        // Given
        final List<TournamentUpdate> tournamentUpdates = List.of(
            ImmutableTournamentUpdate.builder()
                .id("c08fd796-7fea-40d9-9a0a-cb3a49cce2e4")
                .confederation(Confederation.UEFA)
                .build(),
            ImmutableTournamentUpdate.builder()
                .id("6ee28143-1286-4618-a8b9-ad86d348ead1")
                .year(2026)
                .build()
        );

        final QueryResponse<DatabaseRecord> queryResponse = mock(QueryResponse.class);
        when(queryResponse.getRecordCount())
            .thenReturn(2);
        when(queryResponse.getRecords())
            .thenReturn(List.of(EUROS, WORLD_CUP));

        when(queryService.retrieveRecords(any()))
            .thenReturn(queryResponse);

        // When
        final List<Tournament> updates = service.updateTournaments(tournamentUpdates);

        // Then
        final ArgumentCaptor<UpdateRequest<TournamentUpdate>> updateCaptor = ArgumentCaptor.forClass(UpdateRequest.class);
        verify(queryService).updateRecords(updateCaptor.capture());
        final UpdateRequest<TournamentUpdate> updateRequest = updateCaptor.getValue();

        assertEquals(SqlOperator.UPDATE, updateRequest.getOperation());
        assertTable("predictor", "tournaments", updateRequest.getTable());
        assertEquals(2, updateRequest.getRecords().size());

        final ArgumentCaptor<QueryRequest<Tournament>> requestCaptor = ArgumentCaptor.forClass(QueryRequest.class);
        verify(queryService).retrieveRecords(requestCaptor.capture());
        final QueryRequest<Tournament> queryRequest = requestCaptor.getValue();

        assertTable("predictor", "tournaments", queryRequest.getTable());
        assertEquals(1, queryRequest.getConditionGroup().getConditions().size());

        final QueryCondition queryCondition = queryRequest.getConditionGroup().getConditions().get(0);
        assertEquals(List.of("id"), queryCondition.getColumn().getParts());
        assertEquals(ConditionOperator.IN, queryCondition.getOperator());
        assertEquals(List.of("c08fd796-7fea-40d9-9a0a-cb3a49cce2e4", "6ee28143-1286-4618-a8b9-ad86d348ead1"), queryCondition.getValue());

        assertTournament(EUROS, updates.get(0));
        assertTournament(WORLD_CUP, updates.get(1));
    }

    @Test
    void shouldReturnTournamentById() {
        // Given
        final QueryResponse<DatabaseRecord> queryResponse = mock(QueryResponse.class);
        when(queryResponse.getRecordCount())
            .thenReturn(1);
        when(queryResponse.getRecords())
            .thenReturn(List.of(WORLD_CUP));

        when(queryService.retrieveRecords(any()))
            .thenReturn(queryResponse);

        // When
        final Tournament tournament = service.getTournamentById("6ee28143-1286-4618-a8b9-ad86d348ead1");

        // Then
        final ArgumentCaptor<QueryRequest<Tournament>> requestCaptor = ArgumentCaptor.forClass(QueryRequest.class);
        verify(queryService).retrieveRecords(requestCaptor.capture());
        final QueryRequest<Tournament> queryRequest = requestCaptor.getValue();

        assertTable("predictor", "tournaments", queryRequest.getTable());
        assertEquals(1, queryRequest.getConditionGroup().getConditions().size());

        final QueryCondition queryCondition = queryRequest.getConditionGroup().getConditions().get(0);
        assertEquals(List.of("id"), queryCondition.getColumn().getParts());
        assertEquals(ConditionOperator.EQUAL, queryCondition.getOperator());
        assertEquals("6ee28143-1286-4618-a8b9-ad86d348ead1", queryCondition.getValue());

        assertTournament(WORLD_CUP, tournament);
    }

    @Test
    void shouldRaiseExceptionIfTournamentNotFound() {
        // Given
        final QueryResponse<DatabaseRecord> queryResponse = mock(QueryResponse.class);
        when(queryResponse.getRecordCount())
            .thenReturn(0);
        when(queryResponse.getRecords())
            .thenReturn(List.of());

        when(queryService.retrieveRecords(any()))
            .thenReturn(queryResponse);

        // When
        final ResponseStatusException rse = assertThrows(ResponseStatusException.class, () -> service.getTournamentById("6ee28143-1286-4618-a8b9-ad86d348ead1"));

        // Then
        assertEquals(HttpStatus.NOT_FOUND, rse.getStatusCode());
        assertEquals("No tournaments found with a matching id.", rse.getReason());
    }

    @Test
    void shouldDeleteTournamentById() {
        // When
        service.deleteTournamentById("6ee28143-1286-4618-a8b9-ad86d348ead1");

        // Then
        final ArgumentCaptor<Table> tableCaptor = ArgumentCaptor.forClass(Table.class);
        verify(tableService, times(5)).deleteTable(tableCaptor.capture());
        final List<Table> tables = tableCaptor.getAllValues();

        assertTable("predictor", "matches_6ee28143-1286-4618-a8b9-ad86d348ead1", tables.get(0));
        assertTable("predictor", "results_6ee28143-1286-4618-a8b9-ad86d348ead1", tables.get(1));
        assertTable("predictor", "groups_6ee28143-1286-4618-a8b9-ad86d348ead1", tables.get(2));
        assertTable("predictor", "group-teams_6ee28143-1286-4618-a8b9-ad86d348ead1", tables.get(3));
        assertTable("predictor", "rounds_6ee28143-1286-4618-a8b9-ad86d348ead1", tables.get(4));

        final ArgumentCaptor<UpdateRequest<Tournament>> updateCaptor = ArgumentCaptor.forClass(UpdateRequest.class);
        verify(queryService).updateRecords(updateCaptor.capture());
        final UpdateRequest<Tournament> updateRequest = updateCaptor.getValue();

        assertEquals(SqlOperator.DELETE, updateRequest.getOperation());
        assertTable("predictor", "tournaments", updateRequest.getTable());
        assertEquals(1, updateRequest.getConditionGroup().getConditions().size());

        final QueryCondition updateCondition = updateRequest.getConditionGroup().getConditions().get(0);
        assertEquals(List.of("id"), updateCondition.getColumn().getParts());
        assertEquals(ConditionOperator.EQUAL, updateCondition.getOperator());
        assertEquals("6ee28143-1286-4618-a8b9-ad86d348ead1", updateCondition.getValue());
    }

    private static void assertTournament(Tournament expected, Tournament actual) {
        assertEquals(expected.getId(), actual.getId());
        assertEquals(expected.getYear(), expected.getYear());
        assertEquals(expected.getConfederation(), actual.getConfederation());
    }

    private static void assertTableDefinition(String expectedSchema, String expectedTable, TableDefinition tableDefinition) {
        assertEquals(expectedSchema, tableDefinition.getSchema());
        assertEquals(expectedTable, tableDefinition.getTable());
    }

    private static void assertInsertRequest(String expectedSchema, String expectedTable, int expectedRecordCount, UpdateRequest<?> actual) {
        assertEquals(SqlOperator.INSERT, actual.getOperation());
        assertEquals(expectedSchema, actual.getTable().getSchema());
        assertEquals(expectedTable, actual.getTable().getTable());
        assertEquals(expectedRecordCount, actual.getRecords().size());
    }

    private static void assertTable(String expectedSchema, String expectedTable, Table actual) {
        assertEquals(expectedSchema, actual.getSchema());
        assertEquals(expectedTable, actual.getTable());
    }
}
