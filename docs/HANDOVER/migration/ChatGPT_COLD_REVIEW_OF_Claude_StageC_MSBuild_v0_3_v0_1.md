# ChatGPT cold-review disposition - Claude Stage C proposal v0.3

Date: 2026-10-10. Status: Draft for Claude second review; no change applied to project.

## Accepted

- Dave's binding decisions: x64 target and host/tooling, version-independent single VS discovery with no hard-coded root, Build Tools included (`-products *`), mandatory output gates, deferred newest-MSVC compiler policy.
- M1: one installation discovery and explicit capability requirements; verify exact component ID on host.
- M2: `amd64` MSBuild selection plus independent runtime bitness proof.
- M3: guard host environment and reserve VsDevCmd for interactive tools.
- M4: record full toolchain identity and versions each build.
- M5: ratify the *policy*, not the untested specific MSBuild XML expressions.

## Qualified / evidence requests

Q1: `$(DefaultPlatformToolset)` selection and availability before the Configuration group are UNVERIFIED; additionally, a Visual Studio default does not inherently prove the newest qualifying *installed* toolset across all instances. Verify on Dave's system before implementing.

Q2: Microsoft documents `Microsoft.VCToolsVersion.default.txt` as latest **in-support** MSVC build. This may differ from the numerically newest installed build; reconcile the exact policy with Dave before selecting it. `Microsoft.VCToolsVersion.default.txt` is documented; actual file contents/version and selection on Dave's installation are unverified.

Q3: Make the minimum-v145 guard semantically numeric; a naive lexical toolset string comparison is unsafe. Guard execution point and exact condition require local proof.

Q4: `CL`, `_CL_`, `LINK`, `_LINK_`, `Platform` alone are not a complete environment threat model; also consider `PreferredToolArchitecture`, MSBuild global property overrides, and inherited properties while avoiding harmful overblocking. Confirm exact behaviour experimentally.

Q5: Microsoft's `vswhere` wiki confirms `-products *` adds Build Tools and `%ProgramFiles(x86)%\Microsoft Visual Studio\Installer\vswhere.exe` is the conventional installer location. The VC workload component's presence on Dave's machine remains unverified.

Q6: Changing the selected VS installation or MSBuild props/targets (even with identical compiler version) may change emitted switches. The permanent CL/LINK and imports gate must run on every build; the compiler/toolset-change triggers are *additional* warnings and six-index regression, not substitutes.

## Gate continuity

A3 v0.10: W1 PASS (113 content-checked tokens), HostX64 PASS; next warning comparison. Preserve current fixed MSBuild executable and unchanged production project until A3 and Stage A are closed.

## Sources (reviewer-readable)

- Claude review v0.3, attached verbatim to this package.
- Microsoft C++ MSBuild internals: https://learn.microsoft.com/en-us/cpp/build/reference/msbuild-visual-cpp-overview
- Microsoft MSVC tooling/version files: https://learn.microsoft.com/en-us/cpp/overview/acquire-msvc
- Microsoft vswhere documentation: https://github.com/microsoft/vswhere/wiki/Find-MSBuild
- Dave's instructions dated 2026-10-10, plus A3 gate outputs supplied in this conversation.
