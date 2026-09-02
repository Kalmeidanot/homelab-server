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

- Initial temperature: approximately 23-27 C
- Maximum observed during extended test: 54 C
- Automatic safety threshold: 55 C
- Safety threshold was never reached
- Extended self-test completed normally without intervention

Physical spacing around the drive was increased during testing.

## Outcome

Successful.

The drive passed the initial health and extended SMART burn-in tests without errors.

The drive is approved for NAS storage configuration.

## Notes

Temperature should continue to be monitored under normal NAS workloads.

The My Book should remain upright with adequate ventilation.
