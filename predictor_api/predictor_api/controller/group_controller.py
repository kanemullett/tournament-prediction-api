from uuid import UUID

from fastapi import APIRouter

from predictor_api.predictor_api.model.group import Group
from predictor_api.predictor_api.model.group_update import GroupUpdate
from predictor_api.predictor_api.service.group_service import GroupService


class GroupController:
    """
    Controller containing endpoints to perform group-related actions.

    Attributes:
        __service (GroupService): The group service containing group-based
            logic.
    """

    def __init__(self, group_service: GroupService) -> None:
        """
        Initialise the GroupController.

        Attributes:
            group_service (GroupService): The group service containing
                group-based logic.
        """
        self.router: APIRouter = APIRouter(
            tags=["Groups"]
        )
        self.__service = group_service

        self.router.add_api_route(
            "/tournaments/{tournament_id}/groups",
            self.get_groups,
            methods=["GET"],
            responses={
                404: {
                    "description": "Not Found",
                    "content": {
                        "application/json": {
                            "examples": {
                                "tournamentNotFound": {
                                    "summary": "Tournament not found",
                                    "value": {
                                        "detail": "No tournaments found with "
                                                  "a matching id."
                                    }
                                },
                                "noGroupStage": {
                                    "summary": "Tournament has no group stage",
                                    "value": {
                                        "detail": "The tournament with the "
                                                  "supplied id does not have "
                                                  "a group stage."
                                    }
                                }
                            }
                        }
                    }
                }
            }
        )
        self.router.add_api_route(
            "/tournaments/{tournament_id}/groups",
            self.update_groups,
            methods=["PUT"],
            responses={
                404: {
                    "description": "Not Found",
                    "content": {
                        "application/json": {
                            "examples": {
                                "tournamentNotFound": {
                                    "summary": "Tournament not found",
                                    "value": {
                                        "detail": "No tournaments found with "
                                                  "a matching id."
                                    }
                                },
                                "noGroupStage": {
                                    "summary": "Tournament has no group stage",
                                    "value": {
                                        "detail": "The tournament with the "
                                                  "supplied id does not have "
                                                  "a group stage."
                                    }
                                }
                            }
                        }
                    }
                }
            }
        )
        self.router.add_api_route(
            "/tournaments/{tournament_id}/groups/{group_id}",
            self.get_group_by_id,
            methods=["GET"],
            responses={
                404: {
                    "description": "Not Found",
                    "content": {
                        "application/json": {
                            "examples": {
                                "tournamentNotFound": {
                                    "summary": "Tournament not found",
                                    "value": {
                                        "detail": "No tournaments found with "
                                                  "a matching id."
                                    }
                                },
                                "noGroupStage": {
                                    "summary": "Tournament has no group stage",
                                    "value": {
                                        "detail": "The tournament with the "
                                                  "supplied id does not have "
                                                  "a group stage."
                                    }
                                },
                                "groupNotFound": {
                                    "summary": "Group not found",
                                    "value": {
                                        "detail": "No groups found with a "
                                                  "matching id."
                                    }
                                },
                            }
                        }
                    }
                }
            }
        )
        self.router.add_api_route(
            "/tournaments/{tournament_id}/groups/{group_id}/teams",
            self.add_teams_to_group,
            methods=["POST"],
            responses={
                400: {
                    "description": "Bad Request",
                    "content": {
                        "application/json": {
                            "example": {
                                "detail": "No teams found with ids: []"
                            }
                        }
                    }
                },
                404: {
                    "description": "Not Found",
                    "content": {
                        "application/json": {
                            "examples": {
                                "tournamentNotFound": {
                                    "summary": "Tournament not found",
                                    "value": {
                                        "detail": "No tournaments found with "
                                                  "a matching id."
                                    }
                                },
                                "noGroupStage": {
                                    "summary": "Tournament has no group stage",
                                    "value": {
                                        "detail": "The tournament with the "
                                                  "supplied id does not have "
                                                  "a group stage."
                                    }
                                },
                                "groupNotFound": {
                                    "summary": "Group not found",
                                    "value": {
                                        "detail": "No groups found with a "
                                                  "matching id."
                                    }
                                },
                            }
                        }
                    }
                },
                409: {
                    "description": "Conflict",
                    "content": {
                        "application/json": {
                            "example": {
                                "detail": "The number of groups in this "
                                          "tournament's group stage has been "
                                          "exceeded."
                            }
                        }
                    }
                }
            }
        )
        self.router.add_api_route(
            "/tournaments/{tournament_id}/groups/{group_id}/teams/{team_id}",
            self.remove_team_from_group,
            methods=["DELETE"],
            responses={
                404: {
                    "description": "Not Found",
                    "content": {
                        "application/json": {
                            "examples": {
                                "tournamentNotFound": {
                                    "summary": "Tournament not found",
                                    "value": {
                                        "detail": "No tournaments found with "
                                                  "a matching id."
                                    }
                                },
                                "noGroupStage": {
                                    "summary": "Tournament has no group stage",
                                    "value": {
                                        "detail": "The tournament with the "
                                                  "supplied id does not have "
                                                  "a group stage."
                                    }
                                },
                                "groupNotFound": {
                                    "summary": "Group not found",
                                    "value": {
                                        "detail": "No groups found with a "
                                                  "matching id."
                                    }
                                },
                            }
                        }
                    }
                }
            }
        )

    async def get_groups(self, tournament_id: UUID) -> list[Group]:
        """
        GET /tournaments/{tournament_id}/groups endpoint to retrieve stored
        groups.

        Args:
            tournament_id (UUID): The id of the tournament whose groups are
                to be retrieved.

        Returns:
            list[Group]: The stored groups.
        """
        return self.__service.get_groups(tournament_id)

    async def update_groups(
            self,
            tournament_id: UUID,
            groups: list[GroupUpdate]) -> list[Group]:
        """
        PUT /tournaments/{tournament_id}/groups endpoint to update existing
        groups.

        Args:
            tournament_id (UUID): The id of the tournament whose groups are
                to be updated.
            groups (list[GroupUpdate]): The groups to update.

        Returns:
            list[Group]: The newly updated groups.
        """
        return self.__service.update_groups(tournament_id, groups)

    async def get_group_by_id(
            self,
            tournament_id: UUID,
            group_id: UUID) -> Group:
        """
        GET /tournaments/{tournament_id}/groups/{group_id} endpoint to
        retrieve a single stored group by its id.

        Args:
            tournament_id (UUID): The id of the tournament the group belongs
                to.
            group_id (UUID): The id of the group to retrieve.

        Returns:
            Group: The retrieved group.
        """
        return self.__service.get_group_by_id(tournament_id, group_id)

    async def add_teams_to_group(
            self,
            tournament_id: UUID,
            group_id: UUID,
            team_ids: list[UUID]) -> Group:
        """
        POST /tournaments/{tournament_id}/groups/{group_id}/teams endpoint to
        add teams to a group.

        Args:
             tournament_id (UUID): The id of the tournament the group belongs
                to.
             group_id (UUID): The id of the group to add teams to.
             team_ids (list[UUID]): The ids of the teams to add to the group.

        Returns:
            Group: The updated group.
        """
        return self.__service.add_teams_to_group(
            tournament_id,
            group_id,
            team_ids
        )

    async def remove_team_from_group(
            self,
            tournament_id: UUID,
            group_id: UUID,
            team_id: UUID) -> Group:
        """
        DELETE /tournaments/{tournament_id}/groups/{group_id}/teams/{team_id}
        endpoint to remove a single team from a group.

        Args:
            tournament_id (UUID): The id of the tournament the group belongs
                to.
            group_id (UUID): The id of the group to remove the team from.
            team_id (UUID): The id of the team to remove from the group.

        Return:
            Group: The updated group.
        """
        return self.__service.remove_team_from_group(
            tournament_id,
            group_id,
            team_id
        )
