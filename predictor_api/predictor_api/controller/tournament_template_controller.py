from uuid import UUID

from fastapi import APIRouter, Response

from predictor_api.predictor_api.model.tournament_template import (
    TournamentTemplate
)
from predictor_api.predictor_api.model.tournament_template_request import (
    TournamentTemplateRequest
)
from predictor_api.predictor_api.service.tournament_template_service import (
    TournamentTemplateService
)


class TournamentTemplateController:
    """
    Controller containing endpoints to perform tournament template-related
    actions.

    Attributes:
        __service (TournamentTemplateService): The tournament template
            service containing tournament template-based logic.
    """

    def __init__(
            self,
            tournament_template_service: TournamentTemplateService) -> None:
        """
        Initialise the TournamentTemplateController.

        Attributes:
            tournament_template_service (TournamentTemplateService): The
                tournament template service containing tournament
                template-based logic.
        """
        self.router: APIRouter = APIRouter(
            prefix="/tournament-templates",
            tags=["Tournament Templates"]
        )
        self.__service = tournament_template_service

        self.router.add_api_route(
            "/",
            self.get_tournament_templates,
            methods=["GET"]
        )
        self.router.add_api_route(
            "/",
            self.create_tournament_templates,
            methods=["POST"]
        )
        self.router.add_api_route(
            "/{tournament_template_id}",
            self.get_tournament_template_by_id,
            methods=["GET"],
            responses={
                404: {
                    "description": "Not Found - No tournament templates found "
                                   "with a matching id.",
                    "content": {
                        "application/json": {
                            "example": {
                                "detail": "No tournament templates found with "
                                          "a matching id."
                            }
                        }
                    }
                }
            }
        )
        self.router.add_api_route(
            "/{tournament_template_id}",
            self.delete_tournament_template_by_id,
            methods=["DELETE"],
            responses={
                204: {
                    "description": "No Content - The tournament template was "
                                   "successfully deleted."
                },
                409: {
                    "description": "Conflict - Cannot delete tournament "
                                   "template as it is part of an existing "
                                   "tournament.",
                    "content": {
                        "application/json": {
                            "example": {
                                "detail": "Cannot delete tournament template "
                                          "as it is part of an existing "
                                          "tournament."
                            }
                        }
                    }
                }
            }
        )

    async def get_tournament_templates(self) -> list[TournamentTemplate]:
        """
        GET /tournament-templates endpoint to retrieve stored tournament
        templates.

        Returns:
            list[TournamentTemplate]: The stored tournament templates.
        """
        return self.__service.get_tournament_templates()

    async def create_tournament_templates(
            self,
            tournament_templates: list[TournamentTemplateRequest]
    ) -> list[TournamentTemplate]:
        """
        POST /tournament-templates endpoint to create new tournament templates.

        Args:
            tournament_templates (list[TournamentTemplateRequest]): The new
                tournament templates to create.

        Returns:
            list[TournamentTemplate]: The newly created tournament templates.
        """
        return self.__service.create_tournament_templates(tournament_templates)

    async def get_tournament_template_by_id(
            self,
            tournament_template_id: UUID) -> TournamentTemplate:
        """
        GET /tournament-templates/{tournament_template_id} endpoint to
        retrieve a single stored tournament template by its id.

        Args:
            tournament_template_id (UUID): The id of the tournament template
                to retrieve.

        Returns:
            TournamentTemplateBase: The retrieved tournament template.
        """
        return self.__service.get_tournament_template_by_id(
            tournament_template_id
        )

    async def delete_tournament_template_by_id(
            self,
            tournament_template_id: UUID) -> Response:
        """
        DELETE /tournament-templates/{tournament_template_id} endpoint to
        delete a single stored tournament template by its id.

        Args:
            tournament_template_id (UUID): The id of the tournament template
                to delete.
        """
        self.__service.delete_tournament_template_by_id(tournament_template_id)

        return Response(status_code=204)
