import logging
import asyncio
import async_timeout
from datetime import timedelta
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.helpers import discovery
from homeassistant.core import HomeAssistant
from .sgcc import SGCCData
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

UPDATE_INTERVAL = timedelta(minutes=10)


async def async_setup(hass: HomeAssistant, hass_config: dict):
    config = hass_config[DOMAIN]
    certificate = config.get("certificate")
    userid = config.get("userid")
    if certificate is not None or userid is not None:
        coordinator = GJDWCorrdinator(hass, certificate, userid)
        hass.data[DOMAIN] = coordinator
        await coordinator.async_refresh()
        hass.async_create_task(discovery.async_load_platform(
            hass, "sensor", DOMAIN, config, hass_config))
    else:
        _LOGGER.error("The required parameter certificate or userid is missing")
    return True

class GJDWCorrdinator(DataUpdateCoordinator):
    def __init__(self, hass, certificate, userid):
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=UPDATE_INTERVAL
        )
        self._hass = hass
        self._sgcc = SGCCData(certificate, userid)

    async def _async_update_data(self):
        _LOGGER.debug("Data updating...")
        data = self.data
        try:
            async with async_timeout.timeout(60):
                data = await self._hass.async_add_executor_job(
                    self._sgcc.getData
                )
        except asyncio.TimeoutError:
            _LOGGER.warning("Data update timed out")
        return data

