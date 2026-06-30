package com.kanemullett.controller;

import java.util.List;

import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestController;

import com.kanemullett.model.LeagueTemplate;
import com.kanemullett.service.LeagueTemplateService;

@RestController
@RequestMapping("league-templates")
public class LeagueTemplateController {

    private final LeagueTemplateService leagueTemplateService;

    public LeagueTemplateController(LeagueTemplateService leagueTemplateService) {
        this.leagueTemplateService = leagueTemplateService;
    }

    @GetMapping
    public List<LeagueTemplate> getLeagueTemplates() {
        return leagueTemplateService.getLeagueTemplates();
    }

    @PostMapping
    public List<LeagueTemplate> createLeagueTemplates(List<LeagueTemplate> leagueTemplates) {
        return leagueTemplateService.createLeagueTemplates(leagueTemplates);
    }

    @GetMapping("/{leagueTemplateId}")
    public LeagueTemplate getLeagueTemplateById(String leagueTemplateId) {
        return leagueTemplateService.getLeagueTemplateById(leagueTemplateId);
    }

    @DeleteMapping("/{leagueTemplateId}")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    public void deleteLeagueTemplateById(String leagueTemplateId) {
        leagueTemplateService.deleteLeagueTemplateById(leagueTemplateId);
    }
}
