# Solar Digital Twin Database Schema Design

## Purpose

This document defines the canonical database model for the Solar Digital Twin.

The database must support long-term engineering analysis across multiple data sources, including:

- EG4 Portal
- SolarAssistant
- Home Assistant
- JK BMS
- Chilicon
- ESP32 forensic loggers
- Weather data
- Utility/grid data
- Future hardware

The goal is not just to store readings. The goal is to preserve engineering evidence, normalize observations, and make every future report traceable back to raw source data.

## Current Status

EG4 SQLite storage is operational. It is the current normalized engineering
history and query layer for EG4 data. Raw evidence files remain the authoritative
source material.

The broader multi-source schema remains a design direction. SolarAssistant and
ESP32 currently write standalone NDJSON evidence under ignored `evidence/`
directories; neither source is yet normalized into SQLite. Reports, the portal,
Home Assistant, and future APIs are derived consumers rather than authoritative
stores.

## Design Principles

1. Devices exist independently of collectors.
2. Multiple collectors may observe the same physical device.
3. Raw evidence files are authoritative and must be preserved.
4. Normalized measurements must be queryable over time.
5. Events must be distinct from measurements.
6. Derived analysis must be reproducible.
7. The schema should evolve slowly and intentionally.

## Core Concepts

### Site

A site is a physical installation.

For now, the Solar Digital Twin will likely have one site: the home solar system.

Examples:

- The Gardners solar installation
- Future test bench
- Future detached system

### Device

A device is a physical or logical component in the power system.

Examples:

- EG4 12000XP inverter
- JK battery pack 1
- JK battery pack 2
- Chilicon microinverter
- SolarAssistant Raspberry Pi
- Home Assistant VM
- ESP32 frequency logger
- Utility grid connection
- Generator
- Weather source

Important rule:

A device is not the same thing as a collector.

The same inverter may be observed by EG4 Portal, SolarAssistant, and Home Assistant.

### Collector

A collector is a software process or integration that gathers data.

Examples:

- EG4 Portal collector
- SolarAssistant collector
- Home Assistant collector
- JK BMS collector
- Weather collector
- Utility collector

Collectors produce evidence. A later normalization stage may produce SQLite
measurements when that source's integration is implemented.

### Measurement

A measurement is a timestamped numeric or state value observed from a device.

Examples:

- inverter output watts
- battery SOC percent
- grid voltage
- AC frequency
- PV power
- battery charge watts
- battery discharge watts
- microinverter output
- temperature
- relay state

Measurements are high-volume time-series data.

### Event

An event is something meaningful that happened.

Examples:

- inverter fault
- warning code
- microinverter sleep/wake transition
- battery charge disabled
- configuration changed
- firmware changed
- grid disconnected
- frequency excursion
- collector run completed

Events are not the same as measurements.

### Evidence

Evidence is the raw source material collected before normalization.

Examples:

- EG4 JSON responses
- downloaded CSV files
- portal snapshots
- SolarAssistant exports
- Home Assistant history dumps
- ESP32 logs
- screenshots
- user observations
- manual test notes

Evidence should be preserved even if the normalized schema changes later.

### Derived Analysis

Derived analysis is computed from measurements, events, and evidence.

Examples:

- daily energy summaries
- AC-coupling instability reports
- frequency excursion summaries
- microinverter offline counts
- battery cycling analysis
- inverter replacement evidence package

Derived analysis should be reproducible from stored data.

## Target Multi-Source Tables

A broader multi-source database version may include:

- sites
- devices
- collectors
- evidence_records
- measurements
- events
- analysis_runs

## Open Multi-Source Design Questions

Before extending SQLite beyond the current EG4 implementation, decide:

1. How should physical devices be uniquely identified?
2. How should one physical device be linked to multiple collectors?
3. Should measurement names be fixed in a catalog table?
4. How much raw JSON should be stored inside SQLite versus evidence files?
5. How should manual observations be represented?
6. How should configuration changes be represented?
7. How should derived reports link back to source evidence?


## Historical EG4 MVP Scope

The completed initial implementation was intentionally narrow.

Completed scope:

- One site
- One EG4 12000XP inverter
- One EG4 Portal collector
- Evidence from EG4 API responses
- Normalized EG4 measurements
- Daily engineering report

Deferred beyond the EG4 MVP:

- SolarAssistant-to-SQLite normalization
- ESP32-to-SQLite normalization
- Home Assistant collector
- Weather collector
- Utility/grid collector
- Multi-source portal integration
- Home Assistant publishing

Standalone SolarAssistant/JK BMS and ESP32 collectors now exist, but their
NDJSON evidence is not yet part of normalized SQLite history. The EG4 MVP
created something visible and useful while preserving the long-term architecture.
