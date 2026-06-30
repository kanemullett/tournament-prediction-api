package com.kanemullett.service;

import java.util.List;

import static org.junit.Assert.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import org.junit.jupiter.api.Test;
import org.mockito.ArgumentCaptor;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;
import org.springframework.http.HttpStatus;
import org.springframework.web.server.ResponseStatusException;

import com.kanemullett.model.DatabaseRecord;
import com.kanemullett.model.ImmutableLeagueTemplate;
import com.kanemullett.model.LeagueTemplate;
import com.kanemullett.model.QueryCondition;
import com.kanemullett.model.QueryRequest;
import com.kanemullett.model.QueryResponse;
import com.kanemullett.model.Table;
import com.kanemullett.model.TournamentTemplateRecord;
import com.kanemullett.model.UpdateRequest;
import com.kanemullett.model.type.ConditionOperator;
import com.kanemullett.model.type.SqlOperator;

public class LeagueTemplateServiceTest {

    private final DatabaseQueryService queryService = mock(DatabaseQueryService.class);

    private final LeagueTemplateService service = new LeagueTemplateService(queryService);

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
    void shouldReturnLeagueTemplates() {
        // Given
        final QueryResponse<DatabaseRecord> queryResponse = mock(QueryResponse.class);
        when(queryResponse.getRecordCount())
            .thenReturn(2);
        when(queryResponse.getRecords())
            .thenReturn(List.of(EIGHT_BY_FOUR, SIX_BY_FOUR));

        when(queryService.retrieveRecords(any()))
            .thenReturn(queryResponse);

        // When
        final List<LeagueTemplate> leagueTemplates = service.getLeagueTemplates();

        // Then
        final ArgumentCaptor<QueryRequest<LeagueTemplate>> requestCaptor = ArgumentCaptor.forClass(QueryRequest.class);
        verify(queryService).retrieveRecords(requestCaptor.capture());
        final QueryRequest<LeagueTemplate> queryRequest = requestCaptor.getValue();
        
        final Table table = queryRequest.getTable();
        assertEquals("predictor", table.getSchema());
        assertEquals("league-templates", table.getTable());

        assertEquals(2, leagueTemplates.size());

        assertLeagueTemplate(EIGHT_BY_FOUR, leagueTemplates.get(0));
        assertLeagueTemplate(SIX_BY_FOUR, leagueTemplates.get(1));
    }

    @Test
    void shouldCreateLeagueTemplates() {
        // Given
        final List<LeagueTemplate> leagueTemplates = List.of(EIGHT_BY_FOUR, SIX_BY_FOUR);

        // When
        final List<LeagueTemplate> created = service.createLeagueTemplates(leagueTemplates);

        // Then
        final ArgumentCaptor<UpdateRequest<LeagueTemplate>> updateCaptor = ArgumentCaptor.forClass(UpdateRequest.class);
        verify(queryService).updateRecords(updateCaptor.capture());
        final UpdateRequest<LeagueTemplate> updateRequest = updateCaptor.getValue();

        assertEquals(SqlOperator.INSERT, updateRequest.getOperation());

        final Table table = updateRequest.getTable();
        assertEquals("predictor", table.getSchema());
        assertEquals("league-templates", table.getTable());

        assertEquals(2, updateRequest.getRecords().size());

        assertLeagueTemplate(EIGHT_BY_FOUR, updateRequest.getRecords().get(0));
        assertLeagueTemplate(SIX_BY_FOUR, updateRequest.getRecords().get(1));

        assertEquals(2, created.size());

        assertLeagueTemplate(EIGHT_BY_FOUR, created.get(0));
        assertLeagueTemplate(SIX_BY_FOUR, created.get(1));
    }

    @Test
    void shouldReturnLeagueTemplateById() {
        // Given
        final QueryResponse<DatabaseRecord> queryResponse = mock(QueryResponse.class);
        when(queryResponse.getRecordCount())
            .thenReturn(1);
        when(queryResponse.getRecords())
            .thenReturn(List.of(EIGHT_BY_FOUR));

        when(queryService.retrieveRecords(any()))
            .thenReturn(queryResponse);

        // When
        final LeagueTemplate leagueTemplate = service.getLeagueTemplateById("c08fd796-7fea-40d9-9a0a-cb3a49cce2e4");

        // Then
        final ArgumentCaptor<QueryRequest<LeagueTemplate>> queryCaptor = ArgumentCaptor.forClass(QueryRequest.class);
        verify(queryService).retrieveRecords(queryCaptor.capture());
        final QueryRequest<LeagueTemplate> queryRequest = queryCaptor.getValue();

        final Table table = queryRequest.getTable();
        assertEquals("predictor", table.getSchema());
        assertEquals("league-templates", table.getTable());

        assertEquals(1, queryRequest.getConditionGroup().getConditions().size());

        final QueryCondition condition = queryRequest.getConditionGroup().getConditions().get(0);
        assertEquals(List.of("id"), condition.getColumn().getParts());
        assertEquals(ConditionOperator.EQUAL, condition.getOperator());
        assertEquals("c08fd796-7fea-40d9-9a0a-cb3a49cce2e4", condition.getValue());

        assertLeagueTemplate(EIGHT_BY_FOUR, leagueTemplate);
    }

