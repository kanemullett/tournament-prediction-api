# tournament-prediction-api

Spring Boot backend for the Tournament Prediction application. To run the full stack (database, API and UI) locally, see [tournament-prediction-deployment](https://github.com/kanemullett/tournament-prediction-deployment).

## Prerequisites

- Java 21
- Maven
- A GitHub personal access token (classic) with the `read:packages` scope

## Maven setup

The `database-handler` dependency is published to GitHub Packages, which requires authentication even to read packages. Add a server entry with the id `github` to `~/.m2/settings.xml`:

```xml
<settings>
  <servers>
    <server>
      <id>github</id>
      <username>YOUR_GITHUB_USERNAME</username>
      <password>YOUR_TOKEN</password>
    </server>
  </servers>
</settings>
```

If you already have a `settings.xml`, add just the `<server>` block to its `<servers>` section.

## Build

```sh
mvn package
```

This runs the tests and produces `target/tournament-prediction-api-*.jar`, which the `Dockerfile` copies into the image.

## Configuration

| Variable | Purpose | Default |
|---|---|---|
| `POSTGRES_HOST` | Database host | required |
| `POSTGRES_PORT` | Database port | `5432` |
| `POSTGRES_DB` | Database name | required |
| `POSTGRES_USER` | Database user | required |
| `POSTGRES_PASSWORD` | Database password | required |
| `POSTGRES_SSLMODE` | JDBC `sslmode` | `prefer` |
| `CORS_ORIGINS` | Comma-separated origins allowed to call the API from a browser | none |
| `SERVER_PORT` | HTTP port | `8000` |
| `SPRING_SECURITY_OAUTH2_RESOURCESERVER_JWT_ISSUER_URI` | Keycloak realm URL that tokens must be issued by | `http://localhost:8180/realms/predictor` |
| `SPRING_SECURITY_OAUTH2_RESOURCESERVER_JWT_JWK_SET_URI` | Where to fetch Keycloak's signing keys. Set it when the API reaches Keycloak by a different address than the browser does (e.g. inside Docker or Kubernetes) | issuer URI + `/protocol/openid-connect/certs` |

Tables described by the JSON files in `src/main/resources/definitions/tables` are created on startup if they don't already exist (handled by `database-handler`).

## Authentication

Every endpoint requires a Keycloak access token in an `Authorization: Bearer <token>` header. The exceptions are the health checks and the API docs. Tokens must:

- be signed by the configured realm and not expired
- have that realm as their issuer (`iss`)
- be addressed to `predictor-api` (`aud`)

Requests without a valid token get `401`. Keycloak realm roles (`player`, `admin`) become Spring roles (`ROLE_player`, `ROLE_admin`), ready for rules such as `hasRole("admin")`.

Keycloak runs locally as part of the deployment repo's `docker compose`. The defaults above point at it.

**Trying endpoints in Swagger UI:** click **Authorize**, tick `keycloak`, and click **Authorize** again. You're sent to the Keycloak login page; register an account there if you don't have one. Once you're back, "Try it out" requests include your token.

## Endpoints

- Swagger UI: `/swagger-ui.html`
- Health: `/livez` (liveness) and `/readyz` (readiness, includes the database)
