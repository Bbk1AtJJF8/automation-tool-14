import copy
from typing import Any, Callable, Generator, Union

def _traverse_and_inject(data: Any, path: tuple = ()) -> Generator[tuple, Any, None]:
    """Recursively yields (path, value) pairs and updates in-place if sent a new value."""
    if isinstance(data, dict):
        for key, val in list(data.items()):
            current_path = path + (key,)
            if isinstance(val, (dict, list)):
                yield from _traverse_and_inject(val, current_path)
            else:
                sent = yield (current_path, val)
                if sent is not None:
                    data[key] = sent
    elif isinstance(data, list):
        for idx, val in enumerate(list(data)):
            current_path = path + (idx,)
            if isinstance(val, (dict, list)):
                yield from _traverse_and_inject(val, current_path)
            else:
                sent = yield (current_path, val)
                if sent is not None:
                    data[idx] = sent

def dynamic_weave(data: Union[dict, list], mutation_rules: Callable[[tuple, Any], Any]) -> Union[dict, list]:
    """
    Transforms deep structures dynamically using custom mutation rules.
    Leverages generator coroutines to inject transformed values back into the source.
    """
    if not isinstance(data, (dict, list)):
        return data
    
    cloned_data = copy.deepcopy(data)
    traverser = _traverse_and_inject(cloned_data)
    
    try:
        path, val = next(traverser)
        while True:
            new_val = mutation_rules(path, val)
            if new_val != val:
                path, val = traverser.send(new_val)
            else:
                path, val = next(traverser)
    except StopIteration:
        pass
        
    return cloned_data