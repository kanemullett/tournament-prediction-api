package com.kanemullett.service;

import java.util.List;
import java.util.Map;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

import org.junit.jupiter.api.Test;
import org.mockito.ArgumentCaptor;
import org.springframework.http.HttpStatus;
import org.springframework.web.server.ResponseStatusException;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

import com.kanemullett.model.Column;
import com.kanemullett.model.DatabaseRecord;
import com.kanemullett.model.ImmutableDatabaseRecord;
import com.kanemullett.model.ImmutableKnockoutTemplate;
import com.kanemullett.model.ImmutableLeagueTemplate;
import com.kanemullett.model.ImmutableQueryCondition;
import com.kanemullett.model.ImmutableRoundTemplate;
import com.kanemullett.model.ImmutableTournament;
import com.kanemullett.model.ImmutableTournamentTemplate;
import com.kanemullett.model.ImmutableTournamentTemplateRecord;
import com.kanemullett.model.Join;
import com.kanemullett.model.KnockoutTemplate;
import com.kanemullett.model.LeagueTemplate;
import com.kanemullett.model.QueryCondition;
import com.kanemullett.model.QueryConditionGroup;
import com.kanemullett.model.QueryRequest;
import com.kanemullett.model.QueryResponse;
import com.kanemullett.model.RoundTemplate;
import com.kanemullett.model.Table;
import com.kanemullett.model.TableJoin;
import com.kanemullett.model.TournamentTemplate;
import com.kanemullett.model.TournamentTemplateRecord;
import com.kanemullett.model.UpdateRequest;
import com.kanemullett.model.type.ConditionOperator;
import com.kanemullett.model.type.JoinType;
import com.kanemullett.model.type.SqlOperator;

public class TournamentTemplateServiceTest {

    private final DatabaseQueryService queryService = mock(DatabaseQueryService.class);

    private final TournamentTemplateService service = new TournamentTemplateService(queryService);

    private static final String KNOCKOUT_ONE_ROUNDS = """
        [
            {
                "name": "round1",
                "teamCount": 4,
                "roundOrder": 1,
                "twoLegs": true,
                "extraTime": true,
                "awayGoals": true
            },
            {
                "name": "round2",
                "teamCount": 2,
                "roundOrder": 2,
                "twoLegs": false,
                "extraTime": true,
                "awayGoals": false
            }
        ]  
        """;
    private static final String KNOCKOUT_TWO_ROUNDS = """
        [
            {
                "name": "round3",
                "teamCount": 4,
                "roundOrder": 1,
                "twoLegs": true,
                "extraTime": true,
                "awayGoals": true
            },
            {
                "name": "round4",
                "teamCount": 2,
                "roundOrder": 2,
                "twoLegs": false,
                "extraTime": true,
                "awayGoals": false
            }
        ]
        """;
    private static final DatabaseRecord RECORD_ONE = ImmutableDatabaseRecord.builder()
        .id("c08fd796-7fea-40d9-9a0a-cb3a49cce2e4")
        .data(Map.of(
            "tournamentTemplateName", "tournament1",
            "knockoutTemplateId", "80e9c164-637d-400f-a3cf-bf922073bc9b",
            "knockoutTemplateName", "knockout1",
            "rounds", KNOCKOUT_ONE_ROUNDS
        ))
        .build();
    private static final DatabaseRecord RECORD_TWO = ImmutableDatabaseRecord.builder()
        .id("6ee28143-1286-4618-a8b9-ad86d348ead1")
        .data(Map.of(
            "tournamentTemplateName", "tournament2",
            "leagueTemplateId", "0ca3adf1-f5a5-43e9-9c82-5619340739be",
            "leagueTemplateName", "league1",
            "groupCount", 8,
            "teamsPerGroup", 4,
            "homeAndAway", true
        ))
        .build();
    private static final DatabaseRecord RECORD_THREE = ImmutableDatabaseRecord.builder()
        .id("d15956ef-d199-40b1-b7d7-850a9add97e7")
        .data(Map.of(
            "tournamentTemplateName", "tournament3",
            "leagueTemplateId", "508c8b55-2e0c-415b-8078-2dcb2065c7ca",
            "leagueTemplateName", "league2",
            "groupCount", 6,
            "teamsPerGroup", 4,
            "homeAndAway", false,
            "knockoutTemplateId", "1a4d1cc8-f035-439a-b274-fe739b8fcfa5",
            "knockoutTemplateName", "knockout2",
            "rounds", KNOCKOUT_TWO_ROUNDS
        ))
        .build();
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
    void shouldReturnTournamentTemplatesWithChildTemplates() {
        // Given
        final QueryResponse<DatabaseRecord> queryResponse = mock(QueryResponse.class);
        when(queryResponse.getRecordCount())
            .thenReturn(3);
        when(queryResponse.getRecords())
            .thenReturn(List.of(RECORD_ONE, RECORD_TWO, RECORD_THREE));
        
        when(queryService.retrieveRecords(any()))
            .thenReturn(queryResponse);

        // When
        final List<TournamentTemplate> tournamentTemplates = service.getTournamentTemplates();

        // Then
        final ArgumentCaptor<QueryRequest> requestCaptor = ArgumentCaptor.forClass(QueryRequest.class);
        verify(queryService).retrieveRecords(requestCaptor.capture());
        final QueryRequest<DatabaseRecord> queryRequest = requestCaptor.getValue();

        assertQueryRequest(queryRequest);

        assertEquals(3, tournamentTemplates.size());

        assertTournamentTemplate(TOURNAMENT_TEMPLATE_ONE, tournamentTemplates.get(0));
        assertTournamentTemplate(TOURNAMENT_TEMPLATE_TWO, tournamentTemplates.get(1));
        assertTournamentTemplate(TOURNAMENT_TEMPLATE_THREE, tournamentTemplates.get(2));
    }

