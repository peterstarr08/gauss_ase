import json
from gs.utils.log import get_std_logger

log = get_std_logger(__name__)

def save_json(path, range: list[tuple[int, int]], **kwargs):
    data = {
        **kwargs,
        "range": [list(r) for r in range]
    }

    with open(path, "w") as f:
        json.dump(data, f, indent=2)
        log.info("JSON meta data generated at %s", str(path))

def load_json(path):
    with open(path, "r") as f:
        data = json.load(f)
        log.info("Read JSON meta data at %s", str(path))
    
    # range = [tuple(r) for r in data.pop("range", [])]
    return data

def get_range(path):
    data = load_json(path)
    range = [tuple(r) for r in data.pop("range", [])]
    log.debug("range=%s from %s", str(range), str(path))
    return range


if __name__=="__main__":
    save_json("sample.json", [(0,99),(100,199)])