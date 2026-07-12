# Solar Digital Twin Backlog

## Current Priority

### Visible EG4 MVP
- Create reporting package.
- Generate `reports/engineering_daily_report.md`.
- Read existing EG4 collector CSV outputs.
- Do not modify collector behavior or SQLite schema yet.

## Later

### Home Assistant Integration
- Decide whether the Digital Twin reports to Home Assistant, provides a separate webpage, or both.

### Additional Collectors
- SolarAssistant collector
- Home Assistant collector
- JK BMS collector
- Weather collector
- Utility collector, if useful later

### AC-Couple Forensic Investigation
- Develop an AC-Couple Microinverter Dropout Signature Review.
- Distinguish full dropouts, partial collapses, rebounds, slow-ramp recoveries, volatility, and repeated drop-size patterns.
- State clearly that cloud cover and individual microinverter dropout can look similar in aggregate EG4 data.
- Correlate EG4 events with ESP32 1-second voltage, frequency, estimated power, ramp-rate, and forensic-log evidence.
- Create a future AC-Couple Event Correlation Report with confidence and uncertainty categories.
- Configure and verify time synchronization between solardt and the ESP32 before relying on event correlation.
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

- Raise the VM-side tmux history limit beyond 50000 lines if long output continues to cause copy or scrollback problems.
- Document the preferred Debian WSL -> SSH -> VM-side tmux workflow.

- Enhance status.sh into a lightweight repository health check.
- Check for documentation drift between PROJECT_STATE.md and NEXT_TASK.md.
- Detect duplicate headings in project documentation.
- Detect missing required project files.
- Treat status.sh as the project's startup assistant and improve it over time.
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

