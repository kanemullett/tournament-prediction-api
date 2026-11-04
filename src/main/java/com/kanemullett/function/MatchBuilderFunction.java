package com.kanemullett.function;

import java.sql.Timestamp;
import java.util.Map;
import java.util.function.Function;

import org.springframework.stereotype.Component;

import com.kanemullett.model.DatabaseRecord;
import com.kanemullett.model.Group;
import com.kanemullett.model.ImmutableGroup;
import com.kanemullett.model.ImmutableMatch;
import com.kanemullett.model.ImmutableMatchOutcome;
import com.kanemullett.model.ImmutableRound;
import com.kanemullett.model.ImmutableTeam;
import com.kanemullett.model.Match;
import com.kanemullett.model.MatchOutcome;
import com.kanemullett.model.MatchRecord;
import com.kanemullett.model.Result;
import com.kanemullett.model.Round;
import com.kanemullett.model.Team;
import com.kanemullett.model.type.Confederation;
import com.kanemullett.model.type.Winner;

@Component
public class MatchBuilderFunction implements Function<DatabaseRecord, Match> {

    @Override
    public Match apply(DatabaseRecord databaseRecord) {
        final Map<String, Object> recordData = databaseRecord.getData();

        final Team home = recordData.get("homeId") != null ?
            ImmutableTeam.builder()
                .id((String) recordData.get("homeId"))
                .name((String) recordData.get("homeName"))
                .imagePath((String) recordData.get("homeImagePath"))
                .confederation(Confederation.valueOf((String) recordData.get("homeConfederation")))
                .build() : null;

        final Team away = recordData.get("awayId") != null ?
            ImmutableTeam.builder()
                .id((String) recordData.get("awayId"))
                .name((String) recordData.get("awayName"))
                .imagePath((String) recordData.get("awayImagePath"))
                .confederation(Confederation.valueOf((String) recordData.get("awayConfederation")))
                .build() : null;

        final Winner winner = recordData.get(Result.PENALTIES_WINNER_COLUMN) != null ? Winner.valueOf((String) recordData.get(Result.PENALTIES_WINNER_COLUMN)) : null;
        final MatchOutcome result = recordData.get(Result.HOME_GOALS_COLUMN) != null
            && recordData.get(Result.AWAY_GOALS_COLUMN) != null ?
                ImmutableMatchOutcome.builder()
                    .homeGoals((Integer) recordData.get(Result.HOME_GOALS_COLUMN))
                    .awayGoals((Integer) recordData.get(Result.AWAY_GOALS_COLUMN))
                    .isAfterExtraTime((Boolean) recordData.get(Result.AFTER_EXTRA_TIME_COLUMN))
                    .isAfterPenalties((Boolean) recordData.get(Result.AFTER_PENALTIES_COLUMN))
                    .winner(winner)
                    .build() : null;

        final Group group = recordData.get(MatchRecord.GROUP_ID_COLUMN) != null ?
            ImmutableGroup.builder()
                .id((String) recordData.get(MatchRecord.GROUP_ID_COLUMN))
                .name((String) recordData.get("groupName"))
                .build() : null;

        final Round round = recordData.get(MatchRecord.ROUND_ID_COLUMN) != null ?
            ImmutableRound.builder()
                .id((String) recordData.get(MatchRecord.ROUND_ID_COLUMN))
                .name((String) recordData.get("roundName"))
                .teamCount((Integer) recordData.get(Round.TEAM_COUNT_COLUMN))
                .roundOrder((Integer) recordData.get(Round.ROUND_ORDER_COLUMN))
                .twoLegs((Boolean) recordData.get(Round.TWO_LEGS_COLUMN))
                .extraTime((Boolean) recordData.get(Round.EXTRA_TIME_COLUMN))
                .awayGoals((Boolean) recordData.get("awayGoalsDecider"))
                .build() : null;

        return ImmutableMatch.builder()
            .id((String) recordData.get("matchId"))
            .homeTeam(home)
            .awayTeam(away)
            .kickoff(((Timestamp) recordData.get(MatchRecord.KICKOFF_COLUMN)).toLocalDateTime())
            .groupMatchDay((Integer) recordData.get(MatchRecord.GROUP_MATCH_DAY_COLUMN))
            .group(group)
            .round(round)
            .result(result)
            .build();
    }
}
