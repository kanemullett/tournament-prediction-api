package com.kanemullett.service;

import java.util.List;

import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Service;
import org.springframework.web.server.ResponseStatusException;

import com.kanemullett.model.Column;
import com.kanemullett.model.Competition;
import com.kanemullett.model.CompetitionUpdate;
import com.kanemullett.model.CompetitionUser;
import com.kanemullett.model.ImmutableCompetitionUser;
import com.kanemullett.model.ImmutableQueryCondition;
import com.kanemullett.model.ImmutableQueryRequest;
import com.kanemullett.model.ImmutableUpdateRequest;
import com.kanemullett.model.QueryCondition;
import com.kanemullett.model.QueryConditionGroup;
import com.kanemullett.model.QueryRequest;
import com.kanemullett.model.QueryResponse;
import com.kanemullett.model.Table;
import com.kanemullett.model.UpdateRequest;
import com.kanemullett.model.User;
import com.kanemullett.model.type.ConditionOperator;
import com.kanemullett.model.type.SqlOperator;
import com.kanemullett.util.DatabaseConstants;
import com.kanemullett.util.PredictorConstants;

@Service
public class CompetitionService {
    private final DatabaseQueryService queryService;

    public CompetitionService(DatabaseQueryService queryService) {
        this.queryService = queryService;
    }

    public List<Competition> getCompetitions() {

        final QueryRequest<Competition> request = ImmutableQueryRequest.<Competition>builder()
            .table(Table.of(PredictorConstants.PREDICTOR_SCHEMA, Competition.TARGET_TABLE))
            .recordClass(Competition.class)
            .build();

        final QueryResponse<Competition> response = queryService.retrieveRecords(request);

        return response.getRecords();
    }

    public List<Competition> createCompetitions(List<Competition> competitions) {
        final UpdateRequest<Competition> request = ImmutableUpdateRequest.<Competition>builder()
            .operation(SqlOperator.INSERT)
            .table(Table.of(PredictorConstants.PREDICTOR_SCHEMA, Competition.TARGET_TABLE))
            .records(competitions)
            .recordClass(Competition.class)
            .build();

        queryService.updateRecords(request);

        return competitions;
    }

    public List<Competition> updateCompetitions(List<CompetitionUpdate> competitions) {
        final UpdateRequest<CompetitionUpdate> request = ImmutableUpdateRequest.<CompetitionUpdate>builder()
            .operation(SqlOperator.UPDATE)
            .table(Table.of(PredictorConstants.PREDICTOR_SCHEMA, Competition.TARGET_TABLE))
            .records(competitions)
            .recordClass(CompetitionUpdate.class)
            .build();

        queryService.updateRecords(request);

        final QueryRequest<Competition> updatedRequest = ImmutableQueryRequest.<Competition>builder()
            .table(Table.of(PredictorConstants.PREDICTOR_SCHEMA, Competition.TARGET_TABLE))
            .conditionGroup(QueryConditionGroup.of(
                ImmutableQueryCondition.builder()
                    .column(Column.of(DatabaseConstants.ID))
                    .operator(ConditionOperator.IN)
                    .value(competitions.stream()
                        .map(CompetitionUpdate::getId)
                        .toList())
                    .build()
            ))
            .recordClass(Competition.class)
            .build();

        final QueryResponse<Competition> response = queryService.retrieveRecords(updatedRequest);

        return response.getRecords();
    }

    public Competition getCompetitionById(String competitionId) {
        final QueryRequest<Competition> request = ImmutableQueryRequest.<Competition>builder()
            .table(Table.of(PredictorConstants.PREDICTOR_SCHEMA, Competition.TARGET_TABLE))
            .conditionGroup(QueryConditionGroup.of(
                QueryCondition.of(
                    Column.of(DatabaseConstants.ID),
                    competitionId
                )
            ))
            .recordClass(Competition.class)
            .build();

        final QueryResponse<Competition> response = queryService.retrieveRecords(request);

        if (response.getRecordCount() == 0 || response.getRecords() == null) {
            throw new ResponseStatusException(HttpStatus.NOT_FOUND, "No competitions found with a matching id.");
        }

        return response.getRecords().get(0);
    }

    public void deleteCompetitionById(String competitionId) {
        final UpdateRequest<Competition> request = ImmutableUpdateRequest.<Competition>builder()
            .operation(SqlOperator.DELETE)
            .table(Table.of(PredictorConstants.PREDICTOR_SCHEMA, Competition.TARGET_TABLE))
            .conditionGroup(QueryConditionGroup.of(
                QueryCondition.of(
                    Column.of(DatabaseConstants.ID),
                    competitionId
                )
            ))
            .build();

        queryService.updateRecords(request);
    }

