import os
import requests
import pandas as pd

var_id = 1724853
url = f"https://bdl.stat.gov.pl/api/v1/data/by-variable/{var_id}"
page = 0
all_records = []

while True:
    params = {
        "unit-level": 2,  # 2 - це рівень воєводств
        "page-size": 100,
        "page": page
    }
    response = requests.get(url, params=params)
    if response.status_code != 200:
        print(f"Error at page {page}: {response.status_code}")
        break
    
    data = response.json()
    results = data.get("results", [])
    if not results:
        break
        
    for unit in results:
        unit_id = unit.get("id")
        unit_name = unit.get("name")
        for v in unit.get("values", []):
            all_records.append({
                "wojewodztwo_id": unit_id,
                "wojewodztwo_name": unit_name,
                "year": v.get("year"),
                "expense_value": v.get("val")
            })
            
    print(f"Page processed: {page}")
    page += 1

if all_records:
    df = pd.DataFrame(all_records)
    os.makedirs("/Users/tempdelta/Desktop/ua_pl/expenses_data", exist_ok=True)
    df.to_csv("/Users/tempdelta/Desktop/ua_pl/expenses_data/wojewodztwa_expenses_care.csv", index=False)
    print(f"Saved {len(df)} rows to expenses_data/wojewodztwa_expenses_care.csv")