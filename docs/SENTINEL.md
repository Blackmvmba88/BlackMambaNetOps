# BlackMamba Sentinel

Sentinel is the defensive security plane of BlackMamba NetOps.

Its job is not to declare that an attacker exists. Its job is to preserve observations, correlate independent witnesses, expose unexplained behavior, and make rebuild-to-rebuild comparison cheap.

## Operating model

The workstation is treated as an **epoch**. A clean install begins a new epoch. Sentinel records compact evidence during that epoch and exports evidence before the workstation is rebuilt.

```
clean install -> baseline -> observe -> correlate -> evidence bundle -> rebuild -> next epoch
```

This matches machines where local storage is intentionally disposable while source code and published assets already live elsewhere.

## Sensor families

- **Host witness:** processes, sockets, listeners, routes, neighbors, persistence and platform security metadata.
- **Container witness:** containers, image identity, published ports, networks, mounts, privileges and Docker socket exposure.
- **Network witness:** router observations plus bounded packet/flow metadata.
- **Artifact witness:** hashes and later YARA/YARA-X style classification of selected artifacts.

Sensors begin read-only. Observation and containment are separate capabilities.

## Correlation rule

A finding preserves provenance. Two independent sources agreeing is stronger than one source repeating itself. Correlation is not attribution: Sentinel does not invent attacker identity or label ordinary drift as malicious.

## Big-gun integrations

The architecture can accept richer witnesses without making them mandatory: Zeek/Suricata for network evidence, osquery for host state, Falco/eBPF on supported Linux nodes, and platform-native macOS collectors. These are adapters into the evidence plane, not authorities over it.

## Rebuild model

Evidence bundles should be compact enough to keep off-host (for example on removable storage): event metadata, hashes, baselines, selected diagnostic excerpts and explicit operator annotations. Bulk captures remain bounded and opt-in.
