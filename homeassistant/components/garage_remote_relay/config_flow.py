"""Config flow for Garage Remote Relay integration."""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult

from .const import (
    DOMAIN,
    CONF_SERIAL_PORT,
    CONF_COVER_MOVEMENT_DURATION,
    CONF_REMOTE_PRESS_DURATION,
    CONF_COVER_AUTO_CLOSE_DELAY,
)

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_SERIAL_PORT): str,
        vol.Required(CONF_REMOTE_PRESS_DURATION): vol.Coerce(float),
        vol.Required(CONF_COVER_MOVEMENT_DURATION): vol.Coerce(float),
        vol.Required(CONF_COVER_AUTO_CLOSE_DELAY): vol.Coerce(float),
    }
)


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Garage Remote Relay."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        if user_input is not None:
            config = {
                CONF_SERIAL_PORT: user_input[CONF_SERIAL_PORT],
                CONF_REMOTE_PRESS_DURATION: user_input[CONF_REMOTE_PRESS_DURATION],
                CONF_COVER_MOVEMENT_DURATION: user_input[CONF_COVER_MOVEMENT_DURATION],
                CONF_COVER_AUTO_CLOSE_DELAY: user_input[CONF_COVER_AUTO_CLOSE_DELAY],
            }

            await self.async_set_unique_id("garage_remote_relay")
            self._abort_if_unique_id_configured()

            return self.async_create_entry(
                title=f"Garage Remote Relay", 
                data=config,
                description=config[CONF_SERIAL_PORT]
            )

        return self.async_show_form(
            step_id="user", data_schema=STEP_USER_DATA_SCHEMA
        )
