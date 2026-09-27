import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.gridspec import GridSpec
import os

os.environ['MPLCONFIGDIR'] = '/tmp/mpl'

plt.rcParams.update({
    'font.size': 10,
    'font.family': 'serif',
    'axes.labelsize': 11,
    'axes.titlesize': 12,
    'xtick.labelsize': 9,
    'ytick.labelsize': 9,
    'legend.fontsize': 9,
    'mathtext.fontset': 'cm',
    'figure.autolayout': False
})

output_dir = os.path.dirname(os.path.abspath(__file__))
fig_path = os.path.join(output_dir, 'arquitectura_red_cuantizada.png')

fig = plt.figure(figsize=(14.0, 11.2), dpi=300)

# Layout con GridSpec jerárquico
gs_main = GridSpec(3, 1, height_ratios=[1.35, 0.40, 0.95], hspace=0.35,
                   left=0.05, right=0.95, top=0.95, bottom=0.04)

# =============================================================================
# 1. PARTE SUPERIOR: TOPOLOGÍA DE LA RED NEURONAL (42 - 256 - 512 - 256 - 128 - 6)
# =============================================================================
ax_net = fig.add_subplot(gs_main[0])
ax_net.set_title(r'(a) Topología y Arquitectura de Capas de la Red Neuronal UR3eNetwork (42 $\rightarrow$ 256 $\rightarrow$ 512 $\rightarrow$ 256 $\rightarrow$ 128 $\rightarrow$ 6)',
                 fontsize=13, fontweight='bold', pad=18)
ax_net.set_xlim(-0.03, 1.03)
ax_net.set_ylim(-0.32, 1.18)
ax_net.axis('off')

layers = [
    {
        'name': 'Capa Entrada',
        'sub': '42 variables físicas\n(7 grupos cinemáticos)',
        'nodes': 6,
        'color': '#2b6cb0',
        'edge': '#1a365d',
        'act': 'Normalización z-score'
    },
    {
        'name': 'Capa Oculta 1',
        'sub': '256 neuronas\n(10,752 pesos)',
        'nodes': 7,
        'color': '#319795',
        'edge': '#234e52',
        'act': r'LeakyReLU ($\alpha=0.01$)'
    },
    {
        'name': 'Capa Oculta 2',
        'sub': '512 neuronas\n(131,072 pesos)',
        'nodes': 9,
        'color': '#38a169',
        'edge': '#1c4532',
        'act': r'LeakyReLU ($\alpha=0.01$)'
    },
    {
        'name': 'Capa Oculta 3',
        'sub': '256 neuronas\n(131,072 pesos)',
        'nodes': 7,
        'color': '#d69e2e',
        'edge': '#744210',
        'act': r'LeakyReLU ($\alpha=0.01$)'
    },
    {
        'name': 'Capa Oculta 4',
        'sub': '128 neuronas\n(32,768 pesos)',
        'nodes': 5,
        'color': '#dd6b20',
        'edge': '#7b341e',
        'act': r'LeakyReLU ($\alpha=0.01$)'
    },
    {
        'name': 'Capa Salida',
        'sub': '6 neuronas lineales\nPares de esfuerzo',
        'nodes': 6,
        'color': '#e53e3e',
        'edge': '#742a2a',
        'act': r'Lineal (N$\cdot$m)'
    }
]

n_layers = len(layers)
x_coords = np.linspace(0.06, 0.94, n_layers)

# Calcular posiciones y dibujar líneas
node_positions = []
for i, layer in enumerate(layers):
    n_pts = layer['nodes']
    y_pts = np.linspace(0.08, 0.82, n_pts)
    node_positions.append(y_pts)

# Líneas sinápticas
for i in range(n_layers - 1):
    x1, x2 = x_coords[i], x_coords[i+1]
    y1_list, y2_list = node_positions[i], node_positions[i+1]
    for y1 in y1_list:
        for y2 in y2_list:
            ax_net.plot([x1, x2], [y1, y2], color='#cbd5e0', lw=0.45, alpha=0.55, zorder=1)

