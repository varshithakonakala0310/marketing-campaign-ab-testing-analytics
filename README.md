# Marketing Campaign A/B Testing Analytics

## Business problem

Marketing spend is spread across Email, Social, Search and Display. The business needs evidence — not opinion — on whether a new campaign variant (B) actually converts better than the control (A), and which channel returns most.

## Questions

1. Does variant B convert significantly better than variant A?
2. Which channel / variant combination has the highest conversion rate and ROI?

## Dataset

**Synthetic data only** — generated in `analysis.py` with a fixed seed (42): 20,000 users, 2,500 per channel × variant cell. Saved to `data/campaign_data_synthetic.csv`.

## Method

- Conversion rate and ROI by channel and variant
- Chi-square test of independence on the A vs B conversion contingency table (SciPy)

## Key findings (actual run results)

From `results/results_summary.txt` and `results/channel_performance.csv`:

- Overall conversion: **A (control) 0.0671 vs B (variant) 0.0877**
- Chi-square test: **χ² = 29.4255, p = 5.81091e-08** — statistically significant at the 0.05 level; variant B's uplift is not explained by chance in this synthetic experiment
- Best channel / variant by conversion: **Search, variant B — 0.1308 conversion rate**
- Search B also recorded the highest ROI in the table (17.16); see `results/channel_performance.csv` for the full channel breakdown

## Tech stack

Python · pandas · NumPy · SciPy · scikit-learn

## How to run

```bash
pip install -r requirements.txt
python3 analysis.py
```

## Repository structure

```
├── analysis.py
├── data/
├── results/   # results_summary.txt, channel_performance.csv
├── requirements.txt
└── LICENSE
```

## License

MIT — see `LICENSE`. Copyright (c) 2026 Varshitha Konakala.
