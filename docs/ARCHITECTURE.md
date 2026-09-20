# Architecture

BlackMamba NetOps treats a router as one managed organism inside a larger local system.

## Cognitive loop

```
OBSERVE
  ↓
EVIDENCE ──→ NORMALIZE ──→ TOPOLOGY
                           ↓
                     DETECT DRIFT
                           ↓
OPERATOR INTENT ──→ POLICY GATE
                           ↓
                         ACT
                           ↓
                       READBACK
                           ↓
                        VERIFY
                           ↺
```

The loop is intentionally asymmetric: observation may happen continuously, but mutation must cross policy.

## Four planes

### Evidence plane
Facts obtained from the environment. Evidence is immutable history; later interpretation does not rewrite what was observed.

### Model plane
Normalizes vendor-specific data into devices, capabilities, links and topology. Unknown is a valid state.

### Intent plane
Describes desired changes without encoding the vendor mechanism. Policy decides whether an intent may cross into an adapter.

### Adapter plane
Owns firmware quirks, paths, tokens, form shapes and read-back mechanics. A Huawei workaround must never become a global NetOps assumption.

## Adaptive means bounded learning

NetOps may learn:
- which adapter matches a device;
- which management interface reaches it;
- which capabilities are exposed;
- how observed state changes over time;
- operator annotations and trusted aliases.

NetOps must not autonomously learn arbitrary shell commands or bypass protected provisioning boundaries.

## Future modules

The architecture deliberately leaves room for:
- topology visualization;
- temporal snapshots and replay;
- anomaly scoring from drift history;
- multi-router / AP orchestration;
- passive service inventory;
- network health baselines;
- optional assistant explanations generated from structured evidence.

The assistant is not the authority. The evidence model is.