# Nombres de matrices de pesos
weight_labels = [
    r'$\mathbf{W}_1 \in \mathbb{R}^{256 \times 42}$',
    r'$\mathbf{W}_2 \in \mathbb{R}^{512 \times 256}$',
    r'$\mathbf{W}_3 \in \mathbb{R}^{256 \times 512}$',
    r'$\mathbf{W}_4 \in \mathbb{R}^{128 \times 256}$',
    r'$\mathbf{W}_5 \in \mathbb{R}^{6 \times 128}$'
]
for i in range(n_layers - 1):
    xm = 0.5 * (x_coords[i] + x_coords[i+1])
    ax_net.text(xm, -0.06, weight_labels[i], ha='center', va='center',
                fontsize=8.8, style='italic', color='#1a365d',
                bbox=dict(boxstyle='round,pad=0.25', facecolor='#ebf8ff', edgecolor='#90cdf4', lw=0.8, zorder=2))

# Dibujar nodos usando scatter para círculos perfectos
node_scatter_size = 480
for i, layer in enumerate(layers):
    xc = x_coords[i]
    y_pts = node_positions[i]
    n_pts = len(y_pts)
    
    # Nodos
    for j, yc in enumerate(y_pts):
        if n_pts >= 7 and j == n_pts // 2:
            ax_net.scatter(xc, yc, s=node_scatter_size, color='#ffffff', edgecolors=layer['edge'], lw=1.5, zorder=3)
            ax_net.text(xc, yc, r'$\vdots$', ha='center', va='center', fontsize=12, fontweight='bold', color=layer['edge'], zorder=4)
        else:
            ax_net.scatter(xc, yc, s=node_scatter_size, color=layer['color'], edgecolors=layer['edge'], lw=1.5, zorder=3)
            if i == 0:
                labels_in = [r'$q_1$', r'$q_6$', r'$\dot{q}$', r'$\ddot{q}$', r'$q_d$', r'$\tau_R$']
                lbl = labels_in[j] if j < len(labels_in) else ''
                ax_net.text(xc, yc, lbl, ha='center', va='center', fontsize=7.2, color='#ffffff', fontweight='bold', zorder=4)
            elif i == n_layers - 1:
                ax_net.text(xc, yc, rf'$\tau_{j+1}$', ha='center', va='center', fontsize=7.5, color='#ffffff', fontweight='bold', zorder=4)

    # Texto encabezado
    ax_net.text(xc, 1.06, layer['name'], ha='center', va='center', fontsize=10.2, fontweight='bold', color=layer['edge'])
    ax_net.text(xc, 0.95, layer['sub'], ha='center', va='center', fontsize=8.2, color='#2d3748', linespacing=1.2)
    
    # Etiqueta activación
    ax_net.text(xc, -0.19, layer['act'], ha='center', va='center', fontsize=8.2,
                bbox=dict(boxstyle='square,pad=0.25', facecolor='#edf2f7', edgecolor='#cbd5e0', lw=0.6))

# Corchete o desglose de entrada a la izquierda
in_desc = (
    r"$\mathbf{x} \in \mathbb{R}^{42}:$" + "\n"
    r"• Posiciones actuales $\mathbf{q} \in \mathbb{R}^6$" + "\n"
    r"• Velocidades actuales $\dot{\mathbf{q}} \in \mathbb{R}^6$" + "\n"
    r"• Aceleraciones actuales $\ddot{\mathbf{q}}_{act} = \mathbf{0} \in \mathbb{R}^6$" + "\n"
    r"• Posiciones deseadas $\mathbf{q}_d \in \mathbb{R}^6$" + "\n"
    r"• Velocidades deseadas $\dot{\mathbf{q}}_d \in \mathbb{R}^6$" + "\n"
    r"• Aceleraciones deseadas $\ddot{\mathbf{q}}_d \in \mathbb{R}^6$" + "\n"
    r"• Pares analíticos $\bm{\tau}_{RNEA} \in \mathbb{R}^6$"
)
# Reemplazar \bm por \mathbf para matplotlib
in_desc = in_desc.replace(r'\bm{', r'\mathbf{')
ax_net.text(x_coords[0] - 0.055, 0.45, in_desc, ha='right', va='center', fontsize=7.8, color='#1a365d',
            bbox=dict(boxstyle='round,pad=0.35', facecolor='#f7fafc', edgecolor='#cbd5e0', lw=0.8))

