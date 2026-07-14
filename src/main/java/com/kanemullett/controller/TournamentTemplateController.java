package com.kanemullett.controller;

import java.util.List;

import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestController;

import com.kanemullett.model.TournamentTemplate;
import com.kanemullett.model.TournamentTemplateRecord;
import com.kanemullett.service.TournamentTemplateService;

@RestController
@RequestMapping("tournament-templates")
public class TournamentTemplateController {

    private final TournamentTemplateService tournamentTemplateService;

    public TournamentTemplateController(TournamentTemplateService tournamentTemplateService) {
        this.tournamentTemplateService = tournamentTemplateService;
    }

    @GetMapping
    public List<TournamentTemplate> getTournamentTemplates() {
        return tournamentTemplateService.getTournamentTemplates();
    }

    @PostMapping
    public List<TournamentTemplate> createTournamentTemplates(@RequestBody List<TournamentTemplateRecord> tournamentTemplates) {
        return tournamentTemplateService.createTournamentTemplates(tournamentTemplates);
    }

    @GetMapping("/{tournamentTemplateId}")
    public TournamentTemplate getTournamentTemplateById(@PathVariable String tournamentTemplateId) {
        return tournamentTemplateService.getTournamentTemplateById(tournamentTemplateId);
    }

    @DeleteMapping("/{tournamentTemplateId}")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    public void deleteTournamentTemplateById(@PathVariable String tournamentTemplateId) {
        tournamentTemplateService.deleteTournamentTemplateById(tournamentTemplateId);
    }
}
