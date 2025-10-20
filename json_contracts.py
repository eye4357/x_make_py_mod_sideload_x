"""JSON contracts for x_make_py_mod_sideload_x."""

from __future__ import annotations

_JSON_VALUE_SCHEMA: dict[str, object] = {
    "type": ["object", "array", "string", "number", "boolean", "null"],
}

_NON_EMPTY_STRING: dict[str, object] = {"type": "string", "minLength": 1}

_PARAMETERS_SCHEMA: dict[str, object] = {
    "type": "object",
    "properties": {
        "base_path": _NON_EMPTY_STRING,
        "module": _NON_EMPTY_STRING,
        "attribute": {
            "oneOf": [
                _NON_EMPTY_STRING,
                {"type": "null"},
            ]
        },
        "loader_options": {
            "type": "object",
            "additionalProperties": _JSON_VALUE_SCHEMA,
        },
    },
    "required": ["base_path", "module"],
    "additionalProperties": False,
}

INPUT_SCHEMA: dict[str, object] = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "x_make_py_mod_sideload_x input",
    "type": "object",
    "properties": {
        "command": {"const": "x_make_py_mod_sideload_x"},
        "parameters": _PARAMETERS_SCHEMA,
    },
    "required": ["command", "parameters"],
    "additionalProperties": False,
}

_OUTPUT_RESULT_SCHEMA: dict[str, object] = {
    "type": "object",
    "properties": {
        "status": {"const": "success"},
        "schema_version": {"const": "x_make_py_mod_sideload_x.run/1.0"},
        "module_file": _NON_EMPTY_STRING,
        "attribute": {
            "oneOf": [
                _NON_EMPTY_STRING,
                {"type": "null"},
            ]
        },
        "object_kind": {
            "type": "string",
            "enum": ["module", "attribute"],
        },
        "messages": {
            "type": "array",
            "items": _NON_EMPTY_STRING,
        },
        "metadata": {
            "type": "object",
            "additionalProperties": _JSON_VALUE_SCHEMA,
        },
    },
    "required": ["status", "schema_version", "module_file", "object_kind"],
    "additionalProperties": False,
}

OUTPUT_SCHEMA = _OUTPUT_RESULT_SCHEMA

ERROR_SCHEMA: dict[str, object] = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "x_make_py_mod_sideload_x error",
    "type": "object",
    "properties": {
        "status": {"const": "failure"},
        "message": _NON_EMPTY_STRING,
        "details": {
            "type": "object",
            "additionalProperties": _JSON_VALUE_SCHEMA,
        },
    },
    "required": ["status", "message"],
    "additionalProperties": True,
}

__all__ = ["ERROR_SCHEMA", "INPUT_SCHEMA", "OUTPUT_SCHEMA"]
