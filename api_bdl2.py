import requests

url = "https://bdl.stat.gov.pl/api/v1/variables/search"
params = {
    "name": "ludność ogółem stan w dniu 31 xii",
    "page-size": 100
}
response = requests.get(url, params=params)
if response.status_code == 200:
    for item in response.json().get("results", []):
        if item.get("level") == 6:
            parts = []
            for i in range(1, 6):
                part = item.get(f"n{i}")
                if part:
                    parts.append(str(part))
            full_name = " // ".join(parts)
            print(f"ID: {item}")
else:
    print(response.status_code)