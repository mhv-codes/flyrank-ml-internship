# Build-in-public post draft — do not publish without your review

I built a small content-review ranking experiment during my FlyRank internship. The question was whether a logistic-regression model could improve on a simple prior-impressions rule when ranking pages that later showed a 20%+ impression decline.

I used the anonymized 30,000-row starter slice, kept the later 30-day window out of the features, and held out whole clients for evaluation. On one seven-client holdout, the model's precision@50 was 0.98 versus 0.92 for the rule. That is three additional observed declines in the first 50 on this split; the holdout decline rate was already 0.91, and the experiment does not show that refreshing pages causes traffic recovery.

My main design choice was to make the output a review queue rather than an automatic edit. The next step is an untouched future-time evaluation and an editor feedback log. The notebook, metrics, and limitations are in my repo: https://github.com/mhv-codes/flyrank-ml-internship

#MachineLearning #DataScience #SEO
