from typing import Optional
from uuid import UUID

from predictor_api.predictor_api.model.group_update import GroupUpdate
from predictor_api.predictor_api.model.team import Team


class Group(GroupUpdate):
    """
    Object representing a group.

    Attributes:
        teams (Optional[list[Team]]): The teams competing in the group.
    """
    teams: Optional[list[Team]] = None

    @classmethod
    def get_target_table(cls, tournament_id: UUID) -> str:
        return f"groups_{tournament_id}"
