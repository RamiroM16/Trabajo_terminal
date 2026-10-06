import os
os.environ['MPLCONFIGDIR'] = '/tmp/mpl'
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

# Configuración tipográfica y de estilo editorial formal
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['DejaVu Serif', 'Times New Roman', 'Liberation Serif']
plt.rcParams['mathtext.fontset'] = 'cm'
plt.rcParams['font.size'] = 11

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

def create_ctc_diagram():
    """Figura 1.1: Diagrama de Bloques del Control por Par Calculado (CTC)"""
    fig, ax = plt.subplots(figsize=(15.6, 6.4), dpi=300)
    ax.set_xlim(0, 15.6)
    ax.set_ylim(0, 6.4)
    ax.axis('off')
    
    # Paleta de colores institucionales y de control
    c_border = '#1E293B'
    c_outer = '#E0F2FE'       # Azul suave (Lazo Exterior PD)
    c_outer_border = '#0284C7'
    c_inner = '#FEF3C7'       # Ámbar suave (Lazo Interior Dinámica Inversa)
    c_inner_border = '#D97706'
    c_plant = '#DCFCE7'       # Verde suave (Planta Manipulador)
    c_plant_border = '#16A34A'
    c_maroon = '#6B1736'      # Granate IPN
    
    fig.patch.set_facecolor('white')
    
    # Título o Encabezado
    ax.text(7.8, 6.05, 'Estructura de Control por Par Calculado (Computed Torque Control)',
            ha='center', va='center', fontsize=13, fontweight='bold', color=c_border)
    ax.text(7.8, 5.72, 'Lazo Exterior Lineal Desacoplado + Lazo Interior de Compensación Dinámica No Lineal',
            ha='center', va='center', fontsize=10.2, fontstyle='italic', color='#475569')
    
    # 1. ENTRADA DE TRAYECTORIA DESEADA
    ax.text(0.9, 3.8, 'Trayectoria\nDeseada\n$\\mathbf{q}_d, \\dot{\\mathbf{q}}_d, \\ddot{\\mathbf{q}}_d$',
            ha='center', va='center', fontsize=9.8, fontweight='bold', color='#0F172A',
            bbox=dict(boxstyle='round,pad=0.45', facecolor='#F1F5F9', edgecolor='#94A3B8', lw=1.3))
    
    # Flecha a nodo suma outer
    ax.annotate('', xy=(2.0, 3.8), xytext=(1.6, 3.8),
                arrowprops=dict(arrowstyle="-|>", color=c_border, lw=1.8, mutation_scale=14))
    
    # 2. COMPARADOR / NODO SUMA EXTERIOR
    circle_sum1 = plt.Circle((2.2, 3.8), 0.2, facecolor='white', edgecolor=c_border, lw=1.5)
    ax.add_patch(circle_sum1)
    ax.text(2.2, 3.8, '$+$', ha='center', va='center', fontsize=13, fontweight='bold')
    ax.text(2.0, 3.35, '$-$', ha='center', va='center', fontsize=13, fontweight='bold')
    ax.text(2.2, 4.35, 'Error articular\n$\\mathbf{e} = \\mathbf{q}_d - \\mathbf{q}$',
            ha='center', va='bottom', fontsize=8.8, color='#334155')
    
    # Flecha de nodo suma a bloque PD
    ax.annotate('', xy=(2.7, 3.8), xytext=(2.4, 3.8),
                arrowprops=dict(arrowstyle="-|>", color=c_border, lw=1.8, mutation_scale=14))
    
    # 3. LAZO EXTERIOR: CONTROL LINEAL PD
    # x: 2.65 a 4.95 (ancho 2.3)
    rect_outer_box = patches.FancyBboxPatch((2.65, 2.2), 2.3, 3.1,
                                           boxstyle="round,pad=0.15",
                                           facecolor=c_outer, edgecolor=c_outer_border,
                                           lw=1.5, linestyle='--')
    ax.add_patch(rect_outer_box)
    ax.text(3.8, 5.05, 'Lazo Exterior Lineal',
            ha='center', fontsize=9.8, fontweight='bold', color='#0369A1')
    
    # Bloque PD
    rect_pd = patches.FancyBboxPatch((2.78, 3.15), 2.04, 1.3,
                                     boxstyle="round,pad=0.1",
                                     facecolor='white', edgecolor=c_outer_border, lw=1.4)
    ax.add_patch(rect_pd)
    ax.text(3.8, 3.8, 'Control PD Auxiliar\n$\\mathbf{K}_p \\mathbf{e} + \\mathbf{K}_d \\dot{\\mathbf{e}}$',
            ha='center', va='center', fontsize=9.5, fontweight='bold', color=c_border)
    
    # Flecha de salida PD a suma con ddq_d
    ax.annotate('', xy=(5.95, 3.8), xytext=(4.85, 3.8),
                arrowprops=dict(arrowstyle="-|>", color=c_border, lw=1.8, mutation_scale=14))
    
    # Nodo suma a_cmd (entre los dos lazos)
    circle_sum2 = plt.Circle((6.15, 3.8), 0.2, facecolor='white', edgecolor=c_border, lw=1.5)
    ax.add_patch(circle_sum2)
    ax.text(6.15, 3.8, '$+$', ha='center', va='center', fontsize=12, fontweight='bold')
    ax.text(5.92, 3.35, '$+$', ha='center', va='center', fontsize=11, fontweight='bold')
    
    # Señal feedforward de ddq_d hacia el nodo a_cmd
    ax.plot([0.9, 0.9, 6.15, 6.15], [3.2, 1.85, 1.85, 3.6], color='#0284C7', lw=1.5, linestyle=':')
    ax.annotate('', xy=(6.15, 3.6), xytext=(6.15, 2.0),
                arrowprops=dict(arrowstyle="-|>", color='#0284C7', lw=1.5, mutation_scale=12))
    ax.text(3.5, 1.6, 'Prealimentación de aceleración nominal $\\ddot{\\mathbf{q}}_d$',
            ha='center', va='top', fontsize=8.8, color='#0284C7')
    
    # Etiqueta de la señal a_cmd centrada en el nodo suma
    ax.text(6.15, 4.4, 'Aceleración comando\n$\\mathbf{a}_{cmd} = \\ddot{\\mathbf{q}}_d + \\mathbf{K}_d\\dot{\\mathbf{e}} + \\mathbf{K}_p\\mathbf{e}$',
            ha='center', va='bottom', fontsize=8.8, fontweight='bold', color='#0F172A')
    
    # Flecha de a_cmd a Lazo Interior
    ax.annotate('', xy=(7.7, 3.8), xytext=(6.35, 3.8),
                arrowprops=dict(arrowstyle="-|>", color=c_border, lw=1.8, mutation_scale=14))
    
    # 4. LAZO INTERIOR: COMPENSACIÓN DINÁMICA NO LINEAL
    # x: 7.7 a 11.0 (ancho 3.3)
    rect_inner_box = patches.FancyBboxPatch((7.7, 2.1), 3.3, 3.2,
                                           boxstyle="round,pad=0.15",
                                           facecolor=c_inner, edgecolor=c_inner_border,
                                           lw=1.5, linestyle='--')
    ax.add_patch(rect_inner_box)
    ax.text(9.35, 5.05, 'Lazo Interior (Dinámica Inversa)',
            ha='center', fontsize=10, fontweight='bold', color='#B45309')
    
    rect_dyn = patches.FancyBboxPatch((7.88, 2.5), 2.94, 2.1,
                                     boxstyle="round,pad=0.1",
                                     facecolor='white', edgecolor=c_inner_border, lw=1.4)
    ax.add_patch(rect_dyn)
    ax.text(9.35, 3.55, 'Modelo Dinámico Inverso\n$\\hat{\\mathbf{M}}(\\mathbf{q})\\mathbf{a}_{cmd} + \\hat{\\mathbf{c}}(\\mathbf{q},\\dot{\\mathbf{q}}) + \\hat{\\mathbf{g}}(\\mathbf{q})$\n\n(Algoritmo RNEA / QNN)',
            ha='center', va='center', fontsize=9.0, fontweight='bold', color=c_border)
    
    # Flecha par de control tau (entre 11.0 y 12.1)
    ax.annotate('', xy=(12.1, 3.8), xytext=(11.0, 3.8),
                arrowprops=dict(arrowstyle="-|>", color=c_maroon, lw=2.2, mutation_scale=14))
    ax.text(11.55, 4.15, 'Par de\ncomando $\\mathbf{\\tau}$', ha='center', va='bottom',
            fontsize=9.2, fontweight='bold', color=c_maroon)
    
    # 5. PLANTA DEL ROBOT MANIPULADOR
    # x: 12.1 a 14.7 (ancho 2.6)
    rect_plant = patches.FancyBboxPatch((12.1, 2.6), 2.6, 2.3,
                                       boxstyle="round,pad=0.15",
                                       facecolor=c_plant, edgecolor=c_plant_border, lw=1.8)
    ax.add_patch(rect_plant)
    ax.text(13.4, 3.75, 'Manipulador Robótico\n(Planta UR3e)\n\n$\\mathbf{M}(\\mathbf{q})\\ddot{\\mathbf{q}} + \\mathbf{c} + \\mathbf{g} = \\mathbf{\\tau}$',
            ha='center', va='center', fontsize=9.5, fontweight='bold', color='#14532D')
    
    # 6. SALIDA Y RETROALIMENTACIÓN DE ESTADO
    ax.plot([14.7, 15.2, 15.2], [3.8, 3.8, 0.8], color=c_border, lw=1.8)
    ax.annotate('', xy=(15.1, 3.8), xytext=(14.7, 3.8),
                arrowprops=dict(arrowstyle="-|>", color=c_border, lw=1.8, mutation_scale=12))
    ax.text(15.05, 4.15, '$\\mathbf{q}, \\dot{\\mathbf{q}}$', ha='center', fontsize=10.5, fontweight='bold', color=c_border)
    
    # Línea de realimentación inferior
    ax.plot([15.2, 2.2], [0.8, 0.8], color=c_border, lw=1.8)
    ax.plot([2.2, 2.2], [0.8, 3.6], color=c_border, lw=1.8)
    ax.annotate('', xy=(2.2, 3.6), xytext=(2.2, 2.8),
                arrowprops=dict(arrowstyle="-|>", color=c_border, lw=1.8, mutation_scale=14))
    
    # Derivador / Vector de estado en la realimentación
    ax.text(8.7, 0.5, 'Retroalimentación de Estado Articular Real $(\\mathbf{q}, \\dot{\\mathbf{q}})$',
            ha='center', va='center', fontsize=9.5, fontweight='bold', color='#334155',
            bbox=dict(boxstyle='square,pad=0.35', facecolor='#F1F5F9', edgecolor='#CBD5E1', lw=1.0))
    
    # Ramificación de realimentación hacia el modelo dinámico interior
    ax.plot([9.35, 9.35], [0.8, 2.5], color='#B45309', lw=1.5, linestyle='--')
    ax.annotate('', xy=(9.35, 2.5), xytext=(9.35, 1.8),
                arrowprops=dict(arrowstyle="-|>", color='#B45309', lw=1.5, mutation_scale=12))
    ax.text(10.05, 1.45, 'Actualización\nde $\\mathbf{q}, \\dot{\\mathbf{q}}$', ha='center', fontsize=8.2, color='#B45309')
    
    plt.tight_layout()
    out_path = os.path.join(OUTPUT_DIR, 'bloques_control_par_calculado.png')
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✅ Generado: {out_path}")

