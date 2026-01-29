from typing import Annotated as A

from ophyd_async.core import SignalRW, StandardReadable, StandardReadableFormat as Format
from ophyd_async.tango.core import TangoDevice, TangoPolling
from ophyd_async.core import AsyncStatus
from bluesky.protocols import Triggerable, Status

from accml.core.utils.ophyd_async.new_value import wait_for_new_value


class Tunes(TangoDevice, StandardReadable, Triggerable):
    # fmt:off
    hor:  A[ SignalRW[float] , Format.HINTED_UNCACHED_SIGNAL , TangoPolling(.5, 0.01, 1e-4) ]
    vert: A[ SignalRW[float] , Format.HINTED_UNCACHED_SIGNAL , TangoPolling(.5, 0.01, 1e-4) ]
    # fmt:on

    @AsyncStatus.wrap
    async def trigger(self) -> Status:
        await wait_for_new_value(self.vert)

    # count : A[ SignalRW[int] , Format.HINTED_UNCACHED_SIGNAL  ]
