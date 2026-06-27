import pandas as pd

df = pd.read_csv('./outputs/submission.csv')
for _, row in df.head(10).iterrows():
    print(f"Rank {row['rank']} | Score {row['score']} | {row['candidate_id']}")
    print(f"  {row['reasoning']}")
    print()