import os, warnings; warnings.filterwarnings("ignore")
import numpy as np, pandas as pd
from scipy import stats
BASE=os.path.dirname(os.path.abspath(__file__)); os.makedirs(os.path.join(BASE,"data"),exist_ok=True); os.makedirs(os.path.join(BASE,"results"),exist_ok=True)
rng=np.random.default_rng(42)
channels=["Email","Social","Search","Display"]
rows=[]
uid=1
for ch in channels:
    base_rate={"Email":0.08,"Social":0.05,"Search":0.11,"Display":0.03}[ch]
    for variant, lift in [("A_control",0.0),("B_variant",0.02)]:
        n=2500; conv=rng.binomial(1, min(base_rate+lift,0.95), n)
        spend=rng.uniform(800,2500); rev_per=rng.lognormal(3.8,0.5,size=n)*conv
        for i in range(n):
            rows.append({"user_id":uid,"channel":ch,"variant":variant,"converted":int(conv[i]),"revenue":round(float(rev_per[i]),2),"spend_allocated":round(spend/n,4)}); uid+=1
df=pd.DataFrame(rows); df.to_csv(os.path.join(BASE,"data","campaign_data_synthetic.csv"),index=False)
a=df[df.variant=="A_control"]; b=df[df.variant=="B_variant"]
table=np.array([[a.converted.sum(), len(a)-a.converted.sum()],[b.converted.sum(), len(b)-b.converted.sum()]])
chi2,p,_,_=stats.chi2_contingency(table)
by=df.groupby(["channel","variant"]).agg(users=("user_id","count"),conversions=("converted","sum"),revenue=("revenue","sum"),spend=("spend_allocated","sum")).reset_index()
by["conversion_rate"]=by.conversions/by.users; by["roi"]=(by.revenue-by.spend)/by.spend
by.to_csv(os.path.join(BASE,"results","channel_performance.csv"),index=False)
with open(os.path.join(BASE,"results","results_summary.txt"),"w") as f:
    f.write("Marketing Campaign A/B Testing Analytics — SYNTHETIC RESULTS\n")
    f.write(f"Total users: {len(df)}, Overall conversion A: {a.converted.mean():.4f}, B: {b.converted.mean():.4f}\n")
    f.write(f"Chi-square test A vs B: chi2={chi2:.4f}, p-value={p:.6g}, significant_at_0.05={p<0.05}\n")
    for _,r in by.iterrows(): f.write(f"  {r['channel']} {r['variant']}: users={int(r['users'])} conv_rate={r['conversion_rate']:.4f} revenue=GBP {r['revenue']:.2f} ROI={r['roi']:.2f}\n")
    best=by.sort_values("conversion_rate",ascending=False).iloc[0]; f.write(f"Best channel/variant by conversion: {best['channel']} {best['variant']} ({best['conversion_rate']:.4f})\n")
print(f"p={p:.6g} A={a.converted.mean():.4f} B={b.converted.mean():.4f}")
