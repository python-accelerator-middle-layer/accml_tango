import logging
from typing import Annotated as A

from ophyd_async.core import (
    derived_signal_rw,
    AsyncStageable,
    AsyncStatus,
    SignalR,
    SignalRW,
    StandardReadableFormat as Format,
    StandardReadable,
)
from ophyd_async.tango.core import TangoPolling, TangoDevice

from accml.core.utils.ophyd_async.multiplexer_for_settable_devices import _MultiplexerItemProxy


class MultiplexerItemProxy(_MultiplexerItemProxy):
     """
     Todo:
         need to provide difference current
     """

     pass


class _PowerConverterBase(StandardReadable, AsyncStageable):
    """

    Warning:
        current tango version: signals are the names of the properties of the
        tango device. These have to declared in a derived class using
        Annotation.

        These are renamed to setpoint and readback.
        Name clashes with the tango device can result in interesting behaviour

    """

    def __init__(
        self, trl: str | None = "", name="", *, setpoint_name: str, readback_name: str
    ):
        super().__init__(trl, name=name)
        self.setpoint_ = getattr(self, setpoint_name)
        self.readback_ = getattr(self, readback_name)

        self._ref_current = None

        self.delta_set_current = derived_signal_rw(
            self._to_relative_current,
            self._set_diff_current,
            current=self.setpoint_,
            derived_precision=5,
        )
        self.add_readables([self.delta_set_current])

    def _to_relative_current(self, current: float) -> float:
        assert (
            self._ref_current is not None
        ), "reference current None, was device staged?"
        r = current - self._ref_current
        self.log.debug(
            f"Computing relative current {current} - {self._ref_current}-> {r}"
        )
        return r

    async def _set_diff_current(self, dv: float):
        current = dv + self._ref_current
        self.log.debug(f"Setting {dv=} -> {current=}")
        await self.setpoint_.set(current)
        if self.log.getEffectiveLevel() >= logging.DEBUG:
            rdbk = await self.setpoint_._cache.backend.get_value()
            setp = await self.setpoint_._cache.backend.get_setpoint()
            self.log.debug(f"Setting {dv=} -> {current=}: {setp=}, {rdbk=}")

    async def read(self):
        """
        Todo:
            need to find out why I have to call read explicitly
        """
        d = await super().read()
        entry = d[self.setpoint_.name]
        d[self.delta_set_current.name] = dict(
            value=self._to_relative_current(entry["value"]),
            timestamp=entry["timestamp"],
        )
        return d

    @AsyncStatus.wrap
    async def stage(self) -> None:
        self.log.info("staging")
        r = await super().stage()
        self._ref_current = await self.setpoint_.get_value()
        return r

    @AsyncStatus.wrap
    async def unstage(self) -> None:
        self.log.info("unstaging")
        r = await super().unstage()
        self._ref_current = None
        return r


class PowerConverter(TangoDevice, StandardReadable, AsyncStageable):
    """
    Todo:
        need to find out why signals must be marked as uncached...
    """

    # fmt: off
    current_set: A[ SignalRW[float] , Format.HINTED_UNCACHED_SIGNAL, TangoPolling(1.0, 0.01, 1e-4) ]
    current_readback: A[ SignalR[float] ,  Format.UNCACHED_SIGNAL,        TangoPolling(1.0, 0.01, 1e-4) ]
    # fmt: on
