#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `bodsutils` package."""

import pytest
import json
from jsonschema import Draft4Validator


from bodsutils import bodsutils

# content of test_sample.py
def func(x):
    return x + 1

def test_answer():
    assert func(3) == 4


@pytest.fixture
def bods_schema():
    """
    BODS schema fixture.
    Version is currently dependent on the submodule checked out.
    """
    with open("./data-standard/schema/beneficial-ownership-statements.json", 'r') as f:
    	schema = json.load(f)
    return schema

@pytest.fixture
def valid_bods():
	"""Minimal valid BODS"""
	bods = {
	        "statementGroups":
	          [
	            {
	              "id": "265fad50-ac77-4703-9aa6-0e6523f23767",
	              "entityStatements":
	              [
	              ],
	              "beneficialOwnershipStatements":
	              [
	                {
	                  "id": "23569c9b-2f99-456f-a22a-23459e66a31f",
	                  "identifiers":
	                  [
	                    {
	                      "scheme": "GB-COH",
	                      "id": "00990099"
	                    }
	                  ]
	                }
	              ]
	            }
	          ]
	        }
	return bods

def test_valid_bods(valid_bods, bods_schema):
    """Sample pytest test function with the pytest fixture as an argument."""
    # from bs4 import BeautifulSoup
    # assert 'GitHub' in BeautifulSoup(response.content).title.string
    v = Draft4Validator(bods_schema)
    for error in sorted(v.iter_errors(valid_bods), key=str):
    	print(error.message)
    assert v.is_valid(valid_bods)
