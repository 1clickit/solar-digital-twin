# Next Task

## Objective

Design a reusable AI engineering framework MVP from the Solar Digital Twin workflow.

## Context

The EG4 portal, automated refresh timer, timezone handling, stale-data protection, and repository health checks are operational.

The repository currently mixes reusable engineering workflow rules with Solar Digital Twin-specific instructions.

## Scope

Define the boundary between reusable framework components and project-specific components. Do not extract or fork the framework yet.

## Success

A reviewed framework MVP design identifies what can be reused by unrelated coding projects without carrying Solar Digital Twin-specific assumptions.

## Consider Later

Improve portal browser freshness without changing data collection:

- discourage browser caching so newly opened windows show the latest generated HTML
- optionally reload an open portal tab automatically
- preserve generated time, source time, and stale-data warnings
- keep browser reloads separate from the 15-minute EG4 collection timer
