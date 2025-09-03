import sys, json, pathlib, yaml
from jsonschema import Draft202012Validator

# Loader that keeps timestamps as plain strings
class NoDatesSafeLoader(yaml.SafeLoader):
    pass
# remove implicit resolver for timestamps
for ch, mapping in list(NoDatesSafeLoader.yaml_implicit_resolvers.items()):
    NoDatesSafeLoader.yaml_implicit_resolvers[ch] = [
        (tag, regexp) for (tag, regexp) in mapping if tag != 'tag:yaml.org,2002:timestamp'
    ]

schema = json.loads(pathlib.Path("schema/proof_manifest.schema.json").read_text())
errors = 0
paths = sys.argv[1:]
for path in paths or []:
    p = pathlib.Path(path)
    if not p.exists():
        print(f"[skip] {p} not found")
        continue
    data = yaml.load(p.read_text(), Loader=NoDatesSafeLoader)
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