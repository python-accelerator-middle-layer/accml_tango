from typing import Annotated as A

from event_model import DataKey
from ophyd_async.core import SignalRW, StandardReadable, StandardReadableFormat as Format
from ophyd_async.tango.core import TangoDevice, TangoPolling
from ophyd_async.core import AsyncStatus
from bluesky.protocols import Triggerable, Status

from accml.core.utils.ophyd_async.new_value import wait_for_new_value


class Tunes(TangoDevice, StandardReadable, Triggerable):
    # fmt:off
    Tune_h:  A[ SignalRW[float] , Format.HINTED_UNCACHED_SIGNAL , TangoPolling(.5, 1e-3, 1e-4) ]
    Tune_v: A[ SignalRW[float] , Format.HINTED_UNCACHED_SIGNAL , TangoPolling(.5, 1e-3, 1e-4) ]
    # fmt:on

    @AsyncStatus.wrap
    async def trigger(self) -> Status:
        await wait_for_new_value(self.Tune_v)


    async def describe(self) -> dict[str, DataKey]:
        """adjust precision to a higher value
        """
        d = await super().describe()
        for name in ["Tune_h", "Tune_v"]:
            d[f"{self.name}-{name}"]["precision"] = 5
        return d

    # count : A[ SignalRW[int] , Format.HINTED_UNCACHED_SIGNAL  ]
