package com.kanemullett.service;

import java.util.List;

import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Service;
import org.springframework.web.server.ResponseStatusException;

import com.kanemullett.model.Column;
import com.kanemullett.model.DatabaseRecord;
import com.kanemullett.model.ImmutableQueryCondition;
import com.kanemullett.model.ImmutableQueryRequest;
import com.kanemullett.model.ImmutableTableJoin;
import com.kanemullett.model.ImmutableUpdateRequest;
import com.kanemullett.model.QueryCondition;
import com.kanemullett.model.QueryConditionGroup;
import com.kanemullett.model.QueryRequest;
import com.kanemullett.model.QueryResponse;
import com.kanemullett.model.Round;
import com.kanemullett.model.RoundUpdate;
import com.kanemullett.model.Table;
import com.kanemullett.model.Tournament;
import com.kanemullett.model.TournamentTemplateRecord;
import com.kanemullett.model.UpdateRequest;
import com.kanemullett.model.type.ConditionOperator;
import com.kanemullett.model.type.JoinType;
import com.kanemullett.model.type.SqlOperator;
import com.kanemullett.util.DatabaseConstants;
import com.kanemullett.util.PredictorConstants;

import jakarta.annotation.Nullable;

@Service
public class RoundService {

    private final DatabaseQueryService queryService;

    private static final String TOURNAMENTS_TABLE_ALIAS = "to";
    private static final String TOURNAMENT_TEMPLATES_TABLE_ALIAS = "tt";

    public RoundService(DatabaseQueryService queryService) {
        this.queryService = queryService;
    }

    public List<Round> getRounds(String tournamentId) {
        verifyTournament(tournamentId);
        return retrieveRounds(tournamentId);
    }

    public List<Round> updateRounds(String tournamentId, List<RoundUpdate> rounds) {
        verifyTournament(tournamentId);

        final UpdateRequest<RoundUpdate> updateRequest = ImmutableUpdateRequest.<RoundUpdate>builder()
            .operation(SqlOperator.UPDATE)
            .table(Table.of(PredictorConstants.PREDICTOR_SCHEMA, Round.getTargetTable(tournamentId)))
            .records(rounds)
            .recordClass(RoundUpdate.class)
            .build();

        queryService.updateRecords(updateRequest);

        final QueryConditionGroup conditionGroup = QueryConditionGroup.of(
            ImmutableQueryCondition.builder()
                .column(Column.of(DatabaseConstants.ID))
                .operator(ConditionOperator.IN)
                .value(rounds.stream()
                    .map(RoundUpdate::getId)
                    .toList())
                .build()
        );

        return retrieveRounds(tournamentId, conditionGroup);
    }

    public Round getRoundById(String tournamentId, String roundId) {
        verifyTournament(tournamentId);
        verifyRound(tournamentId, roundId);

        return retrieveRound(tournamentId, roundId);
    }

    private void verifyTournament(String tournamentId) {
        final QueryRequest<DatabaseRecord> queryRequest = ImmutableQueryRequest.builder()
            .columns(List.of(
                Column.of(TOURNAMENTS_TABLE_ALIAS, DatabaseConstants.ID),
                Column.of(TOURNAMENT_TEMPLATES_TABLE_ALIAS, TournamentTemplateRecord.KNOCKOUT_TEMPLATE_ID_COLUMN)
            ))
            .table(Table.of(PredictorConstants.PREDICTOR_SCHEMA, Tournament.TARGET_TABLE, TOURNAMENTS_TABLE_ALIAS))
            .joins(List.of(ImmutableTableJoin.builder()
                .table(Table.of(
                    PredictorConstants.PREDICTOR_SCHEMA,
                    TournamentTemplateRecord.TARGET_TABLE,
                    TOURNAMENT_TEMPLATES_TABLE_ALIAS
                ))
                .joinType(JoinType.INNER)
                .joinCondition(QueryCondition.of(
                    Column.of(TOURNAMENTS_TABLE_ALIAS, Tournament.TEMPLATE_ID_COLUMN),
                    Column.of(TOURNAMENT_TEMPLATES_TABLE_ALIAS, DatabaseConstants.ID)
                ))
                .build()
            ))
            .conditionGroup(QueryConditionGroup.of(
                QueryCondition.of(
                    Column.of(TOURNAMENTS_TABLE_ALIAS, DatabaseConstants.ID),
                    tournamentId
                )
            ))
            .recordClass(DatabaseRecord.class)
            .build();

        final QueryResponse<DatabaseRecord> queryResponse = queryService.retrieveRecords(queryRequest);

        if (queryResponse.getRecordCount() == 0) {
            throw new ResponseStatusException(HttpStatus.NOT_FOUND, "No tournaments found with a matching id.");
        }

        final DatabaseRecord tournamentRecord = queryResponse.getRecords().get(0);

        if (tournamentRecord.getData().get(TournamentTemplateRecord.KNOCKOUT_TEMPLATE_ID_COLUMN) == null) {
            throw new ResponseStatusException(HttpStatus.NOT_FOUND, "The tournament with the supplied id does not have a knockout stage.");
        }
    }

    private void verifyRound(String tournamentId, String roundId) {
        final QueryRequest<Round> queryRequest = ImmutableQueryRequest.<Round>builder()
            .table(Table.of(PredictorConstants.PREDICTOR_SCHEMA, Round.getTargetTable(tournamentId)))
            .conditionGroup(QueryConditionGroup.of(
                QueryCondition.of(
                    Column.of(DatabaseConstants.ID),
                    roundId
                )
            ))
            .recordClass(Round.class)
            .build();

        final QueryResponse<Round> queryResponse = queryService.retrieveRecords(queryRequest);

        if (queryResponse.getRecordCount() == 0) {
            throw new ResponseStatusException(HttpStatus.NOT_FOUND, "No rounds found with a matching id.");
        }
    }

    private Round retrieveRound(String tournamentId, String roundId) {
        final QueryConditionGroup conditionGroup = QueryConditionGroup.of(
            QueryCondition.of(
                Column.of(DatabaseConstants.ID),
                roundId
            )
        );

        return retrieveRounds(tournamentId, conditionGroup).get(0);
    }

    private List<Round> retrieveRounds(String tournamentId) {
        return retrieveRounds(tournamentId, null);
    }

    private List<Round> retrieveRounds(String tournamentId, @Nullable QueryConditionGroup conditionGroup) {

        final QueryRequest<Round> roundRequest = ImmutableQueryRequest.<Round>builder()
            .table(Table.of(PredictorConstants.PREDICTOR_SCHEMA, Round.getTargetTable(tournamentId)))
            .conditionGroup(conditionGroup)
            .recordClass(Round.class)
            .build();

        final QueryResponse<Round> roundResponse = queryService.retrieveRecords(roundRequest);

        return roundResponse.getRecords();
    }
}
