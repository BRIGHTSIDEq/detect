from pathlib import Path
import json
p=Path('artifacts/coreml/classes.json')
assert p.exists(), 'Нет metadata classes.json'
json.loads(p.read_text(encoding='utf-8'))
print('Core ML metadata OK')
