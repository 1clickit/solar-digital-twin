# Solar Digital Twin Security Model

## Status and Scope

This document records the approved strategic direction for project-wide
security. Solar Digital Twin will mirror the practical security profile of a
well-configured Home Assistant installation: appropriate for a home office and
home automation, not banking, military, or large-enterprise identity systems.

The SolarAssistant-specific custom root-bootstrap experiment was reviewed and
superseded before installation. The dedicated `solardt-sa` runtime was later
installed, and its metadata and access verification passed. The protected
SolarAssistant credential was installed using the approved installer, and the
completed long-duration capture and later bounded three-source analysis
succeeded. Trusted read-only telemetry analysis now uses a least-privilege
reader model; credentials, authorization data, tokens, protected logs,
unrelated runtime files, and write access remain restricted. The practical
Home Assistant-style operating model below remains in force.

## Trusted-Host Boundary

`solardt` is a trusted home-automation and telemetry host. It may eventually
hold access to many explicitly approved solar and automation functions. A full
compromise of `solardt` means locally usable credentials and authorized device
functions must be treated as compromised. Increasingly elaborate Python
credential wrappers cannot meaningfully protect secrets after an attacker has
full control of the trusted host.

Recovery from confirmed host compromise is to:

1. Isolate or shut down the compromised host.
2. Rebuild it from known-good source and backups.
3. Verify the replacement host.
4. Rotate affected device credentials.
5. Restore automation only after verification.

## Primary Threat Priorities

Design strongly against credentials entering Git, chat, logs, reports, shell
history, or command arguments. Prevent accidental disclosure, unnecessary
collector privilege, cross-collector credential access, unsafe authentication
retry loops, unsolicited inbound internet exposure, and lateral movement from
weak solar or IoT devices. Configuration changes must not remove direct operator
access, and recovery must not depend on the failed collector itself.

Security is risk-calibrated: ordinary read-only telemetry and bounded offline
analysis are lower risk than credential, configuration, control, destructive,
or public-exposure actions. Controls must remain proportional to plausible
harm; unnecessary delay, manual intervention, and complexity are themselves
project risks. `CONTRIBUTING.md` defines the shared approval classes.

## Internet Access

Outbound access and inbound exposure are different controls. Controlled
outbound internet access is permitted for approved Ubuntu security and package
updates, GitHub, DNS, time synchronization, intentional Codex/OpenAI use,
approved package repositories, and explicitly approved vendor services.

Unsolicited inbound WAN access must not directly reach `solardt`, SSH, project
portals, collector services, databases, Home Assistant, SolarAssistant,
ESPHome or ESP32 management interfaces, EG4-related interfaces, or other solar
and IoT APIs. Future remote access should use the planned OPNsense VPN,
firewall, and segmentation design.

## Network Containment

Future OPNsense VLANs and firewall rules are the primary planned network-
containment boundary. The design should consider separate trust zones for
management clients, automation servers such as Home Assistant and `solardt`,
solar and IoT equipment, ordinary LAN clients, guest or untrusted devices, and
WAN access. Open device Wi-Fi, weak authentication, and insecure legacy
protocols must not grant unrestricted access to the rest of the LAN.

## Credential Model

- Secrets remain outside source code, Git, chat, normal reports, and command arguments.
- Conventional protected credential files and normal Linux permissions are the default direction.
- Collectors run unprivileged and receive only credentials needed for their approved function.
- A custom root-owned credential bootstrap will not be created for every device.
- Stronger isolation may be considered for unusually powerful credentials, such as future firewall administration.
- Credential directories and files are administrator controlled; collector identities may read approved credentials but may not create, replace, modify, or delete them.
- Credentials remain outside the project tree, logs, reports, shell history, and ordinary project backups.
- Recovery normally uses secure re-entry, replacement, or rotation.
- SolarAssistant paths, ownership, groups, permissions, and installer commands are implemented and verified as documented in `docs/SOLARASSISTANT_RUNTIME.md`.

The existing operational EG4 workflow predates this decision and remains
documented separately. It does not establish the future project-wide credential
architecture. The approved SolarAssistant credential installer and protected
credential consumer are implemented; no persistent systemd service has been
created or enabled.

