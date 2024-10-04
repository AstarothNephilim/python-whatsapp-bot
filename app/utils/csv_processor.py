import pandas as pd
import os
from pathlib import Path

data_folder = Path(__file__).parent.parent.parent / "data" 

adr_template = pd.DataFrame(columns=["R","SERIE","KG","D","VM","VMP","RM","P(W)","Perfil","Ejer.","Atleta","Ecuacion"])

print(adr_template)
for csv_file in data_folder.glob("*.csv"):
    adr_data = pd.read_csv(csv_file)
    adr_template = pd.concat([adr_template, adr_data], ignore_index=True)
    print(adr_template)
    print("FIN")