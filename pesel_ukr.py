import os
import requests
import re

dataset_id = 2715
res_url = f"https://api.dane.gov.pl/1.4/datasets/{dataset_id}/resources?sort=-data_date&per_page=100"

response = requests.get(res_url)
if response.status_code == 200:
    resources = response.json().get("data", [])
    
    os.makedirs("pesel_ukr_data/annual_slices", exist_ok=True)
    
    # Вибираємо по одному файлу на кожен рік (найпізніший звіт у році)
    selected_files = {}
    for r in resources:
        title = r["attributes"]["title"]
        match = re.search(r"(\d{2}\.\d{2}\.)(\d{4})", title)
        if match and "powiat" in r["attributes"]["file_url"].lower():
            year = match.group(2)
            if year not in selected_files:
                selected_files[year] = r["attributes"]["file_url"]
                print(f"Обрано для {year}: {title}")

    # Завантаження
    for year, url in selected_files.items():
        output_path = f"pesel_ukr_data/annual_slices/pesel_{year}.xlsx"
        print(f"Завантаження {year}...")
        file_response = requests.get(url)
        with open(output_path, "wb") as f:
            f.write(file_response.content)
            
    print("Готово. Річні звіти збережено в папці 'annual_slices'.")