package com.kanemullett.config;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.util.List;
import java.util.Map;

import org.junit.jupiter.api.Test;
import org.springframework.web.cors.CorsConfiguration;
import org.springframework.web.servlet.config.annotation.CorsRegistry;

class CorsConfigTest {

    @Test
    void shouldParseCommaSeparatedOrigins() {
        assertEquals(
            List.of("http://localhost:3000", "https://example.com"),
            CorsConfig.parseOrigins(" http://localhost:3000 , https://example.com,")
        );
    }

    @Test
    void shouldParseEmptyOrNullOriginsAsEmpty() {
        assertEquals(List.of(), CorsConfig.parseOrigins(""));
        assertEquals(List.of(), CorsConfig.parseOrigins(null));
    }

    @Test
    void shouldRegisterAllowedOriginsForAllPaths() {
        // Given
        final CorsConfig corsConfig = new CorsConfig("http://localhost:3000,https://example.com");
        final InspectableCorsRegistry registry = new InspectableCorsRegistry();

        // When
        corsConfig.addCorsMappings(registry);

        // Then
        final CorsConfiguration configuration = registry.configurations().get("/**");
        assertEquals(List.of("http://localhost:3000", "https://example.com"), configuration.getAllowedOrigins());
        assertEquals(List.of("GET", "POST", "PUT", "DELETE", "OPTIONS"), configuration.getAllowedMethods());
        assertEquals(List.of("*"), configuration.getAllowedHeaders());
    }

    @Test
    void shouldNotRegisterMappingsWhenNoOriginsConfigured() {
        // Given
        final CorsConfig corsConfig = new CorsConfig("");
        final InspectableCorsRegistry registry = new InspectableCorsRegistry();

        // When
        corsConfig.addCorsMappings(registry);

        // Then
        assertTrue(registry.configurations().isEmpty());
    }

    private static class InspectableCorsRegistry extends CorsRegistry {
        Map<String, CorsConfiguration> configurations() {
            return getCorsConfigurations();
        }
    }
}
