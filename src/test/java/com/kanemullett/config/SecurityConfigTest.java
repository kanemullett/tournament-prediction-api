package com.kanemullett.config;

import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.options;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.content;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.header;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.context.annotation.Import;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.security.oauth2.jwt.BadJwtException;
import org.springframework.security.oauth2.jwt.Jwt;
import org.springframework.security.oauth2.jwt.JwtDecoder;
import org.springframework.test.context.TestPropertySource;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

/**
 * Runs requests through the real security filter chain. The token decoder is mocked, so these tests
 * cover what happens once a token is (or isn't) accepted; Spring Boot's own validators check the
 * signature, issuer and audience.
 */
@WebMvcTest(controllers = SecurityConfigTest.TestController.class)
@Import({SecurityConfig.class, CorsConfig.class, SecurityConfigTest.TestController.class})
@TestPropertySource(properties = "cors.allowed-origins=http://localhost:3000")
class SecurityConfigTest {

    private static final String VALID_TOKEN = "valid-token";

    @Autowired
    private MockMvc mvc;

    @MockBean
    private JwtDecoder jwtDecoder;

    @RestController
    static class TestController {

        @GetMapping("/protected")
        String roles(Authentication authentication) {
            return authentication.getAuthorities().stream()
                .map(GrantedAuthority::getAuthority)
                .sorted()
                .collect(Collectors.joining(","));
        }
    }

    @Test
    void shouldRejectRequestsWithoutToken() throws Exception {
        mvc.perform(get("/protected"))
            .andExpect(status().isUnauthorized())
            .andExpect(header().string("WWW-Authenticate", "Bearer"));
    }

    @Test
    void shouldRejectRequestsWithInvalidToken() throws Exception {
        // Given
        when(jwtDecoder.decode(anyString())).thenThrow(new BadJwtException("Invalid audience"));

        // When / Then
        mvc.perform(get("/protected").header("Authorization", "Bearer forged-token"))
            .andExpect(status().isUnauthorized());
    }

    @Test
    void shouldAcceptValidTokenAndMapRealmRoles() throws Exception {
        // Given
        when(jwtDecoder.decode(VALID_TOKEN)).thenReturn(Jwt.withTokenValue(VALID_TOKEN)
            .header("alg", "RS256")
            .subject("user-id")
            .claim("realm_access", Map.of("roles", List.of("player", "admin")))
            .build());

        // When / Then
        mvc.perform(get("/protected").header("Authorization", "Bearer " + VALID_TOKEN))
            .andExpect(status().isOk())
            .andExpect(content().string("ROLE_admin,ROLE_player"));
    }

    @Test
    void shouldLetPublicPathsThroughWithoutToken() throws Exception {
        // Nothing is mapped at these paths in this test, so getting past security means a 404.
        for (String path : List.of("/livez", "/readyz", "/actuator/health/liveness", "/swagger-ui/index.html", "/v3/api-docs")) {
            mvc.perform(get(path)).andExpect(status().isNotFound());
        }
    }

    @Test
    void shouldAnswerCorsPreflightWithoutToken() throws Exception {
        mvc.perform(options("/protected")
                .header("Origin", "http://localhost:3000")
                .header("Access-Control-Request-Method", "GET")
                .header("Access-Control-Request-Headers", "authorization"))
            .andExpect(status().isOk())
            .andExpect(header().string("Access-Control-Allow-Origin", "http://localhost:3000"));
    }

    @Test
    void shouldRejectCorsPreflightFromUnknownOrigin() throws Exception {
        mvc.perform(options("/protected")
                .header("Origin", "http://evil.example")
                .header("Access-Control-Request-Method", "GET"))
            .andExpect(status().isForbidden());
    }
}