# Desglose de salida a la derecha
out_desc = (
    r"$\mathbf{y} \in \mathbb{R}^6:$" + "\n"
    r"• $\tau_1$: Base" + "\n"
    r"• $\tau_2$: Hombro" + "\n"
    r"• $\tau_3$: Codo" + "\n"
    r"• $\tau_4$: Muñeca 1" + "\n"
    r"• $\tau_5$: Muñeca 2" + "\n"
    r"• $\tau_6$: Muñeca 3" + "\n"
    r"(Saturación $\pm 55\ \mathrm{N}\cdot\mathrm{m}$)"
)
ax_net.text(x_coords[-1] + 0.055, 0.45, out_desc, ha='left', va='center', fontsize=7.8, color='#742a2a',
            bbox=dict(boxstyle='round,pad=0.35', facecolor='#fff5f5', edgecolor='#feb2b2', lw=0.8))

# Banner inferior de parámetros
ax_net.text(0.5, -0.28, r'Total de parámetros entrenables: $306,432$ pesos sinápticos + $1,158$ sesgos $\approx 307{,}590$ parámetros',
            ha='center', va='center', fontsize=9.8, fontweight='bold', color='#1a202c',
            bbox=dict(boxstyle='round,pad=0.35', facecolor='#edf2f7', edgecolor='#a0aec0', lw=1.0))


# =============================================================================
# 2. FILA MEDIA: DIAGRAMA DE FORMATO DE BITS (FP32 vs INT8)
# =============================================================================
gs_mid = gs_main[1].subgridspec(1, 2, wspace=0.18)

# --- Subpanel Mid-Left: Registro FP32 ---
ax_mid_fp = fig.add_subplot(gs_mid[0, 0])
ax_mid_fp.set_title(r'(b1) Registro FP32: Precisión Simple IEEE 754 (32 bits = 4 bytes / peso)',
                    fontsize=10.2, fontweight='bold', color='#1a365d', pad=8)
ax_mid_fp.set_xlim(0, 1)
ax_mid_fp.set_ylim(0, 1)
ax_mid_fp.axis('off')

# Dibujar las 3 cajas de bits
# Signo 1b
rect_s = patches.Rectangle((0.02, 0.38), 0.10, 0.38, facecolor='#e53e3e', edgecolor='#1a365d', lw=1.2)
ax_mid_fp.add_patch(rect_s)
ax_mid_fp.text(0.07, 0.57, 'Signo\n1 bit', ha='center', va='center', fontsize=7.5, color='white', fontweight='bold')

# Exponente 8b
rect_e = patches.Rectangle((0.13, 0.38), 0.30, 0.38, facecolor='#3182ce', edgecolor='#1a365d', lw=1.2)
ax_mid_fp.add_patch(rect_e)
ax_mid_fp.text(0.28, 0.57, r'Exponente sesgado' + '\n' + r'8 bits ($e \in [0, 255]$)', ha='center', va='center', fontsize=7.5, color='white', fontweight='bold')

# Mantisa 23b
rect_m = patches.Rectangle((0.44, 0.38), 0.54, 0.38, facecolor='#2b6cb0', edgecolor='#1a365d', lw=1.2)
ax_mid_fp.add_patch(rect_m)
ax_mid_fp.text(0.71, 0.57, r'Mantisa / Fracción normalizada' + '\n' + r'23 bits ($m = 1.f_{22}f_{21}\dots f_0$)', ha='center', va='center', fontsize=7.5, color='white', fontweight='bold')

