# This is a Mockup
import json
from pathlib import Path

DEBUG = True

active_planes = {}

def parse_json(file):
    # returns the raw json data as a dict
    with open(file) as f:
        data = json.load(f)
    return data

def parse_jsonc(file):
    with open(file) as f:
        lines = f.readlines()

    # remove comments
    content = "".join([line for line in lines if not line.strip().startswith("/")])

    return json.loads(content)

def get_aircraft(json_data):
    aircraft_list = {}
    
    for aircraft in json_data.get("aircraft", []):
        icao = aircraft.get("hex")
        
        # Hopefully my understanding of the data structure is correct, if not, -_- (Internal screaming)
        if "lat" in aircraft and "lon" in aircraft:
            aircraft_list[icao] = {
                "flight": aircraft.get("flight", "Unknown").strip(),
                "lat": aircraft["lat"],
                "lon": aircraft["lon"],
                "alt": aircraft.get("alt_baro", 0), # baro altitude in feet
                "speed": aircraft.get("gs", 0), # gs is the ground speed in knots (or others, dump1090 cant differentiate)
                "track": aircraft.get("track", 0) # track is the direction the plane is moving in degrees
            }
            
    return aircraft_list

def main():
    current_file = Path(__file__).resolve()
    main_dir = current_file.parent
    project_root = main_dir.parent

    # this is supposed to be (system_root)/run/aircraft.json, rn It's for testing
    dump1090_dir = project_root / "run"

    dump1090_json = dump1090_dir / "aircraft.jsonc"

    data = parse_jsonc(dump1090_json)

    if DEBUG:
        print("[DEBUG] Current file:", current_file)
        print("[DEBUG] Main directory:", main_dir)
        print("[DEBUG] Root directory:", project_root)
        print("[DEBUG] Dump1090 directory:", dump1090_dir)
        print("[DEBUG] RAWWWW json:", dump1090_json)

    print(get_aircraft(data))
    

if __name__ == "__main__":
    main()
