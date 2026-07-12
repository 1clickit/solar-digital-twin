# Next Task

## Objective

Improve portal browser freshness without changing EG4 data collection.

## Scope

- discourage browser caching of the generated portal HTML
- optionally reload an already-open portal tab automatically
- preserve generated time, source time, and stale-data warnings
- keep browser refresh behavior separate from the 15-minute collection timer
- keep the portal read-only

## Exclusions

- do not change EG4 collection frequency
- do not modify collector behavior or SQLite schema
- do not require EG4 credentials
- do not implement forensic correlation yet

## Success

A newly opened portal shows the current generated HTML, and any automatic browser reload does not trigger additional EG4 collection.