    @Test
    void shouldCreateTournamentTemplates() {
        // Given
        final List<TournamentTemplateRecord> templates = List.of(
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

        final QueryResponse<DatabaseRecord> queryResponse = mock(QueryResponse.class);
        when(queryResponse.getRecordCount())
            .thenReturn(3);
        when(queryResponse.getRecords())
            .thenReturn(List.of(RECORD_ONE, RECORD_TWO, RECORD_THREE));

        when(queryService.retrieveRecords(any()))
            .thenReturn(queryResponse);

        // When
        final List<TournamentTemplate> created = service.createTournamentTemplates(templates);

        // Then
        final ArgumentCaptor<UpdateRequest> updateCaptor = ArgumentCaptor.forClass(UpdateRequest.class);
        verify(queryService).updateRecords(updateCaptor.capture());
        final UpdateRequest<TournamentTemplateRecord> updateRequest = updateCaptor.getValue();

        assertEquals(SqlOperator.INSERT, updateRequest.getOperation());
        assertEquals("predictor", updateRequest.getTable().getSchema());
        assertEquals("tournament-templates", updateRequest.getTable().getTable());
        assertEquals(3, updateRequest.getRecords().size());

        final TournamentTemplateRecord record1 = updateRequest.getRecords().get(0);
        assertEquals("tournament1", record1.getName());
        assertEquals("80e9c164-637d-400f-a3cf-bf922073bc9b", record1.getKnockoutTemplateId());

        final TournamentTemplateRecord record2 = updateRequest.getRecords().get(1);
        assertEquals("tournament2", record2.getName());
        assertEquals("0ca3adf1-f5a5-43e9-9c82-5619340739be", record2.getLeagueTemplateId());

        final TournamentTemplateRecord record3 = updateRequest.getRecords().get(2);
        assertEquals("tournament3", record3.getName());
        assertEquals("508c8b55-2e0c-415b-8078-2dcb2065c7ca", record3.getLeagueTemplateId());
        assertEquals("1a4d1cc8-f035-439a-b274-fe739b8fcfa5", record3.getKnockoutTemplateId());

        final ArgumentCaptor<QueryRequest> requestCaptor = ArgumentCaptor.forClass(QueryRequest.class);
        verify(queryService).retrieveRecords(requestCaptor.capture());
        final QueryRequest<DatabaseRecord> queryRequest = requestCaptor.getValue();

        final QueryConditionGroup expectedConditionGroup = QueryConditionGroup.of(
            ImmutableQueryCondition.builder()
                .column(Column.of("tt", "id"))
                .operator(ConditionOperator.IN)
                .value(templates.stream()
                    .map(TournamentTemplateRecord::getId)
                    .toList())
                .build()
        );
        assertQueryRequest(queryRequest, expectedConditionGroup);

        assertEquals(3, created.size());

        assertTournamentTemplate(TOURNAMENT_TEMPLATE_ONE, created.get(0));
        assertTournamentTemplate(TOURNAMENT_TEMPLATE_TWO, created.get(1));
        assertTournamentTemplate(TOURNAMENT_TEMPLATE_THREE, created.get(2));
    }

    @Test
    void shouldReturnTournamentTemplateById() {
        // Given
        final QueryResponse<DatabaseRecord> queryResponse = mock(QueryResponse.class);
        when(queryResponse.getRecordCount())
            .thenReturn(1);
        when(queryResponse.getRecords())
            .thenReturn(List.of(RECORD_THREE));
        
        when(queryService.retrieveRecords(any()))
            .thenReturn(queryResponse);

        // When
        final TournamentTemplate tournamentTemplate = service.getTournamentTemplateById("d15956ef-d199-40b1-b7d7-850a9add97e7");

        // Then
        final ArgumentCaptor<QueryRequest> requestCaptor = ArgumentCaptor.forClass(QueryRequest.class);
        verify(queryService).retrieveRecords(requestCaptor.capture());
        final QueryRequest<DatabaseRecord> queryRequest = requestCaptor.getValue();

        final QueryConditionGroup expectedConditionGroup = QueryConditionGroup.of(
            QueryCondition.of(
                Column.of("tt", "id"),
                "d15956ef-d199-40b1-b7d7-850a9add97e7"
            )
        );
        assertQueryRequest(queryRequest, expectedConditionGroup);

        assertTournamentTemplate(TOURNAMENT_TEMPLATE_THREE, tournamentTemplate);
    }

    @Test
    void shouldRaiseExceptionIfTournamentTemplateNotFound() {
        // Given
        final QueryResponse<DatabaseRecord> queryResponse = mock(QueryResponse.class);
        when(queryResponse.getRecordCount())
            .thenReturn(0);
        when(queryResponse.getRecords())
            .thenReturn(List.of());

        when(queryService.retrieveRecords(any()))
            .thenReturn(queryResponse);

        // When
        final ResponseStatusException rse = assertThrows(ResponseStatusException.class, () -> service.getTournamentTemplateById("c08fd796-7fea-40d9-9a0a-cb3a49cce2e4"));

        // Then
        assertEquals(HttpStatus.NOT_FOUND, rse.getStatusCode());
        assertEquals("No tournament templates found with a matching id.", rse.getReason());
    }

    @Test
    void shouldDeleteTournamentTemplateById() {
        // Given
        final QueryResponse<DatabaseRecord> queryResponse = mock(QueryResponse.class);
        when(queryResponse.getRecordCount())
            .thenReturn(0);
        when(queryResponse.getRecords())
            .thenReturn(List.of());

        when(queryService.retrieveRecords(any()))
            .thenReturn(queryResponse);

        // When
        service.deleteTournamentTemplateById("c08fd796-7fea-40d9-9a0a-cb3a49cce2e4");

        // Then
        final ArgumentCaptor<UpdateRequest> updateCaptor = ArgumentCaptor.forClass(UpdateRequest.class);
        verify(queryService).updateRecords(updateCaptor.capture());
        final UpdateRequest<TournamentTemplateRecord> updateRequest = updateCaptor.getValue();

        assertEquals(SqlOperator.DELETE, updateRequest.getOperation());
        assertEquals("predictor", updateRequest.getTable().getSchema());
        assertEquals("tournament-templates", updateRequest.getTable().getTable());

        assertEquals(1, updateRequest.getConditionGroup().getConditions().size());

        final QueryCondition queryCondition = updateRequest.getConditionGroup().getConditions().get(0);
        assertEquals(List.of("id"), queryCondition.getColumn().getParts());
        assertEquals(ConditionOperator.EQUAL, queryCondition.getOperator());
        assertEquals("c08fd796-7fea-40d9-9a0a-cb3a49cce2e4", queryCondition.getValue());
    }

    @Test
    void shouldNotDeleteTournamentTemplateIfUsedByTournament() {
        // Given
        final QueryResponse<DatabaseRecord> queryResponse = mock(QueryResponse.class);
        when(queryResponse.getRecordCount())
            .thenReturn(1);
        when(queryResponse.getRecords())
            .thenReturn(List.of(
                ImmutableTournament.builder()
                    .name("tournament")
                    .year(2026)
                    .templateId("c08fd796-7fea-40d9-9a0a-cb3a49cce2e4")
                    .build()
            ));

        when(queryService.retrieveRecords(any()))
            .thenReturn(queryResponse);

        // When
        final ResponseStatusException rse = assertThrows(ResponseStatusException.class, () -> service.deleteTournamentTemplateById("c08fd796-7fea-40d9-9a0a-cb3a49cce2e4"));

        // Then
        assertEquals(HttpStatus.CONFLICT, rse.getStatusCode());
        assertEquals("Cannot delete tournament template as it is part of an existing tournament.", rse.getReason());
    }

    private static void assertQueryRequest(QueryRequest<DatabaseRecord> actual) {
        final List<Column> columns = actual.getColumns();
        assertEquals(10, columns.size());

        final Column column1 = columns.get(0);
        assertEquals(List.of("tt", "id"), column1.getParts());

        final Column column2 = columns.get(1);
        assertEquals(List.of("tt", "name"), column2.getParts());
        assertEquals("tournamentTemplateName", column2.getAlias());

        final Column column3 = columns.get(2);
        assertEquals(List.of("tt", "leagueTemplateId"), column3.getParts());

        final Column column4 = columns.get(3);
        assertEquals(List.of("lt", "name"), column4.getParts());
        assertEquals("leagueTemplateName", column4.getAlias());

        final Column column5 = columns.get(4);
        assertEquals(List.of("lt", "groupCount"), column5.getParts());

        final Column column6 = columns.get(5);
        assertEquals(List.of("lt", "teamsPerGroup"), column6.getParts());

        final Column column7 = columns.get(6);
        assertEquals(List.of("lt", "homeAndAway"), column7.getParts());

        final Column column8 = columns.get(7);
        assertEquals(List.of("tt", "knockoutTemplateId"), column8.getParts());

        final Column column9 = columns.get(8);
        assertEquals(List.of("kt", "name"), column9.getParts());
        assertEquals("knockoutTemplateName", column9.getAlias());

        final Column column10 = columns.get(9);
        assertEquals(List.of("kt", "rounds"), column10.getParts());

        assertEquals("predictor", actual.getTable().getSchema());
        assertEquals("tournament-templates", actual.getTable().getTable());

        final List<Join> joins = actual.getJoins();
        assertEquals(2, joins.size());

        final TableJoin join1 = (TableJoin) joins.get(0);
        assertEquals(JoinType.LEFT, join1.getJoinType());

        final Table join1Table = join1.getTable();
        assertEquals("predictor", join1Table.getSchema());
        assertEquals("league-templates", join1Table.getTable());
        assertEquals("lt", join1Table.getAlias());

        final QueryCondition join1Condition = join1.getJoinCondition();
        assertEquals(List.of("tt", "leagueTemplateId"), join1Condition.getColumn().getParts());
        assertEquals(ConditionOperator.EQUAL, join1Condition.getOperator());
        assertEquals(List.of("lt", "id"), ((Column) join1Condition.getValue()).getParts());

        final TableJoin join2 = (TableJoin) joins.get(1);
        assertEquals(JoinType.LEFT, join2.getJoinType());

        final Table join2Table = join2.getTable();
        assertEquals("predictor", join2Table.getSchema());
        assertEquals("knockout-templates", join2Table.getTable());
        assertEquals("kt", join2Table.getAlias());

        final QueryCondition join2Condition = join2.getJoinCondition();
        assertEquals(List.of("tt", "knockoutTemplateId"), join2Condition.getColumn().getParts());
        assertEquals(ConditionOperator.EQUAL, join2Condition.getOperator());
        assertEquals(List.of("kt", "id"), ((Column) join2Condition.getValue()).getParts());
    }

    private static void assertQueryRequest(QueryRequest<DatabaseRecord> actual, QueryConditionGroup expectedConditionGroup) {
        assertQueryRequest(actual);
        assertEquals(expectedConditionGroup.getConditions().get(0).getColumn().getParts(), actual.getConditionGroup().getConditions().get(0).getColumn().getParts());
        assertEquals(expectedConditionGroup.getConditions().get(0).getOperator(), actual.getConditionGroup().getConditions().get(0).getOperator());
        assertEquals(expectedConditionGroup.getConditions().get(0).getValue(), actual.getConditionGroup().getConditions().get(0).getValue());
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
