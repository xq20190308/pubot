import datetime

from nonebot_plugin_datastore import get_plugin_data
from sqlalchemy.orm import Mapped, mapped_column

# 定义模型
Model = get_plugin_data().Model


class EventList(Model):
    """示例模型"""
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    category: Mapped[str]
    address: Mapped[str]
    joinCount: Mapped[int]
    limitCount: Mapped[int]
    credit: Mapped[str]
    sTime: Mapped[str]
    eTime: Mapped[str]
    regStartTimeStr: Mapped[str]
    regEndTimeStr: Mapped[str]
    eventStatus: Mapped[int]
    isJoin: Mapped[int]