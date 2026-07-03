package com.kanemullett.service;

import static org.junit.Assert.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

import java.util.List;

import org.junit.jupiter.api.Test;
import org.mockito.ArgumentCaptor;
import org.springframework.http.HttpStatus;
import org.springframework.web.server.ResponseStatusException;

import com.kanemullett.model.DatabaseRecord;
import com.kanemullett.model.ImmutableKnockoutTemplate;
import com.kanemullett.model.ImmutableRoundTemplate;
import com.kanemullett.model.KnockoutTemplate;
import com.kanemullett.model.QueryCondition;
import com.kanemullett.model.QueryRequest;
import com.kanemullett.model.QueryResponse;
import com.kanemullett.model.RoundTemplate;
import com.kanemullett.model.Table;
import com.kanemullett.model.TournamentTemplateRecord;
import com.kanemullett.model.UpdateRequest;
import com.kanemullett.model.type.ConditionOperator;
import com.kanemullett.model.type.SqlOperator;

public class KnockoutTemplateServiceTest {

    private final DatabaseQueryService queryService = mock(DatabaseQueryService.class);

    private final KnockoutTemplateService service = new KnockoutTemplateService(queryService);

    private static final RoundTemplate SIXTEEN_ROUND_ONE = ImmutableRoundTemplate.builder()
        .name("Round of 16")
        .teamCount(16)
        .roundOrder(1)
        .twoLegs(false)
        .extraTime(true)
        .awayGoals(false)
        .build();
    private static final RoundTemplate SIXTEEN_ROUND_TWO = ImmutableRoundTemplate.builder()
        .name("Quarter-Finals")
        .teamCount(8)
        .roundOrder(2)
        .twoLegs(false)
        .extraTime(true)
        .awayGoals(false)
        .build();
    private static final RoundTemplate SIXTEEN_ROUND_THREE = ImmutableRoundTemplate.builder()
        .name("Semi-Finals")
        .teamCount(4)
        .roundOrder(3)
        .twoLegs(false)
        .extraTime(true)
        .awayGoals(false)
        .build();
    private static final RoundTemplate SIXTEEN_ROUND_FOUR = ImmutableRoundTemplate.builder()
        .name("Third-Place Play-Off")
        .teamCount(2)
        .roundOrder(4)
        .twoLegs(false)
        .extraTime(true)
        .awayGoals(false)
        .build();
    private static final RoundTemplate SIXTEEN_ROUND_FIVE = ImmutableRoundTemplate.builder()
        .name("Final")
        .teamCount(2)
        .roundOrder(5)
        .twoLegs(false)
        .extraTime(true)
        .awayGoals(false)
        .build();
    private static final RoundTemplate EIGHT_ROUND_ONE = ImmutableRoundTemplate.builder()
        .name("Quarter-Finals")
        .teamCount(8)
        .roundOrder(1)
        .twoLegs(true)
        .extraTime(true)
        .awayGoals(true)
        .build();
    private static final RoundTemplate EIGHT_ROUND_TWO = ImmutableRoundTemplate.builder()
        .name("Semi-Finals")
        .teamCount(4)
        .roundOrder(2)
        .twoLegs(true)
        .extraTime(true)
        .awayGoals(true)
        .build();
    private static final RoundTemplate EIGHT_ROUND_THREE = ImmutableRoundTemplate.builder()
        .name("Final")
        .teamCount(2)
        .roundOrder(3)
        .twoLegs(false)
        .extraTime(true)
        .awayGoals(false)
        .build();

    private static final KnockoutTemplate SIXTEEN_TEMPLATE = ImmutableKnockoutTemplate.builder()
        .id("c08fd796-7fea-40d9-9a0a-cb3a49cce2e4")
        .name("16-Team Single-Leg")
        .rounds(List.of(
            SIXTEEN_ROUND_ONE,
            SIXTEEN_ROUND_TWO,
            SIXTEEN_ROUND_THREE,
            SIXTEEN_ROUND_FOUR,
            SIXTEEN_ROUND_FIVE
        ))
        .build();
    private static final KnockoutTemplate EIGHT_TEMPLATE = ImmutableKnockoutTemplate.builder()
        .id("6ee28143-1286-4618-a8b9-ad86d348ead1")
        .name("8-Team Double-Leg Away Goals")
        .rounds(List.of(
            EIGHT_ROUND_ONE,
            EIGHT_ROUND_TWO,
            EIGHT_ROUND_THREE
        ))
        .build();

