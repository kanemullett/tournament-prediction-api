package com.kanemullett.service;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNull;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.times;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

import java.sql.Timestamp;
import java.time.LocalDateTime;
import java.util.List;

import org.junit.jupiter.api.Test;
import org.mockito.ArgumentCaptor;
import org.springframework.http.HttpStatus;
import org.springframework.web.server.ResponseStatusException;

import com.kanemullett.function.MatchBuilderFunction;
import com.kanemullett.model.Column;
import com.kanemullett.model.DatabaseRecord;
import com.kanemullett.model.Group;
import com.kanemullett.model.ImmutableDatabaseRecord;
import com.kanemullett.model.ImmutableGroup;
import com.kanemullett.model.ImmutableMatch;
import com.kanemullett.model.ImmutableMatchUpdate;
import com.kanemullett.model.ImmutableQueryCondition;
import com.kanemullett.model.ImmutableRound;
import com.kanemullett.model.ImmutableTeam;
import com.kanemullett.model.Match;
import com.kanemullett.model.MatchUpdate;
import com.kanemullett.model.OrderBy;
import com.kanemullett.model.QueryCondition;
import com.kanemullett.model.QueryConditionGroup;
import com.kanemullett.model.QueryRequest;
import com.kanemullett.model.QueryResponse;
import com.kanemullett.model.Round;
import com.kanemullett.model.Table;
import com.kanemullett.model.TableJoin;
import com.kanemullett.model.Team;
import com.kanemullett.model.UpdateRequest;
import com.kanemullett.model.type.ConditionOperator;
import com.kanemullett.model.type.Confederation;
import com.kanemullett.model.type.JoinType;
import com.kanemullett.model.type.OrderDirection;
import com.kanemullett.model.type.SqlOperator;

import jakarta.annotation.Nullable;

public class MatchServiceTest {

    private final DatabaseQueryService queryService = mock(DatabaseQueryService.class);
    private final TournamentService tournamentService = mock(TournamentService.class);
    private final GroupService groupService = mock(GroupService.class);
    private final RoundService roundService = mock(RoundService.class);
    private final MatchBuilderFunction matchBuilderFunction = mock(MatchBuilderFunction.class);

    private final MatchService matchService = new MatchService(queryService, tournamentService, groupService, roundService, matchBuilderFunction);

    private static final DatabaseRecord BIH_NGA_RECORD = ImmutableDatabaseRecord.builder()
        .putData("matchId", "8efaf853-980e-4607-9b45-d854460ec5e0")
        .putData("homeId", "bbec1707-7ea3-49cb-9791-7a1358a2b894")
        .putData("homeName", "Bosnia & Herzegovina")
        .putData("homeImagePath", "BIH.png")
        .putData("homeConfederation", "UEFA")
        .putData("awayId", "463de8d9-8520-4fa4-b30c-5aac0f3b363c")
        .putData("awayName", "Nigeria")
        .putData("awayImagePath", "NGA.png")
        .putData("awayConfederation", "CAF")
        .putData("kickoff", Timestamp.valueOf(LocalDateTime.of(2025, 6, 1, 14, 0, 0)))
        .putData("groupMatchDay", 1)
        .putData("groupId", "4c2c8046-0007-48db-a76a-865f9048d9de")
        .putData("homeGoals", 2)
        .putData("awayGoals", 1)
        .putData("afterExtraTime", false)
        .putData("afterPenalties", false)
        .putData("groupName", "Group A")
        .build();
    private static final DatabaseRecord ARG_IRI_RECORD = ImmutableDatabaseRecord.builder()
        .putData("matchId", "d8b3685b-3749-438d-9d85-da29c97ebaef")
        .putData("homeId", "977f3f69-0149-43fd-adb0-7c524aea37aa")
        .putData("homeName", "Argentina")
        .putData("homeImagePath", "ARG.png")
        .putData("homeConfederation", "CONMEBOL")
        .putData("awayId", "58adea3b-bdda-496a-be74-64501e34622b")
        .putData("awayName", "Iran")
        .putData("awayImagePath", "IRI.png")
        .putData("awayConfederation", "AFC")
        .putData("kickoff", Timestamp.valueOf(LocalDateTime.of(2025, 6, 1, 17, 30, 0)))
        .putData("roundId", "322ab9d0-ae46-49ac-89b3-c789a0d9d889")
        .putData("homeGoals", 2)
        .putData("awayGoals", 1)
        .putData("afterExtraTime", false)
        .putData("afterPenalties", false)
        .putData("roundName", "Round of 16")
        .putData("teamCount", 16)
        .putData("roundOrder", 1)
        .putData("twoLegs", false)
        .putData("extraTime", true)
        .putData("awayGoalsDecider", false)
        .build();

