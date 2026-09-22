import numpy as np
import matplotlib.pyplot as plt

from uncertainties import ufloat
from uncertainties.umath import sqrt

from scipy import odr


# ============================================================
# Datos experimentales
# ============================================================

data = np.genfromtxt(
    'data/datos_experimentales.csv',
    delimiter=',',
    names=True
)

h_raw = data['h_raw_cm']
H_raw = data['H_raw_cm']
h_err = data['u_h_cm']
H_err = data['u_H_cm']
H_raw *= 2
H_err *= 2

# Conversión a ufloat
data = np.array([
    [ufloat(h, uh), ufloat(H, uH)]
    for h, H, uh, uH in zip(h_raw, H_raw, h_err, H_err)
], dtype=object)

data0 = np.array([
    ufloat(x, dx)
    for x, dx in zip(
        [9.15, 2*3.65],
        [0.05, 0.10]
    )
], dtype=object)


# ============================================================
# Constantes y dimensiones
# ============================================================

atm = ufloat(844.8529411764705, 0.10914953242129191)  # hPa
rho = ufloat(998.929, 0.018)  # kg/m³

g = 9.78197801  # m/s²

d_T = ufloat(0.65, 0.05)  # cm
d_M = ufloat(0.50, 0.05)  # cm
L_M = ufloat(33, 0.05)  # cm
L_T0 = ufloat(90, 0.05)  # cm
DL = ufloat(0.85, 0.05)  # cm

L_T = L_T0 - DL
Data = data - data0


# ============================================================
# Modelo teórico
# ============================================================

def TeoricalHeight(h):
    h_meter = h / 100
    L_T_meter = L_T / 100
    L_M_meter = L_M / 100
    d_T_meter = d_T / 100
    d_M_meter = d_M / 100
    atm_Pa = atm * 100

    V_0 = (
        np.pi / 4 * d_T_meter**2 * L_T_meter
        + np.pi / 4 * d_M_meter**2 * L_M_meter
    )

    A = np.pi / 8 * (
        2 * d_T_meter**2 + d_M_meter**2
    )

    B = np.pi / 4 * d_T_meter**2 * h_meter

    a = A * rho * g
    b = A * atm_Pa + (V_0 - B) * rho * g
    c = -B * atm_Pa

    discriminante = b**2 - 4 * a * c

    delta_h_meter = (
        -b + sqrt(discriminante)
    ) / (2 * a)

    return delta_h_meter * 100


def HidrostaticPressure(H):
    return rho * g * H / 100


def TeoricalHidrostaticPreasure(h):
    return HidrostaticPressure(
        TeoricalHeight(h)
    )

# ============================================================
# Presión experimental y modelo teórico
# ============================================================

P_exp = np.array([
    HidrostaticPressure(H) / 100
    for H in H_exp
], dtype=object)

H_teo = np.array([
    TeoricalHeight(h)
    for h in h_exp
], dtype=object)

P_teo = np.array([
    TeoricalHidrostaticPreasure(h) / 100
    for h in h_exp
], dtype=object)


# Valores nominales e incertidumbres

P_exp_val = np.array([x.n for x in P_exp])
P_exp_err = np.array([x.s for x in P_exp])

H_teo_val = np.array([x.n for x in H_teo])
H_teo_err = np.array([x.s for x in H_teo])

P_teo_val = np.array([x.n for x in P_teo])
P_teo_err = np.array([x.s for x in P_teo])


# ============================================================
# Ajuste ODR: H = m*h + b
# ============================================================

def funcion_lineal(B, x):
    return B[0] * x + B[1]


modelo_lineal = odr.Model(funcion_lineal)

datos_odr = odr.RealData(
    h_exp_val,
    H_exp_val,
    sx=h_exp_err,
    sy=H_exp_err
)

odr_run = odr.ODR(
    datos_odr,
    modelo_lineal,
    beta0=[1.0, 0.0]
)

res_odr = odr_run.run()

m_fit, b_fit = res_odr.beta
m_err_fit, b_err_fit = res_odr.sd_beta

print("\n=== REGRESIÓN ODR DE H vs h ===")
print(
    f"H = ({m_fit:.5f} ± {m_err_fit:.5f})h "
    f"+ ({b_fit:.5f} ± {b_err_fit:.5f}) cm"
)

