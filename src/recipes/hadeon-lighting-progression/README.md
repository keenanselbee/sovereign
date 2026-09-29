Hadeon lighting progression authoring
=====================================

Run `node src/recipes/hadeon-lighting-progression/generate.mjs` from the
repository root after changing the accepted ignition formula or order. The
script rewrites only the 96 paired ignition initializers in
`src/events/m18_00_00_00.emevd.dcx.js`. It is idempotent; compiling and accepting
the EMEVD remain separate workflow steps.

`ignition-order.json` preserves the previous thirty-second sequence's fixed
shuffled rank order, with one zero-based ignition slot per rank. The script
precomputes eleven HP thresholds per slot. It splits them between event 5750401
(losses 0-5) and event 5750407 (losses 6-10) to keep each event within the
native condition-group limit. Each slot also receives the minimum death-tier
flag that lights it at full boss HP; 1055425273 is the unused sentinel for
positions requiring boss damage even after ten losses.
