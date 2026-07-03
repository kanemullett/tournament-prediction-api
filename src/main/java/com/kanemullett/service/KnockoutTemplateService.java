package com.kanemullett.service;

import java.util.List;

import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Service;
import org.springframework.web.server.ResponseStatusException;

import com.kanemullett.model.Column;
import com.kanemullett.model.ImmutableQueryRequest;
import com.kanemullett.model.ImmutableUpdateRequest;
import com.kanemullett.model.KnockoutTemplate;
import com.kanemullett.model.QueryCondition;
import com.kanemullett.model.QueryConditionGroup;
import com.kanemullett.model.QueryRequest;
import com.kanemullett.model.QueryResponse;
import com.kanemullett.model.Table;
import com.kanemullett.model.TournamentTemplateRecord;
import com.kanemullett.model.UpdateRequest;
import com.kanemullett.model.type.SqlOperator;
import com.kanemullett.util.DatabaseConstants;
import com.kanemullett.util.PredictorConstants;

@Service
public class KnockoutTemplateService {

    private final DatabaseQueryService queryService;

    public KnockoutTemplateService(DatabaseQueryService queryService) {
        this.queryService = queryService;
    }

    public List<KnockoutTemplate> getKnockoutTemplates() {
        final QueryRequest<KnockoutTemplate> queryRequest = ImmutableQueryRequest.<KnockoutTemplate>builder()
            .table(Table.of(PredictorConstants.PREDICTOR_SCHEMA, KnockoutTemplate.TARGET_TABLE))
            .recordClass(KnockoutTemplate.class)
            .build();

        final QueryResponse<KnockoutTemplate> queryResponse = queryService.retrieveRecords(queryRequest);

        return queryResponse.getRecords();
    }

    public List<KnockoutTemplate> createKnockoutTemplates(List<KnockoutTemplate> knockoutTemplates) {
        final UpdateRequest<KnockoutTemplate> updateRequest = ImmutableUpdateRequest.<KnockoutTemplate>builder()
            .operation(SqlOperator.INSERT)
            .table(Table.of(PredictorConstants.PREDICTOR_SCHEMA, KnockoutTemplate.TARGET_TABLE))
            .records(knockoutTemplates)
            .build();

        queryService.updateRecords(updateRequest);

        return knockoutTemplates;
    }

    public KnockoutTemplate getKnockoutTemplateById(String knockoutTemplateId) {
        final QueryRequest<KnockoutTemplate> queryRequest = ImmutableQueryRequest.<KnockoutTemplate>builder()
            .table(Table.of(PredictorConstants.PREDICTOR_SCHEMA, KnockoutTemplate.TARGET_TABLE))
            .conditionGroup(QueryConditionGroup.of(
                QueryCondition.of(
                    Column.of(DatabaseConstants.ID),
                    knockoutTemplateId
                )
            ))
            .recordClass(KnockoutTemplate.class)
            .build();

        final QueryResponse<KnockoutTemplate> queryResponse = queryService.retrieveRecords(queryRequest);

        if (queryResponse.getRecordCount() == 0) {
            throw new ResponseStatusException(HttpStatus.NOT_FOUND, "No knockout templates found with a matching id.");
        }

        return queryResponse.getRecords().get(0);
    }

    public void deleteKnockoutTemplateById(String knockoutTemplateId) {
        final QueryRequest<TournamentTemplateRecord> queryRequest = ImmutableQueryRequest.<TournamentTemplateRecord>builder()
            .table(Table.of(PredictorConstants.PREDICTOR_SCHEMA, TournamentTemplateRecord.TARGET_TABLE))
            .conditionGroup(QueryConditionGroup.of(
                QueryCondition.of(
                    Column.of(TournamentTemplateRecord.KNOCKOUT_TEMPLATE_ID_COLUMN),
                    knockoutTemplateId
                )
            ))
            .recordClass(TournamentTemplateRecord.class)
            .build();

        final QueryResponse<TournamentTemplateRecord> queryResponse = queryService.retrieveRecords(queryRequest);

        if (queryResponse.getRecordCount() > 0) {
            throw new ResponseStatusException(HttpStatus.CONFLICT, "Cannot delete knockout template as it is part of an existing tournament template.");
        }

        final UpdateRequest<KnockoutTemplate> updateRequest = ImmutableUpdateRequest.<KnockoutTemplate>builder()
            .operation(SqlOperator.DELETE)
            .table(Table.of(PredictorConstants.PREDICTOR_SCHEMA, KnockoutTemplate.TARGET_TABLE))
            .conditionGroup(QueryConditionGroup.of(
                QueryCondition.of(
                    Column.of(DatabaseConstants.ID),
                    knockoutTemplateId
                )
            ))
            .build();

        queryService.updateRecords(updateRequest);
    }
}
