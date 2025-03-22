from uuid import UUID

from fastapi import APIRouter, Response

from predictor_api.predictor_api.model.result import Result
from predictor_api.predictor_api.service.result_service import ResultService


class ResultController:

    def __init__(self, result_service: ResultService) -> None:
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
        return self.__service.create_results(tournament_id, results)

    async def update_results(self, tournament_id: UUID, results: list[Result]) -> list[Result]:
        return self.__service.update_results(tournament_id, results)

    async def delete_result_by_id(self, tournament_id: UUID, result_id: UUID) -> Response:
        self.__service.delete_result_by_id(tournament_id, result_id)

        return Response(status_code=204)
