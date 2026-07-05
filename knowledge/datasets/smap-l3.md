---
type: dataset
title: "SMAP L3 radiometer soil moisture (SPL3SMP, SPL3SMP_E)"
description: "Daily global volumetric soil moisture for the top ~5 cm from the SMAP radiometer, 36 km and enhanced 9 km EASE-Grid; retrieval-quality flags gate every cell."
tags: [smap, soil-moisture, radiometer, ease-grid, nsidc]
timestamp: 2026-07-05
resource: https://nsidc.org/data/spl3smp_e
version: "SPL3SMP and SPL3SMP_E, CMR-verified 2026-07-05 (with SPL3FTP freeze/thaw and the SPL4 model-assimilated family as adjacent lines)"
status: verified
verified: 2026-07-05
verified_by: Paul Ramirez (steward pro tem)
---

# SMAP L3 radiometer soil moisture

**Identity.** NASA SMAP L-band radiometer retrievals of volumetric
soil moisture (m3/m3) for roughly the top 5 cm: SPL3SMP (36 km
EASE-Grid, daily) and SPL3SMP_E (enhanced 9 km posting), AM and PM
overpasses kept distinct. Archive NSIDC DAAC. The SPL4 family is
model-assimilated surface AND root-zone moisture: value-added model
output, a different epistemic class from the L3 retrievals.

**Structure.** Daily composite grids with per-cell retrieval-quality
flags (recommended vs uncertain), surface-condition flags (frozen
ground, dense vegetation, RFI, water fraction), and the retrieval
uncertainty fields the product documentation defines.

## Uncertainty

- The mission's core requirement is retrieval accuracy of about
  0.04 m3/m3 (ubRMSE) under acceptable vegetation conditions;
  performance degrades with vegetation water content and is not
  validated everywhere. Product uncertainty fields and quality flags
  are the per-cell instruments.
- The enhanced 9 km posting (SPL3SMP_E) is an interpolation-based
  enhancement of the same radiometer measurement, not new information
  at 9 km; feature-scale claims respect the native ~36 km footprint
  (the same oversell trap as other enhanced-posting products).
- Retrieval flags are categorical gates, not quantitative uncertainty
  (core QC rule); ~5 cm depth semantics are part of every claim.

## Known issues

- [smap-radar-loss](../gotchas/smap-radar-loss.md).
