package com.kanemullett.controller;

import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

import org.junit.jupiter.api.Test;
import org.springframework.http.HttpStatus;
import org.springframework.web.server.ResponseStatusException;

import static org.mockito.ArgumentMatchers.anyList;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.Mockito.doThrow;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.when;

import com.kanemullett.model.ImmutableKnockoutTemplate;
import com.kanemullett.model.KnockoutTemplate;
import com.kanemullett.service.KnockoutTemplateService;

public class KnockoutTemplateControllerTest {

    private final KnockoutTemplateService service = mock(KnockoutTemplateService.class);

    private final KnockoutTemplateController controller = new KnockoutTemplateController(service);

    private static final KnockoutTemplate SIXTEEN_TEMPLATE = ImmutableKnockoutTemplate.builder()
        .id("c08fd796-7fea-40d9-9a0a-cb3a49cce2e4")
        .name("16-Team Single-Leg")
        .build();
    private static final KnockoutTemplate EIGHT_TEMPLATE = ImmutableKnockoutTemplate.builder()
        .id("6ee28143-1286-4618-a8b9-ad86d348ead1")
        .name("8-Team Double-Leg Away Goals")
        .build();

    @Test
    void shouldPassKnockoutTemplatesAsResponse() {
        // Given
        when(service.getKnockoutTemplates())
            .thenReturn(List.of(SIXTEEN_TEMPLATE, EIGHT_TEMPLATE));

        // When
        final List<KnockoutTemplate> knockoutTemplates = controller.getKnockoutTemplates();

        // Then
        assertEquals(2, knockoutTemplates.size());
        assertKnockoutTemplate(SIXTEEN_TEMPLATE, knockoutTemplates.get(0));
        assertKnockoutTemplate(EIGHT_TEMPLATE, knockoutTemplates.get(1));
    }

    @Test
    void shouldPassCreatedKnockoutTemplatesAsResponse() {
        // Given
        when(service.createKnockoutTemplates(anyList()))
            .thenReturn(List.of(SIXTEEN_TEMPLATE, EIGHT_TEMPLATE));

        // When
        final List<KnockoutTemplate> created = controller.createKnockoutTemplates(List.of(SIXTEEN_TEMPLATE, EIGHT_TEMPLATE));

        // Then
        assertEquals(2, created.size());
        assertKnockoutTemplate(SIXTEEN_TEMPLATE, created.get(0));
        assertKnockoutTemplate(EIGHT_TEMPLATE, created.get(1));
    }

    @Test
    void shouldPassFoundKnockoutTemplateAsResponse() {
        // Given
        when(service.getKnockoutTemplateById(anyString()))
            .thenReturn(EIGHT_TEMPLATE);

        // When
        final KnockoutTemplate knockoutTemplate = controller.getKnockoutTemplateById("c08fd796-7fea-40d9-9a0a-cb3a49cce2e4");

        // Then
        assertKnockoutTemplate(EIGHT_TEMPLATE, knockoutTemplate);
    }

    @Test
    void shouldPassErrorIfKnockoutTemplateNotFound() {
        // Given
        when(service.getKnockoutTemplateById(anyString()))
            .thenThrow(new ResponseStatusException(HttpStatus.NOT_FOUND, "No knockout templates found with a matching id."));

        // When
        final ResponseStatusException rse = assertThrows(ResponseStatusException.class, () -> controller.getKnockoutTemplateById("c08fd796-7fea-40d9-9a0a-cb3a49cce2e4"));

        // Then
        assertEquals(HttpStatus.NOT_FOUND, rse.getStatusCode());
        assertEquals("No knockout templates found with a matching id.", rse.getReason());
    }

    @Test
    void shouldPassErrorIfKnockoutTemplateIsBeingUsed() {
        // Given
        doThrow(new ResponseStatusException(HttpStatus.CONFLICT, "Cannot delete knockout template as it is part of an existing tournament template."))
            .when(service)
                .deleteKnockoutTemplateById(anyString());

        // When
        final ResponseStatusException rse = assertThrows(ResponseStatusException.class, () -> controller.deleteKnockoutTemplateById("c08fd796-7fea-40d9-9a0a-cb3a49cce2e4"));

        // Then
        assertEquals(HttpStatus.CONFLICT, rse.getStatusCode());
        assertEquals("Cannot delete knockout template as it is part of an existing tournament template.", rse.getReason());
    }

    private static void assertKnockoutTemplate(KnockoutTemplate expected, KnockoutTemplate actual) {
        assertEquals(expected.getId(), actual.getId());
        assertEquals(expected.getName(), actual.getName());
    }
}
