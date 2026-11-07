package com.kanemullett.config;

import static org.springframework.security.config.Customizer.withDefaults;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.config.annotation.web.configurers.AbstractHttpConfigurer;
import org.springframework.security.config.http.SessionCreationPolicy;
import org.springframework.security.oauth2.server.resource.authentication.JwtAuthenticationConverter;
import org.springframework.security.web.SecurityFilterChain;

/**
 * Every endpoint needs a valid Keycloak access token, apart from health checks and the API docs.
 *
 * <p>Token checks (signature, expiry, issuer and the {@code predictor-api} audience) are set up by
 * Spring Boot from the {@code spring.security.oauth2.resourceserver.jwt.*} properties.
 */
@Configuration
@EnableWebSecurity
public class SecurityConfig {

    static final String[] PUBLIC_PATHS = {
        "/livez",
        "/readyz",
        "/actuator/health/**",
        "/swagger-ui.html",
        "/swagger-ui/**",
        "/v3/api-docs/**",
        "/error"
    };

    @Bean
    public SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception {
        return http
            // Uses the origins from CorsConfig, and answers preflight requests before authentication.
            .cors(withDefaults())
            // Tokens are sent in the Authorization header, never in cookies, so CSRF doesn't apply.
            .csrf(AbstractHttpConfigurer::disable) // NOSONAR java:S4502 - stateless bearer-token API, no cookies
            .sessionManagement(session -> session.sessionCreationPolicy(SessionCreationPolicy.STATELESS))
            .authorizeHttpRequests(auth -> auth
                .requestMatchers(PUBLIC_PATHS).permitAll()
                .anyRequest().authenticated())
            .oauth2ResourceServer(oauth2 -> oauth2.jwt(withDefaults()))
            .build();
    }

    /** Makes Keycloak realm roles available as {@code ROLE_<name>}, e.g. for {@code hasRole("admin")}. */
    @Bean
    public JwtAuthenticationConverter jwtAuthenticationConverter() {
        final JwtAuthenticationConverter converter = new JwtAuthenticationConverter();
        converter.setJwtGrantedAuthoritiesConverter(new KeycloakRealmRoleConverter());
        return converter;
    }
}