    @Test
    void shouldRaiseExceptionIfLeagueTemplateNotFound() {
        // Given
        final QueryResponse<DatabaseRecord> queryResponse = mock(QueryResponse.class);
        when(queryResponse.getRecordCount())
            .thenReturn(0);

        when(queryService.retrieveRecords(any()))
            .thenReturn(queryResponse);

        // When
        final ResponseStatusException rse = assertThrows(ResponseStatusException.class, () -> service.getLeagueTemplateById("c08fd796-7fea-40d9-9a0a-cb3a49cce2e4"));

        // Then
        assertEquals(HttpStatus.NOT_FOUND, rse.getStatusCode());
        assertEquals("No league templates found with a matching id.", rse.getReason());
    }

    @Test
    void shouldDeleteLeagueTemplateById() {
        // Given
        final QueryResponse<DatabaseRecord> queryResponse = mock(QueryResponse.class);
        when(queryResponse.getRecordCount())
            .thenReturn(0);

        when(queryService.retrieveRecords(any()))
            .thenReturn(queryResponse);

        // When
        service.deleteLeagueTemplateById("c08fd796-7fea-40d9-9a0a-cb3a49cce2e4");

        // Then
        final ArgumentCaptor<QueryRequest<TournamentTemplateRecord>> queryCaptor = ArgumentCaptor.forClass(QueryRequest.class);
        verify(queryService).retrieveRecords(queryCaptor.capture());
        final QueryRequest<TournamentTemplateRecord> queryRequest = queryCaptor.getValue();

        final Table queryTable = queryRequest.getTable();
        assertEquals("predictor", queryTable.getSchema());
        assertEquals("tournament-templates", queryTable.getTable());

        assertEquals(1, queryRequest.getConditionGroup().getConditions().size());

        final QueryCondition queryCondition = queryRequest.getConditionGroup().getConditions().get(0);
        assertEquals(List.of("leagueTemplateId"), queryCondition.getColumn().getParts());
        assertEquals(ConditionOperator.EQUAL, queryCondition.getOperator());
        assertEquals("c08fd796-7fea-40d9-9a0a-cb3a49cce2e4", queryCondition.getValue());

        final ArgumentCaptor<UpdateRequest<LeagueTemplate>> updateCaptor = ArgumentCaptor.forClass(UpdateRequest.class);
        verify(queryService).updateRecords(updateCaptor.capture());
        final UpdateRequest<LeagueTemplate> updateRequest = updateCaptor.getValue();

        assertEquals(SqlOperator.DELETE, updateRequest.getOperation());

        final Table table = updateRequest.getTable();
        assertEquals("predictor", table.getSchema());
        assertEquals("league-templates", table.getTable());

        assertEquals(1, updateRequest.getConditionGroup().getConditions().size());

        final QueryCondition condition = updateRequest.getConditionGroup().getConditions().get(0);
        assertEquals(List.of("id"), condition.getColumn().getParts());
        assertEquals(ConditionOperator.EQUAL, condition.getOperator());
        assertEquals("c08fd796-7fea-40d9-9a0a-cb3a49cce2e4", condition.getValue());
    }

    @Test
    void shouldNotDeleteLeagueTemplateIfUsedByTournamentTemplate() {
        // Given
        final QueryResponse<DatabaseRecord> queryResponse = mock(QueryResponse.class);
        when(queryResponse.getRecordCount())
            .thenReturn(1);

        when(queryService.retrieveRecords(any()))
            .thenReturn(queryResponse);

        // When
        final ResponseStatusException rse = assertThrows(ResponseStatusException.class, () -> service.deleteLeagueTemplateById("c08fd796-7fea-40d9-9a0a-cb3a49cce2e4"));

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
