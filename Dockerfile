# Runtime image for the pre-built Spring Boot jar.
# Build the jar first with `mvn package`: database-handler comes from GitHub Packages
# (or the local ~/.m2 for snapshots), which isn't reachable from inside a plain docker build.
FROM eclipse-temurin:21-jre

RUN useradd --system --uid 1001 app
WORKDIR /app

COPY target/tournament-prediction-api-*.jar app.jar

USER app
EXPOSE 8000

# Size the heap from the container's memory limit rather than the host's.
ENV JAVA_TOOL_OPTIONS="-XX:MaxRAMPercentage=75"

ENTRYPOINT ["java", "-jar", "/app/app.jar"]
