import json
import re
import sys
from pathlib import Path

from VTS import VTSController

sys.stdout.reconfigure(encoding="utf-8")

def sanitize_folder_name(name: str) -> str:
    return re.sub(r'[\\/*?:"<>|]', "", name).strip()

def sanitize_tag(name_or_file: str) -> str:
    clean = re.sub(r"\.exp3\.json$|\.json$", "", name_or_file, flags=re.IGNORECASE)

    clean = re.sub(r"^\d+[\s_-]*", "", clean)

    clean = clean.lower().strip()
    clean = re.sub(r"[\s-]+", "_", clean)

    return clean

def update_config():
    vts = VTSController()
    vts.start()
    
    try:
        model_info = vts.get_current_model()
        model_loaded = model_info.get("modelLoaded", False)
    
        if not model_loaded:
            print("Tidak ada model yang dimuat!")
            return
    
        model_name = model_info.get("modelName", "Unknown Model")
        print(f"Memproses data untuk model: {model_name}")
        
        safe_name = sanitize_folder_name(model_name)
        model_dir = Path("model_data") / safe_name
        
        model_dir.mkdir(parents=True, exist_ok=True)
        
        params = vts.list_parameters()
        hotkeys = vts.list_hotkeys()
        expressions = vts.list_expressions()
            
            
        (model_dir / "parameters.json").write_text(params, encoding="utf-8")
        (model_dir / "hotkeys.json").write_text(hotkeys, encoding="utf-8")
        (model_dir / "expressions.json").write_text(expressions, encoding="utf-8")
        
        data = json.loads((model_dir / "expressions.json").read_text(encoding="utf-8"))
        expressions_map_dict = {key: info["file"] for key, info in data.items()}
        expressions_map_json = json.dumps(expressions_map_dict, indent=4, ensure_ascii=False)
        (model_dir / "expressions_map.json").write_text(expressions_map_json, encoding="utf-8")
        
        
        print(f"Berhasil menyimpan data model di: {model_dir}!")
    finally:
        vts.stop()
    
if __name__ == "__main__":
    update_config()