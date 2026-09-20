# BlackMamba NetOps

**Adaptive local network control plane. Observe → Model → Act → Verify.**

BlackMamba NetOps is not a prettier router page. It is a local-first control plane that learns the management surface of a network device, normalizes what it observes, keeps operator intent separate from raw evidence, and refuses to call an action successful until read-back confirms reality.

## Core rules

1. **Observed is not inferred.** A hostname, MAC, SSID or lease is evidence; identity and trust are separate annotations.
2. **Capability discovery beats hard-coding.** Interfaces, radios, SSIDs and management paths are resolved at runtime.
3. **READ and WRITE are different trust domains.** Discovery is safe by default; mutations pass an explicit action gate.
4. **Act → Read back → Verify.** A successful HTTP response is not proof that the router changed.
5. **Protected core.** GPON/LOID/VLAN/WAN provisioning stays locked until a dedicated adapter explicitly supports it.
6. **Local-first.** UI/API bind to loopback by default. No telemetry, CDN or arbitrary shell execution.
7. **Human-assisted adaptation.** The engine may discover facts; the operator supplies meaning where evidence cannot.

## Architecture

```text
                         BLACKMAMBA NETOPS
┌─────────────────────────────────────────────────────────────┐
│ UI / API / Reports                                          │
├─────────────────────────────────────────────────────────────┤
│ Intent Gate     │ Inventory       │ Diagnostics             │
│ safe mutations  │ evidence model  │ bounded local tools     │
├─────────────────┴─────────────────┴─────────────────────────┤
│ Adaptive Control Plane                                      │
│ Observe → Resolve → Normalize → Act → Readback → Verify     │
├─────────────────────────────────────────────────────────────┤
│ Device Adapters                                             │
│ Huawei HG8145X6-10 first; additional devices are plugins    │
├─────────────────────────────────────────────────────────────┤
│ ManagementLink                                              │
│ route/interface/link discovery — never assume en0           │
└─────────────────────────────────────────────────────────────┘
```

## First hardware target

Huawei OptiXstar HG8145X6-10 / compatible Huawei web firmware.

The current field prototype has already exercised login, radio-state reads, client inventory and an idempotent OFF→OFF radio write. A firmware quirk was observed where `/set.cgi` requires the Wi-Fi page as its `Referer`; adapters own quirks like this so the rest of NetOps does not.

## Repository direction

```text
blackmamba_netops/
  core/          # evidence, capabilities, intents, verification
  adapters/      # vendor/firmware-specific behavior
  diagnostics/   # bounded local diagnostics
  api/           # loopback control surface
tests/
docs/
```

## Safety model

NetOps is deliberately boring at the dangerous boundary:

- no arbitrary destination URLs;
- no arbitrary shell endpoint;
- bounded diagnostic targets;
- secrets never committed;
- mutation results require read-back;
- provisioning-sensitive operations are denied unless explicitly implemented.

The interesting part lives above that boundary: adaptive discovery, topology synthesis, history, anomaly detection and operator-assisted classification.

## Status

**Phase 0 — field-proven prototype → canonical architecture.**

Next gate: make the live Huawei state, normalized model, API state and rendered UI agree on the same truth, especially the distinction between physical radio, SSID, interface and client.

---
BlackMamba RECORDS / Iyari Gomez — engineering systems that learn the environment before they touch it.
