# Capstone report — Refresh / Content Opportunity Scoring

- **Author:** Harsha Vardhan
- **Lane:** Refresh / Content Opportunity Scoring
- **Repo:** https://github.com/mhv-codes/flyrank-ml-internship
- **Date:** 2026-11-13

## 0. Abstract

Can a small logistic-regression ranking model help an editor prioritize pages with a later 20% or greater impression decline over a prior-impressions rule? I used the repository's 30,000-row anonymized starter slice, retaining 11,119 eligible rows and holding out 7 entire clients (783 rows). The model used prior-window impressions and clicks plus age at cutoff, with seed 42 and a training-only log/scaling pipeline; the baseline ranked by prior impressions on the same split. Precision@50 was 0.98 for the model versus 0.92 for the rule, while the holdout decline base rate was 0.911 and ROC AUC was 0.646. The score is a review-priority aid for a human editor, not evidence that refreshing a page causes recovery.

## 1. Problem framing

With a limited editorial review budget, choose which pages a person should inspect first. The unit is a pseudonymous content item; the output is a ranking and a predicted probability of a later-window decline. The editor can check page accuracy, search intent, data quality, and freshness before deciding whether any change is appropriate. A false positive uses review time; a false negative leaves a possible issue unexamined. ML is worth testing because three observed pre-cutoff signals may produce a more useful ordering than a fixed exposure rule, but the model is not permitted to edit pages.

## 2. Data safety

Input: `data/raw/content_refresh_anonymized.csv`, 30,000 rows × 44 columns, one row per pseudonymized content item from the starter slice. The exact public data commit is `48d0dac47169e9f14b106037938d414b16529aaf`; SHA-256 is `c43bdac4eccfa17fcd8a33974fe36f2c998c03a3ae3af8d80cf712abab5d6396`. This run filters for age at cutoff ≥30 days and prior impressions ≥500, leaving 11,119 eligible rows. It uses the `prev_30d` fields as features and `last_30d` impressions only to make the outcome. `trend_pct`, `trend_direction`, the decline label, composite flags, IDs, URLs, queries, and page text are excluded from features. `client_id` only groups the split; IDs do not appear in exported results. This is the starter slice, not a new run over the 78.8-million-row warehouse release.

## 3. Baseline

The transparent baseline ranks by impressions in the prior 30-day window, matching the eligible queue and evaluation split. It is a fair comparator because it uses a pre-cutoff observable signal and does not include the later-window label. On the same 783 held-out rows, it achieved precision@10 0.80, precision@50 0.92, average precision 0.9309, and ROC AUC 0.6205.

## 4. Model / analysis

The target is `impressions_last_30d < 0.8 × impressions_prev_30d`. The model is `log1p` → standard scaling → regularized logistic regression (`max_iter=1000`, seed 42). Features: prior impressions, prior clicks, and age at cutoff (content age shifted back by 30 days). It was chosen because this is a binary observed-label ranking task and logistic regression is simple to inspect. The scaler and model fit on training data only. No hyperparameter tuning was conducted.

## 5. Evaluation

A seeded 75/25 `GroupShuffleSplit` holds out entire clients: 21 training clients and 7 test clients. The split contains 10,336 training rows and 783 test rows, with zero client overlap. Both baseline and model use the same test rows. The holdout decline base rate is 0.9106 (713 / 783), compared with 0.585 in training as recorded by the prior modeling notebook; this difference matters when interpreting precision. Logistic regression reached precision@10 1.00, precision@50 0.98, average precision 0.9483 and ROC AUC 0.6463. Its top-50 improvement is 0.06, or three additional observed declines among 50 ranked items on this split. This is modest and directional. At a separate 0.50 probability threshold, there were 185 false negatives and 39 false positives, showing the score does not remove review errors.

## 6. Interpretation

The model adds some ranking signal to prior exposure on this particular held-out set. The high base rate means precision alone overstates practical separation; ROC AUC remains modest. Logistic coefficients are associations for standardized log-transformed inputs, not independent causal effects, especially because impressions and clicks are related. The error summary is aggregated and does not reveal row IDs.

## 7. Recommendation

Use the model only to order a small queue for human review. Before any edit, confirm that the decline is not a measurement change or seasonal variation; check current intent, claims, source dates, and page context. Log editor decisions and evaluate against an untouched later date window before operational use. Do not auto-publish, rewrite factual claims, change indexing/canonicals, delete/merge pages, contact clients, allocate spend, or promise traffic or revenue.

## 8. Reproducibility

Notebook: [`work/notebooks/capstone.ipynb`](notebooks/capstone.ipynb). Prior action playbook: [`work/notebooks/w07_action_playbook.ipynb`](notebooks/w07_action_playbook.ipynb). Install `requirements.txt`, open the capstone notebook in Colab or Jupyter, and run all cells. Seed 42 and the pinned dataset hash are checked. It regenerates `work/outputs/capstone_metrics.json` and two aggregate SVGs under `work/figures/`. The row-level queue is not committed by repository policy. Tested locally against the checked-in starter slice on pandas 2.2.3 / scikit-learn 1.8.0.

## 9. Acknowledgments & data credit

Built on the [FlyRank ML Internship dataset](https://flyrank.ai). The public page and figures disclose only aggregated metrics and do not include client names, domains, URLs, queries, pseudonymous IDs, or row-level outcomes.
