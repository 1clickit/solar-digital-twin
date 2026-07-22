# Solar Digital Twin Backlog

## Current Priority

Current implementation work is defined by `NEXT_TASK.md`. Backlog items remain
deferred until explicitly promoted and approved.

## Later

### Collector Hardening and History
- Implement approved SolarAssistant meaningful-change deadbands only after a longer evidence capture, renewed assessment, and project-owner approval.
- Renew SolarAssistant deadband analysis from the completed 24-hour evidence
  only after a separate local-verification work unit confirms the static
  collector observations and defines the analysis scope. Preserve complete raw
  and separate retained evidence; do not manipulate equipment to create states.
- Complete later SolarAssistant persistent-service work only after runtime installation, credential installation, manual live verification, evidence capture, and deadband review are separately approved.
- Normalize SolarAssistant and ESP32 history into SQLite after standalone collectors are hardened.
- Add rolling raw buffers and automatic pre-event, event, and post-event preservation.
- Integrate trusted JK BMS and ESP32 data into the primary engineering portal.

### Home Assistant Integration
- The bounded GET-only import method is validated in
  `docs/EG4_HOME_ASSISTANT_TELEMETRY.md`. Production import/export remains
  deferred until the common provenance contract exists; do not replace
  authoritative evidence/history, enable control, or count copied data twice.

### Portal Improvements
- Analyze existing and future synchronized SolarAssistant/EG4 logs to determine
  whether a reliable household-load derivation is possible from the native
  EG4-reported aggregate AC-use metric and its included AC-coupled solar
  contribution. Define operating-mode applicability, timing alignment,
  provenance, and source-semantic portal labels before any implementation; do
  not approve or apply the subtraction as a universal transformation merely by
  recording this backlog item.
- Add a future secured `Refresh data now` workflow so F5 or an explicit portal control can request one bounded EG4 collection, report, and portal-generation cycle before displaying newly generated data. Prevent overlapping jobs, rapid repeated requests, uncontrolled command execution, and credential exposure; report in-progress, success, failure, and last-completed status clearly.
- Add an optional local portal-development live-reload mode so Chris can watch visible changes while Codex works. Keep it separate from the production portal and from telemetry collection.

### Additional Collectors
- Home Assistant collector
- Weather collector
- Utility collector, if useful later
- On-site plane-of-array irradiance and module/reference-cell temperature under
  `docs/IRRADIANCE_MEASUREMENT_PLAN.md` after separate design, safety, and
  installation authorization.

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

## Workflow

`NEXT_TASK.md` defines current work. `CONTRIBUTING.md` is canonical for bounded
workflow, approvals, protected boundaries, commits, and pushes.

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
