# solardt VM Health Review and Log

## Purpose and authority

This authoritative append-only document defines lightweight read-only
performance, capacity, and storage reviews for the `solardt` VM. It contains no
current measurement yet. Append future health entries; do not silently edit or
remove prior entries. Correct an inaccurate entry with a later referenced
correction.

Health entries must not contain passwords, tokens, API keys, authorization
headers, credential contents, secret command arguments, full process listings,
large raw logs, or unrelated sensitive details.

## Required timing

Perform a review:

- at least once every 30 calendar days;
- before and after a long-duration or high-volume telemetry capture;
- before and after a significant deployment or operational service change;
- after a package installation or upgrade that materially affects runtime;
- when evidence growth, performance degradation, failed services, storage
  warnings, or unusual behavior is observed; and
- before adding a large collector or dataset.

Thirty days is the minimum interval. Warning signs justify an earlier review.

## Read-only observations

Record concise summaries of:

- root-filesystem capacity, used percentage, and available space;
- inode use and availability;
- memory and available memory;
- swap use;
- uptime and load averages;
- highest CPU and memory consumers without unrelated sensitive details;
- relevant failed systemd units;
- obvious filesystem or disk warnings available through approved local
  read-only mechanisms;
- aggregate evidence, database, report, and log growth; and
- whether capacity is sufficient for the next planned capture or analysis.

Do not commit full process listings or large raw logs. Use read-only commands
and approved local information only.

## Storage classification guidance

- **Below 70% filesystem use:** normal.
- **70% to below 80%:** advisory; review growth.
- **80% to below 90%:** prepare a capacity or archive plan before another
  high-volume capture.
- **90% or higher:** do not start another high-volume capture without Chris's
  explicit approval and a documented capacity plan.

Apply equivalent judgment to inode exhaustion. These thresholds never
authorize automatic deletion. Storage pressure is not authorization to delete
raw evidence.

Address pressure through safe archiving, approved additional storage,
relocation of reproducible derived products, reviewed retention changes, or
another documented capacity plan. Preserve unique operational artifacts and
follow `CONTRIBUTING.md`; when uncertain, archive rather than delete.

## No automatic remediation

The review is read-only unless an authorized milestone explicitly includes a
corrective action. It must not automatically delete or rotate unique evidence,
stop or restart services, change retention, move databases, resize disks,
restart the VM, or change runtime configuration.

A normal read-only review needs no `CHANGE_AUDIT.md` entry. A significant
engineering finding or persistent report may warrant one; every persistent
corrective action requires one.

## Entry template

Copy this template beneath `## Health entries` and replace placeholders with
measured facts. Do not invent unavailable measurements.

### YYYY-MM-DDTHH:MM:SSZ — normal | advisory | action required

- **Reason:**
- **Responsible actor:**
- **Root filesystem:** used percentage and available space
- **Inodes:** used percentage and availability
- **Memory and swap:** total/available memory and swap use
- **Uptime and load:** uptime and load averages
- **Leading consumers:** concise CPU/memory summary
- **Failed units:** relevant failed-unit summary
- **Storage growth:** evidence, database, report, and log observations
- **Previous-entry comparison:** or `No prior baseline`
- **Capacity assessment:** suitability for the next planned work
- **Classification:** normal | advisory | action required
- **Recommended follow-up:**

## Health entries

At policy creation, no VM health measurement had been recorded.

### 2026-07-18T03:52:24Z — Normal

- **Reason:** Initial measured baseline
- **Responsible actor:** ChatGPT-directed Codex
- **System identity:** `solardt`; Ubuntu 24.04.4 LTS; Linux
  `6.8.0-134-generic` on x86_64
- **Root filesystem:** ext4, 78 GiB total, 13 GiB used, 62 GiB available,
  17% used. Project paths use the same root filesystem; no separate local
  project filesystem was found
- **Inodes:** 5,177,344 total, 178,929 used, 4,998,415 available, 4% used
- **Memory and swap:** 3.8 GiB memory total, 1.6 GiB used, 2.2 GiB available;
  3.8 GiB swap total with 525 MiB used. Available memory, negligible load, and
  low consumer percentages show no current memory pressure; swap use should be
  compared at later reviews
- **Uptime and load:** 10 days 23 hours; 2 CPUs; load averages 0.00, 0.02,
  and 0.02, negligible relative to CPU capacity
- **Leading consumers:** `python` was the highest sampled CPU consumer at
  2.1%; `MainThread` was the highest sampled memory process name at 14.3%,
  followed by other `MainThread` processes and `codex` at 6.8%. Command
  arguments and environments were not recorded
- **Failed units:** systemd state `running`; no failed units reported
- **Storage growth:** repository 841,560,064 bytes, dominated by the
  801,882,112-byte repository evidence directory. The two largest project
  files were ESP32 raw and retained evidence at 156,174,965 and 149,568,755
  bytes. SolarAssistant protected evidence used 80,965,632 allocated bytes
  through existing read-only access. EG4 SQLite was 5,341,184 bytes; reports
  used 4,366,336 bytes; no repository log files were found. Relevant `/tmp`
  project files were small (largest observed: 12,641 bytes). Evidence run
  directories span July 7–17, but no prior health baseline exists for a
  measured growth-rate comparison
- **Filesystem/disk warnings:** bounded unprivileged journal review found no
  filesystem error, I/O error, out-of-space condition, or read-only remount.
  Older boot warnings concerned virtual PCI hot-plug initialization and a
  device reset, not an observed storage-capacity or filesystem fault. Direct
  `dmesg` access was unavailable without privilege and was not bypassed
- **Inaccessible measurements:** direct privileged disk diagnostics and the
  kernel ring buffer were unavailable by design. Credential locations,
  protected collector/monitor logs, and unrelated private files were not
  accessed
- **Previous-entry comparison:** No prior measured baseline
- **Capacity assessment:** ample filesystem, inode, memory, and CPU capacity
  exists for the next bounded offline analysis. Current storage is far below
  the 70% advisory threshold
- **Classification:** Normal
- **Recommended follow-up:** proceed with the bounded ESP32 retention-candidate
  comparison. Repeat this health review within 30 calendar days and at the
  documented event-driven checkpoints; compare swap and evidence growth then
