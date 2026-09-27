import numpy as np
import matplotlib.pyplot as plt
import os

# Configuración de estilo formal para tesis/artículo
plt.rcParams.update({
    'font.size': 11,
    'font.family': 'serif',
    'axes.labelsize': 12,
    'axes.titlesize': 13,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'legend.fontsize': 10,
    'figure.titlesize': 14,
    'mathtext.fontset': 'cm',
    'figure.autolayout': True
})

output_dir = os.path.dirname(os.path.abspath(__file__))

# -------------------------------------------------------------
# FIGURA 1: Distribución en 8 bits (Pesos y Activaciones ReLU)
# -------------------------------------------------------------
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8.5, 6.2), dpi=300)

# Subplot 1: Pesos sinápticos gaussianos
w = np.linspace(-1.2, 1.2, 1000)
sigma = 0.18
pdf = (1 / (sigma * np.sqrt(2 * np.pi))) * np.exp(-0.5 * (w / sigma) ** 2)

ax1.plot(w, pdf, 'b-', lw=2, label=r'Densidad de Pesos $\mathcal{N}(0, \sigma^2)$ (Adam + $L_2$)')
ax1.fill_between(w, pdf, color='blue', alpha=0.12)

# Mapeo ingenuo lineal
ax1.axvline(-1.15, color='gray', linestyle=':', label='Extremos de outliers (Mapeo Lineal Fijo)')
ax1.axvline(1.15, color='gray', linestyle=':')
ax1.annotate('Zona de colas vacías\n(Niveles INT8 desperdiciados)', xy=(0.85, 0.2), xytext=(0.65, 0.75),
             arrowprops=dict(arrowstyle='->', color='crimson', lw=1.2), color='crimson', fontsize=8.5, fontweight='bold')

# Mapeo simétrico INT8 adaptativo
ax1.axvspan(-3*sigma, 3*sigma, color='green', alpha=0.15, label=r'Soporte útil $[-3\sigma, +3\sigma]$ (99.73% datos)')
ax1.set_title(r'(a) Distribución de Pesos Sinápticos: Partición Lineal Fija vs. Cuantización Simétrica $S_w$')
ax1.set_xlabel('Valor del peso $W$')
ax1.set_ylabel('Densidad de probabilidad')
ax1.set_xlim([-1.2, 1.2])
ax1.set_ylim([-0.05, 2.5])
ax1.grid(True, linestyle='--', alpha=0.5)
ax1.legend(loc='upper left', framealpha=0.9)

# Subplot 2: Activaciones ReLU (asimetría no negativa)
a = np.linspace(-1.0, 4.0, 1000)
relu_pdf = np.zeros_like(a)
relu_pdf[a >= 0] = np.exp(-a[a >= 0] / 0.8) # Distribución exponencial típica
relu_pdf[a < 0] = 0

ax2.plot(a, relu_pdf, 'darkorange', lw=2, label=r'Activaciones post-ReLU ($a \geq 0$)')
ax2.fill_between(a[a >= 0], relu_pdf[a >= 0], color='orange', alpha=0.15)
ax2.axvspan(-1.0, 0.0, color='red', alpha=0.1, label='Semiplano negativo nulo (Desperdicio en Cuantización Simétrica)')

ax2.annotate(r'Punto cero móvil $Z_a = -128$' + '\n(Alinea $a=0$ con cota inferior)', xy=(0.0, 0.8), xytext=(-0.92, 0.65),
             arrowprops=dict(arrowstyle='->', color='darkgreen', lw=1.5), color='darkgreen', fontsize=8.5, fontweight='bold')
ax2.annotate(r'100% de los 256 niveles de INT8' + '\ndedicados al rango positivo $[0, a_{max}]$', xy=(1.5, 0.25), xytext=(1.8, 0.55),
             arrowprops=dict(arrowstyle='->', color='navy', lw=1.2), color='navy', fontsize=8.5)

ax2.set_title(r'(b) Activaciones ReLU: Cuantización Afín con Punto Cero Móvil ($Z_a$)')
ax2.set_xlabel('Valor de activación $a$')
ax2.set_ylabel('Densidad de activación')
ax2.set_xlim([-1.0, 4.0])
ax2.set_ylim([-0.05, 1.15])
ax2.grid(True, linestyle='--', alpha=0.5)
ax2.legend(loc='upper right', framealpha=0.9)

plt.tight_layout()
fig1_path = os.path.join(output_dir, 'distribucion_cuantizacion_int8.png')
plt.savefig(fig1_path, dpi=300)
plt.close()
print(f"✅ Generada Figura 1 refinada: {fig1_path}")


# -------------------------------------------------------------
# FIGURA 2: Perfil Polinomial Quíntico de Clase C^2
# -------------------------------------------------------------
T = 4.0 # Duración de 4 segundos
t = np.linspace(0, T, 1000)
tau_norm = t / T

q0, qf = 0.0, 1.5708 # Desplazamiento de 90 grados (pi/2)
delta_q = qf - q0

q = q0 + delta_q * (10 * tau_norm**3 - 15 * tau_norm**4 + 6 * tau_norm**5)
dq = (delta_q / T) * (30 * tau_norm**2 - 60 * tau_norm**3 + 30 * tau_norm**4)
ddq = (delta_q / (T**2)) * (60 * tau_norm - 180 * tau_norm**2 + 120 * tau_norm**3)

fig, (ax_pos, ax_vel, ax_acc) = plt.subplots(3, 1, figsize=(8.0, 6.5), sharex=True, dpi=300)

