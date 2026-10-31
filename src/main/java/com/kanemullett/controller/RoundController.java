package com.kanemullett.controller;

import java.util.List;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.kanemullett.model.Round;
import com.kanemullett.model.RoundUpdate;
import com.kanemullett.service.RoundService;

@RestController
@RequestMapping("/tournaments/{tournamentId}/rounds")
public class RoundController {

    private final RoundService roundService;

    public RoundController(RoundService roundService) {
        this.roundService = roundService;
    }

    @GetMapping
    public List<Round> getRounds(@PathVariable String tournamentId) {
        return roundService.getRounds(tournamentId);
    }

    @PutMapping
    public List<Round> updateRounds(@PathVariable String tournamentId, @RequestBody List<RoundUpdate> updates) {
        return roundService.updateRounds(tournamentId, updates);
    }

    @GetMapping("/{roundId}")
    public Round getRoundById(@PathVariable String tournamentId, @PathVariable String roundId) {
        return roundService.getRoundById(tournamentId, roundId);
    }
}
