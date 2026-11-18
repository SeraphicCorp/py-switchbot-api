"""Hub device constants from the SwitchBot API v1.1 specifications.

AI Hub exposes firmware and onlineStatus. Hub 2 exposes temperature in
celsius, humidity, firmware, and lightLevel (1-20). Hub 3 adds the boolean
moveDetected and onlineStatus, with lightLevel ranging from 1 to 10.

Hub 4 status reports version, temperature, humidity, lightLevel (1-10),
boolean moveDetected and onlineStatus (online/offline). Its changeReport
webhook uses deviceType "Hub 4" and reports temperature, humidity, light
or motion changes. The context uses detectionState (DETECTED or NOT_DETECTED)
for motion, lightLevel on the same 1-10 scale, and scale for temperature units.

OnlineStatus and DetectionState enums are shared in common.models.
Use sensor.utils.sensor_detection_state for the boolean moveDetected status
or the detectionState webhook field. REST status temperature is in Celsius.
Webhook payloads keep their scale field so callers can determine the unit.

Source: https://github.com/OpenWonderLabs/SwitchBotAPI/tree/main/devices/hubs
"""

from typing import Final

HUB: Final = "Hub"
HUB_PLUS: Final = "Hub Plus"
HUB_MINI: Final = "Hub Mini"
HUB_2: Final = "Hub 2"
HUB_3: Final = "Hub 3"
HUB_4: Final = "Hub 4"
HUB_4_LIGHT_LEVEL_RANGE: Final = range(1, 11)
AI_HUB: Final = "AI Hub"

# Discovery names are used here. Hub 2 webhooks identify it as WoHub2.
HUB_DEVICE_TYPES: Final[list[str]] = [
    HUB,
    HUB_PLUS,
    HUB_MINI,
    HUB_2,
    HUB_3,
    HUB_4,
    AI_HUB,
]