    private static final Match BIH_NGA_MATCH = ImmutableMatch.builder()
        .id("8efaf853-980e-4607-9b45-d854460ec5e0")
        .kickoff(LocalDateTime.of(2025, 6, 1, 14, 0, 0))
        .groupMatchDay(1)
        .homeTeam(ImmutableTeam.builder()
            .id("bbec1707-7ea3-49cb-9791-7a1358a2b894")
            .name("Bosnia & Herzegovina")
            .imagePath("BIH.png")
            .confederation(Confederation.UEFA)
            .build())
        .awayTeam(ImmutableTeam.builder()
            .id("463de8d9-8520-4fa4-b30c-5aac0f3b363c")
            .name("Nigeria")
            .imagePath("NGA.png")
            .confederation(Confederation.CAF)
            .build())
        .group(ImmutableGroup.builder()
            .id("4c2c8046-0007-48db-a76a-865f9048d9de")
            .name("Group A")
            .build())
        .build();
    private static final Match ARG_IRI_MATCH = ImmutableMatch.builder()
        .id("d8b3685b-3749-438d-9d85-da29c97ebaef")
        .kickoff(LocalDateTime.of(2025, 6, 1, 17, 30, 0))
        .homeTeam(ImmutableTeam.builder()
            .id("977f3f69-0149-43fd-adb0-7c524aea37aa")
            .name("Argentina")
            .imagePath("ARG.png")
            .confederation(Confederation.CONMEBOL)
            .build())
        .awayTeam(ImmutableTeam.builder()
            .id("58adea3b-bdda-496a-be74-64501e34622b")
            .name("Iran")
            .imagePath("IRI.png")
            .confederation(Confederation.AFC)
            .build())
        .round(ImmutableRound.builder()
            .id("322ab9d0-ae46-49ac-89b3-c789a0d9d889")
            .name("Round of 16")
            .teamCount(16)
            .roundOrder(1)
            .twoLegs(false)
            .extraTime(true)
            .awayGoals(false)
            .build())
        .build();

    @Test
    void shouldReturnMatches() {
        // Given
        when(groupService.tournamentHasGroupStage(anyString()))
            .thenReturn(true);
        when(roundService.tournamentHasKnockoutStage(anyString()))
            .thenReturn(true);

        final QueryResponse<DatabaseRecord> matchResponse = mock(QueryResponse.class);
        when(matchResponse.getRecordCount())
            .thenReturn(2);
        when(matchResponse.getRecords())
            .thenReturn(List.of(BIH_NGA_RECORD, ARG_IRI_RECORD));

        when(queryService.retrieveRecords(any()))
            .thenReturn(matchResponse);

        when(matchBuilderFunction.apply(any()))
            .thenReturn(BIH_NGA_MATCH, ARG_IRI_MATCH);

        // When
        final List<Match> matches = matchService.getMatches("5341cff8-df9f-4068-8a42-4b4288ecba87", null, null, null);

        // Then
        verify(tournamentService).getTournamentById("5341cff8-df9f-4068-8a42-4b4288ecba87");
        verify(groupService).tournamentHasGroupStage("5341cff8-df9f-4068-8a42-4b4288ecba87");
        verify(roundService).tournamentHasKnockoutStage("5341cff8-df9f-4068-8a42-4b4288ecba87");

        final ArgumentCaptor<QueryRequest<DatabaseRecord>> requestCaptor = ArgumentCaptor.forClass(QueryRequest.class);
        verify(queryService).retrieveRecords(requestCaptor.capture());
        final QueryRequest<DatabaseRecord> matchRequest = requestCaptor.getValue();

        assertMatchRequest(matchRequest, true, true, null);

        final ArgumentCaptor<DatabaseRecord> recordCaptor = ArgumentCaptor.forClass(DatabaseRecord.class);
        verify(matchBuilderFunction, times(2)).apply(recordCaptor.capture());
        final List<DatabaseRecord> records = recordCaptor.getAllValues();

        assertEquals(BIH_NGA_RECORD, records.get(0));
        assertEquals(ARG_IRI_RECORD, records.get(1));

        assertEquals(2, matches.size());
        assertMatch(BIH_NGA_MATCH, matches.get(0));
        assertMatch(ARG_IRI_MATCH, matches.get(1));
    }

