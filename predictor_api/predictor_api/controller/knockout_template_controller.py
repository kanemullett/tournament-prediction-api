from uuid import UUID

from fastapi import APIRouter, Response

from predictor_api.predictor_api.model.knockout_template import KnockoutTemplate
from predictor_api.predictor_api.service.knockout_template_service import KnockoutTemplateService


class KnockoutTemplateController:
    """
    Controller containing endpoints to perform knockout template-related actions.

    Attributes:
        __knockout_template_service (KnockoutTemplateService): The knockout template service containing knockout
            template-based logic.
    """

    def __init__(self, knockout_template_service: KnockoutTemplateService) -> None:
        """
        Initialise the KnockoutTemplateController.

        Attributes:
            knockout_template_service (KnockoutTemplateService): The knockout template service containing knockout
                template-based logic.
        """
        self.router: APIRouter = APIRouter(prefix="/knockout-templates", tags=["Knockout Templates"])
        self.__knockout_template_service = knockout_template_service

        self.router.add_api_route(
            "/",
            self.get_knockout_templates,
            methods=["GET"]
        )
        self.router.add_api_route(
            "/",
            self.create_knockout_templates,
            methods=["POST"]
        )
        self.router.add_api_route(
            "/{knockout_template_id}",
            self.get_knockout_template_by_id,
            methods=["GET"],
            responses={
                404: {
                    "description": "Not Found - No knockout templates found with a matching id.",
                    "content": {
                        "application/json": {
                            "example": {
                                "detail": "No knockout templates found with a matching id."
                            }
                        }
                    }
                }
            }
        )
        self.router.add_api_route(
            "/{knockout_template_id}",
            self.delete_knockout_template_by_id,
            methods=["DELETE"],
            responses={
                204: {
                    "description": "No Content - The knockout template was successfully deleted."
                },
                409: {
                    "description": "Conflict - The knockout template cannot be deleted as it is part of an existing "
                                   "tournament template.",
                    "content": {
                        "application/json": {
                            "example": {
                                "detail": "Cannot delete knockout template as it is part of an existing tournament "
                                          "template."
                            }
                        }
                    }
                }
            }
        )

    async def get_knockout_templates(self) -> list[KnockoutTemplate]:
        """
        GET /knockout-templates endpoint to retrieve stored knockout templates.

        Returns:
            list[KnockoutTemplate]: The stored knockout templates.
        """
        return self.__knockout_template_service.get_knockout_templates()

    async def create_knockout_templates(self, knockout_templates: list[KnockoutTemplate]) -> list[KnockoutTemplate]:
        """
        POST /knockout-templates endpoint to create new knockout templates.

        Args:
            knockout_templates (list[KnockoutTemplate]): The new knockout templates to create.

        Returns:
            list[KnockoutTemplate]: The newly created knockout templates.
        """
        return self.__knockout_template_service.create_knockout_templates(knockout_templates)

    async def get_knockout_template_by_id(self, knockout_template_id: UUID) -> KnockoutTemplate:
        """
        GET /knockout-templates/{knockout_template_id} endpoint to retrieve a single stored knockout template by its id.

        Args:
            knockout_template_id (UUID): The id of the knockout template to retrieve.

        Returns:
            KnockoutTemplate: The retrieved knockout template.
        """
        return self.__knockout_template_service.get_knockout_template_by_id(knockout_template_id)

    async def delete_knockout_template_by_id(self, knockout_template_id: UUID) -> Response:
        """
        DELETE /knockout-templates/{knockout_template_id} endpoint to delete a single stored knockout template by its
        id.

        Args:
            knockout_template_id (UUID): The id of the knockout template to delete.
        """
        self.__knockout_template_service.delete_knockout_template_by_id(knockout_template_id)

        return Response(status_code=204)
