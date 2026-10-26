import json
import uuid
from pathlib import Path

import websocket


class VTSController:
    def __init__(self, host="localhost", port=8001, plugin_name="YOUR_PLUGIN_NAME", author="YOUR_NAME"):
        self.url = f"ws://{host}:{port}"
        
        self.ws = None
        self.token = None
        self.token_file = Path("token.json")
        self.plugin_name = plugin_name
        self.author = author
        
    def start(self):
        self._load_token()
        self._connect()
        if self.token is None:
            self._request_token()
            self._save_token()
        
        self._authenticate()
        
    def stop(self):
        if self.ws is not None:    
            self.ws.close()
            self.ws = None
        
    def _connect(self):
        self.ws = websocket.create_connection(self.url)  
        
    def _send_request(self, message_type, data):
        request = {
            "apiName": "VTubeStudioPublicAPI",
                "apiVersion": "1.0",
                "requestID": self._generate_uuid(),
                "messageType": message_type,
                "data": data
        }
        self.ws.send(json.dumps(request))
        
        response = self.ws.recv()
        
        return json.loads(response)
        
    def get_api_state(self):
        return self._send_request(
            "APIStateRequest",
            {}
        )
        
    def _request_token(self):
        response =  self._send_request(
            "AuthenticationTokenRequest",
            {
                "pluginName": self.plugin_name,
                "pluginDeveloper": self.author
            }
        )
        
        self.token = response["data"]["authenticationToken"]
        
    def _load_token(self):
        if self.token_file.exists():
            data = json.loads(self.token_file.read_text())
            self.token = data["token"]
    
    def _save_token(self):
        data = {
            "token": self.token
        }
        self.token_file.write_text(json.dumps(data))
        
    def _authenticate(self):
        response = self._send_request(
            "AuthenticationRequest",
            {
                "pluginName": self.plugin_name,
                "pluginDeveloper": self.author,
                "authenticationToken": self.token
            }
        )
        if response["data"]["authenticated"] == False:
            self._request_token()
            self._save_token()
            response = self._send_request(
                "AuthenticationRequest",
                {
                    "pluginName": self.plugin_name,
                    "pluginDeveloper": self.author,
                    "authenticationToken": self.token
                }
            )
            
        return response
        
    def _generate_uuid(self):
        return str(uuid.uuid4())
        
    def get_current_model(self):
        response =  self._send_request(
            "CurrentModelRequest",
            {}
        )
        
        return response.get("data", {})
    
    def list_parameters(self):
        response = self._send_request(
            "InputParameterListRequest",
            {}
        )
        
        return self._extract_data(
            response=response,
            response_type=["defaultParameters", "customParameters"],
            key_field="name",
            fields_wanted=["addedBy", "value", "min", "max", "defaultValue"],
            indent=4
        )
    
    def set_parameter(self, parameter_id, value):
        return self._send_request(
            "InjectParameterDataRequest",
            {
                "faceFound": False,
                "mode": "set",
                "parameterValues": [
                    {
                        "id": parameter_id,
                        "value": value
                    }
                ]
            }
        )
        
    def trigger_hotkey(self, hotkey_id):
        return self._send_request("HotkeyTriggerRequest", {
            "hotkeyID": hotkey_id
        })
        
    def request_parameter_creation(self, parameter_name, min_val=0, max_val=1, default_val=0):
        if not parameter_name:
            raise ValueError("Parameter harus memiliki Nama!")
        
        return self._send_request("ParameterCreationRequest",
            {
                "parameterName": parameter_name,
		        "explanation": "Parameter created by VTS Controller.",
		        "min": min_val,
		        "max": max_val,
		        "defaultValue": default_val
            })
    
    def move_current_model(self, time_seconds=0.5, posX=0.0, posY=0.0, rotation=0, size=-65):
        return self._send_request("MoveModelRequest",
                {
                    "timeInSeconds": time_seconds,
                    "positionX": posX,
		            "positionY": posY,
		            "rotation": rotation,
		            "size": size
                }
            )
        
    def list_hotkeys(self):
        response = self._send_request("HotkeysInCurrentModelRequest", {})
        
        return self._extract_data(
            response=response,
            response_type="availableHotkeys",
            key_field="name",
            fields_wanted=["file", "hotkeyID", "type"],
            indent=4
        )
    
    def _extract_data(self, response, response_type, key_field, fields_wanted, indent=None):
        response_types = [response_type] if isinstance(response_type, str) else response_type
        
        result = {}
        for r_type in response_types:
            raw_list =  response.get("data", {}).get(r_type, [])
            for item in raw_list:
                outer_key = item.get(key_field)
                if outer_key:
                    result[outer_key] = {field: item.get(field) for field in fields_wanted}
                
        if indent is not None:
            return json.dumps(result, indent=indent, ensure_ascii=False)
        
        return result
    
    def set_expression(self, expression_file, active=True, fadeTime=0.0):
        return self._send_request("ExpressionActivationRequest", {
            "expressionFile": expression_file, 
            "fadeTime": fadeTime,
            "active": active                     
        })
        
    def list_expressions(self):
        response = self._send_request("ExpressionStateRequest",{
            "details": True
        })
        
        data = self._extract_data(
            response=response,
            response_type="expressions",
            key_field="name",
            fields_wanted=["file", "active", "usedInHotkeys"],
            indent=4
        )
        
        return data
        