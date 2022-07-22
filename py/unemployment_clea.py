import os
import pathlib
import pandas as pd

# make sure we in the project directory
os.chdir(pathlib.Path(__file__).parent.parent.absolute())
print(os.getcwd())

fin = "data/unemployment/unemployment17raw.csv"
fout = "data/unemployment/unemployment17.csv"
want_vars = ["STATE_FIPS", "COUNTY_FIPS", "NAME", "RATE"]

ue = pd.read_csv(fin)
ue.columns = [c.upper().replace(" ", "_") for c in ue.columns]
ue = ue[want_vars]
ue.dropna(inplace=True)
ue.STATE_FIPS = ue.STATE_FIPS.astype(int)
ue.COUNTY_FIPS = ue.COUNTY_FIPS.astype(int)

states = pd.read_csv("data/areas/states.csv")
abb = {}
for _, s in states.iterrows():
    abb[s.ABB] = s.NAME

names = ue.NAME.apply(lambda n: [i.strip().upper() for i in n.split(",")])
ue["STATE"] = names.apply(lambda n: abb[n[1]] if len(n) >= 2 else n[0])
ue["COUNTY"] = names.apply(
    lambda n: n[0].replace("COUNTY", "").replace("MUNICIPIO", "").strip()
)
ue.drop("NAME", axis=1, inplace=True)

ue.to_csv(fout, index=False)
