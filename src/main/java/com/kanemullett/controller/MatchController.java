package com.kanemullett.controller;

import java.util.List;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import com.kanemullett.model.Match;
import com.kanemullett.model.MatchUpdate;
import com.kanemullett.service.MatchService;

@RestController
@RequestMapping("/tournaments/{tournamentId}/matches")
public class MatchController {

    private final MatchService matchService;

    public MatchController(MatchService matchService) {
        this.matchService = matchService;
    }

    @GetMapping
    public List<Match> getMatches(
            @PathVariable String tournamentId,
            @RequestParam(required = false) String groupId,
            @RequestParam(required = false) Integer groupMatchDay,
            @RequestParam(required = false) String roundId) {

        return matchService.getMatches(tournamentId, groupId, groupMatchDay, roundId);
    }

    @PutMapping
    public List<Match> updateMatches(
            @PathVariable String tournamentId,
            @RequestBody List<MatchUpdate> updates) {

        return matchService.updateMatches(tournamentId, updates);
    }

    @GetMapping("/{matchId}")
    public Match getMatchById(
            @PathVariable String tournamentId,
            @PathVariable String matchId) {

        return matchService.getMatchById(tournamentId, matchId);
    }
}