def create_rnea_diagram():
    """Figura 1.2: Diagrama de Flujo del Algoritmo Recursivo de Newton-Euler (RNEA)"""
    fig, ax = plt.subplots(figsize=(14.2, 8.0), dpi=300)
    ax.set_xlim(0, 14.2)
    ax.set_ylim(0, 8.0)
    ax.axis('off')
    
    c_blue_bg = '#EFF6FF'
    c_blue_border = '#1D4ED8'
    c_red_bg = '#FEF2F2'
    c_red_border = '#B91C1C'
    c_maroon = '#6B1736'
    
    fig.patch.set_facecolor('white')
    
    # Encabezado
    ax.text(7.1, 7.65, 'Estructura Algorítmica del Algoritmo Recursivo Newton-Euler (RNEA)',
            ha='center', va='center', fontsize=13, fontweight='bold', color='#0F172A')
    ax.text(7.1, 7.32, 'Complejidad Lineal $\\mathcal{O}(n)$ para Manipuladores Seriales de $n$ Grados de Libertad (Craig / Luh et al.)',
            ha='center', va='center', fontsize=10.5, fontstyle='italic', color='#475569')
    
    # CONTENEDOR IZQUIERDO: PASADA HACIA ADELANTE (CINEMÁTICA)
    rect_fwd_box = patches.FancyBboxPatch((0.5, 0.4), 5.7, 6.6,
                                          boxstyle="round,pad=0.2",
                                          facecolor=c_blue_bg, edgecolor=c_blue_border, lw=1.8)
    ax.add_patch(rect_fwd_box)
    
    ax.text(3.35, 6.65, 'PASADA HACIA ADELANTE: Cinemática\n(Propagación Base $\\to$ Efector Final: $i = 1, 2, \\dots, n$)',
            ha='center', va='center', fontsize=10.0, fontweight='bold', color=c_blue_border)
    
    # Bloque 1: Condiciones Iniciales
    rect_f1 = patches.FancyBboxPatch((0.75, 5.4), 5.2, 0.9, boxstyle="round,pad=0.1",
                                     facecolor='white', edgecolor='#93C5FD', lw=1.2)
    ax.add_patch(rect_f1)
    ax.text(3.35, 5.85, '1. Condiciones de Frontera en la Base ($i=0$)\n$\\mathbf{\\omega}_0 = \\mathbf{0}, \\quad \\dot{\\mathbf{\\omega}}_0 = \\mathbf{0}, \\quad \\dot{\\mathbf{v}}_0 = [0, 0, 9.81]^T\\,\\mathrm{m/s}^2$ (Gravedad)',
            ha='center', va='center', fontsize=8.8, color='#1E293B')
    
    ax.annotate('', xy=(3.35, 4.95), xytext=(3.35, 5.4),
                arrowprops=dict(arrowstyle="-|>", color=c_blue_border, lw=1.6, mutation_scale=12))
    
    # Bloque 2: Velocidades y Aceleraciones Angulares
    rect_f2 = patches.FancyBboxPatch((0.75, 3.95), 5.2, 1.0, boxstyle="round,pad=0.1",
                                     facecolor='white', edgecolor='#93C5FD', lw=1.2)
    ax.add_patch(rect_f2)
    ax.text(3.35, 4.45, '2. Propagación de Velocidad y Aceleración Angular\n$\\mathbf{\\omega}_i = (\\mathbf{R}_i^{i-1})^T \\mathbf{\\omega}_{i-1} + \\dot{q}_i \\mathbf{z}_0$\n$\\dot{\\mathbf{\\omega}}_i = (\\mathbf{R}_i^{i-1})^T \\dot{\\mathbf{\\omega}}_{i-1} + ((\\mathbf{R}_i^{i-1})^T \\mathbf{\\omega}_{i-1}) \\times (\\dot{q}_i \\mathbf{z}_0) + \\ddot{q}_i \\mathbf{z}_0$',
            ha='center', va='center', fontsize=8.6, color='#1E293B')
    
    ax.annotate('', xy=(3.35, 3.5), xytext=(3.35, 3.95),
                arrowprops=dict(arrowstyle="-|>", color=c_blue_border, lw=1.6, mutation_scale=12))
    
    # Bloque 3: Aceleración Lineal de Orígenes
    rect_f3 = patches.FancyBboxPatch((0.75, 2.35), 5.2, 1.15, boxstyle="round,pad=0.1",
                                     facecolor='white', edgecolor='#93C5FD', lw=1.2)
    ax.add_patch(rect_f3)
    ax.text(3.35, 2.92, '3. Aceleración Lineal del Origen y Centro de Masa\n$\\dot{\\mathbf{v}}_i = (\\mathbf{R}_i^{i-1})^T \\dot{\\mathbf{v}}_{i-1} + \\dot{\\mathbf{\\omega}}_i \\times \\mathbf{P}_i^{i-1} + \\mathbf{\\omega}_i \\times (\\mathbf{\\omega}_i \\times \\mathbf{P}_i^{i-1})$\n$\\dot{\\mathbf{v}}_{c,i} = \\dot{\\mathbf{v}}_i + \\dot{\\mathbf{\\omega}}_i \\times \\mathbf{r}_{c,i} + \\mathbf{\\omega}_i \\times (\\mathbf{\\omega}_i \\times \\mathbf{r}_{c,i})$',
            ha='center', va='center', fontsize=8.6, color='#1E293B')
    
    ax.annotate('', xy=(3.35, 1.9), xytext=(3.35, 2.35),
                arrowprops=dict(arrowstyle="-|>", color=c_blue_border, lw=1.6, mutation_scale=12))
    
    # Bloque 4: Fuerzas y Momentos Inerciales del Eslabón
    rect_f4 = patches.FancyBboxPatch((0.75, 0.7), 5.2, 1.2, boxstyle="round,pad=0.1",
                                     facecolor='white', edgecolor='#93C5FD', lw=1.2)
    ax.add_patch(rect_f4)
    ax.text(3.35, 1.3, '4. Fuerzas y Momentos Dinámicos de Newton-Euler\n$\\mathbf{F}_i = m_i \\dot{\\mathbf{v}}_{c,i} \\quad$ (Fuerza inercial neta)\n$\\mathbf{N}_i = \\mathbf{I}_i \\dot{\\mathbf{\\omega}}_i + \\mathbf{\\omega}_i \\times (\\mathbf{I}_i \\mathbf{\\omega}_i) \\quad$ (Momento baricéntrico)',
            ha='center', va='center', fontsize=8.8, color='#1E293B')
    
    # TRANSICIÓN CENTRAL ENTRE PASADAS
    rect_trans = patches.FancyBboxPatch((6.45, 0.6), 1.3, 1.4, boxstyle="round,pad=0.08",
                                        facecolor='#F8FAFC', edgecolor='#64748B', lw=1.2, linestyle=':')
    ax.add_patch(rect_trans)
    ax.text(7.1, 1.35, 'Frontera\nExtremo', ha='center', fontsize=8.2, fontweight='bold', color='#334155')
    ax.text(7.1, 0.95, '$\\mathbf{f}_{n+1} = \\mathbf{0}$\n$\\mathbf{n}_{n+1} = \\mathbf{0}$',
            ha='center', fontsize=8.0, color='#475569')
    
    ax.annotate('', xy=(7.9, 1.3), xytext=(6.1, 1.3),
                arrowprops=dict(arrowstyle="-|>", color='#334155', lw=2.0, mutation_scale=14))
    
    # CONTENEDOR DERECHO: PASADA HACIA ATRÁS (CINÉTICA / BALANCE DE FUERZAS)
    rect_bwd_box = patches.FancyBboxPatch((8.0, 0.4), 5.7, 6.6,
                                          boxstyle="round,pad=0.2",
                                          facecolor=c_red_bg, edgecolor=c_red_border, lw=1.8)
    ax.add_patch(rect_bwd_box)
    
    ax.text(10.85, 6.65, 'PASADA HACIA ATRÁS: Dinámica y Pares\n(Propagación Efector Final $\\to$ Base: $i = n, n-1, \\dots, 1$)',
            ha='center', va='center', fontsize=10.0, fontweight='bold', color=c_red_border)
    
    # Bloque B1: Balance de Fuerzas Articulares
    rect_b1 = patches.FancyBboxPatch((8.25, 4.95), 5.2, 1.2, boxstyle="round,pad=0.1",
                                     facecolor='white', edgecolor='#FCA5A5', lw=1.2)
    ax.add_patch(rect_b1)
    ax.text(10.85, 5.55, '5. Balance de Fuerzas de Contacto Articular\n$\\mathbf{f}_i = \\mathbf{R}_{i+1}^i \\mathbf{f}_{i+1} + \\mathbf{F}_i$\nTransmisión de fuerza del eslabón distal sumada a la inercia local.',
            ha='center', va='center', fontsize=8.8, color='#1E293B')
    
    ax.annotate('', xy=(10.85, 4.5), xytext=(10.85, 4.95),
                arrowprops=dict(arrowstyle="<|-", color=c_red_border, lw=1.6, mutation_scale=12))
    
    # Bloque B2: Balance de Momentos Articulares
    rect_b2 = patches.FancyBboxPatch((8.25, 2.95), 5.2, 1.55, boxstyle="round,pad=0.1",
                                     facecolor='white', edgecolor='#FCA5A5', lw=1.2)
    ax.add_patch(rect_b2)
    ax.text(10.85, 3.72, '6. Balance de Momentos Articulares\n$\\mathbf{n}_i = \\mathbf{N}_i + \\mathbf{R}_{i+1}^i \\mathbf{n}_{i+1} + \\mathbf{r}_{c,i} \\times \\mathbf{F}_i + \\mathbf{P}_{i+1}^i \\times (\\mathbf{R}_{i+1}^i \\mathbf{f}_{i+1})$\nEquilibrio de pares respecto al marco del eslabón $i$.',
            ha='center', va='center', fontsize=8.8, color='#1E293B')
    
    ax.annotate('', xy=(10.85, 2.5), xytext=(10.85, 2.95),
                arrowprops=dict(arrowstyle="<|-", color=c_red_border, lw=1.6, mutation_scale=12))
    
    # Bloque B3: Proyección del Par Articular
    rect_b3 = patches.FancyBboxPatch((8.25, 0.7), 5.2, 1.8, boxstyle="round,pad=0.1",
                                     facecolor='#FEF2F2', edgecolor=c_maroon, lw=1.6)
    ax.add_patch(rect_b3)
    ax.text(10.85, 1.6, '7. Cálculo del Par Articular Escalar\n$\\tau_{rnea, i} = \\mathbf{n}_i^T \\mathbf{z}_0 \\quad (\\mathrm{Eje\\ rotacional}\\ \\mathbf{z}_0 = [0, 0, 1]^T)$\n\n'
                         '$\\mathbf{\\tau}_{RNEA} = [\\tau_1, \\tau_2, \\tau_3, \\tau_4, \\tau_5, \\tau_6]^T$\n'
                         'Cálculo Eficiente en C++ ($t_{prom} \\approx 151.2\\,\\mu\\mathrm{s}$ en UR3e)',
            ha='center', va='center', fontsize=9.0, fontweight='bold', color=c_maroon)
    
    plt.tight_layout()
    out_path = os.path.join(OUTPUT_DIR, 'diagrama_flujo_rnea.png')
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✅ Generado: {out_path}")

