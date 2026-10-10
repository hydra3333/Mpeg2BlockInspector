# Stage A A3 v0.9 - Predicted CL/LINK delta

**Candidate SHA-256:** `ebfcde82405fd2dc25aa7a14a160f89375465d545927b3e4583e7a40fd1af668`  
**A1 SHA-256:** `87acd9ad1c94e5545f84fe57857c076781ca499523d2a80545919ae571dc7a57`

This is a prediction for review. The post-application tlogs and dumpbin outputs are authoritative. Any unexplained delta stops the gate.

## Tool host

Both Debug and Release:

```text
HostX86\x64 -> HostX64\x64
```

Target architecture remains x64.

## Debug CL

Measured checkpoint behavior retained unless listed below.

Deliberate/pinned changes:

```text
/ZI -> /Zi
add /Oi
add /Ot
add /Ob2
add /arch:AVX2
add /guard:cf
add /favor:blend
add /Gy-
add /GF-
```

The candidate explicitly preserves `/MDd`, `/GS`, `/RTC1`, `/JMC`, `/Od`, `/fp:precise`, compile-as-C, warning/diagnostic switches, `/Zc:inline`, `/Fd`, and other measured behavior.

`/Qspectre` must remain absent. `/fp:contract` must remain absent.

## Release CL

Deliberate/pinned changes:

```text
/MD -> /MT
add /GL
add /arch:AVX2
add /guard:cf
add /favor:blend
```

The `/O2` component settings `/Oi /Ot /Ob2 /GF /Gy` are explicitly represented in the project. Their exact emitted spelling/order is verified from the post-A3 tlog.

`/Qspectre` must remain absent. `/fp:contract` must remain absent.

## Debug LINK

Deliberate/pinned changes:

```text
/DEBUG -> /DEBUG:FULL
add /GUARD:CF
add /CETCOMPAT
add explicit /HIGHENTROPYVA
add /OPT:NOREF
add /OPT:NOICF
add /LARGEADDRESSAWARE
add /TSAWARE
```

The candidate explicitly preserves `/INCREMENTAL:NO`, `/MANIFEST`, `asInvoker`, `uiAccess=false`, `/manifest:embed`, the segment-heap manifest input, `/PDB`, `/SUBSYSTEM:CONSOLE`, `/TLBID:1`, `/DYNAMICBASE`, `/NXCOMPAT`, `/IMPLIB`, `/MACHINE:X64`, Large Address Aware, Terminal Server Aware, and Debug no-REF/no-ICF semantics.

`Manifest/EnableSegmentHeap=true` is the single project owner of the segment-heap input. The post-A3 tlog must show exactly one effective `/manifestinput:` entry resolving to `segmentheap.manifest`. Any duplication is a stop condition.

## Release LINK

Deliberate/pinned changes:

```text
/DEBUG -> /DEBUG:FULL
add /LTCG
add /GUARD:CF
add /CETCOMPAT
add explicit /HIGHENTROPYVA
add /PDBALTPATH:%_PDB%
add /LARGEADDRESSAWARE
add /TSAWARE
```

Release retains `/OPT:REF` and `/OPT:ICF`.

## Default libraries

The measured default list remains deliberately unpinned as `AdditionalDependencies`:

```text
kernel32.lib user32.lib gdi32.lib winspool.lib comdlg32.lib advapi32.lib
shell32.lib ole32.lib oleaut32.lib uuid.lib odbc32.lib odbccp32.lib
```

Reason: unreferenced libraries cannot reach the image. The Release standalone import gate, which allows only `KERNEL32.dll`, proves the shipped outcome.

## Release standalone dependency gate

The Release binary must contain none of:

```text
VCRUNTIME*
MSVCP*
api-ms-win-crt-*
ucrtbase*
CONCRT*
VCOMP*
MSVCR1*
```

Expected allowed Release dependency set:

```text
KERNEL32.dll
```

Any additional DLL stops the gate.

## PE/security gate

Post-A3 `dumpbin /headers /loadconfig /imports /dependents` must prove:

- x64 PE32+;
- Large Address Aware;
- High Entropy VA;
- Dynamic Base / ASLR;
- NX / DEP;
- full CFG image state, including non-zero Guard CF function table/count;
- CET compatible;
- security cookie retained;
- manifest present;
- Release CodeView PDB entry contains file name only under D6.

The project setting alone is not proof.

## Explicit default-enum non-emission

The following chosen enum values are explicitly pinned but are expected to emit no switch of their own:

```text
Debug LINK: LinkTimeCodeGeneration=Default
Release CL: BasicRuntimeChecks=Default
```

The post-A3 tlogs are authoritative. If these values emit an unexpected switch, stop and reconcile it rather than treating it as harmless noise.

## Claude v0.8 U2 provenance

The newly listed `/Gy-`, `/GF-`, `/OPT:NOREF`, `/OPT:NOICF`, `/LARGEADDRESSAWARE` and `/TSAWARE` spellings were derived from the installed v180 rule XML during Claude's cold review. They are explicit spellings of intended/preserved behavior, not newly adopted product behavior.
