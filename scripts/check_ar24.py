import pandas as pd

df = pd.read_csv('Data/ar24/ar24.csv')

print(f"Total rows: {len(df):,}")
print(f"Unique counties: {df['county_name'].nunique()}")
print(f"\nCounties included:")
for county in sorted(df['county_name'].unique()):
    print(f"  - {county}")

print(f"\nUnique offices:")
for office in df['office'].unique():
    print(f"  - {office}")

print(f"\nSample vote counts by candidate (Presidential):")
pres = df[df['office'] == 'US PRESIDENT'].groupby('candidate')['votes'].sum().sort_values(ascending=False)
print(pres.head(10))
