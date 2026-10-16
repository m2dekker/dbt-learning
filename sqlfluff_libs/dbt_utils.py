"""Lint-only stubs for dbt_utils macros.

SQLFluff's jinja templater does not run dbt, so package macros are unknown to it.
These stubs return SQL of the same *shape* so the linter can parse the model.
They are never used by dbt itself. Add a stub here when a model uses a new macro.
"""


def generate_surrogate_key(field_list):
    return "md5(" + " || '-' || ".join(f"cast({f} as varchar)" for f in field_list) + ")"