def create_ptq_vs_qat_diagram():
    """Figura 1.3: Comparativa de Pipelines de Cuantización (PTQ vs QAT)"""
    fig, ax = plt.subplots(figsize=(13.5, 7.2), dpi=300)
    ax.set_xlim(0, 13.5)
    ax.set_ylim(0, 7.2)
    ax.axis('off')
    
    c_ptq_bg = '#F0FDF4'
    c_ptq_border = '#16A34A'
    c_qat_bg = '#FEF3C7'
    c_qat_border = '#D97706'
    c_border = '#1E293B'
    
    fig.patch.set_facecolor('white')
    
    # Encabezado
    ax.text(6.75, 6.85, 'Comparativa de Metodologías de Cuantización de Redes Neuronales',
            ha='center', va='center', fontsize=13, fontweight='bold', color=c_border)
    ax.text(6.75, 6.55, 'Flujo de Trabajo y Tratamiento de Gradientes: PTQ (Post-Entrenamiento) vs. QAT (Consciente de Cuantización)',
            ha='center', va='center', fontsize=10.5, fontstyle='italic', color='#475569')
    
    # RUTA 1: PTQ (SUPERIOR)
    rect_ptq_box = patches.FancyBboxPatch((0.5, 3.4), 12.5, 2.85,
                                          boxstyle="round,pad=0.2",
                                          facecolor=c_ptq_bg, edgecolor=c_ptq_border, lw=1.8)
    ax.add_patch(rect_ptq_box)
    ax.text(1.8, 5.95, 'RUTA A: Post-Training Quantization (PTQ)',
            ha='left', va='center', fontsize=11, fontweight='bold', color='#15803D')
    
    # Bloques PTQ
    steps_ptq = [
        ('1. Modelo FP32\nPre-entrenado\n(PyTorch .pth)', 1.7),
        ('2. Calibración\nDataset Representativo\n(Recolección Min-Max)', 4.6),
        ('3. Parámetros\nEscala $S$ y Zero-Point $Z$\n$S = \\frac{x_{max}-x_{min}}{255}$', 7.5),
        ('4. Conversión y Mapeo\n$x_q = \\mathrm{clamp}\\left(\\mathrm{round}\\left(\\frac{x}{S}\\right)+Z\\right)$\nPesos y Activaciones a INT8', 10.4)
    ]
    
    for text, cx in steps_ptq:
        rect = patches.FancyBboxPatch((cx-1.2, 3.8), 2.4, 1.6, boxstyle="round,pad=0.1",
                                      facecolor='white', edgecolor=c_ptq_border, lw=1.3)
        ax.add_patch(rect)
        ax.text(cx, 4.6, text, ha='center', va='center', fontsize=8.8, fontweight='medium', color='#0F172A')
    
    # Flechas PTQ
    for i in range(len(steps_ptq)-1):
        x1 = steps_ptq[i][1] + 1.2
        x2 = steps_ptq[i+1][1] - 1.2
        ax.annotate('', xy=(x2, 4.6), xytext=(x1, 4.6),
                    arrowprops=dict(arrowstyle="-|>", color=c_ptq_border, lw=2.0, mutation_scale=14))
    
    ax.text(6.75, 3.55, 'Características: Rápido, no requiere re-entrenar, ideal para inferencia en CPU/ONNX Runtime. Compresión 74.4% en este TT.',
            ha='center', va='center', fontsize=9.0, fontstyle='italic', color='#166534')
    
    # RUTA 2: QAT (INFERIOR)
    rect_qat_box = patches.FancyBboxPatch((0.5, 0.3), 12.5, 2.9,
                                          boxstyle="round,pad=0.2",
                                          facecolor=c_qat_bg, edgecolor=c_qat_border, lw=1.8)
    ax.add_patch(rect_qat_box)
    ax.text(1.8, 2.85, 'RUTA B: Quantization-Aware Training (QAT)',
            ha='left', va='center', fontsize=11, fontweight='bold', color='#B45309')
    
    steps_qat = [
        ('1. Inserción de Nodos\nFake-Quantization\n(Grafo Computacional)', 1.7),
        ('2. Forward Pass\nSimulación Discreta\n$\\hat{x}_{FQ} = S(\\mathrm{quant}(x)-Z)$', 4.6),
        ('3. Backward Pass\nEstimador STE\n$\\frac{\\partial \\hat{x}_{FQ}}{\\partial x} \\approx 1$', 7.5),
        ('4. Adaptación Dinámica\nPesos compensan el\nruido de cuantización', 10.4)
    ]
    
    for text, cx in steps_qat:
        rect = patches.FancyBboxPatch((cx-1.2, 0.7), 2.4, 1.6, boxstyle="round,pad=0.1",
                                      facecolor='white', edgecolor=c_qat_border, lw=1.3)
        ax.add_patch(rect)
        ax.text(cx, 1.5, text, ha='center', va='center', fontsize=8.8, fontweight='medium', color='#0F172A')
    
    # Flechas QAT
    for i in range(len(steps_qat)-1):
        x1 = steps_qat[i][1] + 1.2
        x2 = steps_qat[i+1][1] - 1.2
        ax.annotate('', xy=(x2, 1.5), xytext=(x1, 1.5),
                    arrowprops=dict(arrowstyle="-|>", color=c_qat_border, lw=2.0, mutation_scale=14))
    
    ax.text(6.75, 0.45, 'Características: Modela el error de redondeo durante el descenso de gradiente. Maximiza precisión en regímenes sub-8 bits (INT4/INT6).',
            ha='center', va='center', fontsize=9.0, fontstyle='italic', color='#92400E')
    
    plt.tight_layout()
    out_path = os.path.join(OUTPUT_DIR, 'comparativa_ptq_qat.png')
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✅ Generado: {out_path}")

