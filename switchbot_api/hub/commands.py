"""Hub command availability in the SwitchBot API v1.1 specifications.

The official capability table marks device control commands as unsupported
for AI Hub, Hub 2, Hub 3, Hub 4, Hub, Hub Plus, and Hub Mini. No command enums are
defined here. Device discovery and supported status queries use the existing
client methods; infrared control targets virtual remote device IDs.

Hub 2, Hub 3 and Hub 4 support sensor webhooks; AI Hub has no documented webhook.
Source: https://github.com/OpenWonderLabs/SwitchBotAPI#hubs
"""
