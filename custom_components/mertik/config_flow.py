import logging

from typing import Any, Dict, Optional

from homeassistant import config_entries
from homeassistant.const import CONF_NAME, CONF_HOST
import voluptuous as vol

from .const import DOMAIN

from .mertik import Mertik

_LOGGER = logging.getLogger(__name__)


class MertikConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Mertik config flow."""

    data: Optional[Dict[str, Any]]

    async def async_step_user(self, device_input: Optional[Dict[str, Any]] = None):
        """Invoked when a user initiates a flow via the user interface."""
        errors: Dict[str, str] = {}
        if device_input is not None:
            self.data = device_input

            return self.async_create_entry(title="Mertik Maxitrol", data=self.data)

        DEVICE_SCHEMA = vol.Schema(
            {vol.Required(CONF_NAME): str, vol.Required(CONF_HOST): str}
        )

        return self.async_show_form(
            step_id="user", data_schema=DEVICE_SCHEMA, errors=errors
        )