def create_scrum_diagram():
    """Figura 1.4: Metodología Scrum adaptada al Desarrollo Mecatrónico"""
    fig, ax = plt.subplots(figsize=(13.5, 6.8), dpi=300)
    ax.set_xlim(0, 13.5)
    ax.set_ylim(0, 6.8)
    ax.axis('off')
    
    c_maroon = '#6B1736'
    c_navy = '#1E3A8A'
    c_slate = '#334155'
    
    fig.patch.set_facecolor('white')
    
    # Encabezado
    ax.text(6.75, 6.45, 'Marco Metodológico Ágil Scrum Adaptado a Ingeniería Mecatrónica',
            ha='center', va='center', fontsize=13, fontweight='bold', color='#0F172A')
    ax.text(6.75, 6.15, 'Ciclo Iterativo e Incremental para Desarrollo Sincronizado de Software, Inteligencia Artificial y Hardware',
            ha='center', va='center', fontsize=10.5, fontstyle='italic', color='#475569')
    
    # BLOQUE 1: PRODUCT BACKLOG
    rect_pb = patches.FancyBboxPatch((0.5, 1.8), 2.5, 3.8, boxstyle="round,pad=0.15",
                                     facecolor='#F1F5F9', edgecolor=c_navy, lw=1.6)
    ax.add_patch(rect_pb)
    ax.text(1.75, 5.25, 'PRODUCT BACKLOG\n(Requerimientos)', ha='center', fontsize=10, fontweight='bold', color=c_navy)
    
    items_pb = [
        '• Dinámica Inversa RNEA',
        '• Gemelo Digital Gazebo',
        '• Controlador C++ ROS 2',
        '• Generador Trayectorias $C^2$',
        '• Pipeline Entrenamiento AI',
        '• Cuantización INT8 ONNX',
        '• Telemetría de Alta Frecuencia',
        '• Verificación Sim-to-Real'
    ]
    y_pos = 4.6
    for it in items_pb:
        ax.text(0.7, y_pos, it, ha='left', va='center', fontsize=8.2, color='#1E293B')
        y_pos -= 0.38
        
    ax.annotate('', xy=(3.4, 3.7), xytext=(3.0, 3.7),
                arrowprops=dict(arrowstyle="-|>", color=c_navy, lw=2.0, mutation_scale=14))
    
    # BLOQUE 2: SPRINT PLANNING & SPRINT BACKLOG
    rect_sp = patches.FancyBboxPatch((3.4, 2.3), 2.5, 2.8, boxstyle="round,pad=0.15",
                                     facecolor='#EFF6FF', edgecolor='#2563EB', lw=1.6)
    ax.add_patch(rect_sp)
    ax.text(4.65, 4.75, 'SPRINT PLANNING\n& SPRINT BACKLOG', ha='center', fontsize=10, fontweight='bold', color='#1D4ED8')
    ax.text(4.65, 3.95, 'Selección de épicos\ny metas priorizadas\n(Duración: 2 a 4 semanas)',
            ha='center', va='center', fontsize=8.8, color='#1E293B')
    ax.text(4.65, 3.0, 'Definición de criterios\nde aceptación técnicos\n(Métricas de control/error)',
            ha='center', va='center', fontsize=8.5, fontstyle='italic', color='#3B82F6')
    
    ax.annotate('', xy=(6.3, 3.7), xytext=(5.9, 3.7),
                arrowprops=dict(arrowstyle="-|>", color='#2563EB', lw=2.0, mutation_scale=14))
    
    # BLOQUE 3: EL SPRINT MECATRÓNICO (CICLO CENTRAL CON REUNIONES DE AVANCE)
    rect_sprint = patches.FancyBboxPatch((6.3, 1.5), 3.8, 4.3, boxstyle="round,pad=0.2",
                                         facecolor='#FAF5FF', edgecolor=c_maroon, lw=2.0)
    ax.add_patch(rect_sprint)
    ax.text(8.2, 5.45, 'SPRINT MECATRÓNICO\n(2 - 4 Semanas)', ha='center', fontsize=11, fontweight='bold', color=c_maroon)
    
    # Componentes sincronizados mecatrónicos
    c_mods = [
        ('Mecánica y Simulación (UR3e Gazebo)', 4.6),
        ('Software y Control (ROS 2 / C++17)', 4.0),
        ('Inteligencia Artificial (ONNX / INT8)', 3.4),
        ('Seguridad y Benchmarking', 2.8)
    ]
    for name, yp in c_mods:
        r = patches.FancyBboxPatch((6.6, yp-0.22), 3.2, 0.44, boxstyle="round,pad=0.08",
                                   facecolor='white', edgecolor='#D8B4FE', lw=1.0)
        ax.add_patch(r)
        ax.text(8.2, yp, name, ha='center', va='center', fontsize=8.4, fontweight='medium', color='#4C1D95')
    
    # Evento de asesoría semanal (Daily Scrum adaptado)
    ax.text(8.2, 2.05, 'Reuniones de Avance Periódicas\nSupervisión con Asesores / Sincronización',
            ha='center', va='center', fontsize=8.2, fontweight='bold', color='#701A75',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='#FDF4FF', edgecolor='#E879F9', lw=1.0))
    
    ax.annotate('', xy=(10.5, 3.7), xytext=(10.1, 3.7),
                arrowprops=dict(arrowstyle="-|>", color=c_maroon, lw=2.0, mutation_scale=14))
    
    # BLOQUE 4: SPRINT REVIEW, RETROSPECTIVA E INCREMENTO
    rect_inc = patches.FancyBboxPatch((10.5, 1.8), 2.5, 3.8, boxstyle="round,pad=0.15",
                                      facecolor='#F0FDF4', edgecolor='#16A34A', lw=1.8)
    ax.add_patch(rect_inc)
    ax.text(11.75, 5.25, 'INCREMENTO EVALUABLE\n(Potencialmente Desplegable)',
            ha='center', fontsize=9.5, fontweight='bold', color='#15803D')
    
    inc_items = [
        '• Plugin de control C++ optimizado',
        '• Red Cuantizada validada',
        '• Error RMSE cuantificado',
        '• Logs de simulación MCAP',
        '• Avance documentado TT1'
    ]
    yp = 4.35
    for it in inc_items:
        ax.text(10.7, yp, it, ha='left', va='center', fontsize=8.2, color='#14532D')
        yp -= 0.38
        
    ax.text(11.75, 2.3, 'Sprint Review &\nRetrospective\n(Ajuste de Backlog)',
            ha='center', va='center', fontsize=8.5, fontweight='bold', color='#166534',
            bbox=dict(boxstyle='square,pad=0.3', facecolor='white', edgecolor='#86EFAC', lw=1.0))
    
    # Bucle de retroalimentación hacia el Product Backlog
    ax.plot([11.75, 11.75, 1.75, 1.75], [1.8, 0.8, 0.8, 1.8], color='#047857', lw=1.8, linestyle='--')
    ax.annotate('', xy=(1.75, 1.8), xytext=(1.75, 1.2),
                arrowprops=dict(arrowstyle="-|>", color='#047857', lw=1.8, mutation_scale=14))
    ax.text(6.75, 0.55, 'Ciclo de Mejora Continua y Ajuste Dinámico del Alcance',
            ha='center', va='center', fontsize=9.2, fontweight='bold', color='#047857')
    
    plt.tight_layout()
    out_path = os.path.join(OUTPUT_DIR, 'metodologia_scrum_mecatronica.png')
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✅ Generado: {out_path}")

if __name__ == '__main__':
    print("Iniciando generación de figuras vectoriales para Capítulo 1...")
    create_ctc_diagram()
    create_rnea_diagram()
    create_ptq_vs_qat_diagram()
    create_scrum_diagram()
    print("Todas las figuras fueron generadas con éxito.")