    @Test
    void shouldReturnGroupMatchDayMatches() {
        // Given
        when(groupService.tournamentHasGroupStage(anyString()))
            .thenReturn(true);
        when(roundService.tournamentHasKnockoutStage(anyString()))
            .thenReturn(true);

        final QueryResponse<DatabaseRecord> matchResponse = mock(QueryResponse.class);
        when(matchResponse.getRecordCount())
            .thenReturn(1);
        when(matchResponse.getRecords())
            .thenReturn(List.of(BIH_NGA_RECORD));

        when(queryService.retrieveRecords(any()))
            .thenReturn(matchResponse);

        when(matchBuilderFunction.apply(any()))
            .thenReturn(BIH_NGA_MATCH);

        // When
        final List<Match> matches = matchService.getMatches("5341cff8-df9f-4068-8a42-4b4288ecba87", "4c2c8046-0007-48db-a76a-865f9048d9de", 1, null); 

        // Then
        verify(tournamentService).getTournamentById("5341cff8-df9f-4068-8a42-4b4288ecba87");
        verify(groupService).tournamentHasGroupStage("5341cff8-df9f-4068-8a42-4b4288ecba87");
        verify(roundService).tournamentHasKnockoutStage("5341cff8-df9f-4068-8a42-4b4288ecba87");

        final ArgumentCaptor<QueryRequest<DatabaseRecord>> requestCaptor = ArgumentCaptor.forClass(QueryRequest.class);
        verify(queryService).retrieveRecords(requestCaptor.capture());
        final QueryRequest<DatabaseRecord> matchRequest = requestCaptor.getValue();

        assertMatchRequest(
            matchRequest, 
            true, 
            true, 
            QueryConditionGroup.of(
                QueryCondition.of(
                    Column.of("match", "groupId"),
                    "4c2c8046-0007-48db-a76a-865f9048d9de"
                ),
                QueryCondition.of(
                    Column.of("match", "groupMatchDay"), 
                    1
                )
            )
        );

        final ArgumentCaptor<DatabaseRecord> recordCaptor = ArgumentCaptor.forClass(DatabaseRecord.class);
        verify(matchBuilderFunction).apply(recordCaptor.capture());
        final DatabaseRecord dbRecord = recordCaptor.getValue();

        assertEquals(BIH_NGA_RECORD, dbRecord);

        assertEquals(1, matches.size());
        assertMatch(BIH_NGA_MATCH, matches.get(0));
    }

    @Test
    void shouldReturnRoundMatches() {
        // Given
        when(groupService.tournamentHasGroupStage(anyString()))
            .thenReturn(true);
        when(roundService.tournamentHasKnockoutStage(anyString()))
            .thenReturn(true);

        final QueryResponse<DatabaseRecord> matchResponse = mock(QueryResponse.class);
        when(matchResponse.getRecordCount())
            .thenReturn(1);
        when(matchResponse.getRecords())
            .thenReturn(List.of(ARG_IRI_RECORD));

        when(queryService.retrieveRecords(any()))
            .thenReturn(matchResponse);

        when(matchBuilderFunction.apply(any()))
            .thenReturn(ARG_IRI_MATCH);

        // When
        final List<Match> matches = matchService.getMatches("5341cff8-df9f-4068-8a42-4b4288ecba87", null, null, "322ab9d0-ae46-49ac-89b3-c789a0d9d889"); 

        // Then
        verify(tournamentService).getTournamentById("5341cff8-df9f-4068-8a42-4b4288ecba87");
        verify(groupService).tournamentHasGroupStage("5341cff8-df9f-4068-8a42-4b4288ecba87");
        verify(roundService).tournamentHasKnockoutStage("5341cff8-df9f-4068-8a42-4b4288ecba87");

        final ArgumentCaptor<QueryRequest<DatabaseRecord>> requestCaptor = ArgumentCaptor.forClass(QueryRequest.class);
        verify(queryService).retrieveRecords(requestCaptor.capture());
        final QueryRequest<DatabaseRecord> matchRequest = requestCaptor.getValue();

        assertMatchRequest(
            matchRequest, 
            true, 
            true, 
            QueryConditionGroup.of(
                QueryCondition.of(
                    Column.of("match", "roundId"),
                    "322ab9d0-ae46-49ac-89b3-c789a0d9d889"
                )
            )
        );

        final ArgumentCaptor<DatabaseRecord> recordCaptor = ArgumentCaptor.forClass(DatabaseRecord.class);
        verify(matchBuilderFunction).apply(recordCaptor.capture());
        final DatabaseRecord dbRecord = recordCaptor.getValue();

        assertEquals(ARG_IRI_RECORD, dbRecord);

        assertEquals(1, matches.size());
        assertMatch(ARG_IRI_MATCH, matches.get(0));
    }

    @Test
    void shouldReturnMatchesForTournamentWithNoGroupStage() {
        // Given
        when(groupService.tournamentHasGroupStage(anyString()))
            .thenReturn(false);
        when(roundService.tournamentHasKnockoutStage(anyString()))
            .thenReturn(true);

        final QueryResponse<DatabaseRecord> matchResponse = mock(QueryResponse.class);
        when(matchResponse.getRecordCount())
            .thenReturn(1);
        when(matchResponse.getRecords())
            .thenReturn(List.of(ARG_IRI_RECORD));

        when(queryService.retrieveRecords(any()))
            .thenReturn(matchResponse);

        when(matchBuilderFunction.apply(any()))
            .thenReturn(ARG_IRI_MATCH);

        // When
        final List<Match> matches = matchService.getMatches("5341cff8-df9f-4068-8a42-4b4288ecba87", null, null, null);

        // Then
        verify(tournamentService).getTournamentById("5341cff8-df9f-4068-8a42-4b4288ecba87");
        verify(groupService).tournamentHasGroupStage("5341cff8-df9f-4068-8a42-4b4288ecba87");
        verify(roundService).tournamentHasKnockoutStage("5341cff8-df9f-4068-8a42-4b4288ecba87");

        final ArgumentCaptor<QueryRequest<DatabaseRecord>> requestCaptor = ArgumentCaptor.forClass(QueryRequest.class);
        verify(queryService).retrieveRecords(requestCaptor.capture());
        final QueryRequest<DatabaseRecord> matchRequest = requestCaptor.getValue();

        assertMatchRequest(matchRequest, false, true, null);

        final ArgumentCaptor<DatabaseRecord> recordCaptor = ArgumentCaptor.forClass(DatabaseRecord.class);
        verify(matchBuilderFunction).apply(recordCaptor.capture());
        final DatabaseRecord dbRecord = recordCaptor.getValue();

        assertEquals(ARG_IRI_RECORD, dbRecord);

        assertEquals(1, matches.size());
        assertMatch(ARG_IRI_MATCH, matches.get(0));
    }

