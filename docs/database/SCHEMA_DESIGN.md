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

## Design Principles

1. Devices exist independently of collectors.
2. Multiple collectors may observe the same physical device.
3. Raw evidence must be preserved.
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

Collectors produce evidence and normalized measurements.

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

## Initial Core Tables

The first database version should likely include:

- sites
- devices
- collectors
- evidence_records
- measurements
- events
- analysis_runs

## Open Design Questions

Before writing SQL, we need to decide:

1. How should physical devices be uniquely identified?
2. How should one physical device be linked to multiple collectors?
3. Should measurement names be fixed in a catalog table?
4. How much raw JSON should be stored inside SQLite versus evidence files?
5. How should manual observations be represented?
6. How should configuration changes be represented?
7. How should derived reports link back to source evidence?


## MVP Scope

The first implementation will intentionally be narrow.

Initial scope:

- One site
- One EG4 12000XP inverter
- One EG4 Portal collector
- Evidence from EG4 API responses
- Normalized EG4 measurements
- Daily engineering report

Deferred until later:

- SolarAssistant collector
- Home Assistant collector
- JK BMS collector
- Weather collector
- Utility/grid collector
- Web dashboard
- Home Assistant publishing

The purpose of the MVP is to create something visible and useful quickly while preserving the long-term architecture.
