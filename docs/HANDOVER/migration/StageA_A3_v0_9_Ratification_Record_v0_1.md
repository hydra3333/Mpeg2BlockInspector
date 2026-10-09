# Stage A A3 v0.9 Ratification Record

**Filename:** `StageA_A3_v0_9_Ratification_Record_v0_1.md`
**Version:** 0.1
**Date:** 2026-10-10
**Candidate:** `Mpeg2BlockInspector_A3_APPLYABLE_CANDIDATE_v0_9.vcxproj`
**Candidate SHA-256:** `ebfcde82405fd2dc25aa7a14a160f89375465d545927b3e4583e7a40fd1af668`
**READY package SHA-256:** `4feea4ecbdc82448ab8480a3c28350b917bb5a8101aa87ff1cde5b89e130a921`
**Claude review:** `Claude_REVIEW_OF_ChatGPT_StageA_A3_v0_9_Candidate_v0_1.md`

## Decision

Claude's cold review verdict is:

```text
Ratifiable.
```

Claude found U1 and U2 fixed, no new MUST or SHOULD issues, and recommended that Dave ratify the exact SHA-256 above, then apply it and run the planned A3 gate.

Dave ratified that exact candidate in the migration ChatGPT conversation on 2026-10-10 by replying "yes please" to the explicit ratification prompt naming SHA-256:

```text
ebfcde82405fd2dc25aa7a14a160f89375465d545927b3e4583e7a40fd1af668
```

This ratification authorizes application of that exact candidate only.

It does not waive or pre-accept any A3 post-application gate. Stage A remains open until the build, tlog, PE/security, import/dependency, warning, timing, frozen-hash and six-index gates pass and Claude reviews the results.

## Current published repository baseline before A3 application

```text
34e8a46 Add vapoursynth include files ready for use with DLL building
```

The production A3 project was still unapplied when this record was created.