    @Test
    void shouldReturnMatchesForTournamentWithNoKnockoutStage() {
        // Given
        when(groupService.tournamentHasGroupStage(anyString()))
            .thenReturn(true);
        when(roundService.tournamentHasKnockoutStage(anyString()))
            .thenReturn(false);

        final QueryResponse<DatabaseRecord> matchResponse = mock(QueryResponse.class);
        when(matchResponse.getRecordCount())
            .thenReturn(1);
        when(matchResponse.getRecords())
            .thenReturn(List.of(BIH_NGA_RECORD));

        when(queryService.retrieveRecords(any()))
            .thenReturn(matchResponse);

        when(matchBuilderFunction.apply(any()))
            .thenReturn(BIH_NGA_MATCH);

        // When
        final List<Match> matches = matchService.getMatches("5341cff8-df9f-4068-8a42-4b4288ecba87", null, null, null);

        // Then
        verify(tournamentService).getTournamentById("5341cff8-df9f-4068-8a42-4b4288ecba87");
        verify(groupService).tournamentHasGroupStage("5341cff8-df9f-4068-8a42-4b4288ecba87");
        verify(roundService).tournamentHasKnockoutStage("5341cff8-df9f-4068-8a42-4b4288ecba87");

        final ArgumentCaptor<QueryRequest<DatabaseRecord>> requestCaptor = ArgumentCaptor.forClass(QueryRequest.class);
        verify(queryService).retrieveRecords(requestCaptor.capture());
        final QueryRequest<DatabaseRecord> matchRequest = requestCaptor.getValue();

        assertMatchRequest(matchRequest, true, false, null);

        final ArgumentCaptor<DatabaseRecord> recordCaptor = ArgumentCaptor.forClass(DatabaseRecord.class);
        verify(matchBuilderFunction).apply(recordCaptor.capture());
        final DatabaseRecord dbRecord = recordCaptor.getValue();

        assertEquals(BIH_NGA_RECORD, dbRecord);

        assertEquals(1, matches.size());
        assertMatch(BIH_NGA_MATCH, matches.get(0));
    }

    @Test
    void shouldErrorIfTournamentDoesNotExist() {
        // Given
        when(tournamentService.getTournamentById(anyString()))
            .thenThrow(new ResponseStatusException(HttpStatus.NOT_FOUND, "No tournaments found with a matching id."));

        // When
        final ResponseStatusException rse = assertThrows(ResponseStatusException.class, () -> matchService.getMatches("5341cff8-df9f-4068-8a42-4b4288ecba87", null, null, null));

        // Then
        assertEquals(HttpStatus.NOT_FOUND, rse.getStatusCode());
        assertEquals("No tournaments found with a matching id.", rse.getReason());
    }

