#  Pyrogram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present Dan <https://github.com/delivrance>
#
#  This file is part of Pyrogram.
#
#  Pyrogram is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Pyrogram is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with Pyrogram.  If not, see <http://www.gnu.org/licenses/>.

from datetime import datetime

from pyrogram import raw, utils
from ..object import Object


class StoriesStealthMode(Object):
    """Information about the current stealth mode session.

    Parameters:
        active_until_date (:py:obj:`~datetime.datetime`, *optional*):
            The date up to which stealth mode will be active.

        cooldown_until_date (:py:obj:`~datetime.datetime`, *optional*):
            The date starting from which the user will be allowed to re-enable stealth mode again.
    """

    def __init__(self, *, active_until_date: datetime = None, cooldown_until_date: datetime = None):
        super().__init__(None)

        self.active_until_date = active_until_date
        self.cooldown_until_date = cooldown_until_date

    @staticmethod
    def _parse(ssm: "raw.types.StoriesStealthMode") -> "StoriesStealthMode":
        return StoriesStealthMode(
            active_until_date=utils.timestamp_to_datetime(getattr(ssm, "active_until_date", None)),
            cooldown_until_date=utils.timestamp_to_datetime(getattr(ssm, "cooldown_until_date", None)),
        )