    @Test
    void shouldReturnKnockoutTemplates() {
        // Given
        final QueryResponse<DatabaseRecord> queryResponse = mock(QueryResponse.class);
        when(queryResponse.getRecordCount())
            .thenReturn(2);
        when(queryResponse.getRecords())
            .thenReturn(List.of(SIXTEEN_TEMPLATE, EIGHT_TEMPLATE));

        when(queryService.retrieveRecords(any()))
            .thenReturn(queryResponse);

        // When
        final List<KnockoutTemplate> knockoutTemplates = service.getKnockoutTemplates();

        // Then
        final ArgumentCaptor<QueryRequest<KnockoutTemplate>> requestCaptor = ArgumentCaptor.forClass(QueryRequest.class);
        verify(queryService).retrieveRecords(requestCaptor.capture());
        final QueryRequest<KnockoutTemplate> queryRequest = requestCaptor.getValue();
        
        final Table table = queryRequest.getTable();
        assertEquals("predictor", table.getSchema());
        assertEquals("knockout-templates", table.getTable());

        assertEquals(2, knockoutTemplates.size());

        assertKnockoutTemplate(SIXTEEN_TEMPLATE, knockoutTemplates.get(0));
        assertRoundTemplate(SIXTEEN_ROUND_ONE, knockoutTemplates.get(0).getRounds().get(0));
        assertRoundTemplate(SIXTEEN_ROUND_TWO, knockoutTemplates.get(0).getRounds().get(1));
        assertRoundTemplate(SIXTEEN_ROUND_THREE, knockoutTemplates.get(0).getRounds().get(2));
        assertRoundTemplate(SIXTEEN_ROUND_FOUR, knockoutTemplates.get(0).getRounds().get(3));
        assertRoundTemplate(SIXTEEN_ROUND_FIVE, knockoutTemplates.get(0).getRounds().get(4));

        assertKnockoutTemplate(EIGHT_TEMPLATE, knockoutTemplates.get(1));
        assertRoundTemplate(EIGHT_ROUND_ONE, knockoutTemplates.get(1).getRounds().get(0));
        assertRoundTemplate(EIGHT_ROUND_TWO, knockoutTemplates.get(1).getRounds().get(1));
        assertRoundTemplate(EIGHT_ROUND_THREE, knockoutTemplates.get(1).getRounds().get(2));
    }

