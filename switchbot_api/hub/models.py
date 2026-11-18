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
Webhook temperature units remain in the raw scale field; status temperature
is documented in celsius. Hub 2 webhook deviceType is WoHub2, whereas
Hub 3 uses its discovery type, Hub 3.

Source: https://github.com/OpenWonderLabs/SwitchBotAPI/tree/main/devices/hubs
Hub 4 source: SwitchBot OpenAPI document, revision 11124, Hub 4 section.
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

HUB_DEVICE_TYPES: Final[list[str]] = [
    HUB,
    HUB_PLUS,
    HUB_MINI,
    HUB_2,
    HUB_3,
    HUB_4,
    AI_HUB,
]
