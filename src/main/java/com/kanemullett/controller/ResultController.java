package com.kanemullett.controller;

import java.util.List;

import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.kanemullett.model.Result;
import com.kanemullett.service.ResultService;

@RestController
@RequestMapping("/tournaments/{tournamentId}/results")
public class ResultController {

    private final ResultService resultService;

    public ResultController(ResultService resultService) {
        this.resultService = resultService;
    }

    @PostMapping
    public List<Result> createResults(@PathVariable String tournamentId, @RequestBody List<Result> results) {
        return resultService.createResults(tournamentId, results);
    }

    @PutMapping
    public List<Result> updateResults(@PathVariable String tournamentId, @RequestBody List<Result> updates) {
        return resultService.updateResults(tournamentId, updates);
    }

    @DeleteMapping("/{resultId}")
    public void deleteResultById(@PathVariable String tournamentId, @PathVariable String resultId) {
        resultService.deleteResultById(tournamentId, resultId);
    }
}
