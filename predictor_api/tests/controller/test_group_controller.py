from unittest.mock import MagicMock
from uuid import UUID

import pytest

from fastapi import HTTPException
from pytest import raises

from predictor_api.predictor_api.controller.group_controller import GroupController
from predictor_api.predictor_api.model.group import Group
from predictor_api.predictor_api.model.group_update import GroupUpdate
from predictor_api.predictor_api.model.team import Team
from predictor_api.predictor_api.model.type.confederation import Confederation
from predictor_common.test_resources.assertions import Assertions


class TestGroupController:
    __service: MagicMock = MagicMock()

    __controller: GroupController = GroupController(__service)

    def setup_method(self):
        self.__service.get_groups.reset_mock()
        self.__service.get_groups.return_value = None
        self.__service.get_groups.side_effect = None

        self.__service.update_groups.reset_mock()
        self.__service.update_groups.return_value = None
        self.__service.update_groups.side_effect = None

        self.__service.get_group_by_id.reset_mock()
        self.__service.get_group_by_id.return_value = None
        self.__service.get_group_by_id.side_effect = None

        self.__service.add_teams_to_group.reset_mock()
        self.__service.add_teams_to_group.return_value = None
        self.__service.add_teams_to_group.side_effect = None

        self.__service.remove_team_from_group.reset_mock()
        self.__service.remove_team_from_group.return_value = None
        self.__service.remove_team_from_group.side_effect = None

    @pytest.mark.asyncio
    async def test_should_pass_groups_as_response(self):
        # Given
        self.__service.get_groups.return_value = [
            Group(
                id=UUID("96074478-23c4-4b6f-a8a4-1abe9fac2659"),
                name="Group A",
                teams=[
                    Team(
                        id=UUID("525bf855-a5b1-45cf-a1de-c017e67c0ce7"),
                        name="Croatia",
                        imagePath="HRV.png",
                        confederation=Confederation.UEFA
                    ),
                    Team(
                        id=UUID("bc339fee-cfda-4dbd-b1de-337a270bc414"),
                        name="Serbia",
                        imagePath="SRB.png",
                        confederation=Confederation.UEFA
                    )
                ]
            ),
            Group(
                id=UUID("e0ee5d0e-9d57-4c74-b938-0aa306a2313e"),
                name="Group B",
                teams=[
                    Team(
                        id=UUID("6c1496f5-b819-4ed3-b4c3-17bdaa6f252d"),
                        name="Bosnia & Herzegovina",
                        imagePath="BIH.png",
                        confederation=Confederation.UEFA
                    ),
                    Team(
                        id=UUID("1708fce1-2862-4604-b863-5fb4f00b68d2"),
                        name="Slovenia",
                        imagePath="SLO.png",
                        confederation=Confederation.UEFA
                    )
                ]
            )
        ]

        # When
        groups: list[Group] = await self.__controller.get_groups(
            UUID("1c29f6c3-9f98-41a8-ba0f-e07013742797")
        )

        # Then
        Assertions.assert_equals(2, len(groups))

        group1: Group = groups[0]
        Assertions.assert_equals(UUID("96074478-23c4-4b6f-a8a4-1abe9fac2659"), group1.id)
        Assertions.assert_equals("Group A", group1.name)
        Assertions.assert_equals(2, len(group1.teams))

        group1_team1: Team = group1.teams[0]
        Assertions.assert_equals(UUID("525bf855-a5b1-45cf-a1de-c017e67c0ce7"), group1_team1.id)
        Assertions.assert_equals("Croatia", group1_team1.name)
        Assertions.assert_equals("HRV.png", group1_team1.imagePath)
        Assertions.assert_equals(Confederation.UEFA, group1_team1.confederation)

        group1_team2: Team = group1.teams[1]
        Assertions.assert_equals(UUID("bc339fee-cfda-4dbd-b1de-337a270bc414"), group1_team2.id)
        Assertions.assert_equals("Serbia", group1_team2.name)
        Assertions.assert_equals("SRB.png", group1_team2.imagePath)
        Assertions.assert_equals(Confederation.UEFA, group1_team2.confederation)

        group2: Group = groups[1]
        Assertions.assert_equals(UUID("e0ee5d0e-9d57-4c74-b938-0aa306a2313e"), group2.id)
        Assertions.assert_equals("Group B", group2.name)
        Assertions.assert_equals(2, len(group2.teams))

        group2_team1: Team = group2.teams[0]
        Assertions.assert_equals(UUID("6c1496f5-b819-4ed3-b4c3-17bdaa6f252d"), group2_team1.id)
        Assertions.assert_equals("Bosnia & Herzegovina", group2_team1.name)
        Assertions.assert_equals("BIH.png", group2_team1.imagePath)
        Assertions.assert_equals(Confederation.UEFA, group2_team1.confederation)

        group2_team2: Team = group2.teams[1]
        Assertions.assert_equals(UUID("1708fce1-2862-4604-b863-5fb4f00b68d2"), group2_team2.id)
        Assertions.assert_equals("Slovenia", group2_team2.name)
        Assertions.assert_equals("SLO.png", group2_team2.imagePath)
        Assertions.assert_equals(Confederation.UEFA, group2_team2.confederation)

    @pytest.mark.asyncio
    async def test_should_pass_error_get_groups(self):
        # Given
        self.__service.get_groups.side_effect = HTTPException(
                status_code=404,
                detail="Not Found"
            )

        # When
        with raises(HTTPException) as httpe:
            await self.__controller.get_groups(
                UUID("1c29f6c3-9f98-41a8-ba0f-e07013742797")
            )

        # Then
        Assertions.assert_equals(404, httpe.value.status_code)
        Assertions.assert_equals("Not Found", httpe.value.detail)

    @pytest.mark.asyncio
    async def test_should_pass_updated_groups(self):
        # Given
        group_updates: list[GroupUpdate] = [
            GroupUpdate(
                id=UUID("96074478-23c4-4b6f-a8a4-1abe9fac2659"),
                name="Group A"
            ),
            GroupUpdate(
                id=UUID("e0ee5d0e-9d57-4c74-b938-0aa306a2313e"),
                name="Group B"
            )
        ]

        self.__service.update_groups.return_value = [
            Group(
                id=UUID("96074478-23c4-4b6f-a8a4-1abe9fac2659"),
                name="Group A",
                teams=[
                    Team(
                        id=UUID("525bf855-a5b1-45cf-a1de-c017e67c0ce7"),
                        name="Croatia",
                        imagePath="HRV.png",
                        confederation=Confederation.UEFA
                    ),
                    Team(
                        id=UUID("bc339fee-cfda-4dbd-b1de-337a270bc414"),
                        name="Serbia",
                        imagePath="SRB.png",
                        confederation=Confederation.UEFA
                    )
                ]
            ),
            Group(
                id=UUID("e0ee5d0e-9d57-4c74-b938-0aa306a2313e"),
                name="Group B",
                teams=[
                    Team(
                        id=UUID("6c1496f5-b819-4ed3-b4c3-17bdaa6f252d"),
                        name="Bosnia & Herzegovina",
                        imagePath="BIH.png",
                        confederation=Confederation.UEFA
                    ),
                    Team(
                        id=UUID("1708fce1-2862-4604-b863-5fb4f00b68d2"),
                        name="Slovenia",
                        imagePath="SLO.png",
                        confederation=Confederation.UEFA
                    )
                ]
            )
        ]

        # When
        groups: list[Group] = await self.__controller.update_groups(
            UUID("1c29f6c3-9f98-41a8-ba0f-e07013742797"),
            group_updates
        )

        # Then
        Assertions.assert_equals(2, len(groups))

        group1: Group = groups[0]
        Assertions.assert_equals(UUID("96074478-23c4-4b6f-a8a4-1abe9fac2659"), group1.id)
        Assertions.assert_equals("Group A", group1.name)
        Assertions.assert_equals(2, len(group1.teams))

        group1_team1: Team = group1.teams[0]
        Assertions.assert_equals(UUID("525bf855-a5b1-45cf-a1de-c017e67c0ce7"), group1_team1.id)
        Assertions.assert_equals("Croatia", group1_team1.name)
        Assertions.assert_equals("HRV.png", group1_team1.imagePath)
        Assertions.assert_equals(Confederation.UEFA, group1_team1.confederation)

        group1_team2: Team = group1.teams[1]
        Assertions.assert_equals(UUID("bc339fee-cfda-4dbd-b1de-337a270bc414"), group1_team2.id)
        Assertions.assert_equals("Serbia", group1_team2.name)
        Assertions.assert_equals("SRB.png", group1_team2.imagePath)
        Assertions.assert_equals(Confederation.UEFA, group1_team2.confederation)

        group2: Group = groups[1]
        Assertions.assert_equals(UUID("e0ee5d0e-9d57-4c74-b938-0aa306a2313e"), group2.id)
        Assertions.assert_equals("Group B", group2.name)
        Assertions.assert_equals(2, len(group2.teams))

        group2_team1: Team = group2.teams[0]
        Assertions.assert_equals(UUID("6c1496f5-b819-4ed3-b4c3-17bdaa6f252d"), group2_team1.id)
        Assertions.assert_equals("Bosnia & Herzegovina", group2_team1.name)
        Assertions.assert_equals("BIH.png", group2_team1.imagePath)
        Assertions.assert_equals(Confederation.UEFA, group2_team1.confederation)

        group2_team2: Team = group2.teams[1]
        Assertions.assert_equals(UUID("1708fce1-2862-4604-b863-5fb4f00b68d2"), group2_team2.id)
        Assertions.assert_equals("Slovenia", group2_team2.name)
        Assertions.assert_equals("SLO.png", group2_team2.imagePath)
        Assertions.assert_equals(Confederation.UEFA, group2_team2.confederation)

    @pytest.mark.asyncio
    async def test_should_pass_error_update_groups(self):
        # Given
        group_updates: list[GroupUpdate] = [
            GroupUpdate(
                id=UUID("96074478-23c4-4b6f-a8a4-1abe9fac2659"),
                name="Group A"
            ),
            GroupUpdate(
                id=UUID("e0ee5d0e-9d57-4c74-b938-0aa306a2313e"),
                name="Group B"
            )
        ]

        self.__service.update_groups.side_effect = HTTPException(
            status_code=404,
            detail="Not Found"
        )

        # When
        with raises(HTTPException) as httpe:
            await self.__controller.update_groups(
                UUID("1c29f6c3-9f98-41a8-ba0f-e07013742797"),
                group_updates
            )

        # Then
        Assertions.assert_equals(404, httpe.value.status_code)
        Assertions.assert_equals("Not Found", httpe.value.detail)

    @pytest.mark.asyncio
    async def test_should_pass_group(self):
        # Given
        self.__service.get_group_by_id.return_value = (
            Group(
                id=UUID("96074478-23c4-4b6f-a8a4-1abe9fac2659"),
                name="Group A",
                teams=[
                    Team(
                        id=UUID("525bf855-a5b1-45cf-a1de-c017e67c0ce7"),
                        name="Croatia",
                        imagePath="HRV.png",
                        confederation=Confederation.UEFA
                    ),
                    Team(
                        id=UUID("bc339fee-cfda-4dbd-b1de-337a270bc414"),
                        name="Serbia",
                        imagePath="SRB.png",
                        confederation=Confederation.UEFA
                    )
                ]
            )
        )

        # When
        group: Group = await self.__controller.get_group_by_id(
            UUID("1c29f6c3-9f98-41a8-ba0f-e07013742797"),
            UUID("96074478-23c4-4b6f-a8a4-1abe9fac2659")
        )

        # Then
        Assertions.assert_equals(UUID("96074478-23c4-4b6f-a8a4-1abe9fac2659"), group.id)
        Assertions.assert_equals("Group A", group.name)
        Assertions.assert_equals(2, len(group.teams))

        team1: Team = group.teams[0]
        Assertions.assert_equals(UUID("525bf855-a5b1-45cf-a1de-c017e67c0ce7"), team1.id)
        Assertions.assert_equals("Croatia", team1.name)
        Assertions.assert_equals("HRV.png", team1.imagePath)
        Assertions.assert_equals(Confederation.UEFA, team1.confederation)

        team2: Team = group.teams[1]
        Assertions.assert_equals(UUID("bc339fee-cfda-4dbd-b1de-337a270bc414"), team2.id)
        Assertions.assert_equals("Serbia", team2.name)
        Assertions.assert_equals("SRB.png", team2.imagePath)
        Assertions.assert_equals(Confederation.UEFA, team2.confederation)

    @pytest.mark.asyncio
    async def test_should_pass_error_get_group_by_id(self):
        # Given
        self.__service.get_group_by_id.side_effect = HTTPException(
            status_code=404,
            detail="Not Found"
        )

        # When
        with raises(HTTPException) as httpe:
            await self.__controller.get_group_by_id(
                UUID("1c29f6c3-9f98-41a8-ba0f-e07013742797"),
                UUID("96074478-23c4-4b6f-a8a4-1abe9fac2659")
            )

        # Then
        Assertions.assert_equals(404, httpe.value.status_code)
        Assertions.assert_equals("Not Found", httpe.value.detail)

    @pytest.mark.asyncio
    async def test_should_pass_updated_group(self):
        # Given
        team_ids: list[UUID] = [
            UUID("525bf855-a5b1-45cf-a1de-c017e67c0ce7"),
            UUID("bc339fee-cfda-4dbd-b1de-337a270bc414")
        ]

        self.__service.add_teams_to_group.return_value = (
            Group(
                id=UUID("96074478-23c4-4b6f-a8a4-1abe9fac2659"),
                name="Group A",
                teams=[
                    Team(
                        id=UUID("525bf855-a5b1-45cf-a1de-c017e67c0ce7"),
                        name="Croatia",
                        imagePath="HRV.png",
                        confederation=Confederation.UEFA
                    ),
                    Team(
                        id=UUID("bc339fee-cfda-4dbd-b1de-337a270bc414"),
                        name="Serbia",
                        imagePath="SRB.png",
                        confederation=Confederation.UEFA
                    )
                ]
            )
        )

        # When
        group: Group = await self.__controller.add_teams_to_group(
            UUID("1c29f6c3-9f98-41a8-ba0f-e07013742797"),
            UUID("96074478-23c4-4b6f-a8a4-1abe9fac2659"),
            team_ids
        )

        # Then
        Assertions.assert_equals(UUID("96074478-23c4-4b6f-a8a4-1abe9fac2659"), group.id)
        Assertions.assert_equals("Group A", group.name)
        Assertions.assert_equals(2, len(group.teams))

        team1: Team = group.teams[0]
        Assertions.assert_equals(UUID("525bf855-a5b1-45cf-a1de-c017e67c0ce7"), team1.id)
        Assertions.assert_equals("Croatia", team1.name)
        Assertions.assert_equals("HRV.png", team1.imagePath)
        Assertions.assert_equals(Confederation.UEFA, team1.confederation)

        team2: Team = group.teams[1]
        Assertions.assert_equals(UUID("bc339fee-cfda-4dbd-b1de-337a270bc414"), team2.id)
        Assertions.assert_equals("Serbia", team2.name)
        Assertions.assert_equals("SRB.png", team2.imagePath)
        Assertions.assert_equals(Confederation.UEFA, team2.confederation)

    @pytest.mark.asyncio
    async def test_should_pass_error_add_teams_to_group(self):
        # Given
        team_ids: list[UUID] = [
            UUID("525bf855-a5b1-45cf-a1de-c017e67c0ce7"),
            UUID("bc339fee-cfda-4dbd-b1de-337a270bc414")
        ]

        self.__service.add_teams_to_group.side_effect = HTTPException(
            status_code=404,
            detail="Not Found"
        )

        # When
        with raises(HTTPException) as httpe:
            await self.__controller.add_teams_to_group(
                UUID("1c29f6c3-9f98-41a8-ba0f-e07013742797"),
                UUID("96074478-23c4-4b6f-a8a4-1abe9fac2659"),
                team_ids
            )

        # Then
        Assertions.assert_equals(404, httpe.value.status_code)
        Assertions.assert_equals("Not Found", httpe.value.detail)

    @pytest.mark.asyncio
    async def test_should_pass_group_after_delete(self):
        # Given
        self.__service.remove_team_from_group.return_value = (
            Group(
                id=UUID("96074478-23c4-4b6f-a8a4-1abe9fac2659"),
                name="Group A",
                teams=[
                    Team(
                        id=UUID("525bf855-a5b1-45cf-a1de-c017e67c0ce7"),
                        name="Croatia",
                        imagePath="HRV.png",
                        confederation=Confederation.UEFA
                    ),
                    Team(
                        id=UUID("bc339fee-cfda-4dbd-b1de-337a270bc414"),
                        name="Serbia",
                        imagePath="SRB.png",
                        confederation=Confederation.UEFA
                    )
                ]
            )
        )

        # When
        group: Group = await self.__controller.remove_team_from_group(
            UUID("1c29f6c3-9f98-41a8-ba0f-e07013742797"),
            UUID("96074478-23c4-4b6f-a8a4-1abe9fac2659"),
            UUID("75ffd159-4e7f-456a-98a5-b077a98b724d")
        )

        # Then
        Assertions.assert_equals(UUID("96074478-23c4-4b6f-a8a4-1abe9fac2659"), group.id)
        Assertions.assert_equals("Group A", group.name)
        Assertions.assert_equals(2, len(group.teams))

        team1: Team = group.teams[0]
        Assertions.assert_equals(UUID("525bf855-a5b1-45cf-a1de-c017e67c0ce7"), team1.id)
        Assertions.assert_equals("Croatia", team1.name)
        Assertions.assert_equals("HRV.png", team1.imagePath)
        Assertions.assert_equals(Confederation.UEFA, team1.confederation)

        team2: Team = group.teams[1]
        Assertions.assert_equals(UUID("bc339fee-cfda-4dbd-b1de-337a270bc414"), team2.id)
        Assertions.assert_equals("Serbia", team2.name)
        Assertions.assert_equals("SRB.png", team2.imagePath)
        Assertions.assert_equals(Confederation.UEFA, team2.confederation)

    @pytest.mark.asyncio
    async def test_should_pass_error_add_teams_to_group(self):
        # Given
        self.__service.remove_team_from_group.side_effect = HTTPException(
            status_code=404,
            detail="Not Found"
        )

        # When
        with raises(HTTPException) as httpe:
            await self.__controller.remove_team_from_group(
                UUID("1c29f6c3-9f98-41a8-ba0f-e07013742797"),
                UUID("96074478-23c4-4b6f-a8a4-1abe9fac2659"),
                UUID("75ffd159-4e7f-456a-98a5-b077a98b724d")
            )

        # Then
        Assertions.assert_equals(404, httpe.value.status_code)
        Assertions.assert_equals("Not Found", httpe.value.detail)
