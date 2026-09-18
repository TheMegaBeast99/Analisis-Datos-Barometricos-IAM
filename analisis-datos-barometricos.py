import pandas as pd
df = pd.read_csv("DatosIAM1al8-sep26-capturados18sep26.txt", skiprows=3, sep=r'\s+', header=None)
time = pd.date_range("07:00", "09:00", freq="10min").strftime("%I:%M%p").str.lower().str.replace(" ", "").str.lstrip("0").str.replace("m", "")
data = df[df[1].isin(time)][16].astype(float)
mean = data.mean()
err = data.sem()
print(f'Mean: {mean} +- {err}')