# BuildLens — Learning Ledger (index)

The ledger was split by phase on 2026-09-14. Every record is preserved verbatim, in its original order, in the file for its phase. Nothing was reworded, deduplicated, or removed.

**Append new evidence to the file for the current phase** (currently `LEARNING_LEDGER_PHASE_9.md`). Start a new `LEARNING_LEDGER_PHASE_<n>.md` when a phase starts. References elsewhere to `learning/LEARNING_LEDGER.md` mean this index and the phase files together.

## Files

- [`LEARNING_LEDGER_TEMPLATES.md`](LEARNING_LEDGER_TEMPLATES.md)
- [`LEARNING_LEDGER_PHASE_0.md`](LEARNING_LEDGER_PHASE_0.md)
- [`LEARNING_LEDGER_PHASE_1.md`](LEARNING_LEDGER_PHASE_1.md)
- [`LEARNING_LEDGER_PHASE_2.md`](LEARNING_LEDGER_PHASE_2.md)
- [`LEARNING_LEDGER_PHASE_3.md`](LEARNING_LEDGER_PHASE_3.md)
- [`LEARNING_LEDGER_PHASE_4.md`](LEARNING_LEDGER_PHASE_4.md)
- [`LEARNING_LEDGER_PHASE_5.md`](LEARNING_LEDGER_PHASE_5.md)
- [`LEARNING_LEDGER_PHASE_6.md`](LEARNING_LEDGER_PHASE_6.md)
- [`LEARNING_LEDGER_PHASE_7.md`](LEARNING_LEDGER_PHASE_7.md)
- [`LEARNING_LEDGER_PHASE_8.md`](LEARNING_LEDGER_PHASE_8.md)
- [`LEARNING_LEDGER_PHASE_9.md`](LEARNING_LEDGER_PHASE_9.md)

## How records were assigned

- Each record goes to the phase named in its evidence ID (`EV-P<n>-...`), its `BUILD PHASE` field, or its phase heading.
- Records without a phase (session notes, cumulative-review and counter records, corrections) stay with the phase they were written in.
- Major cumulative review 2, the Phase 8 -> 9 architecture reset, and the tests/docs layout work (all before Phase 9 started) are in the Phase 8 file.
- Phases 1 and 2, and phases 4 and 5, were interleaved; their files contain several ranges each, in original order.

## Reconstruction map

Concatenating these ranges in order, taking the next unread bytes from each file, reproduces the pre-split ledger byte for byte (SHA-256 `a6785814660eaba3654394b1661500f4abd620b4e41f59c57fedb9d0ca4abd6a`, 1868385 bytes, 51991 lines).

| # | File | Original lines | Bytes |
|---|---|---|---|
| 1 | `LEARNING_LEDGER_TEMPLATES.md` | 1-385 | 6935 |
| 2 | `LEARNING_LEDGER_PHASE_0.md` | 386-1213 | 25852 |
| 3 | `LEARNING_LEDGER_PHASE_1.md` | 1214-12151 | 369800 |
| 4 | `LEARNING_LEDGER_PHASE_2.md` | 12152-12575 | 11825 |
| 5 | `LEARNING_LEDGER_PHASE_1.md` | 12576-12838 | 6821 |
| 6 | `LEARNING_LEDGER_PHASE_2.md` | 12839-13212 | 10561 |
| 7 | `LEARNING_LEDGER_PHASE_1.md` | 13213-13594 | 10328 |
| 8 | `LEARNING_LEDGER_PHASE_2.md` | 13595-13938 | 10145 |
| 9 | `LEARNING_LEDGER_PHASE_1.md` | 13939-16069 | 72440 |
| 10 | `LEARNING_LEDGER_PHASE_3.md` | 16070-17373 | 46951 |
| 11 | `LEARNING_LEDGER_PHASE_5.md` | 17374-18568 | 41332 |
| 12 | `LEARNING_LEDGER_PHASE_4.md` | 18569-18824 | 8474 |
| 13 | `LEARNING_LEDGER_PHASE_5.md` | 18825-25602 | 189377 |
| 14 | `LEARNING_LEDGER_PHASE_6.md` | 25603-29421 | 134172 |
| 15 | `LEARNING_LEDGER_PHASE_7.md` | 29422-33068 | 141295 |
| 16 | `LEARNING_LEDGER_PHASE_8.md` | 33069-51233 | 737207 |
| 17 | `LEARNING_LEDGER_PHASE_9.md` | 51234-51992 | 44870 |
