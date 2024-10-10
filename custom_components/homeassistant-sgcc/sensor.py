from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN
from homeassistant.const import(
    DEVICE_CLASS_ENERGY,
    ENERGY_KILO_WATT_HOUR,
    STATE_UNKNOWN
)

SGCC_SENSORS = {
    "address": {
        "name": "寝室",
        "icon": "mdi:bed"
    },
    "allowance": {
        "name": "电费余额",
        "icon": "mdi:wallet-bifold",
        "unit_of_measurement": "CNY"
    },
    "month_bill": {
        "name": "本月电费",
        "icon": "hass:cash-100",
        "unit_of_measurement": "CNY"
    },
    "month_elec": {
        "name": "本月用电",
        "icon": "mdi:lightning-bolt",
        "unit_of_measurement": "kWh"
    },
    "price": {
        "name": "当前电价",
        "icon": "mdi:cart",
        "unit_of_measurement": "CNY/kWh"
    },
}

async def async_setup_platform(hass, config, async_add_devices, discovery_info=None):
    sensors = []
    coordinator = hass.data[DOMAIN]
    data = coordinator.data
    for key in SGCC_SENSORS.keys():
        if key in data.keys():
            sensors.append(SGCCSensor(coordinator, key))
    for month in range(13):
        sensors.append(SGCCHistorySensor(coordinator, month))
    async_add_devices(sensors, True)


class SGCCSensor(CoordinatorEntity):
    def __init__(self, coordinator, sensor_key):
        super().__init__(coordinator)
        self._sensor_key = sensor_key
        self._config = SGCC_SENSORS[self._sensor_key]
        self._attributes = self._config.get("attributes")
        self._coordinator = coordinator
        self._unique_id = f"{DOMAIN}.{sensor_key}"
        self.entity_id = self._unique_id

    def get_value(self, attribute = None):
        try:
            if attribute is None:
                return self._coordinator.data.get(self._sensor_key)
            return self._coordinator.data.get(attribute)
        except KeyError:
            return STATE_UNKNOWN

    @property
    def unique_id(self):
        return self._unique_id

    @property
    def should_poll(self):
        return False

    @property
    def name(self):
        return self._config.get("name")

    @property
    def state(self):
        return self.get_value()

    @property
    def icon(self):
        return self._config.get("icon")

    @property
    def device_class(self):
        return self._config.get("device_class")

    @property
    def unit_of_measurement(self):
        return self._config.get("unit_of_measurement")

    @property
    def extra_state_attributes(self):
        attributes = {}
        if self._attributes is not None:
            try:
                for attribute in self._attributes:
                    attributes[attribute] = self.get_value(attribute)
            except KeyError:
                pass
        return attributes


class SGCCHistorySensor(CoordinatorEntity):
    def __init__(self, coordinator, index):
        super().__init__(coordinator)
        self._coordinator = coordinator
        self._index = index
        self._unique_id = f"{DOMAIN}.history_{index + 1}"
        self.entity_id = self._unique_id

    @property
    def unique_id(self):
        return self._unique_id

    @property
    def should_poll(self):
        return False

    @property
    def name(self):
        try:
            month = self._coordinator.data.get("bill")[self._index].get("month")
            year = self._coordinator.data.get("bill")[self._index].get("year")
            return f'{year}-{month}'
        except KeyError:
            return STATE_UNKNOWN

    @property
    def state(self):
        try:
            # return self._coordinator.data.get("bill")[self._index].get("electric")
            return self._coordinator.data.get("bill")[self._index].get("electric")
        except KeyError:
            return STATE_UNKNOWN

    @property
    def extra_state_attributes(self):
        try:
            return {
                "consume_bill": self._coordinator.data.get("bill")[self._index].get("money")
            }
        except KeyError:
            return {"consume_bill": 0.0}

    @property
    def device_class(self):
        return DEVICE_CLASS_ENERGY

    @property
    def unit_of_measurement(self):
        return ENERGY_KILO_WATT_HOUR
