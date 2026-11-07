package com.kanemullett.config;

import static org.junit.jupiter.api.Assertions.assertEquals;

import java.util.Collection;
import java.util.List;
import java.util.Map;

import org.junit.jupiter.api.Test;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.security.oauth2.jwt.Jwt;

class KeycloakRealmRoleConverterTest {

    private final KeycloakRealmRoleConverter converter = new KeycloakRealmRoleConverter();

    @Test
    void shouldPrefixRealmRoles() {
        // Given
        final Jwt jwt = jwtWithClaim("realm_access", Map.of("roles", List.of("player", "admin")));

        // When
        final Collection<GrantedAuthority> authorities = converter.convert(jwt);

        // Then
        assertEquals(List.of("ROLE_player", "ROLE_admin"), names(authorities));
    }

    @Test
    void shouldReturnNoAuthoritiesWithoutRealmAccess() {
        // Given
        final Jwt jwt = jwtWithClaim("sub", "user-id");

        // When
        final Collection<GrantedAuthority> authorities = converter.convert(jwt);

        // Then
        assertEquals(List.of(), names(authorities));
    }

    @Test
    void shouldIgnoreMalformedRealmAccess() {
        assertEquals(List.of(), names(converter.convert(jwtWithClaim("realm_access", "player"))));
        assertEquals(List.of(), names(converter.convert(jwtWithClaim("realm_access", Map.of("roles", "player")))));
    }

    @Test
    void shouldSkipRolesThatAreNotStrings() {
        // Given
        final Jwt jwt = jwtWithClaim("realm_access", Map.of("roles", List.of("player", 42)));

        // When
        final Collection<GrantedAuthority> authorities = converter.convert(jwt);

        // Then
        assertEquals(List.of("ROLE_player"), names(authorities));
    }

    private static Jwt jwtWithClaim(String name, Object value) {
        return Jwt.withTokenValue("token")
            .header("alg", "RS256")
            .claim(name, value)
            .build();
    }

    private static List<String> names(Collection<GrantedAuthority> authorities) {
        return authorities.stream().map(GrantedAuthority::getAuthority).toList();
    }
}
