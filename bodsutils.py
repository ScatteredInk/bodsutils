import uuid
import jsonpatch
from jsonschema import validate
from jsonpath_ng import jsonpath, parse

__all__ = ['find_matching_paths',
           'json_paths_to_json_patch_paths',
           'patch_replace_from_paths_values',
           'patch_delete_from_paths',
           'replace_uuids']

def find_matching_paths(json, jsonpexpr = '$..id'):
    jsonpath_expr = parse(jsonpexpr)
    return [str(match.full_path) for match in jsonpath_expr.find(json)]

def json_paths_to_json_patch_paths(paths):
    patch_paths = []
    for path in paths:
        p = str.replace(path, ".", "/")
        p = str.replace(p, "[", "")
        p = str.replace(p, "]", "")
        patch_paths.append("/" + p)
    return patch_paths

def patch_replace_from_paths_values(paths, values):
    patches = []
    for p, v in zip(paths, values):
        patch = {'op': 'replace',
                 'path': p,
                 'value': v}
        patches.append(patch)
    return jsonpatch.JsonPatch(patches)

def patch_delete_from_paths(paths):
    patches = []
    for p in paths:
        patch = {'op': 'remove',
                 'path': p
                }
        patches.append(patch)
    return jsonpatch.JsonPatch(patches)

def replace_uuids(json):
    """
    Replace the uuids in each 'id' element.
    Assumes a Beneficial Ownership Data Standard object, 
    and so exlcudes id fields within an 'identifiers' object.
    """
    # find matching JSON Paths
    matches = find_matching_paths(json)
    matches = [match for match in matches if 'identifier' not in match]
    # convert paths to JSON Patch paths
    paths = json_paths_to_json_patch_paths(matches)
    # create a JSON Patch object
    uuids = [str(uuid.uuid4()) for _ in range(len(paths))]
    patch = patch_replace_from_paths_values(paths, uuids)
    result = patch.apply(json)
    return result