    @Test
    void shouldUpdateMatches() {
        // Given
        final List<MatchUpdate> updates = List.of(
            ImmutableMatchUpdate.builder()
                .id("8efaf853-980e-4607-9b45-d854460ec5e0")
                .kickoff(LocalDateTime.of(2025, 6, 1, 14, 0, 0))
                .build(),
            ImmutableMatchUpdate.builder()
                .id("d8b3685b-3749-438d-9d85-da29c97ebaef")
                .kickoff(LocalDateTime.of(2025, 6, 1, 17, 30, 0))
                .build()
        );

        when(groupService.tournamentHasGroupStage(anyString()))
            .thenReturn(true);
        when(roundService.tournamentHasKnockoutStage(anyString()))
            .thenReturn(true);

        final QueryResponse<DatabaseRecord> matchResponse = mock(QueryResponse.class);
        when(matchResponse.getRecordCount())
            .thenReturn(1);
        when(matchResponse.getRecords())
            .thenReturn(List.of(BIH_NGA_RECORD, ARG_IRI_RECORD));

        when(queryService.retrieveRecords(any()))
            .thenReturn(matchResponse);

        when(matchBuilderFunction.apply(any()))
            .thenReturn(BIH_NGA_MATCH, ARG_IRI_MATCH);

        // When
        final List<Match> updated = matchService.updateMatches("5341cff8-df9f-4068-8a42-4b4288ecba87", updates);

        // Then
        verify(tournamentService).getTournamentById("5341cff8-df9f-4068-8a42-4b4288ecba87");

        final ArgumentCaptor<UpdateRequest<MatchUpdate>> updateCaptor = ArgumentCaptor.forClass(UpdateRequest.class);
        verify(queryService).updateRecords(updateCaptor.capture());
        final UpdateRequest<MatchUpdate> updateRequest = updateCaptor.getValue();

        assertEquals(SqlOperator.UPDATE, updateRequest.getOperation());
        assertTable("predictor", "matches_5341cff8-df9f-4068-8a42-4b4288ecba87", updateRequest.getTable());

        assertEquals(2, updateRequest.getRecords().size());
        assertMatchUpdate("8efaf853-980e-4607-9b45-d854460ec5e0", LocalDateTime.of(2025, 6, 1, 14, 0, 0), updateRequest.getRecords().get(0));
        assertMatchUpdate("d8b3685b-3749-438d-9d85-da29c97ebaef", LocalDateTime.of(2025, 6, 1, 17, 30, 0), updateRequest.getRecords().get(1));

        verify(groupService).tournamentHasGroupStage("5341cff8-df9f-4068-8a42-4b4288ecba87");
        verify(roundService).tournamentHasKnockoutStage("5341cff8-df9f-4068-8a42-4b4288ecba87");

        final ArgumentCaptor<QueryRequest<DatabaseRecord>> requestCaptor = ArgumentCaptor.forClass(QueryRequest.class);
        verify(queryService).retrieveRecords(requestCaptor.capture());
        final QueryRequest<DatabaseRecord> matchRequest = requestCaptor.getValue();

        assertMatchRequest(
            matchRequest, 
            true, 
            true, 
            QueryConditionGroup.of(
                ImmutableQueryCondition.builder()
                    .column(Column.of("match", "id"))
                    .operator(ConditionOperator.IN)
                    .value(List.of("8efaf853-980e-4607-9b45-d854460ec5e0", "d8b3685b-3749-438d-9d85-da29c97ebaef"))
                    .build()
            )
        );

        final ArgumentCaptor<DatabaseRecord> recordCaptor = ArgumentCaptor.forClass(DatabaseRecord.class);
        verify(matchBuilderFunction, times(2)).apply(recordCaptor.capture());
        final List<DatabaseRecord> records = recordCaptor.getAllValues();

        assertEquals(BIH_NGA_RECORD, records.get(0));
        assertEquals(ARG_IRI_RECORD, records.get(1));

        assertEquals(2, updated.size());
        assertMatch(BIH_NGA_MATCH, updated.get(0));
        assertMatch(ARG_IRI_MATCH, updated.get(1));
    }

    @Test
    void shouldErrorIfTournamentDoesNotExistWhenUpdatingMatches() {
        // Given
        final List<MatchUpdate> updates = List.of(
            ImmutableMatchUpdate.builder()
                .id("8efaf853-980e-4607-9b45-d854460ec5e0")
                .kickoff(LocalDateTime.of(2025, 6, 1, 14, 0, 0))
                .build(),
            ImmutableMatchUpdate.builder()
                .id("d8b3685b-3749-438d-9d85-da29c97ebaef")
                .kickoff(LocalDateTime.of(2025, 6, 1, 17, 30, 0))
                .build()
        );

        when(tournamentService.getTournamentById(anyString()))
            .thenThrow(new ResponseStatusException(HttpStatus.NOT_FOUND, "No tournaments found with a matching id."));

        // When
        final ResponseStatusException rse = assertThrows(ResponseStatusException.class, () -> matchService.updateMatches("5341cff8-df9f-4068-8a42-4b4288ecba87", updates));

        // Then
        assertEquals(HttpStatus.NOT_FOUND, rse.getStatusCode());
        assertEquals("No tournaments found with a matching id.", rse.getReason());
    }

    @Test
    void shouldReturnMatchById() {
        // Given
        when(groupService.tournamentHasGroupStage(anyString()))
            .thenReturn(true);
        when(roundService.tournamentHasKnockoutStage(anyString()))
            .thenReturn(true);

        final QueryResponse<DatabaseRecord> matchResponse = mock(QueryResponse.class);
        when(matchResponse.getRecordCount())
            .thenReturn(1);
        when(matchResponse.getRecords())
            .thenReturn(List.of(BIH_NGA_RECORD));

        when(queryService.retrieveRecords(any()))
            .thenReturn(matchResponse);

        when(matchBuilderFunction.apply(any()))
            .thenReturn(BIH_NGA_MATCH);

        // When
        final Match match = matchService.getMatchById("5341cff8-df9f-4068-8a42-4b4288ecba87", "8efaf853-980e-4607-9b45-d854460ec5e0");

        // Then
        verify(tournamentService).getTournamentById("5341cff8-df9f-4068-8a42-4b4288ecba87");
        verify(groupService).tournamentHasGroupStage("5341cff8-df9f-4068-8a42-4b4288ecba87");
        verify(roundService).tournamentHasKnockoutStage("5341cff8-df9f-4068-8a42-4b4288ecba87");

        final ArgumentCaptor<QueryRequest<DatabaseRecord>> requestCaptor = ArgumentCaptor.forClass(QueryRequest.class);
        verify(queryService).retrieveRecords(requestCaptor.capture());
        final QueryRequest<DatabaseRecord> matchRequest = requestCaptor.getValue();

        assertMatchRequest(
            matchRequest, 
            true, 
            true, 
            QueryConditionGroup.of(
                ImmutableQueryCondition.builder()
                    .column(Column.of("match", "id"))
                    .operator(ConditionOperator.IN)
                    .value(List.of("8efaf853-980e-4607-9b45-d854460ec5e0"))
                    .build()
            )
        );

        final ArgumentCaptor<DatabaseRecord> recordCaptor = ArgumentCaptor.forClass(DatabaseRecord.class);
        verify(matchBuilderFunction).apply(recordCaptor.capture());
        final DatabaseRecord dbRecord = recordCaptor.getValue();

        assertEquals(BIH_NGA_RECORD, dbRecord);

        assertMatch(BIH_NGA_MATCH, match);
    }

