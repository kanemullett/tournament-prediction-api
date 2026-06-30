package com.kanemullett.service;

import java.util.List;

import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Service;
import org.springframework.web.server.ResponseStatusException;

import com.kanemullett.model.Column;
import com.kanemullett.model.ImmutableQueryRequest;
import com.kanemullett.model.ImmutableUpdateRequest;
import com.kanemullett.model.LeagueTemplate;
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
public class LeagueTemplateService {

    private final DatabaseQueryService queryService;

    public LeagueTemplateService(DatabaseQueryService queryService) {
        this.queryService = queryService;
    }

    public List<LeagueTemplate> getLeagueTemplates() {
        final QueryRequest<LeagueTemplate> request = ImmutableQueryRequest.<LeagueTemplate>builder()
            .table(Table.of(PredictorConstants.PREDICTOR_SCHEMA, LeagueTemplate.TARGET_TABLE))
            .recordClass(LeagueTemplate.class)
            .build();

        final QueryResponse<LeagueTemplate> response = queryService.retrieveRecords(request);

        return response.getRecords();
    }

    public List<LeagueTemplate> createLeagueTemplates(List<LeagueTemplate> leagueTemplates) {
        final UpdateRequest<LeagueTemplate> updateRequest = ImmutableUpdateRequest.<LeagueTemplate>builder()
            .operation(SqlOperator.INSERT)
            .table(Table.of(PredictorConstants.PREDICTOR_SCHEMA, LeagueTemplate.TARGET_TABLE))
            .records(leagueTemplates)
            .build();

        queryService.updateRecords(updateRequest);

        return leagueTemplates;
    }

    public LeagueTemplate getLeagueTemplateById(String leagueTemplateId) {
        final QueryRequest<LeagueTemplate> queryRequest = ImmutableQueryRequest.<LeagueTemplate>builder()
            .table(Table.of(PredictorConstants.PREDICTOR_SCHEMA, LeagueTemplate.TARGET_TABLE))
            .conditionGroup(QueryConditionGroup.of(
                QueryCondition.of(
                    Column.of(DatabaseConstants.ID),
                    leagueTemplateId
                )
            ))
            .recordClass(LeagueTemplate.class)
            .build();

        final QueryResponse<LeagueTemplate> queryResponse = queryService.retrieveRecords(queryRequest);

        if (queryResponse.getRecordCount() == 0) {
            throw new ResponseStatusException(HttpStatus.NOT_FOUND, "No league templates found with a matching id.");
        }

        return queryResponse.getRecords().get(0);
    }

    public void deleteLeagueTemplateById(String leagueTemplateId) {
        final QueryRequest<TournamentTemplateRecord> queryRequest = ImmutableQueryRequest.<TournamentTemplateRecord>builder()
            .table(Table.of(PredictorConstants.PREDICTOR_SCHEMA, TournamentTemplateRecord.TARGET_TABLE))
            .conditionGroup(QueryConditionGroup.of(
                QueryCondition.of(
                    Column.of(TournamentTemplateRecord.LEAGUE_TEMPLATE_ID_COLUMN),
                    leagueTemplateId
                )
            ))
            .recordClass(TournamentTemplateRecord.class)
            .build();

        final QueryResponse<TournamentTemplateRecord> queryResponse = queryService.retrieveRecords(queryRequest);

        if (queryResponse.getRecordCount() > 0) {
            throw new ResponseStatusException(HttpStatus.CONFLICT, "Cannot delete league template as it is part of an existing tournament template.");
        }

        final UpdateRequest<LeagueTemplate> updateRequest = ImmutableUpdateRequest.<LeagueTemplate>builder()
            .operation(SqlOperator.DELETE)
            .table(Table.of(PredictorConstants.PREDICTOR_SCHEMA, LeagueTemplate.TARGET_TABLE))
            .conditionGroup(QueryConditionGroup.of(
                QueryCondition.of(
                    Column.of(DatabaseConstants.ID),
                    leagueTemplateId
                )
            ))
            .build();

        queryService.updateRecords(updateRequest);
    }
}
