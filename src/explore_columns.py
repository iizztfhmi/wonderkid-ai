import pandas as pd

print("=" * 60)
print("WonderKid AI - Explore Dataset Columns")
print("=" * 60)

# Load dataset
df = pd.read_csv("data/processed/wonderkid_dataset.csv")

print(f"\nRows    : {df.shape[0]}")
print(f"Columns : {df.shape[1]}")

print("\n" + "=" * 60)
print("ALL COLUMN NAMES")
print("=" * 60)

for i, column in enumerate(df.columns, start=1):
    print(f"{i:3}. {column}")

print("\n" + "=" * 60)
print("NUMERIC COLUMNS")
print("=" * 60)

numeric_columns = df.select_dtypes(include="number").columns

for i, column in enumerate(numeric_columns, start=1):
    print(f"{i:3}. {column}")

print("\n" + "=" * 60)
print("USEFUL SEARCH")
print("=" * 60)

keywords = [
    "Gls",
    "Ast",
    "xG",
    "xAG",
    "Sh",
    "SoT",
    "Prg",
    "KP",
    "Cmp",
    "Pass",
    "Tkl",
    "Int",
    "Clr",
    "Blocks",
    "Won",
    "Succ",
    "SCA",
    "GCA",
    "Carr",
    "Touch",
    "Cross",
    "Rec",
]

for keyword in keywords:
    print(f"\n[{keyword}]")

    found = False

    for column in df.columns:
        if keyword.lower() in column.lower():
            print("  ", column)
            found = True

    if not found:
        print("   None")