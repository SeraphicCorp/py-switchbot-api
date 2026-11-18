"""Other physical device and virtual infrared command enums.

Remote and AI MindClip have no device control commands. Kata diary and MindClip
recording queries are separate feature endpoints, not command names. Custom IR
buttons use their configured name with send_command(command_type="customize"),
not a fixed command named customize. All default actions use parameter default.
Source: https://github.com/OpenWonderLabs/SwitchBotAPI/tree/main/devices/others
"""

from switchbot_api.common import Commands


class BotCommands(Commands):
    """Bot actions; power state is useful only in switchMode."""

    ON = "turnOn"
    OFF = "turnOff"
    PRESS = "press"


class ArtFrameCommands(Commands):
    """Image navigation, upload, and one-image cloud deletion."""

    NEXT = "next"
    PREVIOUS = "previous"
    UPLOAD_IMAGE = "uploadImage"
    # String parameter: random, newest, or oldest; protects the displayed image.
    DELETE_IMAGE = "deleteImage"


class ArtFrame2Commands(Commands):
    """Shared image controls for AI Art Frame 2 and AI Art Frame Luma."""

    NEXT = "next"
    PREVIOUS = "previous"
    UPLOAD_IMAGE = "uploadImage"
    # String parameter: random, newest, or oldest; protects the displayed image.
    DELETE_IMAGE = "deleteImage"


class WeatherStationCommands(Commands):
    """Custom display text and cancelCustom (default parameter)."""

    # String parameter: at most 100 characters; use weather_station_quote_parameter.
    CUSTOM_QUOTE = "customQuote"
    CANCEL_CUSTOM = "cancelCustom"
    CUSTOM_PAGE = "customPage"
    # Object parameter: templateID, componentID, text (at most 100 characters).
    CUSTOM_PUT_COMPONENT = "customPutComponent"


class KataFriendsCommands(Commands):
    """Kata controls; backHome uses default, feature switches use on/off."""

    SET_MODE = "mode"
    SET_CHILD_LOCK = "childLock"
    BACK_HOME = "backHome"
    SET_PICTURE_TAKING = "pictureTaking"
    SET_SNAPSHOTS = "snapshots"
    SET_TALK = "talk"


class InfraredPowerCommands(Commands):
    """Power commands for infrared types other than Others."""

    ON = "turnOn"
    OFF = "turnOff"


class InfraredAirConditionerCommands(Commands):
    """Air conditioner setAll parameter is temperature,mode,fan,power."""

    ON = "turnOn"
    OFF = "turnOff"
    SET_ALL = "setAll"


class InfraredTVCommands(Commands):
    """TV-family commands; SetChannel capitalization is significant."""

    ON = "turnOn"
    OFF = "turnOff"
    SET_CHANNEL = "SetChannel"
    VOLUME_UP = "volumeAdd"
    VOLUME_DOWN = "volumeSub"
    CHANNEL_UP = "channelAdd"
    CHANNEL_DOWN = "channelSub"


class InfraredIPTVStreamerCommands(Commands):
    """TV-family commands; SetChannel capitalization is significant."""

    ON = "turnOn"
    OFF = "turnOff"
    SET_CHANNEL = "SetChannel"
    VOLUME_UP = "volumeAdd"
    VOLUME_DOWN = "volumeSub"
    CHANNEL_UP = "channelAdd"
    CHANNEL_DOWN = "channelSub"


class InfraredSetTopBoxCommands(Commands):
    """TV-family commands; SetChannel capitalization is significant."""

    ON = "turnOn"
    OFF = "turnOff"
    SET_CHANNEL = "SetChannel"
    VOLUME_UP = "volumeAdd"
    VOLUME_DOWN = "volumeSub"
    CHANNEL_UP = "channelAdd"
    CHANNEL_DOWN = "channelSub"


class InfraredDVDCommands(Commands):
    """DVD media command spellings differ from Art Frame navigation."""

    ON = "turnOn"
    OFF = "turnOff"
    MUTE = "setMute"
    FAST_FORWARD = "FastForward"
    REWIND = "Rewind"
    NEXT = "Next"
    PREVIOUS = "Previous"
    PAUSE = "Pause"
    PLAY = "Play"
    STOP = "Stop"


class InfraredSpeakerCommands(Commands):
    """Speaker media and volume controls."""

    ON = "turnOn"
    OFF = "turnOff"
    MUTE = "setMute"
    FAST_FORWARD = "FastForward"
    REWIND = "Rewind"
    NEXT = "Next"
    PREVIOUS = "Previous"
    PAUSE = "Pause"
    PLAY = "Play"
    STOP = "Stop"
    VOLUME_UP = "volumeAdd"
    VOLUME_DOWN = "volumeSub"


class InfraredFanCommands(Commands):
    """Virtual infrared fan controls, separate from physical circulator fans."""

    ON = "turnOn"
    OFF = "turnOff"
    SWING = "swing"
    TIMER = "timer"
    LOW_SPEED = "lowSpeed"
    MIDDLE_SPEED = "middleSpeed"
    HIGH_SPEED = "highSpeed"


class InfraredLightCommands(Commands):
    """Virtual infrared light controls."""

    ON = "turnOn"
    OFF = "turnOff"
    BRIGHTNESS_UP = "brightnessUp"
    BRIGHTNESS_DOWN = "brightnessDown"