ax_pos.plot(t, q, 'b-', lw=2)
ax_pos.set_ylabel(r'Posición $q(t)$ [rad]')
ax_pos.set_title(r'Trayectoria Articular Suave Polinomial Quíntica de Clase $\mathcal{C}^2$')
ax_pos.grid(True, linestyle='--', alpha=0.5)

ax_vel.plot(t, dq, 'g-', lw=2)
ax_vel.set_ylabel(r'Velocidad $\dot{q}(t)$ [rad/s]')
ax_vel.axhline(0, color='black', lw=0.8, linestyle='--')
ax_vel.annotate(r'$\dot{q}(0) = \dot{q}(T) = 0$', xy=(3.8, 0.02), xytext=(2.6, 0.35),
                arrowprops=dict(arrowstyle='->', color='green', lw=1.2), color='green', fontsize=9)
ax_vel.grid(True, linestyle='--', alpha=0.5)

ax_acc.plot(t, ddq, 'crimson', lw=2)
ax_acc.set_ylabel(r'Aceleración $\ddot{q}(t)$ [rad/s$^2$]')
ax_acc.set_xlabel('Tiempo [s]')
ax_acc.axhline(0, color='black', lw=0.8, linestyle='--')
ax_acc.annotate(r'$\ddot{q}(0) = \ddot{q}(T) = 0$' + '\n(Continuidad estricta $C^2$)', xy=(0.2, 0.1), xytext=(0.4, 0.8),
                arrowprops=dict(arrowstyle='->', color='crimson', lw=1.2), color='crimson', fontsize=9)
ax_acc.grid(True, linestyle='--', alpha=0.5)

plt.tight_layout()
fig2_path = os.path.join(output_dir, 'perfil_quintico_c2.png')
plt.savefig(fig2_path, dpi=300)
plt.close()
print(f"✅ Generada Figura 2 refinada: {fig2_path}")


# -------------------------------------------------------------
# FIGURA 3: Presupuesto Temporal a 500 Hz (Timing Budget)
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(8.5, 3.8), dpi=300)

categories = ['Lazo 500 Hz']
t_read  = 10.2
t_rnea  = 151.2
t_norm  = 5.1
t_nn    = 29.2
t_des   = 8.4
t_write = 11.3

t_used = t_read + t_rnea + t_norm + t_nn + t_des + t_write # 215.4 us
t_free = 2000.0 - t_used                                   # 1784.6 us

# Barras apiladas
h = 0.42
ax.barh(categories, [t_read],  height=h, color='#2b5c8f', label=r'1. Lectura interfaces ($10.2\,\mu\mathrm{s}$)')
ax.barh(categories, [t_rnea],  height=h, left=[t_read], color='#34495e', label=r'2. Dinámica RNEA ($151.2\,\mu\mathrm{s}$)')
ax.barh(categories, [t_norm],  height=h, left=[t_read + t_rnea], color='#f39c12', label=r'3. Norm. $z$-score ($5.1\,\mu\mathrm{s}$)')
ax.barh(categories, [t_nn],    height=h, left=[t_read + t_rnea + t_norm], color='#27ae60', label=r'4. Inferencia INT8 ($29.2\,\mu\mathrm{s}$)')
ax.barh(categories, [t_des],   height=h, left=[t_read + t_rnea + t_norm + t_nn], color='#d35400', label=r'5. Desnorm. y clamp ($8.4\,\mu\mathrm{s}$)')
ax.barh(categories, [t_write], height=h, left=[t_read + t_rnea + t_norm + t_nn + t_des], color='#c0392b', label=r'6. Escritura esfuerzo ($11.3\,\mu\mathrm{s}$)')
ax.barh(categories, [t_free],  height=h, left=[t_used], color='#ecf0f1', edgecolor='#bdc3c7', hatch='//', label=r'Holgura libre ($1784.6\,\mu\mathrm{s} = 89.23\%$)')

ax.axvline(2000.0, color='red', linestyle='--', lw=1.5, label=r'Periodo admisible $T_s = 2000\,\mu\mathrm{s}$ (500 Hz)')

# Flecha indicadora para el tiempo ocupado
ax.annotate('Tiempo Total Ocupado: 215.4 $\mu$s (10.77%)',
            xy=(t_used / 2, 0.22), xytext=(280, 0.46),
            arrowprops=dict(arrowstyle='->', color='navy', lw=1.3),
            color='navy', fontsize=9.5, fontweight='bold')

# Texto centrado en la holgura libre
ax.text(1100, 0, 'Holgura libre de seguridad: 89.23% (1784.6 $\mu$s)',
        ha='center', va='center', color='#2c3e50', fontweight='bold', fontsize=9.5)

ax.set_xlim([0, 2200])
ax.set_ylim([-0.35, 0.65])
ax.set_xlabel(r'Tiempo transcurrido en el ciclo de control $[\mu\mathrm{s}]$')
ax.set_title(r'Presupuesto Temporal Consolidado del Ciclo Crítico en Tiempo Real (500 Hz)')
ax.legend(loc='lower center', bbox_to_anchor=(0.5, -0.68), ncol=3, framealpha=0.9, fontsize=8.2)
ax.get_yaxis().set_visible(False)
ax.grid(axis='x', linestyle='--', alpha=0.5)

plt.tight_layout()
fig3_path = os.path.join(output_dir, 'timing_budget_500hz.png')
plt.savefig(fig3_path, dpi=300, bbox_inches='tight')
plt.close()
print(f"✅ Generada Figura 3 calibrada: {fig3_path}")