    @Test
    void shouldCreateKnockoutTemplates() {
        // Given
        final List<KnockoutTemplate> knockoutTemplates = List.of(SIXTEEN_TEMPLATE, EIGHT_TEMPLATE);

        // When
        final List<KnockoutTemplate> created = service.createKnockoutTemplates(knockoutTemplates);

        // Then
        final ArgumentCaptor<UpdateRequest<KnockoutTemplate>> updateCaptor = ArgumentCaptor.forClass(UpdateRequest.class);
        verify(queryService).updateRecords(updateCaptor.capture());
        final UpdateRequest<KnockoutTemplate> updateRequest = updateCaptor.getValue();

        assertEquals(SqlOperator.INSERT, updateRequest.getOperation());

        final Table table = updateRequest.getTable();
        assertEquals("predictor", table.getSchema());
        assertEquals("knockout-templates", table.getTable());

        assertKnockoutTemplate(SIXTEEN_TEMPLATE, updateRequest.getRecords().get(0));

        assertEquals(5, updateRequest.getRecords().get(0).getRounds().size());
        assertRoundTemplate(SIXTEEN_ROUND_ONE, updateRequest.getRecords().get(0).getRounds().get(0));
        assertRoundTemplate(SIXTEEN_ROUND_TWO, updateRequest.getRecords().get(0).getRounds().get(1));
        assertRoundTemplate(SIXTEEN_ROUND_THREE, updateRequest.getRecords().get(0).getRounds().get(2));
        assertRoundTemplate(SIXTEEN_ROUND_FOUR, updateRequest.getRecords().get(0).getRounds().get(3));
        assertRoundTemplate(SIXTEEN_ROUND_FIVE, updateRequest.getRecords().get(0).getRounds().get(4));

        assertKnockoutTemplate(EIGHT_TEMPLATE, updateRequest.getRecords().get(1));

        assertEquals(3, updateRequest.getRecords().get(1).getRounds().size());
        assertRoundTemplate(EIGHT_ROUND_ONE, updateRequest.getRecords().get(1).getRounds().get(0));
        assertRoundTemplate(EIGHT_ROUND_TWO, updateRequest.getRecords().get(1).getRounds().get(1));
        assertRoundTemplate(EIGHT_ROUND_THREE, updateRequest.getRecords().get(1).getRounds().get(2));

        assertEquals(2, created.size());

        assertKnockoutTemplate(SIXTEEN_TEMPLATE, created.get(0));

        assertEquals(5, created.get(0).getRounds().size());
        assertRoundTemplate(SIXTEEN_ROUND_ONE, created.get(0).getRounds().get(0));
        assertRoundTemplate(SIXTEEN_ROUND_TWO, created.get(0).getRounds().get(1));
        assertRoundTemplate(SIXTEEN_ROUND_THREE, created.get(0).getRounds().get(2));
        assertRoundTemplate(SIXTEEN_ROUND_FOUR, created.get(0).getRounds().get(3));
        assertRoundTemplate(SIXTEEN_ROUND_FIVE, created.get(0).getRounds().get(4));

        assertKnockoutTemplate(EIGHT_TEMPLATE, created.get(1));

        assertEquals(3, created.get(1).getRounds().size());
        assertRoundTemplate(EIGHT_ROUND_ONE, created.get(1).getRounds().get(0));
        assertRoundTemplate(EIGHT_ROUND_TWO, created.get(1).getRounds().get(1));
        assertRoundTemplate(EIGHT_ROUND_THREE, created.get(1).getRounds().get(2));
    }

    @Test
    void shouldReturnKnockoutTemplateById() {
        // Given
        final QueryResponse<DatabaseRecord> queryResponse = mock(QueryResponse.class);
        when(queryResponse.getRecordCount())
            .thenReturn(1);
        when(queryResponse.getRecords())
            .thenReturn(List.of(SIXTEEN_TEMPLATE));

        when(queryService.retrieveRecords(any()))
            .thenReturn(queryResponse);

        // When
        final KnockoutTemplate knockoutTemplate = service.getKnockoutTemplateById("c08fd796-7fea-40d9-9a0a-cb3a49cce2e4");

        // Then
        final ArgumentCaptor<QueryRequest<KnockoutTemplate>> requestCaptor = ArgumentCaptor.forClass(QueryRequest.class);
        verify(queryService).retrieveRecords(requestCaptor.capture());
        final QueryRequest<KnockoutTemplate> queryRequest = requestCaptor.getValue();

        final Table table = queryRequest.getTable();
        assertEquals("predictor", table.getSchema());
        assertEquals("knockout-templates", table.getTable());

        final QueryCondition condition = queryRequest.getConditionGroup().getConditions().get(0);
        assertEquals(List.of("id"), condition.getColumn().getParts());
        assertEquals(ConditionOperator.EQUAL, condition.getOperator());
        assertEquals("c08fd796-7fea-40d9-9a0a-cb3a49cce2e4", condition.getValue());

        assertKnockoutTemplate(SIXTEEN_TEMPLATE, knockoutTemplate);

        assertEquals(5, knockoutTemplate.getRounds().size());
        assertRoundTemplate(SIXTEEN_ROUND_ONE, knockoutTemplate.getRounds().get(0));
        assertRoundTemplate(SIXTEEN_ROUND_TWO, knockoutTemplate.getRounds().get(1));
        assertRoundTemplate(SIXTEEN_ROUND_THREE, knockoutTemplate.getRounds().get(2));
        assertRoundTemplate(SIXTEEN_ROUND_FOUR, knockoutTemplate.getRounds().get(3));
        assertRoundTemplate(SIXTEEN_ROUND_FIVE, knockoutTemplate.getRounds().get(4));
    }

