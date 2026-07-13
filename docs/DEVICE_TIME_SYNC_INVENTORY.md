# Device Time Synchronization Inventory

## Status

In progress.

## Current Time Architecture

Current design:

NIST IPv4 upstreams -> solardt -> solar devices

Future preferred design after router upgrade:

NIST IPv4 upstreams -> OPNsense -> solardt and solar devices

## Preferred LAN Time Source

- Host: solardt
- IPv4: 192.168.3.11
- NTP service: Chrony
- LAN listener: 192.168.3.11:123
- LAN scope: 192.168.3.0/24
- Timezone standard: America/Chicago
- IPv6 policy: disabled on solardt unless a documented project advantage is found

## solardt Chrony Configuration

Chrony startup options:

- DAEMON_OPTS="-4 -F 1"

Configured upstream NTP servers:

| Server | Address observed | Site |
|---|---:|---|
| time-a-g.nist.gov | 129.6.15.28 | NIST Gaithersburg |
| time-b-g.nist.gov | 129.6.15.29 | NIST Gaithersburg |
| time-a-wwv.nist.gov | 132.163.97.1 | WWV Fort Collins |
| time-a-b.nist.gov | 132.163.96.1 | NIST Boulder |

Ubuntu pool upstreams were disabled and replaced with explicit NIST IPv4 upstreams.

Latest verification:

- Chrony selected time-a-g.nist.gov as the current source.
- Leap status was Normal.
- LAN NTP listener was verified on 192.168.3.11:123.
- IPv6 addresses and routes were absent after disabling IPv6.

## Known Devices

| Device | IPv4 | Status | Notes |
|---|---:|---|---|
| solardt | 192.168.3.11 | synchronized | Current preferred LAN NTP source |
| Starlink management | 192.168.100.1 | NTP verified | UDP 123 open; read-only Chrony query worked |
| LAN gateway | 192.168.3.1 | NTP inconclusive | Reachable; UDP 123 open/filtered |
| Solar Assistant | 192.168.3.12 | static IP verified | Raspberry Pi; monitors PB / JK BMS devices; moved from DHCP 192.168.3.231 |
| Home Assistant | 192.168.3.221 | unknown | Supporting automation system |
| CP-100 / Chilicon gateway | 192.168.3.46 | research required | Espressif MAC 08:3A:F2:13:42:88; no open TCP ports found |
| ESP32 forensic logger | unknown | needs identification | Multiple Espressif devices visible on LAN |

## External NTP Evidence

| Hostname / Address | Result |
|---|---|
| 192.168.100.1 | usable NTP response observed |
| monitor.eg4electronics.com | no suitable NTP source |
| factory.chiliconpower.com | no suitable NTP source |
| cloud.chiliconpower.com | no suitable NTP source |
| cloud1.chiliconpower.com | usable NTP response observed |
| cloud2.chiliconpower.com | no suitable NTP source |
| cloud3.chiliconpower.com | no suitable NTP source |
| cloud4.chiliconpower.com | no suitable NTP source |
| cloud5.chiliconpower.com | no suitable NTP source |
| cloud6.chiliconpower.com | no suitable NTP source |

## Chilicon / CP-100 Notes

The CP-100 is reachable at 192.168.3.46, but no open TCP ports were detected from solardt.

cloud1.chiliconpower.com appears to act as a Chilicon-related NTP source, but this does not prove the CP-100 uses it.

CP-100 local time/NTP configurability remains unknown and requires touchscreen, vendor, or cloud-interface research.

Chilicon web portal research may be useful as read-only follow-up work to identify timestamps, firmware details, cloud endpoints, or API patterns.

## Current Conclusion

Configurable solar equipment should prefer solardt at 192.168.3.11 for NTP during the current project phase.

After the OPNsense router upgrade, OPNsense should be evaluated as the preferred network-wide NTP authority.

Starlink at 192.168.100.1 and Chilicon cloud1 are useful reference observations, but they are not the preferred solar-device configuration target.

## Next Questions

- Which Espressif LAN device is the ESP32 forensic logger?
- Does Solar Assistant allow configurable NTP?
- Does Home Assistant already use solardt or another trusted time source?
- Can the CP-100 touchscreen show time source, timezone, firmware, or cloud settings?
- Which solar devices use static IPs, DHCP reservations, or unknown addressing?
