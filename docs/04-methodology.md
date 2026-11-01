# Analytical methodology

## Margin bridge

Compare selected month (1) with prior calendar month (0). Use gross sale units q_i, aggregate units Q, effective sale price p_i, and captured unit cost c_i for each product i. Returns are attributed separately.

- Volume = (Q1-Q0) * sum[(q0_i/Q0)*(p0_i-c0_i)]
- Mix = Q1 * sum[(q1_i/Q1-q0_i/Q0)*(p0_i-c0_i)]
- Price = sum[q1_i*(p1_i-p0_i)]
- Cost = -sum[q1_i*(c1_i-c0_i)]
- Returns = current returned gross profit - prior returned gross profit

Their sum must equal total gross-profit change within floating-point tolerance. This is an order-dependent accounting decomposition, not causal attribution. New/discontinued products require a separate effect in a production extension; the demo refuses noncomparable zero-volume products. Missing costs block attribution. Month length and weekday composition contribute to the volume effect.

## Forecast target and split

Target: daily gross units sold across all stores/products; returns excluded. Forecast horizon: 28 days. The models consume only history available at each cutoff.

Candidates:
1. Seasonal naive: repeat the most recent seven days.
2. Weekday trend: average each weekday over four weeks, multiplied by the ratio of the most recent fortnight to its predecessor, bounded to 0.85–1.15.

Three non-overlapping 28-day validation folds precede the final untouched 28-day holdout. WAPE = sum absolute errors / sum actual units. Select the candidate with smallest validation WAPE; report both candidates on the holdout without changing the selection. Refit the selected rule on all history for the next 28 days.

Empirical uncertainty uses the 90th percentile of validation absolute errors around each point prediction, clipped below at zero. This is not a calibrated probabilistic model. Report achieved holdout coverage; do not promise 90% future coverage. There is no automatic promotion or retraining service.

Results and exact dates are generated in reports/validation.json. Performance on synthetic patterns is not evidence of real-client generalization.

## Scenario planner

Use complete September gross sales economics. Revenue' = revenue*(1+price_change)*(1+volume_change). Cost' = cost*(1+cost_change)*(1+volume_change). Gross sale profit' = revenue'-cost'. Sliders are independent assumptions and exclude returns, demand elasticity, stock constraints, and fixed operating costs. This is neither a forecast nor an optimization recommendation.