    @Test
    void shouldErrorIfTournamentDoesNotExistWhenRetrievingMatchById() {
        // Given
        when(tournamentService.getTournamentById(anyString()))
            .thenThrow(new ResponseStatusException(HttpStatus.NOT_FOUND, "No tournaments found with a matching id."));

        // When
        final ResponseStatusException rse = assertThrows(ResponseStatusException.class, () -> matchService.getMatchById("5341cff8-df9f-4068-8a42-4b4288ecba87", "8efaf853-980e-4607-9b45-d854460ec5e0"));

        // Then
        assertEquals(HttpStatus.NOT_FOUND, rse.getStatusCode());
        assertEquals("No tournaments found with a matching id.", rse.getReason());
    }

    @Test
    void shouldErrorIfMatchDoesNotExist() {
        // Given
        when(groupService.tournamentHasGroupStage(anyString()))
            .thenReturn(true);
        when(roundService.tournamentHasKnockoutStage(anyString()))
            .thenReturn(true);

        final QueryResponse<DatabaseRecord> matchResponse = mock(QueryResponse.class);
        when(matchResponse.getRecordCount())
            .thenReturn(0);
        when(matchResponse.getRecords())
            .thenReturn(List.of());

        when(queryService.retrieveRecords(any()))
            .thenReturn(matchResponse);

        // When
        final ResponseStatusException rse = assertThrows(ResponseStatusException.class, () -> matchService.getMatchById("5341cff8-df9f-4068-8a42-4b4288ecba87", "8efaf853-980e-4607-9b45-d854460ec5e0"));

        // Then
        verify(tournamentService).getTournamentById("5341cff8-df9f-4068-8a42-4b4288ecba87");
        verify(groupService).tournamentHasGroupStage("5341cff8-df9f-4068-8a42-4b4288ecba87");
        verify(roundService).tournamentHasKnockoutStage("5341cff8-df9f-4068-8a42-4b4288ecba87");

        final ArgumentCaptor<QueryRequest<DatabaseRecord>> requestCaptor = ArgumentCaptor.forClass(QueryRequest.class);
        verify(queryService).retrieveRecords(requestCaptor.capture());
        final QueryRequest<DatabaseRecord> matchRequest = requestCaptor.getValue();

        assertMatchRequest(
            matchRequest, 
            true, 
            true, 
            QueryConditionGroup.of(
                ImmutableQueryCondition.builder()
                    .column(Column.of("match", "id"))
                    .operator(ConditionOperator.IN)
                    .value(List.of("8efaf853-980e-4607-9b45-d854460ec5e0"))
                    .build()
            )
        );

        assertEquals(HttpStatus.NOT_FOUND, rse.getStatusCode());
        assertEquals("No matches found with a matching id.", rse.getReason());
    }

    private static void assertColumn(Column expected, Column actual) {
        assertColumn(expected.getParts(), expected.getAlias(), actual);
    }

    private static void assertColumn(List<String> expectedParts, Column actual) {
        assertColumn(expectedParts, null, actual);
    }

    private static void assertColumn(List<String> expectedParts, @Nullable String expectedAlias, Column actual) {
        assertEquals(expectedParts, actual.getParts());
        assertEquals(expectedAlias, actual.getAlias());
    }

    private static void assertTable(Table expected, Table actual) {
        assertTable(expected.getSchema(), expected.getTable(), expected.getAlias(), actual);
    }

    private static void assertTable(String expectedSchema, String expectedTable, Table actual) {
        assertTable(expectedSchema, expectedTable, null, actual);
    }

    private static void assertTable(String expectedSchema, String expectedTable, @Nullable String expectedAlias, Table actual) {
        assertEquals(expectedSchema, actual.getSchema());
        assertEquals(expectedTable, actual.getTable());
        assertEquals(expectedAlias, actual.getAlias());
    }

    private static void assertJoinCondition(QueryCondition expected, QueryCondition actual) {
        assertColumn(expected.getColumn(), actual.getColumn());
        assertEquals(expected.getOperator(), actual.getOperator());
        assertColumn((Column) expected.getValue(), (Column) actual.getValue());
    }

    private static void assertCondition(QueryCondition expected, QueryCondition actual) {
        assertColumn(expected.getColumn(), actual.getColumn());
        assertEquals(expected.getOperator(), actual.getOperator());
        assertEquals(expected.getValue(), actual.getValue());
    }

