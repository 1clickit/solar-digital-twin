# Solar Digital Twin Backlog

## Current Priority

Current implementation work is defined by `NEXT_TASK.md`. Backlog items remain
deferred until explicitly promoted and approved.

## Later

### Collector Hardening and History
- Implement approved SolarAssistant meaningful-change deadbands only after offline evidence characterization and project-owner approval.
- Complete later SolarAssistant live verification and persistent-service work only after deadband and credential implementation are separately approved.
- Normalize SolarAssistant and ESP32 history into SQLite after standalone collectors are hardened.
- Add rolling raw buffers and automatic pre-event, event, and post-event preservation.
- Integrate trusted JK BMS and ESP32 data into the primary engineering portal.

### Home Assistant Integration
- Add complementary convenience, status, and alerts without replacing the engineering portal or authoritative evidence and history.

### Portal Improvements
- Add a future secured `Refresh data now` workflow so F5 or an explicit portal control can request one bounded EG4 collection, report, and portal-generation cycle before displaying newly generated data. Prevent overlapping jobs, rapid repeated requests, uncontrolled command execution, and credential exposure; report in-progress, success, failure, and last-completed status clearly.
- Add an optional local portal-development live-reload mode so Chris can watch visible changes while Codex works. Keep it separate from the production portal and from telemetry collection.

### Additional Collectors
- Home Assistant collector
- Weather collector
- Utility collector, if useful later

### AC-Couple Forensic Investigation
- Develop an AC-Couple Microinverter Dropout Signature Review.
- Distinguish full dropouts, partial collapses, rebounds, slow-ramp recoveries, volatility, and repeated drop-size patterns.
- State clearly that cloud cover and individual microinverter dropout can look similar in aggregate EG4 data.
- Correlate EG4 events with ESP32 1-second voltage, frequency, estimated power, ramp-rate, and forensic-log evidence.
- Create a future AC-Couple Event Correlation Report with confidence and uncertainty categories.
- Evaluate a temporary five-minute EG4 sampling mode for limited full-sun diagnostic windows.
- Consider one-minute sampling only after conservative endpoint testing and explicit risk approval.
- Research local CP-100 web, API, export, network, or supported integration access before considering RS485.
- Keep all investigation work read-only and preserve existing EG4 collector and portal behavior.

See `docs/EG4_FORENSIC_CORRELATION.md` for the detailed design note.

## Rules
- One small, tested commit at a time.
- Keep main clean.
- Documentation is the source of truth.

## Future Workflow Improvements

- Consider Repomix or a similar repository snapshot tool only for occasional future architecture audits; do not treat it as active workflow or authoritative memory.

- Raise the VM-side tmux history limit beyond 50000 lines if long output continues to cause copy or scrollback problems.
- Document the preferred Debian WSL -> SSH -> VM-side tmux workflow.

- Add narrowly scoped repository health checks when new documented failure modes justify them.
- Keep executable commands clearly separated from discussion text.
- Every session should try to leave the repository easier for the next engineer to use.

## Future Repository Opportunities

- Evaluate whether the Solar Digital Twin workflow should evolve into a reusable engineering framework repository.
- Potential areas:
  - AI engineer onboarding
  - Repository memory architecture
  - Session lifecycle management
  - Documentation-driven development
  - Human/AI collaboration standards
  - Project health monitoring
