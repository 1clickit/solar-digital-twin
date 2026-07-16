# Next Task

## Objective

Prepare and implement the minimum dedicated SolarAssistant Linux runtime
identity and protected credential-delivery boundary required for controlled live
evidence collection under the approved security model.

## Context

The offline deadband assessment in commit `dc1adc9` found the existing evidence
insufficient for defensible numeric thresholds. A longer capture is needed, but
SolarAssistant must first run under a separate unprivileged identity because the
`admin` credential's effective authority remains unknown.

## Scope

- Select and document one dedicated unprivileged SolarAssistant collector identity.
- Select exact administrator-controlled credential, evidence, and necessary runtime paths.
- Permit the identity to read only its required credential, write only approved SolarAssistant outputs and runtime files, execute the required collector runtime, and make the approved outbound SolarAssistant connection.
- Prevent the identity from modifying credential files, reading other collectors' credentials, administering `solardt`, using `sudo`, or changing device configuration.
- Use a practical Home Assistant-style filesystem model with staged validation, safe failure behavior, recovery awareness, and repeatable installation steps.
- Keep credential entry out of arguments, shell history, chat, logs, and repository files; exclude plaintext credentials from ordinary project backups.
- Document credential replacement and one manual verification before re-enabling collection after HTTP `401` or `403`.
- Establish a reviewed path for a later 24-hour capture at the approved normal 10-second polling interval.
- Keep the design modular enough for future collectors without creating speculative device abstractions.

## Boundaries

- Stop for review before installing a real credential, contacting SolarAssistant with newly installed credentials, starting the long capture, or enabling a persistent service.
- Do not weaken the separate-identity requirement or expose the credential to Chris's normal administrative identity during unattended operation, except for secure administrator installation or replacement.
- Do not add SQLite, portal, final deadband implementation, or unrelated integration work.
- Keep runtime-boundary installation and the later evidence capture as separate reviewable stages.

## Success

A focused, reviewable implementation defines and validates the dedicated
SolarAssistant identity, paths, permissions, credential replacement boundary,
and safe installation workflow without installing a real credential, contacting
the device, starting the long capture, or enabling persistent collection.
