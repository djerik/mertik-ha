# Mertik Maxitrol for Home Assistant
- Please use on own risk, I take no responsibility.

## Requirements
- A Mertik Maxitrol wifi module that is connected to your local wifi.

## Installation
Files are installed by downloading the files to your custom_components folder directly from here or by adding it via HACS.

Afterwards you can go to the Integrations sections and click the add integration button. Search for Mertik and choose the newly added Mertik integration.

It will search your local network for the module and add the entities.

## Todo
- Move mertik.py to a python module with own repo
- Change I/O calls to async I/O calls
- Add to HACS repository for even easier installation
- Move Entities to a single Device / Platform
- Implement Zero Conf / autodetect IP

## Changelog
- 2026-02-24 Bug fixes due to breaking HA changes
- 2023-01-15 Initial version
