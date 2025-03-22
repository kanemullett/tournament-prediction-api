from uuid import UUID

from fastapi import APIRouter, Response

from predictor_api.predictor_api.model.result import Result
from predictor_api.predictor_api.service.result_service import ResultService


class ResultController:
    """
    Controller containing endpoints to perform result-related actions.

    Attributes:
        __service (ResultService): The result service containing result-based
            logic.
    """

    def __init__(self, result_service: ResultService) -> None:
        """
        Initialise the ResultController.

        Attributes:
            result_service (ResultService): The result service containing
                result-based logic.
        """
        self.router: APIRouter = APIRouter(
            tags=["Results"]
        )
        self.__service = result_service

        self.router.add_api_route(
            "/tournaments/{tournament_id}/results",
            self.create_results,
            methods=["POST"],
            responses={
                400: {
                    "description": "Bad Request",
                    "content": {
                        "application/json": {
                            "example": {
                                "detail": "One or more results does not have "
                                          "a corresponding match record."
                            }
                        }
                    }
                },
                404: {
                    "description": "Not Found",
                    "content": {
                        "application/json": {
                            "example": {
                                "detail": "No tournaments found with a "
                                          "matching id."
                            }
                        }
                    }
                }
            }
        )
        self.router.add_api_route(
            "/tournaments/{tournament_id}/results",
            self.update_results,
            methods=["PUT"],
            responses={
                404: {
                    "description": "Not Found",
                    "content": {
                        "application/json": {
                            "example": {
                                "detail": "No tournaments found with a "
                                          "matching id."
                            }
                        }
                    }
                }
            }
        )
        self.router.add_api_route(
            "/tournaments/{tournament_id}/results/{result_id}",
            self.delete_result_by_id,
            methods=["DELETE"],
            responses={
                204: {
                    "description": "No Content"
                },
                404: {
                    "description": "Not Found",
                    "content": {
                        "application/json": {
                            "example": {
                                "detail": "No tournaments found with a "
                                          "matching id."
                            }
                        }
                    }
                }
            }
        )

    async def create_results(
            self,
            tournament_id: UUID,
            results: list[Result]) -> list[Result]:
        """
        POST /tournaments/{tournament_id}/results endpoint to create new
        results.

        Args:
            tournament_id (UUID): The id of the tournament to which the
                results belong.
            results (list[Result]): The results to create.

        Returns:
            list[Result]: The newly created results.
        """
        return self.__service.create_results(tournament_id, results)

    async def update_results(
            self,
            tournament_id: UUID,
            results: list[Result]) -> list[Result]:
        """
        PUT /tournaments/{tournament_id}/results endpoint to update existing
        results.

        Args:
            tournament_id (UUID): The id of the tournament to which the
                results belong.
            results (list[Result]): The results to update.

        Returns:
            list[Result]: The newly updated results.
        """
        return self.__service.update_results(tournament_id, results)

    async def delete_result_by_id(
            self,
            tournament_id: UUID,
            result_id: UUID) -> Response:
        """
        DELETE /tournaments/{tournament_id}/results/{result_id} endpoint to
        delete a single stored result by its id.

        Args:
            tournament_id (UUID): The id of the tournament to which the
                result belongs.
            result_id (UUID): The id of the result to delete.
        """
        self.__service.delete_result_by_id(tournament_id, result_id)

        return Response(status_code=204)