    private static void assertConditionGroup(QueryConditionGroup expected, QueryConditionGroup actual) {
        assertEquals(expected.getJoin(), actual.getJoin());
        assertEquals(expected.getConditions().size(), actual.getConditions().size());

        for (int i = 0; i < actual.getConditions().size(); i++) {
            assertCondition(expected.getConditions().get(i), actual.getConditions().get(i));
        }
    }

    private static void assertTableJoin(Table expectedTable, QueryCondition expectedCondition, JoinType expectedJoinType, TableJoin actual) {
        assertTable(expectedTable, actual.getTable());
        assertJoinCondition(expectedCondition, actual.getJoinCondition());
        assertEquals(expectedJoinType, actual.getJoinType());
    }

    private static void assertOrderBy(Column expectedColumn, OrderDirection expectedDirection, OrderBy actual) {
        assertColumn(expectedColumn, actual.getColumn());
        assertEquals(expectedDirection, actual.getDirection());
    }

    private static void assertMatch(Match expected, Match actual) {
        assertEquals(expected.getId(), actual.getId());
        assertEquals(expected.getKickoff(), actual.getKickoff());
        assertEquals(expected.getGroupMatchDay(), actual.getGroupMatchDay());
        assertTeam(expected.getHomeTeam(), actual.getHomeTeam());
        assertTeam(expected.getAwayTeam(), actual.getAwayTeam());

        if (actual.getGroup() != null) {
            assertGroup(expected.getGroup(), actual.getGroup());
        } else {
            assertNull(expected.getGroup());
        }

        if (actual.getRound() != null) {
            assertRound(expected.getRound(), actual.getRound());
        } else {
            assertNull(expected.getRound());
        }
    }

    private static void assertMatchUpdate(String expectedId, LocalDateTime expectedKickoff, MatchUpdate actual) {
        assertEquals(expectedId, actual.getId());
        assertEquals(expectedKickoff, actual.getKickoff());
    }

    private static void assertTeam(Team expected, Team actual) {
        assertEquals(expected.getId(), actual.getId());
        assertEquals(expected.getName(), actual.getName());
        assertEquals(expected.getImagePath(), actual.getImagePath());
        assertEquals(expected.getConfederation(), actual.getConfederation());
    }

    private static void assertGroup(Group expected, Group actual) {
        assertEquals(expected.getId(), actual.getId());
        assertEquals(expected.getName(), actual.getName());
    }

    private static void assertRound(Round expected, Round actual) {
        assertEquals(expected.getId(), actual.getId());
        assertEquals(expected.getName(), actual.getName());
        assertEquals(expected.getTeamCount(), actual.getTeamCount());
        assertEquals(expected.getRoundOrder(), actual.getRoundOrder());
        assertEquals(expected.getTwoLegs(), actual.getTwoLegs());
        assertEquals(expected.getExtraTime(), actual.getExtraTime());
        assertEquals(expected.getAwayGoals(), actual.getAwayGoals());
    }

