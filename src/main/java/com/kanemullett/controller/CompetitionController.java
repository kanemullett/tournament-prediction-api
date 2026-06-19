package com.kanemullett.controller;

import java.util.List;

import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestController;

import com.kanemullett.model.Competition;
import com.kanemullett.model.CompetitionUpdate;
import com.kanemullett.service.CompetitionService;

@RestController
@RequestMapping("/competitions")
public class CompetitionController {

    private final CompetitionService competitionService;

    public CompetitionController(CompetitionService competitionService) {
        this.competitionService = competitionService;
    }

    @GetMapping
    public List<Competition> getCompetitions() {
        return competitionService.getCompetitions();
    }

    @PostMapping
    public List<Competition> createCompetitions(@RequestBody List<Competition> competitions) {
        return competitionService.createCompetitions(competitions);
    }

    @PutMapping
    public List<Competition> updateCompetitions(@RequestBody List<CompetitionUpdate> competitionUpdates) {
        return competitionService.updateCompetitions(competitionUpdates);
    }

    @GetMapping("/{competitionId}")
    public Competition getCompetitionById(@PathVariable String competitionId) {
        return competitionService.getCompetitionById(competitionId);
    }

    @DeleteMapping("/{competitionId}")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    public void deleteCompetitionById(@PathVariable String competitionId) {
        competitionService.deleteCompetitionById(competitionId);
    }

    @PostMapping("/{competitionId}/users")
    @ResponseStatus(HttpStatus.CREATED)
    public void addUsersToCompetition(@PathVariable String competitionId, @RequestBody List<String> usernames) {
        competitionService.addUsersToCompetition(competitionId, usernames);
    }

    @DeleteMapping("/{competitionId}/users/{username}")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    public void removeUserFromCompetition(@PathVariable String competitionId, @PathVariable String username) {
        competitionService.removeUserFromCompetition(competitionId, username);
    }
}
