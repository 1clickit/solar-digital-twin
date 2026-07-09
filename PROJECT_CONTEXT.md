# PROJECT CONTEXT

This document records the long-term engineering
knowledge of the Solar Digital Twin project.

Unlike PROJECT_STATE.md, this document changes
slowly and captures enduring design decisions.

## Mission

Build an engineering-grade digital twin for a
residential solar energy system.

The project supports engineering,
diagnostics, forensics, automation,
historical analysis and future expansion.

## Engineering Philosophy

The system is designed using first principles.

Evidence is preferred over assumptions.

Measurements are preferred over opinions.

Raw evidence is preserved before analysis.

Derived data should always be reproducible.

The repository is the project's memory.

GitHub is the authoritative source for
all committed engineering knowledge.

## System Goals

Collect data from multiple systems.

Correlate measurements across devices.

Maintain a permanent engineering history.

Generate engineering reports.

Support troubleshooting and root cause analysis.

Remain modular.

Remain extensible.

## Current Architecture

Primary data sources include:

- EG4 inverter
- SolarAssistant
- Home Assistant
- Battery management systems
- Weather services
- Utility information

SQLite is the primary engineering database.

## Engineering Practices

One tested change at a time.

One logical commit at a time.

Document important decisions.

Capture engineering knowledge.

Improve the repository continuously.

Future engineers should learn from the
repository instead of previous conversations.

## Design Principles

Simple solutions are preferred.

Automation should replace repetitive work.

Every workflow improvement should be committed.

Every engineering decision should be
understandable months or years later.

The objective is continuous knowledge capture
through the repository.

