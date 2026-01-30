from typing import Annotated as A

from ophyd_async.core import (
    AsyncStageable,
    SignalRW,
    StandardReadable,
    StandardReadableFormat as Format
)
from ophyd_async.tango.core import TangoDevice, TangoPolling


class Magnet(TangoDevice, StandardReadable, AsyncStageable):
    """
    Todo:
        need to find out why signals must be marked as uncached...
    """

    # fmt: off
    Strength: A[SignalRW[float], Format.HINTED_UNCACHED_SIGNAL, TangoPolling(0.2, 1e-4, 1e-4)]
    # magnetic_strength_readback: A[ SignalR[float]  , Format.UNCACHED_SIGNAL        , TangoPolling(0.1, 1e-4, 1e-4) ]
    # current :                   A[ SignalRW[float] , Format.UNCACHED_SIGNAL        , TangoPolling(0.1, 0.01, 1e-4) ]
    # x_kick :                    A[ SignalRW[float] , Format.UNCACHED_SIGNAL        , TangoPolling(0.1, 0.01, 1e-4) ]
    # y_kick :                    A[ SignalRW[float] , Format.UNCACHED_SIGNAL        , TangoPolling(0.1, 0.01, 1e-4) ]
    # fmt: on
