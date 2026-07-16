# Device Access and Recovery Inventory

## Purpose

This initial inventory records only established repository facts. `Pending
assessment` means the project must verify the device or manufacturer-supported
process before relying on it. SolarAssistant is one device within the broader
security model, not the model for every credential.

## SolarAssistant

- **Purpose:** Collection interface for trusted JK BMS battery telemetry.
- **Network location:** `192.168.3.12`.
- **Access type:** Collector behavior is read-only telemetry, but the `admin` credential's effective authority is unconfirmed; use a separate identity.
- **Direct login / credential:** REST metrics access uses fixed username `admin` and a password; operator login and recovery details are pending assessment.
- **Future collector storage:** A separate administrator-controlled directory readable only by the isolated SolarAssistant identity; exact implementation is deferred.
- **Transport:** Documented metrics endpoint uses unencrypted HTTP.
- **Lockout / password recovery / physical recovery / factory reset:** Pending assessment.
- **Configuration backup:** Pending assessment.
- **Collector credential replacement:** Operator correction followed by one manual verification before automation resumes; exact commands are deferred.
- **Collector failure:** Stops SolarAssistant telemetry; it must not alter the device or trusted JK BMS measurements.
- **Device-account failure:** Direct access and manufacturer-supported recovery must remain independent of the collector; details pending.
- **Status:** Partially known.

## Home Assistant

- **Purpose:** Future complementary convenience, status, alerts, and automation consumer; not authoritative evidence storage.
- **Network location:** Not documented in the repository.
- **Access type:** Shared telemetry identity only for a verified restricted telemetry user or token; administrative tokens require isolation and are excluded from routine collectors.
- **Direct login / credential / collector storage / transport / lockout / recovery:** Pending assessment.
- **Physical recovery:** Pending assessment; Home Assistant is documented as a VM in the local Proxmox environment.
- **Factory reset implications / configuration backup:** Home Assistant was restored from a backup, but current backup and reset procedures require assessment.
- **Collector credential replacement:** No Digital Twin integration is implemented.
- **Collector failure:** Must not affect authoritative raw evidence or SQLite history.
- **Account failure:** Must not remove independent device access.
- **Status:** Partially known.

## EG4 Services

- **Purpose:** Existing inverter telemetry collection, reporting, SQLite history, and EG4-only portal input.
- **Network location:** Vendor-service access is documented; no local EG4 device API location is established here.
- **Access type:** Separate collector identity unless a technically enforced read-only credential is identified.
- **Direct login / credential:** Existing unattended credential file is documented outside the repository; credential type and recovery details are not recorded here.
- **Collector storage:** Existing `/etc/solar-digital-twin/eg4.env`; this predates and does not decide the future general model.
- **Transport / lockout / password recovery / physical recovery / factory reset:** Pending assessment.
- **Configuration backup:** Raw evidence, SQLite history, and reports are separate from account recovery; vendor/device configuration backup is pending.
- **Collector credential replacement:** Operator correction and one manual verification before automation resumes; device-specific procedure pending.
- **Collector failure:** Stops fresh EG4 acquisition; preserved evidence and history remain available.
- **Device-account failure:** Vendor or manufacturer-supported recovery is required; specifics pending.
- **Status:** Partially known.

## ESPHome / ESP32 Devices

- **Purpose:** Read-only electrical and AC-couple forensic evidence.
- **Network location:** Forensic logger at `192.168.3.13`.
- **Access type:** Current unauthenticated SSE interface is technically read-only telemetry and may use the shared telemetry identity; OTA and management authority remain separate.
- **Direct login / credential:** Current public SSE endpoint requires no credential; ESPHome Wi-Fi secrets are kept in an ignored firmware secrets file.
- **Future collector storage:** No collector credential is currently required for SSE.
- **Transport:** Current SSE endpoint uses unencrypted HTTP.
- **Lockout / password recovery / physical recovery / factory reset:** Pending assessment.
- **Configuration backup:** ESPHome configuration is preserved in the repository without its ignored secrets.
- **Collector credential replacement:** Not applicable to the current public SSE collector.
- **Collector failure:** Stops new ESP32 evidence but does not control or lock the device.
- **Device-account failure:** Management and recovery path pending assessment.
- **Status:** Partially known.

## `solardt`

- **Purpose:** Trusted Solar Digital Twin collection, evidence, history, reporting, and portal host.
- **Network location:** `192.168.3.11` is documented for its LAN NTP service.
- **Access type:** Administrative host with access to approved telemetry functions; exact future authority grows per approved integration.
- **Direct login / credential / transport:** Local VM terminal and SSH are documented workflows; authentication details are intentionally not stored here.
- **Credential storage:** Administrator-controlled directories organized by runtime identity; `solardt` administration is never part of a collector identity.
- **Lockout / password recovery:** VM and Ubuntu recovery procedures pending documentation.
- **Physical recovery:** Through the local Proxmox environment; exact steps pending.
- **Factory reset implications:** Rebuild from known-good source and off-VM backups rather than treating reset as collector recovery.
- **Configuration backup:** Repository and project backups exist; restoration testing and credential separation require further definition.
- **Collector credential replacement:** Secure operator replacement followed by one manual verification; exact implementation is deferred.
- **Collector failure:** Individual telemetry stops safely; direct device access must remain available.
- **Host-account failure:** May affect all hosted collectors and requires host recovery.
- **Status:** Partially known.

## GitHub and Codex Project Access

- **Purpose:** Authoritative committed project history and intentional AI-assisted local engineering.
- **Network location:** External approved services; no LAN address.
- **Access type:** Administrative project access within approved commit and push boundaries.
- **Direct login / credential / transport:** Authenticated access over encrypted service connections; credential mechanisms and recovery are intentionally not recorded here.
- **Collector storage:** Not a collector credential.
- **Lockout / recovery / configuration backup:** Provider-supported recovery and repository backups; details pending assessment.
- **Collector credential replacement:** Not applicable.
- **Collector failure:** Does not directly control devices.
- **Account failure:** Could affect project history or engineering access; local and off-VM recovery copies remain important.
- **Status:** Partially known.

## Future OPNsense

- **Purpose:** Planned VPN, VLAN, firewall, outbound-policy, and network-containment boundary.
- **Network location:** Pending design.
- **Access type:** Network-wide control requiring a separate identity and stronger isolation.
- **Direct login / credential / storage / transport / lockout / recovery:** Pending assessment before implementation.
- **Physical recovery / factory reset / configuration backup:** Must be documented and tested before reliance; pending.
- **Collector credential replacement:** Not a normal telemetry collector credential.
- **Collector failure:** Monitoring failure must not reconfigure the firewall.
- **Device-account failure:** Could affect network-wide administration and may justify stronger isolation.
- **Status:** Pending assessment.

## Future Solar, IoT, Metering, Battery, Inverter, and Gateway Devices

- **Purpose and network location:** Defined per approved device.
- **Access type:** Must be classified before integration.
- **Direct login, credential type, collector storage, transport, lockout, recovery, reset, and backup:** Pending device-specific assessment; do not infer manufacturer behavior.
- **Collector credential replacement:** Must be documented before unattended use.
- **Collector failure:** Must stop safely without changing the device or blocking direct access.
- **Device-account failure:** Uses verified device or manufacturer-supported recovery.
- **Status:** Pending assessment.
