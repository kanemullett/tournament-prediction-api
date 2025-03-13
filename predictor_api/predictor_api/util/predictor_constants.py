from uuid import UUID


class PredictorConstants:
    PREDICTOR_SCHEMA = "predictor"

    @staticmethod
    def get_group_teams_table(tournament_id: UUID) -> str:
        return f"group-teams_{tournament_id}"
