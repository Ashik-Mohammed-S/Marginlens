# Client demonstration script

Duration: 8–10 minutes. Use the in-app Client briefing view for a printable six-slide presentation.

1. **Business decision:** prioritize margin investigations before negotiation. State immediately that this is a fictional general-merchandise dataset, not Walgreens data.
2. **Performance / August:** show $99,611.24 revenue and $41,914.04 gross profit. Explain ratio-of-sums margin and signed returns.
3. **Margin drivers / September:** show price, volume, product mix, unit cost, and returns; confirm the reconciliation residual is zero. Filter West / Personal care to isolate the seeded price change.
4. **Contract exceptions:** inspect an actual-versus-expected record. Explain authorized overrides and why a potential shortfall is not recovered revenue. Export the selected investigation queue.
5. **Performance / October:** show that incomplete costs suppress total gross profit and margin. Then open Data trust to explain quarantine, nulls, and the source fingerprint.
6. **Forecast:** compare the selected rule with the seasonal baseline on the untouched holdout. Show uncertainty and explain synthetic-data limitations.
7. **Scenario:** increase costs and adjust selling price independently. Explain that the calculation assumes the chosen volume, rather than estimating customer response.
8. **Pilot:** propose authorized data mapping, reconciliation, finance review, and measured outcomes. Do not promise a savings figure.

## Questions to anticipate

- Why not a more complex model? The benchmark is transparent, tested, and sufficient for this synthetic demonstration. Complexity needs measured client-data benefit.
- Can different regions see only their own data? Not in the static demo. Production access must be enforced by the data/API or BI service, not by UI filters.
- Is this production-ready for private company data? No. It is a complete deployable portfolio demonstration with a documented pilot gate.
- Can the numbers be reproduced? Yes: seeded source generation, exact-cent reconciliation, independent dbt parity, and versioned snapshots.