# Ecuación matemática
ax_mid_fp.text(0.5, 0.12, r'$v = (-1)^s \times 2^{e-127} \times (1 + m) \in \mathbb{R}$' + '   ' + r'[Rango dinámico: $\sim \pm 3.4 \times 10^{38}$]',
               ha='center', va='center', fontsize=8.2, style='italic', color='#1a365d')


# --- Subpanel Mid-Right: Registro INT8 ---
ax_mid_int = fig.add_subplot(gs_mid[0, 1])
ax_mid_int.set_title(r'(c1) Registro INT8: Cuantización Entera Afín QInt8 (8 bits = 1 byte / peso)',
                     fontsize=10.2, fontweight='bold', color='#1c4532', pad=8)
ax_mid_int.set_xlim(0, 1)
ax_mid_int.set_ylim(0, 1)
ax_mid_int.axis('off')

# Signo 1b
rect_is = patches.Rectangle((0.15, 0.38), 0.14, 0.38, facecolor='#e53e3e', edgecolor='#1c4532', lw=1.2)
ax_mid_int.add_patch(rect_is)
ax_mid_int.text(0.22, 0.57, 'Signo\n1 bit', ha='center', va='center', fontsize=7.5, color='white', fontweight='bold')

# Entero 7b
rect_im = patches.Rectangle((0.30, 0.38), 0.55, 0.38, facecolor='#38a169', edgecolor='#1c4532', lw=1.2)
ax_mid_int.add_patch(rect_im)
ax_mid_int.text(0.575, 0.57, 'Magnitud Entera en Complemento a 2 (7 bits)\n' + r'$q \in \{-128, -127, \dots, 0, \dots, +127\}$ (256 estados)',
                ha='center', va='center', fontsize=7.5, color='white', fontweight='bold')

# Ecuación matemática
ax_mid_int.text(0.5, 0.12, r'$v \approx S_w \times (q - Z_w), \quad S_w = \frac{\max(|W|)}{127}, \ Z_w = 0$' + '   ' + r'[Compresión: $4\times$ palabra]',
                ha='center', va='center', fontsize=8.2, style='italic', color='#1c4532')


# =============================================================================
# 3. FILA INFERIOR: RESOLUCIÓN PERCEPTUAL Y CUADRO DE RENDIMIENTO
# =============================================================================
gs_bot = gs_main[2].subgridspec(1, 2, wspace=0.18)

# --- Subpanel Bot-Left: Gráfica continua y métricas FP32 ---
ax_bot_fp = fig.add_subplot(gs_bot[0, 0])
ax_bot_fp.set_title(r'(b2) Comportamiento Continuo FP32 y Métricas Experimentales',
                    fontsize=10.2, fontweight='bold', color='#1a365d', pad=8)

# Dividir internamente en gráfica y tarjeta
# Gráfica
t = np.linspace(0, 2*np.pi, 400)
y_cont = np.sin(t) * np.exp(-0.15*t)
ax_bot_fp.plot(t, y_cont, color='#2b6cb0', lw=2.4, label='Función continua analógica (FP32)')
ax_bot_fp.fill_between(t, y_cont, color='#bee3f8', alpha=0.35)
ax_bot_fp.set_xlim(0, 2*np.pi)
ax_bot_fp.set_ylim(-1.15, 1.15)
ax_bot_fp.set_ylabel('Amplitud normalizada', fontsize=8.5)
ax_bot_fp.set_xlabel('Tiempo de ciclo / Fase articular', fontsize=8.5)
ax_bot_fp.grid(True, linestyle=':', alpha=0.5)
ax_bot_fp.legend(loc='upper right', fontsize=8.0, framealpha=0.9)

# Anotación perceptual
ax_bot_fp.text(np.pi, 0.65, 'Gradiente suave y continuo\nSin ruido de discretización',
               ha='center', va='center', fontsize=7.8, style='italic', color='#2b6cb0',
               bbox=dict(boxstyle='round,pad=0.2', facecolor='white', edgecolor='#bee3f8', alpha=0.9))

