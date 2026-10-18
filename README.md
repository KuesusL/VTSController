# VTSController

A lightweight Python controller for interacting with the VTube Studio Public API through WebSocket.

VTSController provides a simple interface for communicating with VTube Studio, managing model parameters, triggering hotkeys, controlling expressions, and moving the current model.

## Features

- **WebSocket Connection** — Connect to the VTube Studio Public API.
- **Authentication** — Request, save, load, and use an authentication token.
- **API State** — Retrieve the API state.
- **Model Information** — Get information about the currently loaded model.
- **Parameter Management**
  - List default and custom input parameters.
  - Set parameter values.
  - Request the creation of custom parameters.
- **Hotkey Management**
  - List available hotkeys.
  - Trigger hotkeys by ID.
- **Expression Management**
  - List expressions and their states.
  - Activate or deactivate expressions.
- **Model Movement** — Change the current model's position, rotation, size, and movement duration.

## Requirements

- Python 3
- VTube Studio
- The `websocket-client` Python package

## Installation

Clone the repository:

```bash
git clone https://github.com/KuesusL/VTSController.git
cd VTSController
```

Install the dependency:

```bash
python -m pip install websocket-client
```

## Setup

1. Launch VTube Studio.
2. Enable the VTube Studio API and ensure its WebSocket server is running.
3. Make sure the configured host and port match your VTube Studio API settings.
4. Run your Python script and approve the plugin authentication request when prompted.

The controller uses the following default connection settings:

| Setting | Default |
|---|---|
| Host | `localhost` |
| Port | `8001` |
| WebSocket URL | `ws://localhost:8001` |
| Plugin name | `YOUR_PLUGIN_NAME` |
| Plugin developer | `YOUR_NAME` |

The plugin name and developer name are defined in the source code.

## Quick Start

```python
from VTS import VTSController

vts = VTSController()

try:
    vts.start()

    print(vts.get_api_state())
    print(vts.get_current_model())

finally:
    vts.stop()
```

`start()` connects to the WebSocket server, loads or requests an authentication token, and attempts to authenticate the plugin.

`stop()` closes the WebSocket connection when one exists.

More [Examples](examples/)

## API Reference

### Connection and Authentication

| Method | Description |
|---|---|
| `start()` | Connects and performs token-based authentication. |
| `stop()` | Closes the WebSocket connection. |
| `get_api_state()` | Requests the current API state. |

### Model Information

| Method | Description |
|---|---|
| `get_current_model()` | Returns the response data for the currently loaded model. |
| `move_current_model(time_seconds=0.5, posX=0.0, posY=0.0, rotation=0, size=-65)` | Requests a change to the current model's position, rotation, size, and movement duration. |

### Parameter Management

| Method | Description |
|---|---|
| `list_parameters()` | Lists default and custom parameters, returning formatted JSON text. |
| `set_parameter(parameter_id, value)` | Requests setting a parameter to a specified value. |
| `request_parameter_creation(parameter_name, min_val=0, max_val=1, default_val=0)` | Requests creation of a custom parameter. |

`request_parameter_creation()` raises a `ValueError` when `parameter_name` is empty.

### Hotkeys

| Method | Description |
|---|---|
| `list_hotkeys()` | Lists available hotkeys and selected metadata as formatted JSON text. |
| `trigger_hotkey(hotkey_id)` | Requests activation of a hotkey by its ID. |

### Expressions

| Method | Description |
|---|---|
| `list_expressions()` | Requests expression details and returns the extracted response data. |
| `set_expression(expression_file, active=True, fadeTime=0.0)` | Requests activation or deactivation of an expression. |

## Usage Examples

### Get the Current Model

```python
model = vts.get_current_model()
print(model)
```

### List Parameters

```python
parameters = vts.list_parameters()
print(parameters)
```

The result is a formatted JSON string containing selected information about each parameter.

### Set a Parameter

```python
vts.set_parameter("YourParameterID", 1.0)
```

Replace `YourParameterID` with a valid parameter ID available in your model or API configuration.

### List and Trigger Hotkeys

```python
hotkeys = vts.list_hotkeys()
print(hotkeys)

vts.trigger_hotkey("YOUR_HOTKEY_ID")
```

Replace the placeholder with an actual hotkey ID returned by the API.

### Activate an Expression

```python
vts.set_expression(
    expression_file="YourExpression.exp3.json",
    active=True,
    fadeTime=0.5
)
```

To deactivate the expression, pass `active=False`.

### Move the Current Model

```python
vts.move_current_model(
    time_seconds=1.0,
    posX=0.2,
    posY=0.0,
    rotation=0,
    size=-65
)
```

The values above are illustrative. Actual movement and size behavior depend on the VTube Studio API and the parameters accepted by the installed version.

### Create a Custom Parameter

```python
vts.request_parameter_creation(
    parameter_name="MyCustomParameter",
    min_val=0,
    max_val=1,
    default_val=0
)
```

The request may require user approval or additional permissions in VTube Studio.

## Authentication and Token Storage

VTSController stores the authentication token in a local file named `token.json`.

The file is created in the process's current working directory when a token is saved.


## Limitations

- The controller uses synchronous WebSocket communication.
- Each request sends one message and waits for one response.
- API errors and WebSocket exceptions are not comprehensively handled by the current implementation.
- Token storage uses a local JSON file.
- The controller assumes that the expected response fields are present in several authentication and data-handling methods.
- Compatibility depends on the VTube Studio Public API and the currently loaded model.

## Project Status

**Status:** Experimental / In development

This project is being developed as a personal programming project to explore Python, WebSocket communication, API integration, and VTube Studio control.

Features and interfaces may change as development continues.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.