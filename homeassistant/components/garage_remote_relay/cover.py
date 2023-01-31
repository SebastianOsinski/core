from __future__ import annotations

from typing import Any

from homeassistant.components.cover import (
    CoverDeviceClass,
    CoverEntity,
    CoverEntityFeature,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import STATE_CLOSED, STATE_CLOSING, STATE_OPEN, STATE_OPENING
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .garage_remote import GarageRemote
from .const import DOMAIN, CONF_COVER_AUTO_CLOSE_DELAY, CONF_COVER_MOVEMENT_DURATION

import asyncio

async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up a BleBox entry."""
    remote = hass.data[DOMAIN][config_entry.entry_id]
    config = config_entry.data
    entities = [GarageDoor(remote, config)]
    async_add_entities(entities, True)


class GarageDoor(CoverEntity):
    def __init__(self, remote: GarageRemote, config) -> None:
        self._attr_device_class = CoverDeviceClass.GARAGE
        self._attr_supported_features = CoverEntityFeature.OPEN
        self._attr_unique_id = "garage_door"
        self._remote = remote
        self._config = config
        self._state = STATE_CLOSED
        self._simulation_task = None

    async def async_open_cover(self, **kwargs: Any) -> None:
        if self._simulation_task is not None and not self._simulation_task.done:
            self._simulation_task.cancel()
            self._simulation_task = None
        
        self._state = STATE_OPENING
        await self.async_update_ha_state()
        await self._remote.press()

        self._simulation_task = asyncio.create_task(self.simulate_operation())

    async def simulate_operation(self) -> None:
        await asyncio.sleep(self._config[CONF_COVER_MOVEMENT_DURATION])
        self._state = STATE_OPEN
        await self.async_update_ha_state()
        
        await asyncio.sleep(self._config[CONF_COVER_AUTO_CLOSE_DELAY])
        self._state = STATE_CLOSING
        await self.async_update_ha_state()
        
        await asyncio.sleep(self._config[CONF_COVER_MOVEMENT_DURATION])
        self._state = STATE_CLOSED
        await self.async_update_ha_state()

    @property
    def is_opening(self) -> bool | None:
        """Return whether cover is opening."""
        return self._state == STATE_OPENING

    @property
    def is_closing(self) -> bool | None:
        """Return whether cover is closing."""
        return self._state == STATE_CLOSING

    @property
    def is_closed(self) -> bool | None:
        """Return whether cover is closed."""
        return self._state == STATE_CLOSED
