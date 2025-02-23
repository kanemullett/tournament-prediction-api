CREATE TABLE IF NOT EXISTS "predictor"."tournament-templates" (
    id VARCHAR PRIMARY KEY,
    name VARCHAR,
    leagueTemplateId VARCHAR,
    knockoutTemplateId VARCHAR
);