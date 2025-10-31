from typing import Annotated as A

from ophyd_async.core import SignalRW, StandardReadableFormat as Format
from ophyd_async.tango.core import TangoReadable, TangoPolling


class Tunes(TangoReadable):
    # fmt:off
    x: A[SignalRW[float], Format.HINTED_UNCACHED_SIGNAL, TangoPolling(.5, 0.01, 1e-4)]
    y: A[SignalRW[float], Format.HINTED_UNCACHED_SIGNAL, TangoPolling(.5, 0.01, 1e-4)]
    # fmt:on
    count: A[SignalRW[int], Format.HINTED_UNCACHED_SIGNAL]
