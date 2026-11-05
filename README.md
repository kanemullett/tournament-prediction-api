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

Database migrations in `src/main/resources/db/migration` run automatically on startup.

## Endpoints

- Swagger UI: `/swagger-ui.html`
- Health: `/livez` (liveness) and `/readyz` (readiness, includes the database)
