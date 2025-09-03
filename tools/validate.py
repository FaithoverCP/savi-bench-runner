import sys, json, yaml, pathlib
from jsonschema import validate, Draft202012Validator

schema = json.loads(pathlib.Path("schema/proof_manifest.schema.json").read_text())
errors = 0
for path in sys.argv[1:] or []:
    p = pathlib.Path(path)
    if not p.exists(): 
        print(f"[skip] {p} not found"); 
        continue
    data = yaml.safe_load(p.read_text())
    v = Draft202012Validator(schema)
    es = sorted(v.iter_errors(data), key=lambda e: e.path)
    if es:
        print(f"[fail] {p}")
        for e in es:
            loc = ".".join([str(x) for x in e.path])
            print(f"  - {loc}: {e.message}")
        errors += 1
    else:
        print(f"[ok]   {p}")
sys.exit(1 if errors else 0)