# SwitchBot Proxy

HTTP REST proxy for SwitchBot devices, providing proper `turnOn`/`turnOff` control for Home Assistant integration.

## Why This Exists

The official Home Assistant SwitchBot integration has limitations:
- Only provides a `press` command, not proper `turnOn`/`turnOff` actions
- SwitchBot Hub 3 motion sensors don't update properly

This proxy bridges those gaps by providing REST endpoints that Home Assistant can call directly.

## Features

- HTTP POST endpoints for `turnOn` and `turnOff` commands
- Direct integration with SwitchBot API
- Docker containerized for easy deployment
- Works with Home Assistant's REST integration

## Quick Start

### Docker

```bash
docker pull muness/switchbot-proxy:latest

docker run -d \
  -p 8099:8099 \
  -e SWITCHBOT_TOKEN="your_token_here" \
  -e SWITCHBOT_SECRET="your_secret_here" \
  --name switchbot-proxy \
  muness/switchbot-proxy:latest
```

Or using docker-compose:

```yaml
version: '3.8'
services:
  switchbot-proxy:
    image: muness/switchbot-proxy:latest
    ports:
      - "8099:8099"
    environment:
      SWITCHBOT_TOKEN: "your_token_here"
      SWITCHBOT_SECRET: "your_secret_here"
    restart: unless-stopped
```

### Configuration

Set your SwitchBot credentials via environment variables:
- `SWITCHBOT_TOKEN` - Your SwitchBot API token
- `SWITCHBOT_SECRET` - Your SwitchBot API secret

Get your credentials from the [SwitchBot Developer Portal](https://developer.switch-bot.com/).

## Home Assistant Integration

### Switch Configuration

Add to your `configuration.yaml`:

```yaml
rest_command:
  flair58_turn_on:
    url: "http://192.168.1.2:8099/devices/D8BFC586721F/turnOn"
    method: POST
  flair58_turn_off:
    url: "http://192.168.1.2:8099/devices/D8BFC586721F/turnOff"
    method: POST

switch:
  - platform: template
    switches:
      flair_58_switchbot:
        unique_id: flair58_switchbot
        turn_on:
          - action: rest_command.flair58_turn_on
        turn_off:
          - action: rest_command.flair58_turn_off
        value_template: "{{ states('switch.flair_58') }}"
```

### Binary Sensor Configuration

For Hub 3 motion sensors:

```yaml
binary_sensor:
  - platform: rest
    name: "Hub 3 Motion"
    unique_id: hub3_motion
    resource: http://192.168.1.2:8099/devices/B0E9FE6ADD0E/status
    value_template: "{{ value_json.body.moveDetected }}"
    device_class: motion
    scan_interval: 60
```

## API Endpoints

### POST /turnOn
Activates the SwitchBot device.

### POST /turnOff
Deactivates the SwitchBot device.

## Development

### Running Locally

```bash
python3 server.py
```

Server runs on `http://0.0.0.0:8099`

### Building Docker Image

```bash
docker build -t switchbot-proxy -f docker/Dockerfile .
```

## GitHub Actions Setup

To enable automatic Docker Hub publishing, add these secrets to your GitHub repository:
- `DOCKERHUB_USERNAME` - Your Docker Hub username
- `DOCKERHUB_TOKEN` - Your Docker Hub access token

The workflow automatically builds and pushes on:
- Pushes to main/master branch → `latest` tag
- Version tags (v*) → semantic version tags
- Pull requests → build only (no push)

## License

MIT
