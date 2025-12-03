import pandas as pd
import json

try:
    data = pd.read_csv("./largedata/data.csv")
    choices = {
        "restaurant_category": data.iloc[:, 0].unique().tolist(),
        "permit_status": data.iloc[:,-3].unique().tolist(),
        "violation_category": data.iloc[:,-1].unique().tolist()
    }
    with open("choices.json", "w") as f:
        json.dump(choices, f, indent=2)
    print("Choices saved to choices.json")
except Exception as e:
    print(f"Error: {e}")
