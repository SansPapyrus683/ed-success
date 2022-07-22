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
want_vars = ["STATE", "COUNTY", "VIOLENT_CRIME", "PROPERTY_CRIME"]

crime = pd.read_csv(fin)
crime.columns = [c.upper().replace(" ", "_") for c in crime.columns]
crime = crime[want_vars]

crime.STATE.fillna(method="ffill", inplace=True)
crime.dropna(inplace=True)

crime.STATE = crime.STATE.apply(lambda s: s.split('-')[0].strip().upper())
crime.COUNTY = crime.COUNTY.apply(
    lambda c: (c.upper()
               .replace("COUNTY", "")
               .replace("POLICE DEPARTMENT", "")
               .strip())
)
crime.VIOLENT_CRIME = crime.VIOLENT_CRIME.apply(lambda n: int(n.replace(",", "")))
crime.PROPERTY_CRIME = crime.PROPERTY_CRIME.apply(lambda n: int(n.replace(",", "")))

bad = {
    "AUGUSTA-RICHMOND",
    "DE KALB",
    "LA PORTE6",
    "HARTSVILLE/TROUSDALE"
}
crime = crime.loc[~crime.COUNTY.isin(bad)]

counties = pd.read_csv("data/areas/counties.csv")
cty_fips = {}
for _, c in counties.iterrows():
    name = (c.NAME
            .replace("MUNICIPIO", "")
            .replace("COUNTY", "")
            .replace("PARISH", "")
            .strip())
    cty_fips[name] = c.FIPS_STATE, c.FIPS_COUNTY

exceptions = {
    "WESTCHESTER PUBLIC SAFETY": "WESTCHESTER",
    "SALT LAKE  UNIFIED": "SALT LAKE"
}
crime["FIPS_STATE"] = crime.COUNTY.apply(
    lambda c: cty_fips[exceptions.get(strip_digits(c), strip_digits(c))][0]
)
crime["FIPS_COUNTY"] = crime.COUNTY.apply(
    lambda c: cty_fips[exceptions.get(strip_digits(c), strip_digits(c))][1]
)

crime.to_csv(fout, index=False)
