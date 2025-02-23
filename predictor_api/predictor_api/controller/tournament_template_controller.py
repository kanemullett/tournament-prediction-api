from predictor_api.predictor_api.service.tournament_template_service import TournamentTemplateService


class TournamentTemplateController:

    def __init__(self, tournament_template_service: TournamentTemplateService) -> None:
        self.__tournament_template_service = tournament_template_service
