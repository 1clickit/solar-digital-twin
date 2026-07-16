# Solar Digital Twin Security Model

## Status and Scope

This document records the approved strategic direction for project-wide
security. Solar Digital Twin will mirror the practical security profile of a
well-configured Home Assistant installation: appropriate for a home office and
home automation, not banking, military, or large-enterprise identity systems.

The SolarAssistant-specific custom root-bootstrap experiment was reviewed and
superseded before installation. No SolarAssistant password was installed and no
authenticated SolarAssistant inventory request occurred. No replacement
credential implementation is approved. Security-model decisions must be
completed with Chris before further credentialed collector work.

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
- Collectors run unprivileged and receive only credentials needed for their approved role.
- A custom root-owned credential bootstrap will not be created for every device.
- Stronger isolation may be considered for unusually powerful credentials, such as future firewall administration.
- The final credential-directory and service-account design remains under discussion.
- No replacement credential implementation is approved yet.

The existing operational EG4 workflow predates this decision and remains
documented separately. It does not establish the future project-wide credential
architecture. No SolarAssistant credential installer or authenticated
credential consumer is currently approved.

## Collector Authority

Collectors normally consume approved credentials only for their documented
telemetry role. They do not automatically change device passwords; create or
delete users; reset accounts; change MFA or recovery settings; factory-reset
devices; reconfigure management access; or repeatedly retry rejected
credentials without operator intervention. Collector failure must stop
telemetry safely rather than alter the device.

## Authentication-Failure Principle

Temporary network failures and authentication failures must be distinguished.
Temporary connection failures may use controlled backoff. Authentication
failures must not cause unlimited rapid retries. Exact retry count, timeout,
disable-state behavior, and credential-replacement workflow remain decisions
for the next discussion. Chris must retain an opportunity to recover or change
the device password and provide the replacement credential. Collectors never
change device passwords automatically.

## Device Independence and Recovery

Direct device access remains independent of collectors. A damaged collector,
credential file, service, or report must not lock Chris out of the device.
Password recovery uses the device or manufacturer-supported process. After
recovery or rotation, the collector credential is replaced and tested. Factory
reset is a final option, not normal collector recovery. Device-specific paths
will be documented as each device is assessed.

## Backups and Recovery

Back up before significant changes, preserve known-good versions, keep recovery
copies off the VM, and test restoration periodically. Plaintext credentials do
not belong in Git or normal project backups. Credential recovery and system
recovery are separate procedures. Prefer re-entering or rotating a device
credential instead of recovering it from project files.

## Decisions Reserved for Chris

The next discussion must decide:

1. One shared ordinary Linux service identity versus separate collector accounts.
2. One protected credential parent directory with separate files.
3. Which collectors justify separate Linux identities.
4. Classification of each device as read-only, limited control, administrative, or network-wide control.
5. Exact handling of HTTP `401` and `403`.
6. Immediate stop, limited retries, or timeout followed by operator-directed authentication retry.
7. How corrected credentials re-enable collectors.
8. How credential backups are handled outside Git.
9. Responsibilities of collectors, `solardt`, Home Assistant, OPNsense, and devices.
10. Which credentials justify stronger isolation.
11. Containment of open Wi-Fi, weak authentication, and unencrypted protocols.
12. How outbound internet access is limited and audited without preventing normal updates.

These choices are deliberately unresolved. Do not implement credential code,
install credentials, enter passwords, or perform new authenticated collector
work until Chris approves them.