    private static void assertMatchRequest(QueryRequest<DatabaseRecord> matchRequest, boolean includeGroup, boolean includeRound, @Nullable QueryConditionGroup conditionGroup) {
        final List<Column> columns = matchRequest.getColumns();
        assertColumn(List.of("match", "id"), "matchId", columns.get(0));
        assertColumn(List.of("home", "id"), "homeId", columns.get(1));
        assertColumn(List.of("home", "name"), "homeName", columns.get(2));
        assertColumn(List.of("home", "imagePath"), "homeImagePath", columns.get(3));
        assertColumn(List.of("home", "confederation"), "homeConfederation", columns.get(4));
        assertColumn(List.of("away", "id"), "awayId", columns.get(5));
        assertColumn(List.of("away", "name"), "awayName", columns.get(6));
        assertColumn(List.of("away", "imagePath"), "awayImagePath", columns.get(7));
        assertColumn(List.of("away", "confederation"), "awayConfederation", columns.get(8));
        assertColumn(List.of("match", "kickoff"), columns.get(9));
        assertColumn(List.of("match", "groupMatchDay"), columns.get(10));
        assertColumn(List.of("match", "groupId"), columns.get(11));
        assertColumn(List.of("match", "roundId"), columns.get(12));
        assertColumn(List.of("result", "homeGoals"), columns.get(13));
        assertColumn(List.of("result", "awayGoals"), columns.get(14));
        assertColumn(List.of("result", "afterExtraTime"), columns.get(15));
        assertColumn(List.of("result", "afterPenalties"), columns.get(16));
        assertColumn(List.of("result", "penaltiesWinner"), columns.get(17));

        assertTable("predictor", "matches_5341cff8-df9f-4068-8a42-4b4288ecba87", "match", matchRequest.getTable());

        final List<TableJoin> tableJoins = matchRequest.getJoins().stream()
            .map(TableJoin.class::cast)
            .toList();
        assertTableJoin(
            Table.of("predictor", "teams", "home"),
            QueryCondition.of(
                Column.of("match", "homeTeamId"),
                Column.of("home", "id")
            ),
            JoinType.LEFT, 
            tableJoins.get(0)
        );
        assertTableJoin(
            Table.of("predictor", "teams", "away"), 
            QueryCondition.of(
                Column.of("match", "awayTeamId"), 
                Column.of("away", "id")
            ), 
            JoinType.LEFT, 
            tableJoins.get(1)
        );
        assertTableJoin(
            Table.of("predictor", "results_5341cff8-df9f-4068-8a42-4b4288ecba87", "result"), 
            QueryCondition.of(
                Column.of("match", "id"),
                Column.of("result", "id")
            ), 
            JoinType.LEFT, 
            tableJoins.get(2)
        );

        if (conditionGroup != null) {
            assertConditionGroup(conditionGroup, matchRequest.getConditionGroup());
        }

        final List<OrderBy> orderBy = matchRequest.getOrderBy();
        assertOrderBy(
            Column.of("match", "kickoff"), 
            OrderDirection.ASCENDING, 
            orderBy.get(0)
        );

        if (includeGroup && includeRound) {
            assertEquals(25, columns.size());

            assertColumn(List.of("group", "name"), "groupName", columns.get(18));
            assertColumn(List.of("round", "name"), "roundName", columns.get(19));
            assertColumn(List.of("round", "teamCount"), columns.get(20));
            assertColumn(List.of("round", "roundOrder"), columns.get(21));
            assertColumn(List.of("round", "twoLegs"), columns.get(22));
            assertColumn(List.of("round", "extraTime"), columns.get(23));
            assertColumn(List.of("round", "awayGoals"), "awayGoalsDecider", columns.get(24));

            assertEquals(5, tableJoins.size());
            assertTableJoin(
                Table.of("predictor", "groups_5341cff8-df9f-4068-8a42-4b4288ecba87", "group"), 
                QueryCondition.of(
                    Column.of("match", "groupId"),
                    Column.of("group", "id")
                ), 
                JoinType.LEFT, 
                tableJoins.get(3)
            );
            assertTableJoin(
                Table.of("predictor", "rounds_5341cff8-df9f-4068-8a42-4b4288ecba87", "round"), 
                QueryCondition.of(
                    Column.of("match", "roundId"),
                    Column.of("round", "id")
                ), 
                JoinType.LEFT, 
                tableJoins.get(4)
            );

            assertEquals(4, orderBy.size());
            assertOrderBy(
                Column.of("group", "name"), 
                OrderDirection.ASCENDING, 
                orderBy.get(1)
            );
            assertOrderBy(
                Column.of("match", "groupMatchDay"), 
                OrderDirection.ASCENDING, 
                orderBy.get(2)
            );
            assertOrderBy(
                Column.of("round", "roundOrder"), 
                OrderDirection.ASCENDING, 
                orderBy.get(3)
            );
        } else if (includeGroup) {
            assertEquals(19, columns.size());

            assertColumn(List.of("group", "name"), "groupName", columns.get(18));

            assertEquals(4, tableJoins.size());
            assertTableJoin(
                Table.of("predictor", "groups_5341cff8-df9f-4068-8a42-4b4288ecba87", "group"), 
                QueryCondition.of(
                    Column.of("match", "groupId"),
                    Column.of("group", "id")
                ), 
                JoinType.LEFT, 
                tableJoins.get(3)
            );

            assertEquals(3, orderBy.size());
            assertOrderBy(
                Column.of("group", "name"), 
                OrderDirection.ASCENDING, 
                orderBy.get(1)
            );
            assertOrderBy(
                Column.of("match", "groupMatchDay"), 
                OrderDirection.ASCENDING, 
                orderBy.get(2)
            );
        } else if (includeRound) {
            assertEquals(24, columns.size());

            assertColumn(List.of("round", "name"), "roundName", columns.get(18));
            assertColumn(List.of("round", "teamCount"), columns.get(19));
            assertColumn(List.of("round", "roundOrder"), columns.get(20));
            assertColumn(List.of("round", "twoLegs"), columns.get(21));
            assertColumn(List.of("round", "extraTime"), columns.get(22));
            assertColumn(List.of("round", "awayGoals"), "awayGoalsDecider", columns.get(23));

            assertEquals(4, tableJoins.size());
            assertTableJoin(
                Table.of("predictor", "rounds_5341cff8-df9f-4068-8a42-4b4288ecba87", "round"), 
                QueryCondition.of(
                    Column.of("match", "roundId"),
                    Column.of("round", "id")
                ), 
                JoinType.LEFT, 
                tableJoins.get(3)
            );

            assertEquals(3, orderBy.size());
            assertOrderBy(
                Column.of("match", "groupMatchDay"), 
                OrderDirection.ASCENDING, 
                orderBy.get(1)
            );
            assertOrderBy(
                Column.of("round", "roundOrder"), 
                OrderDirection.ASCENDING, 
                orderBy.get(2)
            );
        } else {
            assertEquals(18, columns.size());
            assertEquals(3, tableJoins.size());

            assertEquals(2, orderBy.size());
            assertOrderBy(
                Column.of("match", "groupMatchDay"), 
                OrderDirection.ASCENDING, 
                orderBy.get(1)
            );
        }
    }
}
