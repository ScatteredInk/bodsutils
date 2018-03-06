# -*- coding: utf-8 -*-

"""Main module."""
import uuid
import json
import os

import jsonpatch
from jsonschema import validate, Draft4Validator
from jsonpath_ng import jsonpath, parse



def bods_schema():
    """
    BODS schema fixture.
    Version is currently dependent on the submodule checked out.
    """
    base_path = os.path.abspath(os.path.dirname(__file__))
    path = os.path.join(base_path, "../data-standard/schema/beneficial-ownership-statements.json")
    with open(path, 'r') as f:
      schema = json.load(f)
    return schema

def test_valid_bods(bods_json, schema):
    '''Test if fixture is valid BODS JSON.'''
    v = Draft4Validator(schema)
    for error in sorted(v.iter_errors(bods_json), key=str):
      print(error.message)
    assert v.is_valid(bods_json)

def find_matching_paths(json, jsonpexpr = '$..statementID'):
    jsonpath_expr = parse(jsonpexpr)
    return [str(match.full_path) for match in jsonpath_expr.find(json)]

def json_paths_to_json_patch_paths(paths):
    """
    Change JSONPath to JSON patch paths.

    Note: The JSONPatch class uses JSONPath under the hood anyway
    so this is pointless. You can just make a list of paths direct
    and wrap it.
    """
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

    This will only work with nested format. Will need another to link
    statement references for JSONLines serialization.
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
