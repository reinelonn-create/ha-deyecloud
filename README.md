# DeyeCloud for Home Assistant

A Home Assistant custom integration for the official DeyeCloud OpenAPI.

This integration connects Home Assistant to DeyeCloud and automatically imports data from your photovoltaic installation, including power, energy, battery and inverter information.

## Features

- Official DeyeCloud OpenAPI support
- Config Flow setup
- Automatic station and device discovery
- Read-only sensors
- Efficient polling using DataUpdateCoordinator
- Swedish and English translations
- Supports multiple stations
- HACS compatible

## Installation

### HACS

1. Open HACS.
2. Go to **Integrations**.
3. Add this repository as a Custom Repository.
4. Install **DeyeCloud**.
5. Restart Home Assistant.

### Manual installation

Copy the folder:

```
custom_components/deyecloud
```

to:

```
config/custom_components/
```

Restart Home Assistant and add the integration from:

**Settings → Devices & Services → Add Integration**

## Configuration

You will need:

- DeyeCloud Username
- DeyeCloud Password
- App ID
- App Secret
- API Base URL

For Europe use:

```
https://eu1-developer.deyecloud.com
```

## Available Sensors

Depending on your installation, the integration can expose sensors such as:

- PV Power
- Grid Power
- Load Power
- Battery State of Charge
- Battery Power
- Battery Voltage
- Daily Energy
- Monthly Energy
- Yearly Energy
- Total Energy
- Inverter Status

The available sensors depend on the information provided by the DeyeCloud API.

## Supported Systems

The integration is intended for systems connected through the official DeyeCloud platform.

## Languages

- English
- Svenska

## Security

Credentials are stored using Home Assistant's secure storage.

Never publish or commit:

- Passwords
- App Secrets
- Access Tokens
- Refresh Tokens
- secrets.yaml

## Roadmap

Planned improvements include:

- Diagnostics support
- Improved device metadata
- Additional sensors
- Energy Dashboard enhancements

## License

MIT License