## Approved Runtime Isolation Decisions

### Decision 1 — Runtime Service Identities

Classify a collector by the maximum effective authority available to its runtime
identity, not only by what its current code intends to do. Effective authority
includes credentials, unauthenticated interfaces, network access, and protected
resources available to that identity.

Collectors technically restricted to read-only telemetry may share one
ordinary unprivileged telemetry identity. Control-capable, administrative,
network-wide, unusually sensitive, authority-unknown, or mixed-authority access
requires a separate Linux identity and separately protected credentials until
reliable evidence proves technical read-only restriction.

Preliminary classifications are:

- ESP32 SSE telemetry: shared credentialless telemetry identity
  `solardt-telemetry`. The identity, runtime, narrowly writable evidence path,
  trusted reporter access, and dormant static unit are installed and metadata-
  verified; no credential exists, and one finite credentialless passive live
  verification passed without device or security-configuration change. See
  `docs/ESP32_RUNTIME_SECURITY_HARDENING_PLAN.md`.
- SolarAssistant: separate identity until the `admin` credential's effective authority is confirmed.
- EG4 vendor access: separate identity unless a technically enforced read-only credential is identified.
- Home Assistant: shared only with a verified restricted telemetry user or token; administrative tokens are excluded.
- Future OPNsense: separate identity because it has network-wide sensitivity.
- `solardt` administration: never part of a collector identity.

### Decision 2 — Credential Organization

Credentials are organized by runtime service identity. A shared telemetry
identity may have one protected directory containing multiple credentials only
when every credential is technically restricted to read-only telemetry. Each
isolated collector identity receives its own protected directory. No common
group or parent-directory permission may grant every collector access to every
credential.

### Decision 3 — Unknown Authority

Unknown or mixed authority requires a separate unprivileged service identity
and credential directory until reliable evidence confirms technical read-only
restriction. Uncertainty does not prohibit useful telemetry collection, but
read-only collector behavior alone does not prove read-only credential authority.

## Collector Authority

Collectors normally consume approved credentials only for their documented
telemetry role. They do not automatically change device passwords; create or
delete users; reset accounts; change MFA or recovery settings; factory-reset
devices; reconfigure management access; or repeatedly retry rejected
credentials without operator intervention. Collector failure must stop
telemetry safely rather than alter the device.

## Authentication-Failure Principle

Temporary network failures and authentication failures are separate states.
Temporary connection failures and timeouts may use limited retries with
controlled backoff. HTTP `401` or `403` stops automated authentication attempts
and requires operator correction; rejected credentials are not repeatedly
retried. After correction or replacement, one manual verification is allowed
before automation resumes. Authentication failure never triggers password or
account-recovery changes. Collectors never change device passwords automatically.

## Device Independence and Recovery

Direct device access remains independent of collectors. A damaged collector,
credential file, service, or report must not lock Chris out of the device.
Password recovery uses the device or manufacturer-supported process. After
recovery or rotation, the collector credential is replaced and tested. Factory
reset is a final option, not normal collector recovery. Device-specific paths
will be documented as each device is assessed. Unknown lockout, password-
recovery, and vendor behavior remain pending assessments rather than blockers
to appropriately isolated telemetry work.

## Backups and Recovery

Back up before significant changes, preserve known-good versions, keep recovery
copies off the VM, and test restoration periodically. Plaintext credentials do
not belong in Git or normal project backups. Credential recovery and system
recovery are separate procedures. Prefer re-entering or rotating a device
credential instead of recovering it from project files.

## Failure and Recovery Boundaries

Collector failure is repaired or redeployed from known-good source without
changing credentials unless compromise is suspected. Device-account failure is
handled through independent device administration or recovery. VM loss requires
rebuild or restoration from documented source and protected backups, followed
by secure credential re-entry. Confirmed `solardt` compromise requires network
isolation, rebuild, verification, and rotation of every potentially exposed
credential.

Devices with open Wi-Fi, weak authentication, unencrypted protocols, or poorly
controlled management interfaces are contained primarily through future
OPNsense segmentation and narrowly permitted traffic. The accepted risk level
remains practical home-office and home-automation security, not banking or
large-enterprise security.
