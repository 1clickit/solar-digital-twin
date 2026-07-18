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

The review is read-only unless a separate bounded work unit authorizes a
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

No VM health measurement has been recorded yet. The first read-only review is
the immediate operational work unit in `NEXT_TASK.md`.
