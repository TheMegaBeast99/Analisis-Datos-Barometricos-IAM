import pandas as pd
import numpy  as np

# --- Procesamiento de la tabla ---
df = pd.read_csv("DatosIAM1al8-sep26-capturados18sep26.txt", skiprows=3, sep=r'\s+', header=None)
time = pd.date_range("07:00", "09:00", freq="10min").strftime("%I:%M%p").str.lower().str.replace(" ", "").str.lstrip("0").str.replace("m", "")

# Presión atmosférica
bar = df[df[1].isin(time)][16].astype(float)
meanBar = bar.mean() # hPa
errBar = bar.sem()   # Corregido: 'bar' en lugar de 'data'

# Temperatura exterior
temp = pd.to_numeric(df[df[1].isin(time)][2], errors='coerce')
meanTemp = temp.mean()
errTemp = temp.sem()

# --- Cálculo de la densidad ---
def density(meanTemp, errTemp, meanBar, errBar, sdt_mg_L = 250.0):
    # Constantes oficiales de la ecuación de Tanaka (para 1013.25 hPa)
    a1 = 999.97495    # kg/m³
    a2 = 3.983035     # °C
    a3 = 301.797      # °C
    a4 = 522528.9     # °C²
    a5 = 69.34881     # °C
    P_std = 1013.25   # hPa

    beta = 4.5e-9

    def rho_tanaka(T):
        return a1 * (1.0 - ((T - a2)**2 * (T + a3) / (a4 * (T + a5))))

    siapaFactor = sdt_mg_L / 1000.0
    rho_T = rho_tanaka(meanTemp)
    
    meanDensity = (rho_T * (1.0 - beta * (P_std - meanBar))) + siapaFactor
    h = 1e-5

    d_rho_dT = (rho_tanaka(meanTemp + h) * (1.0 - beta * (P_std - meanBar)) - 
                rho_tanaka(meanTemp - h) * (1.0 - beta * (P_std - meanBar))) / (2 * h)
                
    d_rho_dP = (rho_T * (1.0 - beta * (P_std - (meanBar + h))) - 
                rho_T * (1.0 - beta * (P_std - (meanBar - h)))) / (2 * h)

    # Corregido: 'errBar' en lugar de 'err'
    densidad_error = np.sqrt((d_rho_dT * errTemp)**2 + (d_rho_dP * errBar)**2)

    return meanDensity, densidad_error

# Corregido: argumentos pasados a la función (meanBar, errBar)
rho, rho_err = density(meanTemp, errTemp, meanBar, errBar)

print("=== RESULTADOS DE LOS CÁLCULOS ===")
print(f"Presión atomosférica: ({meanBar:.3f} ± {errBar:.3f}) kg/m³")
print(f"Temperatura: ({meanTemp:.3f} ± {errTemp:.3f}) kg/m³")
print(f"Densidad: ({rho:.3f} ± {rho_err:.3f}) kg/m³")
