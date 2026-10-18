import json
from pathlib import Path


def change_expression(vts, model: str, tagOrFile: str, active: bool=True, fadeTime: float=0.0):
    map_file = Path("model_data") / model / "expressions_map.json"
    
    if map_file.exists:
        map = json.loads(map_file.read_text(encoding="utf-8"))
        
        file_name = map.get(tagOrFile, tagOrFile)
    else:
        file_name = tagOrFile
    return vts.set_expression(file_name, active, fadeTime)
