from dataclasses import dataclass

from common.domain.model.user_info_section import UserInfoSection


@dataclass(frozen=True)
class UserInfo:
    user_id: int
    username: str
    sections: list[UserInfoSection]
