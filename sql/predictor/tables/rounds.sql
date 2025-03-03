CREATE TABLE IF NOT EXISTS "predictor"."rounds" (
    "id" VARCHAR PRIMARY KEY,
    "name" VARCHAR,
    "teamCount" INTEGER,
    "roundOrder" INTEGER,
    "twoLegs" BOOLEAN,
    "extraTime" BOOLEAN,
    "awayGoals" BOOLEAN,
    "knockoutTemplateId" VARCHAR
);