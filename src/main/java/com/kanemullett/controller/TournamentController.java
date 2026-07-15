package com.kanemullett.controller;

import java.util.List;

import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestController;

import com.kanemullett.model.Tournament;
import com.kanemullett.model.TournamentUpdate;
import com.kanemullett.service.TournamentService;

@RestController
@RequestMapping("/tournaments")
public class TournamentController {

    private final TournamentService tournamentService;

    public TournamentController(TournamentService tournamentService) {
        this.tournamentService = tournamentService;
    }

    @GetMapping
    public List<Tournament> getTournaments() {
        return tournamentService.getTournaments();
    }

    @PostMapping
    public List<Tournament> createTournaments(List<Tournament> tournaments) {
        return tournamentService.createTournaments(tournaments);
    }

    @PutMapping
    public List<Tournament> updateTournaments(List<TournamentUpdate> tournamentUpdates) {
        return tournamentService.updateTournaments(tournamentUpdates);
    }

    @GetMapping("/{tournamentId}")
    public Tournament getTournamentById(String tournamentId) {
        return tournamentService.getTournamentById(tournamentId);
    }

    @DeleteMapping("/{tournamentId}")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    public void deleteTournamentById(String tournamentId) {
        tournamentService.deleteTournamentById(tournamentId);
    }
}
