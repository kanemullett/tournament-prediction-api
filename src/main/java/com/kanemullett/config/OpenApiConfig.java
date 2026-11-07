package com.kanemullett.config;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import io.swagger.v3.oas.models.Components;
import io.swagger.v3.oas.models.OpenAPI;
import io.swagger.v3.oas.models.security.OAuthFlow;
import io.swagger.v3.oas.models.security.OAuthFlows;
import io.swagger.v3.oas.models.security.Scopes;
import io.swagger.v3.oas.models.security.SecurityRequirement;
import io.swagger.v3.oas.models.security.SecurityScheme;

/**
 * Adds a Keycloak login to Swagger UI. Its "Authorize" button sends you to the Keycloak login page,
 * and "Try it out" requests then carry your access token.
 *
 * <p>Only the authorization code flow is described. Pointing Swagger UI at Keycloak's discovery
 * document instead makes it offer every grant Keycloak supports, most of which the client rejects.
 */
@Configuration
public class OpenApiConfig {

    static final String SCHEME_NAME = "keycloak";

    @Bean
    public OpenAPI openApi(@Value("${spring.security.oauth2.resourceserver.jwt.issuer-uri}") String issuerUri) {
        final OAuthFlow authorizationCode = new OAuthFlow()
            .authorizationUrl(issuerUri + "/protocol/openid-connect/auth")
            .tokenUrl(issuerUri + "/protocol/openid-connect/token")
            .scopes(new Scopes().addString("openid", "Sign in with your Providentia account"));

        final SecurityScheme keycloak = new SecurityScheme()
            .type(SecurityScheme.Type.OAUTH2)
            .flows(new OAuthFlows().authorizationCode(authorizationCode));

        return new OpenAPI()
            .components(new Components().addSecuritySchemes(SCHEME_NAME, keycloak))
            .addSecurityItem(new SecurityRequirement().addList(SCHEME_NAME, "openid"));
    }
}
