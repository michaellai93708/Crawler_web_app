import os
import pandas as pd
from pathlib import Path
excel_dir = Path("/Users/michael/Downloads")
excel_files = excel_dir.glob('*.xls')
df = pd.DataFrame()
for xls in excel_files:
      data = pd.read_excel(xls)
      df = df.append(data)
      os.remove(xls)
df.to_excel(excel_dir / "smart_city/output.xlsx", index = False)