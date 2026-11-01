# Lesson 1 - grain, joins, and trustworthy margin

Estimated time: 30-45 minutes. No installation needed.

## Concept

Grain means exactly what one row represents. If sales has one row per invoice line, joining it to two matching contract records duplicates the sale and can inflate revenue. Define the grain and expected join cardinality before building measures.

Gross margin is a ratio of totals. Averaging percentages gives each row equal weight even when revenue differs substantially.

## Exercise

All amounts below are USD. Net revenue and COGS are already signed; costs are fully known.

| Line | Event | Net revenue | COGS |
|---|---|---:|---:|
| A | Sale | 200 | 140 |
| B | Sale | 50 | 45 |
| C | Return | -20 | -14 |

1. Calculate total net revenue, COGS, gross profit, and gross margin percentage.
2. Explain why averaging each line's margin percentage produces the wrong overall result.
3. A sale matches two overlapping contract records. Should we pick either record, duplicate the sale, or flag the ambiguity? Explain how to preserve revenue totals.
4. A sale has no cost record. Why is assigning zero cost dangerous? What should the dashboard show?
5. Explain why a below-contract price is not automatically recoverable revenue.

Reply in chat with your answers. We will review the reasoning before marking learning complete. You can ask for hints.

## Next step

Translate the reviewed definitions into a data dictionary and deterministic synthetic examples, then implement reconciliation queries.
