# DeyeCloud for Home Assistant

Experimental Home Assistant custom integration for the official DeyeCloud OpenAPI.

## Current status

Version 0.1.0 validates DeyeCloud credentials and verifies that the account's station list can be read. It does not create entities yet.

## Installation for development

Copy `custom_components/deyecloud` to Home Assistant's `/config/custom_components/deyecloud`, restart Home Assistant, then add **DeyeCloud** from **Settings > Devices & services**.

Use the Europe API base URL for European installations:

`https://eu1-developer.deyecloud.com`

## Security

Never commit DeyeCloud passwords, App Secrets, access tokens, refresh tokens, `.env` files, or Home Assistant `secrets.yaml`.

## Roadmap

- 0.1.x: authentication and station discovery
- 0.2.x: coordinator and station/device discovery
- 0.3.x: read-only sensors
- Later: diagnostics, energy dashboard support, and carefully gated control functions
