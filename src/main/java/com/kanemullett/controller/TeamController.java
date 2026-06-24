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
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestController;

import com.kanemullett.model.Team;
import com.kanemullett.model.TeamUpdate;
import com.kanemullett.model.type.Confederation;
import com.kanemullett.service.TeamService;

@RestController
@RequestMapping("/teams")
public class TeamController {

    private final TeamService teamService;

    public TeamController(TeamService teamService) {
        this.teamService = teamService;
    }

    @GetMapping
    public List<Team> getTeams(@RequestParam(required = false) Confederation confederation, @RequestParam(required = false) String tournamentId) {
        return teamService.getTeams(confederation, tournamentId);
    }

    @PostMapping
    public List<Team> createTeams(@RequestBody List<Team> teams) {
        return teamService.createTeams(teams);
    }

    @PutMapping
    public List<Team> updateTeams(@RequestBody List<TeamUpdate> teamUpdates) {
        return teamService.updateTeams(teamUpdates);
    }

    @GetMapping("/{teamId}")
    public Team getTeamById(@PathVariable String teamId) {
        return teamService.getTeamById(teamId);
    }

    @DeleteMapping("/{teamId}")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    public void deleteTeamById(@PathVariable String teamId) {
        teamService.deleteTeamById(teamId);
    }
}