print(
    f"(χ²_red): "
    f"{res_odr.res_var:.5f}"
)


# Recta de ajuste

h_fit = np.linspace(
    min(h_exp_val),
    max(h_exp_val),
    300
)

H_fit = m_fit * h_fit + b_fit


# ============================================================
# Configuración general de gráficas
# ============================================================

plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['font.family'] = 'serif'


# ============================================================
# Gráfica: ΔP vs h
# ============================================================

fig, ax = plt.subplots(figsize=(8, 6))

ax.errorbar(
    h_exp_val,
    P_exp_val,
    xerr=h_exp_err,
    yerr=P_exp_err,
    color='#c0392b',
    marker='o',
    markersize=3,
    markerfacecolor='#e74c3c',
    markeredgewidth=1.5,
    linewidth=1,
    linestyle='None',
    capsize=3,
    capthick=1.2,
    label='Presión experimental'
)

orden = np.argsort(h_exp_val)

h_plot = h_exp_val[orden]
P_plot = P_teo_val[orden]
P_err_plot = P_teo_err[orden]

ax.plot(
    h_plot,
    P_plot,
    color='#2980b9',
    linewidth=1.5,
    label='Modelo teórico'
)

ax.fill_between(
    h_plot,
    P_plot - P_err_plot,
    P_plot + P_err_plot,
    color='#3498db',
    alpha=0.20,
    label='Incertidumbre del modelo'
)

ax.grid(
    which='major',
    linestyle='-',
    linewidth=0.8,
    color='#dcdcdc'
)

ax.grid(
    which='minor',
    linestyle=':',
    linewidth=0.5,
    color='#eeeeee'
)

ax.minorticks_on()

ax.set_xlabel(
    r"Profundidad de la manguera $h$ (cm)",
    fontsize=12
)

ax.set_ylabel(
    r"Presión manométrica $\Delta P$ (hPa)",
    fontsize=12
)

ax.set_xlim(0, 31)
ax.set_ylim(0, 22)

ax.legend()

plt.tight_layout()

plt.savefig(
    'grafica_presion_vs_profundidad.pdf',
    format='pdf',
    bbox_inches='tight',
    dpi=300
)

plt.show()


# ============================================================
# Gráfica: H vs h
# ============================================================

fig, ax = plt.subplots(figsize=(8, 6))

ax.errorbar(
    h_exp_val,
    H_exp_val,
    xerr=h_exp_err,
    yerr=H_exp_err,
    color='#c0392b',
    marker='o',
    markersize=3,
    markerfacecolor='#e74c3c',
    markeredgewidth=1.5,
    linewidth=1,
    linestyle='None',
    capsize=3,
    capthick=1.2,
    label='Datos experimentales'
)

ax.plot(
    h_plot,
    H_teo_val[orden],
    color='#2980b9',
    linewidth=1.5,
    label='Modelo teórico'
)

ax.fill_between(
    h_plot,
    H_teo_val[orden] - H_teo_err[orden],
    H_teo_val[orden] + H_teo_err[orden],
    color='#3498db',
    alpha=0.20,
    label='Incertidumbre del modelo'
)

ax.plot(
    h_fit,
    H_fit,
    color='#2c3e50',
    linewidth=1.5,
    linestyle='--',
    label='Ajuste ODR'
)

ax.grid(
    which='major',
    linestyle='-',
    linewidth=0.8,
    color='#dcdcdc'
)

ax.grid(
    which='minor',
    linestyle=':',
    linewidth=0.5,
    color='#eeeeee'
)

ax.minorticks_on()

ax.set_xlabel(
    r"Profundidad de la manguera $h$ (cm)",
    fontsize=12
)

ax.set_ylabel(
    r"Altura de columna manométrica $H(h)$ (cm)",
    fontsize=12
)

ax.set_xlim(0, 31)
ax.set_ylim(0, 31)

ax.legend()

plt.tight_layout()

plt.savefig(
    'grafica_altura_manometrica.pdf',
    format='pdf',
    bbox_inches='tight',
    dpi=300
)

plt.show()