    @Test
    void shouldRaiseExceptionIfKnockoutTemplateNotFound() {
        // Given
        final QueryResponse<DatabaseRecord> queryResponse = mock(QueryResponse.class);
        when(queryResponse.getRecordCount())
            .thenReturn(0);

        when(queryService.retrieveRecords(any()))
            .thenReturn(queryResponse);

        // When
        final ResponseStatusException rse = assertThrows(ResponseStatusException.class, () -> service.getKnockoutTemplateById("c08fd796-7fea-40d9-9a0a-cb3a49cce2e4"));

        // Then
        assertEquals(HttpStatus.NOT_FOUND, rse.getStatusCode());
        assertEquals("No knockout templates found with a matching id.", rse.getReason());
    }

    @Test
    void shouldDeleteKnockoutTemplateById() {
        // Given
        final QueryResponse<DatabaseRecord> queryResponse = mock(QueryResponse.class);
        when(queryResponse.getRecordCount())
            .thenReturn(0);

        when(queryService.retrieveRecords(any()))
            .thenReturn(queryResponse);

        // When
        service.deleteKnockoutTemplateById("c08fd796-7fea-40d9-9a0a-cb3a49cce2e4");

        // Then
        final ArgumentCaptor<QueryRequest<TournamentTemplateRecord>> requestCaptor = ArgumentCaptor.forClass(QueryRequest.class);
        verify(queryService).retrieveRecords(requestCaptor.capture());
        final QueryRequest<TournamentTemplateRecord> queryRequest = requestCaptor.getValue();

        final Table table = queryRequest.getTable();
        assertEquals("predictor", table.getSchema());
        assertEquals("tournament-templates", table.getTable());

        final QueryCondition condition = queryRequest.getConditionGroup().getConditions().get(0);
        assertEquals(List.of("knockoutTemplateId"), condition.getColumn().getParts());
        assertEquals(ConditionOperator.EQUAL, condition.getOperator());
        assertEquals("c08fd796-7fea-40d9-9a0a-cb3a49cce2e4", condition.getValue());

        final ArgumentCaptor<UpdateRequest<KnockoutTemplate>> updateCaptor = ArgumentCaptor.forClass(UpdateRequest.class);
        verify(queryService).updateRecords(updateCaptor.capture());
        final UpdateRequest<KnockoutTemplate> updateRequest = updateCaptor.getValue();

        assertEquals(SqlOperator.DELETE, updateRequest.getOperation());

        final Table updateTable = updateRequest.getTable();
        assertEquals("predictor", updateTable.getSchema());
        assertEquals("knockout-templates", updateTable.getTable());

        final QueryCondition updateCondition = updateRequest.getConditionGroup().getConditions().get(0);
        assertEquals(List.of("id"), updateCondition.getColumn().getParts());
        assertEquals(ConditionOperator.EQUAL, updateCondition.getOperator());
        assertEquals("c08fd796-7fea-40d9-9a0a-cb3a49cce2e4", updateCondition.getValue());
    }

    @Test
    void shouldNotDeleteKnockoutTemplateIfUsedByTournamentTemplate() {
        // Given
        final QueryResponse<DatabaseRecord> queryResponse = mock(QueryResponse.class);
        when(queryResponse.getRecordCount())
            .thenReturn(1);
        when(queryResponse.getRecords())
            .thenReturn(List.of(SIXTEEN_TEMPLATE));

        when(queryService.retrieveRecords(any()))
            .thenReturn(queryResponse);

        // When
        final ResponseStatusException rse = assertThrows(ResponseStatusException.class, () -> service.deleteKnockoutTemplateById("c08fd796-7fea-40d9-9a0a-cb3a49cce2e4"));

        // Then
        assertEquals(HttpStatus.CONFLICT, rse.getStatusCode());
        assertEquals("Cannot delete knockout template as it is part of an existing tournament template.", rse.getReason());
    }

    private static void assertKnockoutTemplate(KnockoutTemplate expected, KnockoutTemplate actual) {
        assertEquals(expected.getId(), actual.getId());
        assertEquals(expected.getName(), actual.getName());
        assertEquals(expected.getRounds().size(), actual.getRounds().size());
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
