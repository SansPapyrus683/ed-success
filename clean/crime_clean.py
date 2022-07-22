import os
import pathlib
import pandas as pd

# make sure we in the project directory
os.chdir(pathlib.Path(__file__).parent.parent.absolute())
print(os.getcwd())


def strip_digits(s: str) -> str:
    return "".join(c for c in s if not c.isdigit()).strip()


fin = "data/crime/crime17raw.csv"
fout = "data/crime/crime17.csv"
want_vars = ["state", "county", "violent_crime", "property_crime"]

crime = pd.read_csv(fin)
crime.columns = [c.lower().replace(" ", "_") for c in crime.columns]
crime = crime[want_vars]

crime.state.fillna(method="ffill", inplace=True)
crime.dropna(inplace=True)

crime.state = crime.state.apply(lambda s: s.split('-')[0].strip().lower())
crime.county = crime.county.apply(
    lambda c: (c.lower()
               .replace("county", "")
               .replace("police department", "")
               .strip())
)
crime.violent_crime = crime.violent_crime.apply(lambda n: int(n.replace(",", "")))
crime.property_crime = crime.property_crime.apply(lambda n: int(n.replace(",", "")))

bad = {
    "augusta-richmond",
    "de kalb",
    "la porte6",
    "hartsville/trousdale"
}
crime = crime.loc[~crime.county.isin(bad)]

counties = pd.read_csv("data/areas/counties.csv")
cty_fips = {}
for _, c in counties.iterrows():
    name = (c["name"]
            .lower()
            .replace("municipio", "")
            .replace("county", "")
            .replace("parish", "")
            .strip())
    cty_fips[name] = c.fips_state, c.fips_county

exceptions = {
    "westchester public safety": "westchester",
    "salt lake  unified": "salt lake"
}
crime["fips_state"] = crime.county.apply(
    lambda c: cty_fips[exceptions.get(strip_digits(c), strip_digits(c))][0]
)
crime["fips_county"] = crime.county.apply(
    lambda c: cty_fips[exceptions.get(strip_digits(c), strip_digits(c))][1]
)

crime.to_csv(fout, index=False)