    public void addUsersToCompetition(String competitionId, List<String> usernames) {
        getCompetitionById(competitionId);

        final QueryRequest<User> userRequest = ImmutableQueryRequest.<User>builder()
            .table(Table.of(PredictorConstants.PREDICTOR_SCHEMA, User.TARGET_TABLE))
            .conditionGroup(QueryConditionGroup.of(
                ImmutableQueryCondition.builder()
                    .column(Column.of(DatabaseConstants.ID))
                    .operator(ConditionOperator.IN)
                    .value(usernames)
                    .build()
            ))
            .recordClass(User.class)
            .build();

        // TODO: Consider replacing this with a call to UsersService when it's migrated.
        final QueryResponse<User> userResponse = queryService.retrieveRecords(userRequest);

        if (usernames.size() > userResponse.getRecordCount()) {
            final List<String> notExists = usernames.stream()
                .filter(username -> !userResponse.getRecords().stream()
                    .map(User::getId)
                    .toList().contains(username))
                .toList();

            throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "No users found with usernames: " + notExists);
        }

        final QueryRequest<CompetitionUser> existsRequest = ImmutableQueryRequest.<CompetitionUser>builder()
            .table(Table.of(PredictorConstants.PREDICTOR_SCHEMA, CompetitionUser.TARGET_TABLE))
            .conditionGroup(QueryConditionGroup.of(
                QueryCondition.of(
                    Column.of(CompetitionUser.COMPETITION_ID_COLUMN),
                    competitionId
                ),
                ImmutableQueryCondition.builder()
                    .column(Column.of(CompetitionUser.USERNAME_COLUMN))
                    .operator(ConditionOperator.IN)
                    .value(usernames)
                    .build()
            ))
            .recordClass(CompetitionUser.class)
            .build();

        final QueryResponse<CompetitionUser> existsResponse = queryService.retrieveRecords(existsRequest);

        if (existsResponse.getRecordCount() > 0) {
            final List<String> exists = existsResponse.getRecords().stream()
                .map(CompetitionUser::getUsername)
                .toList();

            throw new ResponseStatusException(HttpStatus.CONFLICT, "Users already assigned to this competition: " + exists);
        }

        final List<CompetitionUser> competitionUsers = usernames.stream()
            .map(username -> (CompetitionUser) ImmutableCompetitionUser.builder()
                .competitionId(competitionId)
                .username(username)
                .build())
            .toList();

        final UpdateRequest<CompetitionUser> insertRequest = ImmutableUpdateRequest.<CompetitionUser>builder()
            .operation(SqlOperator.INSERT)
            .table(Table.of(PredictorConstants.PREDICTOR_SCHEMA, CompetitionUser.TARGET_TABLE))
            .records(competitionUsers)
            .build();

        queryService.updateRecords(insertRequest);
    }

    public void removeUserFromCompetition(String competitionId, String username) {
        getCompetitionById(competitionId);

        final QueryRequest<User> userRequest = ImmutableQueryRequest.<User>builder()
            .table(Table.of(PredictorConstants.PREDICTOR_SCHEMA, User.TARGET_TABLE))
            .conditionGroup(QueryConditionGroup.of(
                QueryCondition.of(
                    Column.of(DatabaseConstants.ID),
                    username
                )
            ))
            .recordClass(User.class)
            .build();

        // TODO: Consider replacing this with a call to UsersService when it's migrated.
        final QueryResponse<User> userResponse = queryService.retrieveRecords(userRequest);

        if (userResponse.getRecordCount() == 0) {
            throw new ResponseStatusException(HttpStatus.NOT_FOUND, "No users found with a matching username.");
        }

        final UpdateRequest<?> deleteRequest = ImmutableUpdateRequest.builder()
            .operation(SqlOperator.DELETE)
            .table(Table.of(PredictorConstants.PREDICTOR_SCHEMA, CompetitionUser.TARGET_TABLE))
            .conditionGroup(QueryConditionGroup.of(
                QueryCondition.of(Column.of(CompetitionUser.COMPETITION_ID_COLUMN), competitionId),
                QueryCondition.of(Column.of(CompetitionUser.USERNAME_COLUMN), username)
            ))
            .build();

        queryService.updateRecords(deleteRequest);
    }
}
