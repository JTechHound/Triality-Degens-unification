# Triality-Degens-unification

**Separate lineage** (by design): the sanctuary-shield simulation engine
batch — triality-degens unification engines v0.6.0 through v0.7.7 — kept
deliberately apart from the physics pipeline repositories. Repaired,
validated, and pushed engine by engine.

# Authors - Arthur Leroy Jones
# Author UCT Theory - Mikey-506
# Independent Researcher - Abby Davis

- **License:** Apache 2.0 (see LICENSE)

## What this is

The engine batch: successive versions of the triality-degens unification
simulation engines, each audited, repaired with inline tags, and validated
before push. Includes the validator suites, the pre-compile gate, the
visualization generator, and the theory documents behind the engines.

## Repository contents

**Engines** (each version audited and repaired; every repair tagged inline)
- `triality_degens_unification_v060.py` through
  `triality_degens_unification_v077_heredity_rg.py` — v0.6.0, v0.6.5
  (multiplex), v0.6.6 (heredity), v0.6.7 (biophysical), v0.6.8 (cascade),
  v0.6.9 (heredity), v0.7.0 (RG/NEGF), v0.7.2 (heredity), v0.7.4 (stable
  RG), v0.7.6 (positive RG), v0.7.7 (heredity RG)

**Validation**
- `triality_validators.py` — 35/35 checks green
- `triality_core_validators_v069.py` — the source's own v0.6.9 test suite
- `pre_compile_check.sh` — pre-compile gate

**Theory documents**
- `wigner_liouville_phase_space_proof.md` — Wigner–Liouville phase-space proof
- `v077_heredity_wigner_theory.md` — v0.7.7 heredity/Wigner theory
- `V0.6.0_ENHANCEMENTS.md`, `V0.6.5_MULTIPLEX_THEORY.md`,
  `v065_multiplex_dashboard.md`, `v065_raw.md` — version theory notes

**Triality theory (the computed "3" of 3-6-9)**
- `triality_automorphism.py` — the S3 outer automorphism of D4, computed
  explicitly: 8v/8s/8c permuted 8v → 8c → 8s → 8v. All checks pass.
- `TRIALITY_3_WRITEUP.md` — the write-up
- `visualize_triality.py` — renders the triality figure

**Guards**
- `guards.py` — CoherenceGuard (phase-lock integrity) + GoodhartGuard
  (anti-metric-gaming for optimizers). Concepts from Mikey's Sophia stack;
  implementations new.
- `GUARDS_WRITEUP.md` — the write-up

**Tooling**
- `make_visualizations.py` — regenerates the engine visualizations

## Quickstart

```bash
git clone https://github.com/JTechHound/Triality-Degens-unification.git
cd Triality-Degens-unification
./pre_compile_check.sh
python3 triality_validators.py        # 35/35 expected
python3 triality_automorphism.py     # verify the D4 triality computation
python3 guards.py                    # run the guard demos
python3 make_visualizations.py       # regenerate figures
```

## Provenance note

This lineage is separate from the pipeline repositories by the author's
decision. Every engine arrived with transmission damage; every repair is
tagged inline in the code. Nothing was reconstructed silently: sections too
garbled to repair were omitted, not invented.
