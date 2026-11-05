-- Base tables for the predictor schema.
-- Per-tournament tables (rounds_<id>, groups_<id>, matches_<id>, ...) are created at runtime.
-- Identifiers are quoted because jOOQ quotes them (camelCase columns, hyphenated tables).

CREATE SCHEMA IF NOT EXISTS predictor;

CREATE TABLE IF NOT EXISTS predictor."users" (
    "id"          VARCHAR PRIMARY KEY,
    "displayName" VARCHAR NOT NULL
);

CREATE TABLE IF NOT EXISTS predictor."teams" (
    "id"            VARCHAR PRIMARY KEY,
    "name"          VARCHAR NOT NULL,
    "imagePath"     VARCHAR NOT NULL,
    "confederation" VARCHAR NOT NULL,
    "ranking"       INTEGER
);

CREATE TABLE IF NOT EXISTS predictor."league-templates" (
    "id"            VARCHAR PRIMARY KEY,
    "name"          VARCHAR NOT NULL,
    "groupCount"    INTEGER NOT NULL,
    "teamsPerGroup" INTEGER NOT NULL,
    "homeAndAway"   BOOLEAN NOT NULL
);

CREATE TABLE IF NOT EXISTS predictor."knockout-templates" (
    "id"     VARCHAR PRIMARY KEY,
    "name"   VARCHAR NOT NULL,
    "rounds" JSONB
);

CREATE TABLE IF NOT EXISTS predictor."tournament-templates" (
    "id"                 VARCHAR PRIMARY KEY,
    "name"               VARCHAR NOT NULL,
    "leagueTemplateId"   VARCHAR,
    "knockoutTemplateId" VARCHAR
);

CREATE TABLE IF NOT EXISTS predictor."tournaments" (
    "id"            VARCHAR PRIMARY KEY,
    "name"          VARCHAR NOT NULL,
    "year"          INTEGER NOT NULL,
    "confederation" VARCHAR,
    "templateId"    VARCHAR NOT NULL
);

CREATE TABLE IF NOT EXISTS predictor."competitions" (
    "id"           VARCHAR PRIMARY KEY,
    "name"         VARCHAR NOT NULL,
    "tournamentId" VARCHAR
);

CREATE TABLE IF NOT EXISTS predictor."competition-users" (
    "id"            VARCHAR PRIMARY KEY,
    "competitionId" VARCHAR NOT NULL,
    "username"      VARCHAR NOT NULL
);
