# WD My Book Initial Health Check

Date started: 2026-09-01
Date completed: 2026-09-02

Status: Completed

## Reason

Verify the new 12 TB WD My Book before storing data on it or changing its factory filesystem.

## Drive

- Model: WDC WD120EDGZ-11C4AY0
- Capacity: 12 TB
- Connection: USB
- Initial Linux device: /dev/sda
- Factory partition: exFAT
- Factory partition was not mounted or modified during testing

## SMART Results

- SMART overall health: PASSED
- Short self-test: Completed without error
- Extended self-test: Completed without error
- Reallocated sectors: 0
- Current pending sectors: 0
- Offline uncorrectable sectors: 0
- SMART error log: No Errors Logged
- Pending defects: None

## Temperature

The drive warmed significantly during the extended full-surface test.

- Initial temperature: approximately 23-27 C
- Maximum observed temperature: 54 C
- Temperature during later testing: approximately 51-52 C
- Temperature guard threshold: 55 C
- Temperature guard was never triggered

Physical spacing around the drive was increased during testing.

## Outcome

Successful.

The drive passed the initial health and extended SMART burn-in tests without errors.

The drive is approved to proceed to storage configuration.

## Notes

Temperature should continue to be monitored after normal workloads are established.

The My Book should remain upright with adequate ventilation around the enclosure.