# Cuadro de métricas en la base del gráfico (fuera de los datos)
card_fp_text = (
    "Métricas Reales (Controlador C++ a 500 Hz):\n"
    "• Almacenamiento modelo: 1232.0 KB (1.20 MB - Base)\n"
    "• Latencia inferencia C++: 37.1 us (WCET 42.0 us)\n"
    "• Error dinámico seguimiento: RMSE = 0.092 rad (5.27 deg)\n"
    "• Ejecución: Unidades FPU / Registros AVX2 de 32 bits"
)
ax_bot_fp.text(0.03, 0.05, card_fp_text, transform=ax_bot_fp.transAxes,
               fontsize=7.8, family='monospace', color='#1a365d',
               bbox=dict(boxstyle='round,pad=0.35', facecolor='#ebf8ff', edgecolor='#90cdf4', lw=1.0, alpha=0.95))


# --- Subpanel Bot-Right: Gráfica escalonada y métricas INT8 ---
ax_bot_int = fig.add_subplot(gs_bot[0, 1])
ax_bot_int.set_title(r'(c2) Comportamiento Discreto INT8 y Métricas Experimentales',
                     fontsize=10.2, fontweight='bold', color='#1c4532', pad=8)

# Gráfica discretizada (escalonada)
# Simular cuantización a 12 niveles para visualización clara
n_levels = 12
y_disc = np.round(y_cont * (n_levels / 2)) / (n_levels / 2)
ax_bot_int.step(t, y_disc, color='#38a169', lw=2.2, where='mid', label='Señal discretizada afín (INT8)')
ax_bot_int.plot(t, y_cont, color='#718096', lw=1.0, linestyle='--', alpha=0.6, label='Envolvente FP32 de referencia')
ax_bot_int.fill_between(t, y_disc, color='#c6f6d5', alpha=0.35, step='mid')
ax_bot_int.set_xlim(0, 2*np.pi)
ax_bot_int.set_ylim(-1.15, 1.15)
ax_bot_int.set_ylabel('Amplitud cuantizada', fontsize=8.5)
ax_bot_int.set_xlabel('Tiempo de ciclo / Fase articular', fontsize=8.5)
ax_bot_int.grid(True, linestyle=':', alpha=0.5)
ax_bot_int.legend(loc='upper right', fontsize=8.0, framealpha=0.9)

# Anotación de paso de discretización
ax_bot_int.text(np.pi, 0.65, r'Malla discreta de 256 niveles' + '\n' + r'Paso $\Delta = S_w$ (Aproximación por redondeo)',
                ha='center', va='center', fontsize=7.8, style='italic', color='#1c4532',
                bbox=dict(boxstyle='round,pad=0.2', facecolor='white', edgecolor='#c6f6d5', alpha=0.9))

# Cuadro de métricas INT8
card_int_text = (
    "Métricas Reales (Controlador C++ a 500 Hz):\n"
    "• Almacenamiento modelo: 315.0 KB (-74.43% de reducción)\n"
    "• Latencia inferencia C++: 29.2 us (-21.29% de aceleración)\n"
    "• Error dinámico seguimiento: RMSE = 0.138 rad (7.91 deg)\n"
    "• Ejecución: Aritmética entera ALU / Co-procesador DSP48E"
)
ax_bot_int.text(0.03, 0.05, card_int_text, transform=ax_bot_int.transAxes,
                fontsize=7.8, family='monospace', color='#1c4532',
                bbox=dict(boxstyle='round,pad=0.35', facecolor='#f0fff4', edgecolor='#9ae6b4', lw=1.0, alpha=0.95))

# Guardar figura final en alta definición
plt.savefig(fig_path, dpi=300, facecolor='white', bbox_inches='tight')
print(f"Figura generada con éxito en: {fig_path}")
