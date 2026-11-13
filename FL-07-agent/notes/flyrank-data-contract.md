# FlyRank search intelligence data contract
Source: https://github.com/mhv-codes/flyrank-ml-internship/blob/main/work/notebooks/w03_data_contract.ipynb

The March 2026 development partition spans March 1 through March 31, 2026, inclusive, and contains 9,841,378 rows.
The daily grain is client, content item, and report date. The duplicate-key query returned zero duplicate groups for the March partition.
GA4 was available on 413,966 March rows. Zero-filled GA4 fields on unavailable rows do not represent measured zero engagement.
Client history lengths differ. Confirm actual coverage before using a comparison window.
June 2026 is reserved for future evaluation. Features must be available at the scoring cutoff.
Verified post-refresh outcomes are unavailable. The notebook does not establish that refreshing a page causes lift.
