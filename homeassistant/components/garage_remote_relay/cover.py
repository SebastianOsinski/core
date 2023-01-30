"""BleBox cover entity."""
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
    entities = [GarageDoor(remote)]
    async_add_entities(entities, True)


class GarageDoor(CoverEntity):
    def __init__(self, remote: GarageRemote) -> None:
        self._attr_device_class = CoverDeviceClass.GARAGE
        self._attr_supported_features = CoverEntityFeature.OPEN
        self.remote = remote
        self.state = STATE_CLOSED

    async def async_open_cover(self, **kwargs: Any) -> None:
        await self.remote.press()
        self.state = STATE_OPENING
        await asyncio.sleep(CONF_COVER_MOVEMENT_DURATION)
        self.state = STATE_OPEN
        await asyncio.sleep(CONF_COVER_AUTO_CLOSE_DELAY)
        self.state = STATE_CLOSING
        await asyncio.sleep(CONF_COVER_MOVEMENT_DURATION)
        self.state = STATE_CLOSED

    @property
    def is_opening(self) -> bool | None:
        """Return whether cover is opening."""
        return self.state == STATE_OPENING

    @property
    def is_closing(self) -> bool | None:
        """Return whether cover is closing."""
        return self.state == STATE_CLOSING

    @property
    def is_closed(self) -> bool | None:
        """Return whether cover is closed."""
        return self.state == STATE_CLOSED
