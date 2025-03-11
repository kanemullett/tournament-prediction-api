from uuid import UUID

from fastapi import APIRouter

from predictor_api.predictor_api.model.group import Group
from predictor_api.predictor_api.model.group_update import GroupUpdate
from predictor_api.predictor_api.service.group_service import GroupService


class GroupController:

    def __init__(self, group_service: GroupService) -> None:
        self.router: APIRouter = APIRouter(
            tags=["Groups"]
        )
        self.__service = group_service

        self.router.add_api_route(
            "/tournaments/{tournament_id}/groups",
            self.get_groups,
            methods=["GET"]
        )
        self.router.add_api_route(
            "/tournaments/{tournament_id}/groups",
            self.update_groups,
            methods=["PUT"]
        )
        self.router.add_api_route(
            "/tournaments/{tournament_id}/groups/{group_id}",
            self.get_group_by_id,
            methods=["GET"]
        )
        self.router.add_api_route(
            "/tournaments/{tournament_id}/groups/{group_id}/teams",
            self.add_teams_to_group,
            methods=["POST"]
        )
        self.router.add_api_route(
            "/tournaments/{tournament_id}/groups/{group_id}/teams/{team_id}",
            self.remove_team_from_group,
            methods=["DELETE"]
        )

    async def get_groups(self, tournament_id: UUID) -> list[Group]:
        return self.__service.get_groups(tournament_id)

    async def update_groups(
            self,
            tournament_id: UUID,
            groups: list[GroupUpdate]) -> list[Group]:
        return self.__service.update_groups(tournament_id, groups)

    async def get_group_by_id(
            self,
            tournament_id: UUID,
            group_id: UUID) -> Group:
        return self.__service.get_group_by_id(tournament_id, group_id)

    async def add_teams_to_group(
            self,
            tournament_id: UUID,
            group_id: UUID,
            team_ids: list[UUID]) -> Group:
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
        return self.__service.remove_team_from_group(
            tournament_id,
            group_id,
            team_id
        )
