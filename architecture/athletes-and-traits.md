# Athlete data and tendency fields

**Runtime verified for data exposure**, not direct gameplay behavior. Source: Flame profile/trait matching (Flame Simulator source; private repository) and 0.6.3 probe status (Flame Simulator source; private repository).

The 0.6.1 F7 profile capture was matched against screenshots of named athletes, ages and eight skill values, supporting this empirical mapping of `trait_values` keys:

| Key | Observed UI meaning | Interpretation |
| --- | --- | --- |
| `0` | Aggressive versus Defensive Playstyle | Signed tendency: positive Aggressive, negative Defensive |
| `1` | Fight Joining | Nonnegative tendency in sampled UI comparisons |
| `2` | Lane Ganking | Nonnegative tendency in sampled UI comparisons |

Tooltip language describes activation at threshold 50 (negative direction `≤ -50` for Defensive). **Higher active values do not mean stronger effects:** the tooltip says they require more feedback to deactivate. Physical measurement of threshold crossing and specific AI behavior effects remains separate work.

Flame 0.3.1 physically loaded in game 0.6.3 on 2026-10-08; F7 returned 32/32 complete Athlete records with keys `0`, `1`, `2` and SDK ABI 9. This verifies the field *presence* in 0.6.3, but is not by itself a complete revalidation of every 0.6.1 tooltip interpretation or behavior effect.

For career-scale personality or Dynasty mods: **stable identities across reloads, retirement, transfer, ID reuse, off-map entities, roster depletion, and persistence side effects are not yet verified**. See Dynasties proposed probes (Dynasties source; private repository) and [open investigations](../research/open-questions.md).
