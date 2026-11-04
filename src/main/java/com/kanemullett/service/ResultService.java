package com.kanemullett.service;

import java.util.List;

import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Service;
import org.springframework.web.server.ResponseStatusException;

import com.kanemullett.model.Column;
import com.kanemullett.model.ImmutableQueryCondition;
import com.kanemullett.model.ImmutableQueryRequest;
import com.kanemullett.model.ImmutableUpdateRequest;
import com.kanemullett.model.MatchRecord;
import com.kanemullett.model.QueryCondition;
import com.kanemullett.model.QueryConditionGroup;
import com.kanemullett.model.QueryRequest;
import com.kanemullett.model.QueryResponse;
import com.kanemullett.model.Result;
import com.kanemullett.model.Table;
import com.kanemullett.model.UpdateRequest;
import com.kanemullett.model.type.ConditionOperator;
import com.kanemullett.model.type.SqlOperator;
import com.kanemullett.util.DatabaseConstants;
import com.kanemullett.util.PredictorConstants;

@Service
public class ResultService {

    private final DatabaseQueryService queryService;
    private final TournamentService tournamentService;

    public ResultService(DatabaseQueryService queryService, TournamentService tournamentService) {
        this.queryService = queryService;
        this.tournamentService = tournamentService;
    }

    public List<Result> createResults(String tournamentId, List<Result> results) {
        tournamentService.getTournamentById(tournamentId);

        final QueryRequest<MatchRecord> matchRequest = ImmutableQueryRequest.<MatchRecord>builder()
            .table(Table.of(
                PredictorConstants.PREDICTOR_SCHEMA,
                MatchRecord.getTargetTable(tournamentId)
            ))
            .conditionGroup(QueryConditionGroup.of(
                ImmutableQueryCondition.builder()
                    .column(Column.of(DatabaseConstants.ID))
                    .operator(ConditionOperator.IN)
                    .value(results.stream()
                        .map(Result::getId)
                        .toList())
                    .build()
            ))
            .recordClass(MatchRecord.class)
            .build();
        
        final QueryResponse<MatchRecord> matchResponse = queryService.retrieveRecords(matchRequest);

        if (matchResponse.getRecordCount() < results.size()) {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "One or more results do not have a corresponding match record.");
        }

        final UpdateRequest<Result> updateRequest = ImmutableUpdateRequest.<Result>builder()
            .operation(SqlOperator.INSERT)
            .table(Table.of(
                PredictorConstants.PREDICTOR_SCHEMA,
                Result.getTargetTable(tournamentId)
            ))
            .records(results)
            .build();

        queryService.updateRecords(updateRequest);

        return results;
    }

    public List<Result> updateResults(String tournamentId, List<Result> updates) {
        tournamentService.getTournamentById(tournamentId);

        final UpdateRequest<Result> updateRequest = ImmutableUpdateRequest.<Result>builder()
            .operation(SqlOperator.UPDATE)
            .table(Table.of(
                PredictorConstants.PREDICTOR_SCHEMA,
                Result.getTargetTable(tournamentId)
            ))
            .records(updates)
            .build();

        queryService.updateRecords(updateRequest);

        final QueryRequest<Result> resultRequest = ImmutableQueryRequest.<Result>builder()
            .table(Table.of(
                PredictorConstants.PREDICTOR_SCHEMA,
                Result.getTargetTable(tournamentId)
            ))
            .conditionGroup(QueryConditionGroup.of(
                ImmutableQueryCondition.builder()
                    .column(Column.of(DatabaseConstants.ID))
                    .operator(ConditionOperator.IN)
                    .value(updates.stream()
                        .map(Result::getId)
                        .toList())
                    .build()
            ))
            .recordClass(Result.class)
            .build();

        final QueryResponse<Result> resultResponse = queryService.retrieveRecords(resultRequest);

        return resultResponse.getRecords();
    }

    public void deleteResultById(String tournamentId, String resultId) {
        tournamentService.getTournamentById(tournamentId);

        final UpdateRequest<Result> deleteRequest = ImmutableUpdateRequest.<Result>builder()
            .operation(SqlOperator.DELETE)
            .table(Table.of(
                PredictorConstants.PREDICTOR_SCHEMA,
                Result.getTargetTable(tournamentId)
            ))
            .conditionGroup(QueryConditionGroup.of(
                QueryCondition.of(
                    Column.of(DatabaseConstants.ID),
                    resultId
                )
            ))
            .build();

        queryService.updateRecords(deleteRequest);
    }
}
