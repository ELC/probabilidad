import json
from pathlib import Path

path = Path("book/_build/html/chapters.probability.json")
data = json.loads(path.read_text(encoding="utf-8"))


def find_outputs(o, found):
    if isinstance(o, dict):
        if o.get("type") == "output":
            found.append(o)
        for v in o.values():
            find_outputs(v, found)
    elif isinstance(o, list):
        for x in o:
            find_outputs(x, found)


found: list = []
find_outputs(data, found)
print(f"output nodes: {len(found)}")
for i, node in enumerate(found):
    jd = node.get("jupyter_data", {})
    keys = list((jd.get("data") or {}).keys())
    output_type = jd.get("output_type")
    exec_count = jd.get("execution_count")
    print(f"[{i:2d}] type={output_type} count={exec_count} mime={keys}")
