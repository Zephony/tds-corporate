import json
import pkgutil
import importlib
import inspect
from pathlib import Path

# Ensure project root on path
root = Path(__file__).resolve().parents[1]
import sys
if str(root) not in sys.path:
    sys.path.insert(0, str(root))

from backend.models.base import BaseModel

mapping = {}

package = importlib.import_module('backend.models')

# iterate modules within backend.models
for _, module_name, is_pkg in pkgutil.walk_packages(package.__path__, package.__name__ + '.'):
    if is_pkg:
        continue
    module = importlib.import_module(module_name)
    for name, obj in inspect.getmembers(module, inspect.isclass):
        if not issubclass(obj, BaseModel):
            continue
        if getattr(obj, '__tablename__', None) is None:
            continue
        filterable = getattr(obj, 'filterable_fields', None)
        if not filterable:
            continue
        mapping[obj.__tablename__] = filterable

print(json.dumps(mapping))
