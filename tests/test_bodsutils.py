#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''Tests for `bodsutils` package.'''

import pytest
import pytest_mock

import json
import uuid
from jsonschema import Draft4Validator
from bodsutils import bodsutils


@pytest.fixture
def bods_schema():
    """
    BODS schema fixture.
    Version is currently dependent on the submodule checked out.
    """
    with open('./data-standard/schema/beneficial-ownership-statements.json', 'r') as f:
        schema = json.load(f)
    return schema

@pytest.fixture
def valid_bods():
    '''Minimal valid nested BODS'''
    with open('./tests/dev-0.1-test-data.json') as f:
        bods_data = json.load(f)
    return bods_data

@pytest.fixture
def json_paths():
    paths = [
         'statementGroups.[0].id',
         'statementGroups.[0].beneficialOwnershipStatements.[0].entity.identifiers.[0].id'
         ]
    return paths

@pytest.fixture
def statement_id_paths():
    return [
        'statementGroups.[0].beneficialOwnershipStatements.[0].interestedParty.interestedPerson.statementID',
        'statementGroups.[0].beneficialOwnershipStatements.[0].statementID',
        'statementGroups.[0].beneficialOwnershipStatements.[0].subject.subjectEntity.statementID',
        'statementGroups.[0].beneficialOwnershipStatements.[1].interestedParty.interestedEntity.statementID',
        'statementGroups.[0].beneficialOwnershipStatements.[1].statementID',
        'statementGroups.[0].beneficialOwnershipStatements.[1].subject.subjectEntity.statementID',
        'statementGroups.[0].entityStatements.[0].statementID',
        'statementGroups.[0].entityStatements.[1].statementID',
        'statementGroups.[0].personStatements.[0].statementID',
        'statementGroups.[0].statementID'
        ]

def test_schema_and_test_data_versions_match(valid_bods, bods_schema):
    '''Check version numbers match'''
    assert bods_schema['version'] == valid_bods['version']

def test_valid_bods(valid_bods, bods_schema):
    '''Test if fixture is valid BODS JSON.'''
    v = Draft4Validator(bods_schema)
    for error in sorted(v.iter_errors(valid_bods), key=str):
      print(error.message)
    assert v.is_valid(valid_bods)

def test_find_matching_paths_ids(valid_bods, statement_id_paths):
  paths = sorted(bodsutils.find_matching_paths(valid_bods))
  expected_paths = statement_id_paths
  assert len(paths) == 10
  assert expected_paths == paths

def test_json_paths_to_json_patch_paths():
    paths = json_paths()
    patch = bodsutils.json_paths_to_json_patch_paths(paths)

    assert patch[0] == '/statementGroups/0/id'
    assert patch[1] == '/statementGroups/0/beneficialOwnershipStatements/0/entity/identifiers/0/id'


def test_patch_replace_from_paths_values():
    paths = json_paths()
    values = ['sg_id', 'entity_identifiers_id']
    patch = list(bodsutils.patch_replace_from_paths_values(paths, values))
    assert len(patch) == 2
    assert patch[0] == {'op': 'replace', 'path': 'statementGroups.[0].id', 'value': 'sg_id'}
    assert patch[1] == {'op': 'replace',
                        'path': 'statementGroups.[0].beneficialOwnershipStatements.[0].entity.identifiers.[0].id',
                        'value': 'entity_identifiers_id'}

def test_patch_delete_from_paths():
    paths = json_paths()
    patch = list(bodsutils.patch_delete_from_paths(paths))
    assert len(patch) == 2
    assert patch[0] == {'op': 'remove', 'path': 'statementGroups.[0].id'}
    assert patch[1] == {'op': 'remove',
      'path': 'statementGroups.[0].beneficialOwnershipStatements.[0].entity.identifiers.[0].id'}

def test_replace_uuids(mocker):
    pass
    # mocker.patch.object(uuid, 'uuid4')
    # bods_json = valid_bods()
    # uuid.uuid4.side_effect = ['0761c216-6d16-4874-a9dd-da7613354b2e',
    #                           'cfb31c7f-f5bb-4421-b41c-8cbc174dbff4',
    #                           '5b4adef6-933b-408e-95a8-56847a589856',
    #                           'c1974d21-a24a-4520-bd04-e29a01515f2e']
    # bods_json = bodsutils.replace_uuids(bods_json)
    # assert (bods_json['statementGroups'][0]['id'] ==
    #   '0761c216-6d16-4874-a9dd-da7613354b2e')
    # assert (bods_json['statementGroups'][0]['beneficialOwnershipStatements'][0]['id']
    #   == 'cfb31c7f-f5bb-4421-b41c-8cbc174dbff4')
    # assert (bods_json['statementGroups'][0]['beneficialOwnershipStatements'][0]['entity']['id']
    #   == '5b4adef6-933b-408e-95a8-56847a589856')
    # assert (bods_json['statementGroups'][0]['beneficialOwnershipStatements'][1]['id']
    #   == 'c1974d21-a24a-4520-bd04-e29a01515f2e')
    # assert (bods_json['statementGroups'][0]['beneficialOwnershipStatements'][0]['entity']['identifiers'][0]['id']
    #   == '00990099')
