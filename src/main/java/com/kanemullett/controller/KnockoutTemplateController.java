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

import com.kanemullett.model.KnockoutTemplate;
import com.kanemullett.service.KnockoutTemplateService;

@RestController
@RequestMapping("knockout-templates")
public class KnockoutTemplateController {

    private final KnockoutTemplateService knockoutTemplateService;

    public KnockoutTemplateController(KnockoutTemplateService knockoutTemplateService) {
        this.knockoutTemplateService = knockoutTemplateService;
    }

    @GetMapping
    public List<KnockoutTemplate> getKnockoutTemplates() {
        return knockoutTemplateService.getKnockoutTemplates();
    }

    @PostMapping
    public List<KnockoutTemplate> createKnockoutTemplates(@RequestBody List<KnockoutTemplate> knockoutTemplates) {
        return knockoutTemplateService.createKnockoutTemplates(knockoutTemplates);
    }

    @GetMapping("/{knockoutTemplateId}")
    public KnockoutTemplate getKnockoutTemplateById(@PathVariable String knockoutTemplateId) {
        return knockoutTemplateService.getKnockoutTemplateById(knockoutTemplateId);
    }

    @DeleteMapping("/{knockoutTemplateId}")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    public void deleteKnockoutTemplateById(@PathVariable String knockoutTemplateId) {
        knockoutTemplateService.deleteKnockoutTemplateById(knockoutTemplateId);
    }
}
