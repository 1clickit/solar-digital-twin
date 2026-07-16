# Next Task

## Objective

Review and approve the Solar Digital Twin security, credential,
authentication-failure, and recovery model using a Home Assistant-style
operational approach before implementing additional credentialed collectors.

## Context

The SolarAssistant-specific custom root-bootstrap experiment was reviewed and
superseded before installation. No SolarAssistant credential was installed and
no authenticated redacted inventory request occurred. The project has adopted
a practical Home Assistant-style security direction, but important operating
choices remain deliberately unresolved.

## Scope

- Confirm the trusted-host boundary and accepted home-office risk level.
- Decide shared versus separate Linux service accounts and credential-directory design.
- Classify device access as read-only, limited control, administrative, or network-wide control.
- Decide authentication retry, timeout, stop/disable, lockout-avoidance, and re-enable behavior.
- Define device-level password recovery and collector credential replacement.
- Confirm backup and recovery principles without placing plaintext credentials in Git or normal backups.
- Define controlled outbound internet access and prohibit unsolicited inbound WAN access.
- Assign OPNsense VLAN and firewall responsibilities, including containment of weak or open device interfaces.

## Boundaries

- This milestone is discussion and decision, not implementation.
- Do not add credential code, install credentials, enter passwords, or perform
  live authenticated collector work until Chris approves the decisions.
- Preserve existing collectors and evidence; do not alter device configuration.
- Treat SolarAssistant as one device within the project-wide model.

## Success

Chris approves a documented project-wide security and recovery model that is
specific enough to authorize a later bounded credential implementation work
unit without guessing about identities, storage, retries, lockout, recovery,
network exposure, or accepted risk.
