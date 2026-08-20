# Nonvolatile salt leakage budget

Status: **ANALYTIC / SIMULATION SCREEN ONLY — NO PHYSICAL SPECIMEN**

## Physical rule

Sweat salts are treated as nonvolatile at garment temperatures.

\[
\boxed{J_{salt,vapor}=0}
\]

Water can evaporate; dissolved salt remains in the liquid/solid phases.

## Bulk mass balance for upstream water leakage

Let

- `sigma0 = C0/Csat` be the inlet dissolved-salt concentration normalized by an arbitrary saturation concentration;
- `f_leak` be the fraction of liquid water lost by upstream evaporation before the protected terminal.

With conserved salt flux and water-only vapor loss,

\[
\sigma_{out}=\frac{\sigma_0}{1-f_{leak}}.
\]

Bulk saturation is first reached at

\[
f_{leak,crit}=1-\sigma_0.
\]

No numerical salt solubility is required for this normalized result.

## Important correction

The bulk mass balance does **not** support a claim that a few percent of upstream water evaporation necessarily saturates the whole liquid stream.

For example, 10% water leakage gives only

\[
\frac{1}{0.9}\approx1.11
\]

fold bulk concentration. Twenty percent gives 1.25x; thirty percent gives ~1.43x.

Illustrative normalized thresholds:

| inlet saturation ratio `sigma0` | water loss required for bulk saturation |
|---:|---:|
| 0.01 | 99% |
| 0.05 | 95% |
| 0.10 | 90% |
| 0.20 | 80% |
| 0.50 | 50% |

Therefore an architectural target such as "98–99% of evaporation must occur only at the terminal" **cannot be justified from this bulk salt-saturation equation alone**.

## Why upstream evaporation is still undesirable

The current design still favors liquid-filled protected trunks and terminal evaporation for separate reasons:

1. **water-delivery efficiency** — water lost upstream is unavailable at the selected high-performance terminal;
2. **local wall-film dryout** — a thin meniscus or surface film may locally reach saturation even while the bulk stream remains dilute;
3. **nucleation/deposition** — crystals can form at repeated evaporation sites and progressively alter hydraulic resistance;
4. **cleanability** — terminal deposition can be placed in accessible washable/replaceable regions rather than permanent buried channels;
5. **predictability** — keeping phase change at the exterior separates liquid transport from evaporation.

Items 2–3 are not captured by the present bulk model and remain hypotheses requiring a pore-scale or experimental model.

## Terminal-share targets

If a design objective is simply to deliver a chosen fraction of inlet water to the terminal, the upstream leak budget is direct:

| desired water arriving at terminal | maximum upstream water loss |
|---:|---:|
| 90% | 10% |
| 95% | 5% |
| 98% | 2% |
| 99% | 1% |

These are water-delivery specifications, not salt-saturation thresholds.

## Design implication

The wording used in the project should remain precise:

> internal channels are preferentially protected from evaporation so that water is delivered efficiently to accessible terminal evaporators and so that local salt deposition is displaced away from permanent hydraulic pathways.

Do **not** say that salt evaporates, and do not state that small bulk leakage mathematically guarantees crystallization.

## Next work

1. pore/film-scale local evaporation and concentration polarization;
2. progressive hydraulic-radius loss from wall deposition;
3. dissolution/reset during washing;
4. combine blockage with the capillary redundancy model;
5. multicomponent-solute sensitivity without treating any salt as volatile.
