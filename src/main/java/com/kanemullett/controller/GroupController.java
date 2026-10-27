package com.kanemullett.controller;

import java.util.List;

import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.kanemullett.model.Group;
import com.kanemullett.model.GroupRecord;
import com.kanemullett.service.GroupService;

@RestController
@RequestMapping("/tournaments/{tournamentId}/groups")
public class GroupController {

    private final GroupService groupService;

    public GroupController(GroupService groupService) {
        this.groupService = groupService;
    }

    @GetMapping
    public List<Group> getGroups(@PathVariable String tournamentId) {
        return groupService.getGroups(tournamentId);
    }

    @PutMapping
    public List<Group> updateGroups(@PathVariable String tournamentId, @RequestBody List<GroupRecord> updates) {
        return groupService.updateGroups(tournamentId, updates);
    }

    @GetMapping("/{groupId}")
    public Group getGroupById(@PathVariable String tournamentId, @PathVariable String groupId) {
        return groupService.getGroupById(tournamentId, groupId);
    }

    @PostMapping("/{groupId}/teams")
    public Group addTeamsToGroup(@PathVariable String tournamentId, @PathVariable String groupId, @RequestBody List<String> teamIds) {
        return groupService.addTeamsToGroup(tournamentId, groupId, teamIds);
    }

    @DeleteMapping("/{groupId}/teams/{teamId}")
    public Group removeTeamFromGroup(@PathVariable String tournamentId, @PathVariable String groupId, @PathVariable String teamId) {
        return groupService.removeTeamFromGroup(tournamentId, groupId, teamId);
    }
}
