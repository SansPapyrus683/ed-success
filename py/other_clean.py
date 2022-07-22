import os
import pathlib
import pandas as pd

# make sure we in the project directory
os.chdir(pathlib.Path(__file__).parent.parent.absolute())
print(os.getcwd())

fin = "data/other/other17raw.csv"
fout = "data/other/other17.csv"

counties = pd.read_csv(fin)
counties.columns = [c.upper().replace(" ", "_") for c in counties.columns]
WANT = [
    "STATE",
    "NAME",
    "FIPS",
    "POP2017",
    "HOUSEHOLDS_2017",
    "PER_CAPITA_INCOME_2017",
    "MEDIAN_AGE_2017",
    "WHITE_NOT_HISPANIC_2017",
    "BLACK_2017",
    "ASIAN_2017",
    "HISPANIC_2017",
    "HS_GRAD_2017",
    "SOME_COLLEGE_2017",
    "BACHELORS_2017",
    "COMPUTER_2017",
    "POVERTY_2017",
    "UNINSURED_2017",
    "UNEMPLOYMENT_RATE_2017"
]
counties = counties[WANT].dropna()
counties.STATE = counties.STATE.apply(lambda s: s.upper())
counties.NAME = counties.NAME.apply(
    lambda c: (c.upper()
               .replace("COUNTY", "")
               .strip())
)
counties.rename({"STATE": "COUNTY"})

counties.to_csv(fout, index=False)
