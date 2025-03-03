from uuid import UUID

from fastapi import APIRouter, Response

from predictor_api.predictor_api.model.league_template import LeagueTemplate
from predictor_api.predictor_api.service.league_template_service import (
    LeagueTemplateService
)


class LeagueTemplateController:
    """
    Controller containing endpoints to perform league template-related actions.

    Attributes:
        __service (LeagueTemplateService): The league template service
            containing league template-based logic.
    """

    def __init__(self, league_template_service: LeagueTemplateService) -> None:
        """
        Initialise the LeagueTemplateController.

        Attributes:
            league_template_service (LeagueTemplateService): The league
                template service containing league template-based logic.
        """
        self.router: APIRouter = APIRouter(
            prefix="/league-templates",
            tags=["League Templates"]
        )
        self.__service = league_template_service

        self.router.add_api_route(
            "/",
            self.get_league_templates,
            methods=["GET"]
        )
        self.router.add_api_route(
            "/",
            self.create_league_templates,
            methods=["POST"]
        )
        self.router.add_api_route(
            "/{league_template_id}",
            self.get_league_template_by_id,
            methods=["GET"],
            responses={
                404: {
                    "description": "Not Found - No league templates found "
                                   "with a matching id.",
                    "content": {
                        "application/json": {
                            "example": {
                                "detail": "No league templates found with a "
                                          "matching id."
                            }
                        }
                    }
                }
            }
        )
        self.router.add_api_route(
            "/{league_template_id}",
            self.delete_league_template_by_id,
            methods=["DELETE"],
            responses={
                204: {
                    "description": "No Content - The league template was "
                                   "successfully deleted."
                },
                409: {
                    "description": "Conflict - The league template cannot be "
                                   "deleted as it is part of an existing "
                                   "tournament template.",
                    "content": {
                        "application/json": {
                            "example": {
                                "detail": "Cannot delete league template as "
                                          "it is part of an existing "
                                          "tournament template."
                            }
                        }
                    }
                }
            }
        )

    async def get_league_templates(self) -> list[LeagueTemplate]:
        """
        GET /league-templates endpoint to retrieve stored league templates.

        Returns:
            list[LeagueTemplate]: The stored league templates.
        """
        return self.__service.get_league_templates()

    async def create_league_templates(
            self,
            league_templates: list[LeagueTemplate]) -> list[LeagueTemplate]:
        """
        POST /league-templates endpoint to create new league templates.

        Args:
            league_templates (list[LeagueTemplate]): The new league templates
                to create.

        Returns:
            list[LeagueTemplate]: The newly created league templates.
        """
        return self.__service.create_league_templates(league_templates)

    async def get_league_template_by_id(
            self,
            league_template_id: UUID) -> LeagueTemplate:
        """
        GET /league-templates/{league_template_id} endpoint to retrieve a
        single stored league template by its id.

        Args:
            league_template_id (UUID): The id of the league template to
            retrieve.

        Returns:
            LeagueTemplate: The retrieved league template.
        """
        return self.__service.get_league_template_by_id(league_template_id)

    async def delete_league_template_by_id(
            self,
            league_template_id: UUID) -> Response:
        """
        DELETE /league-templates/{league_template_id} endpoint to delete a
        single stored league template by its id.

        Args:
            league_template_id (UUID): The id of the league template to delete.
        """
        self.__service.delete_league_template_by_id(league_template_id)

        return Response(status_code=204)
