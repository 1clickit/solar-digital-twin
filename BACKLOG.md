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

## Rules
- One small, tested commit at a time.
- Keep main clean.
- Documentation is the source of truth.

## Future Workflow Improvements

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

