# Meltemic — identity system

Everything here derives from one idea: the **Meltemi**, the steady summer wind of
the Aegean. The Greeks called it the *Etesian* — the "annual" wind. It arrives
every year, from the same quarter, with the same force. You don't fight it; you
set a course that uses it.

---

## The mark

A monoline **M**, splayed and raked, drawn as the zigzag a boat makes beating
upwind. It is the monogram, the wave and the tacking course at once.

Constructed geometry — do not redraw by eye:

| Parameter | Value |
| --- | --- |
| Stroke (perpendicular) | 19 units |
| Splay (horizontal step) | 28 units |
| Centreline height | 76 units |
| Middle vertex | −14 units (above the foot baseline) |
| Apex | mitred, then cut flat 12 units down the spike |
| Feet | cut flat, horizontal, on the baseline |
| Lean | 7° to the right |

The flat apex cuts and the flat feet are the same treatment: every terminal in
the mark is a horizontal cut. That is what stops it reading as a generic
lightning zigzag, and what keeps the apex from vanishing below 16 px.

## The lockup

| Relationship | Value |
| --- | --- |
| Mark height | 1.14 × the wordmark ascender |
| Mark position | feet on the wordmark baseline |
| Gap | 0.40 × mark height |

The mark is set *heavier and taller* than pure maths would suggest, because
diagonals read lighter than verticals. Stroke 19 (not 17) and 1.14× (not 1.0×)
are optical corrections, not arbitrary.

## The wordmark

**Archivo**, weight 700, width 100, tracking −26/1000 em, all lowercase.

Lowercase is not a startup affectation here — it is *kleinschreibung*, the
Bauhaus convention, which is also the modernism of Tel Aviv's White City and the
restraint of Danish design. It is the correct register for this founder.

One letter is custom: the final **c**. Its aperture is re-cut as a wedge at ±18°
from a point at x265, opening the terminals on an angle. The `c` is the letter
that turned *Meltemi* into a company, so it is the letter that carries the
craft. Subtle at small sizes, legible at large — which is how a custom letterform
should behave.

## Palette

| Token | Hex | Role | Contrast |
| --- | --- | --- | --- |
| `--ink` | `#0B2733` | Text, dark surfaces | 13.8:1 on limestone (AAA) |
| `--sea` | `#14607A` | Links, active states | 6.2:1 on limestone (AA) |
| `--gust` | `#8FBFCE` | Reversed secondary text | 7.8:1 on ink (AAA) |
| `--clay` | `#C24A26` | The single accent — CTAs only | white on it 4.9:1 (AA) |
| `--limestone` | `#F4F1EA` | Page ground | — |
| `--slate` | `#54707C` | Secondary text on light | 4.7:1 on limestone (AA) |
| `--salt` | `#FFFFFF` | Card surfaces | — |

Warm limestone paper, deep Aegean ink, one Cycladic clay accent. Clay is
rationed: primary buttons and the tack rule. If clay appears three times on a
screen it has stopped being an accent.

## Type system

| Family | Job |
| --- | --- |
| **Archivo** 600/700 | Wordmark, headlines, stat figures |
| **Inter** 400/500/600 | Body and UI text |
| **IBM Plex Mono** 400/500 | Eyebrows, badges, stat labels, footer meta |

The mono register is where "intelligent code" lives. It replaces the old `<`
bracket in the logo — the same signal, but systemic rather than decorative, and
it does not cost the logo its uniqueness.

## Files

| File | Use |
| --- | --- |
| `logo-lockup.svg` | Primary horizontal lockup — `currentColor` |
| `logo-stacked.svg` | Vertical lockup for square-ish spaces |
| `logo-mark.svg` | Mark alone — `currentColor` |
| `logo-wordmark.svg` | Wordmark alone |
| `icon.svg` / `icon-sea.svg` | App icon and avatar, rounded square |
| `icon-square.svg` | Full-bleed square (iOS applies its own mask) |
| `favicon.svg` / `.ico` / `-16` / `-32` | Browser tabs |
| `apple-touch-icon.png` | 180 px, iOS home screen |
| `icon-512.png` / `icon-192.png` | PWA, Open Graph, social profiles |
| `rule-tack.svg` | The tacking-course rule — section device |

All logo SVGs use `fill="currentColor"`, so one file works in ink, limestone or
clay. Set the color on the parent element.

## Rules

- **Minimum lockup height: 18 px.** Below that use the mark or the icon.
- **Clear space: one mark-width on every side.** Nothing enters it.
- Do not re-letter the wordmark in stock Archivo — the custom `c` will be lost.
- Do not outline, gradient, shadow or rotate the mark. The 7° lean is built in;
  adding more is double-counting.
- The mark is never stretched. Scale proportionally or not at all.
- On photography, use the ink or limestone lockup on a plain field — never
  directly over busy water.

## Rebuilding

The geometry is generated, not hand-drawn, so it can be reproduced exactly.
The full brand review — the audit, the exploration and the reasoning behind
every number above — is in [`_review/brand-review.html`](../_review/brand-review.html) — kept in the
repository but excluded from the published site via `_config.yml`. The scripts
that generate the marks are in [`src/`](src/); run `python src/build.py` to
regenerate every SVG from the parameters above.
