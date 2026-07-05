---
name: smap
description: "SMAP soil moisture: L3 radiometer products (36 km and enhanced 9 km), retrieval quality flags, the 2015 radar loss and product lineage, L4 model-value-added."
user-invocable: false
---

# smap

Background expertise for SMAP soil moisture. Product facts live in
`knowledge/datasets/smap-l3.md`; the lineage break in
`knowledge/gotchas/smap-radar-loss.md`.

## Knowledge first

Consult and restate: the radar-loss gotcha for ANY record touching
2015 (the combined radar/radiometer product line ends 2015-07-07;
what continues is radiometer-only); the dataset concept's flag and
uncertainty notes.

## Working facts

- The L3 radiometer line (CMR-audited 2026-07-05): SPL3SMP (36 km
  EASE-Grid daily) and SPL3SMP_E (enhanced 9 km); freeze/thaw
  variants (SPL3FTP*); the L4 family (SPL4SM*) is MODEL-assimilated
  surface and root-zone moisture, a different epistemic class from
  the L3 retrievals and never mixed silently with them.
- SPL3SMAP (radar/radiometer combined 9 km) exists only April to
  July 2015; its enhanced resolution came from the radar that failed.
- Retrieval quality flags gate cells (recommended-quality vs
  uncertain); dense vegetation, frozen ground, RFI, and open water
  degrade or invalidate retrievals; flags are categorical, not
  quantitative uncertainty (core QC rule).
- L3 is volumetric soil moisture (m3/m3) for the top ~5 cm;
  "soil moisture" claims state the depth they mean, especially next
  to root-zone L4 values.

## Must NOT

- Never span the 2015 radar loss as one homogeneous record.
- Never mix L3 retrievals and L4 model output without stating the
  class difference.
- Never use non-recommended-quality retrievals in statistics without
  saying so.
- Never quote surface (~5 cm) moisture as root-zone.
