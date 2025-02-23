CREATE TABLE IF NOT EXISTS "predictor"."league-templates" (
    id VARCHAR PRIMARY KEY,
    name VARCHAR,
    groupCount INTEGER,
    teamsPerGroup INTEGER,
    homeAndAway BOOLEAN
);