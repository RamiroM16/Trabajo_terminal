import os
os.environ['MPLCONFIGDIR'] = '/tmp/mpl'
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Configuración tipográfica y de estilo editorial formal
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['DejaVu Serif', 'Times New Roman', 'Liberation Serif']
plt.rcParams['mathtext.fontset'] = 'cm'
plt.rcParams['font.size'] = 11

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

def create_von_neumann_figure():
    """Figura Introductoria: Arquitectura Von Neumann, Cuello de Botella y Solución de Cuantización"""
    fig, ax = plt.subplots(figsize=(15.6, 6.6), dpi=300)
    ax.set_xlim(0, 15.6)
    ax.set_ylim(0, 6.6)
    ax.axis('off')

    c_border = '#1E293B'
    c_cpu = '#E0F2FE'         # Azul claro
    c_cpu_b = '#0284C7'
    c_mem = '#FEF3C7'         # Ámbar claro
    c_mem_b = '#D97706'
    c_wall = '#FEE2E2'        # Rojo suave (Memory Wall)
    c_wall_b = '#DC2626'
    c_qnn = '#DCFCE7'         # Verde claro (INT8 / Solución)
    c_qnn_b = '#16A34A'
    c_maroon = '#6B1736'

    fig.patch.set_facecolor('white')

    # Encabezado principal
    ax.text(7.8, 6.25, 'Arquitectura Von Neumann: Cuello de Botella de Memoria y Optimización por Cuantización',
            ha='center', va='center', fontsize=13.5, fontweight='bold', color=c_border)
    ax.text(7.8, 5.92, 'Impacto del Tráfico de Datos en Bucles de Control Robótico en Tiempo Real (100 Hz)',
            ha='center', va='center', fontsize=10.2, fontstyle='italic', color='#475569')

    # ==========================================
    # PANEL IZQUIERDO: ARQUITECTURA COMPUTACIONAL TRADICIONAL
    # ==========================================
    # Contenedor General Von Neumann
    rect_vn = patches.FancyBboxPatch((0.5, 0.7), 9.2, 4.9, boxstyle="round,pad=0.15",
                                    facecolor='#F8FAFC', edgecolor='#94A3B8', lw=1.5, linestyle=':')
    ax.add_patch(rect_vn)
    ax.text(5.1, 5.35, 'Arquitectura Digital Von Neumann Convencional',
            ha='center', va='center', fontsize=10.5, fontweight='bold', color='#334155')

    # Bloque CPU
    rect_cpu = patches.FancyBboxPatch((0.8, 2.0), 3.0, 3.0, boxstyle="round,pad=0.1",
                                     facecolor=c_cpu, edgecolor=c_cpu_b, lw=1.6)
    ax.add_patch(rect_cpu)
    ax.text(2.3, 4.65, 'Unidad de Procesamiento\n(CPU / Núcleo)', ha='center', va='center',
            fontsize=10, fontweight='bold', color='#0369A1')

    # Sub-bloques dentro de la CPU
    rect_alu = patches.FancyBboxPatch((1.0, 3.1), 2.6, 1.0, boxstyle="round,pad=0.08",
                                     facecolor='white', edgecolor=c_cpu_b, lw=1.2)
    ax.add_patch(rect_alu)
    ax.text(2.3, 3.6, 'Unidad Aritmética Lógica (ALU)\nOperaciones MAC FP32',
            ha='center', va='center', fontsize=8.5, fontweight='bold', color=c_border)

    rect_cu = patches.FancyBboxPatch((1.0, 2.15), 2.6, 0.75, boxstyle="round,pad=0.08",
                                    facecolor='white', edgecolor=c_cpu_b, lw=1.2)
    ax.add_patch(rect_cu)
    ax.text(2.3, 2.52, 'Unidad de Control (UC)',
            ha='center', va='center', fontsize=8.8, color='#334155')

    # Bloque Memoria Principal
    rect_mem = patches.FancyBboxPatch((6.4, 2.0), 3.0, 3.0, boxstyle="round,pad=0.1",
                                     facecolor=c_mem, edgecolor=c_mem_b, lw=1.6)
    ax.add_patch(rect_mem)
    ax.text(7.9, 4.65, 'Memoria Principal\n(RAM / Jerarquía Caché)', ha='center', va='center',
            fontsize=10, fontweight='bold', color='#B45309')

    # Sub-bloques dentro de la Memoria
    rect_prog = patches.FancyBboxPatch((6.6, 3.2), 2.6, 0.9, boxstyle="round,pad=0.08",
                                      facecolor='white', edgecolor=c_mem_b, lw=1.2)
    ax.add_patch(rect_prog)
    ax.text(7.9, 3.65, 'Instrucciones de Control\n(Código Binario)',
            ha='center', va='center', fontsize=8.5, color=c_border)

    rect_data = patches.FancyBboxPatch((6.6, 2.15), 2.6, 0.9, boxstyle="round,pad=0.08",
                                      facecolor='white', edgecolor=c_mem_b, lw=1.2)
    ax.add_patch(rect_data)
    ax.text(7.9, 2.6, 'Datos y Coeficientes\nPesos FP32 (32 bits)',
            ha='center', va='center', fontsize=8.5, fontweight='bold', color=c_border)

    # Bus del Sistema (Cuello de Botella)
    rect_bus = patches.FancyBboxPatch((4.0, 2.3), 2.2, 1.8, boxstyle="round,pad=0.1",
                                     facecolor=c_wall, edgecolor=c_wall_b, lw=1.8, linestyle='--')
    ax.add_patch(rect_bus)
    ax.text(5.1, 3.75, 'Bus Compartido\n(Ancho de banda acotado)',
            ha='center', va='center', fontsize=8.6, fontweight='bold', color=c_wall_b)

    # Flechas bidireccionales de transferencia
    ax.annotate('', xy=(3.8, 3.1), xytext=(4.2, 3.1),
                arrowprops=dict(arrowstyle="<|-|>", color=c_wall_b, lw=2.2, mutation_scale=12))
    ax.annotate('', xy=(6.0, 3.1), xytext=(6.4, 3.1),
                arrowprops=dict(arrowstyle="<|-|>", color=c_wall_b, lw=2.2, mutation_scale=12))

    ax.text(5.1, 2.75, 'CUELLO DE BOTELLA\n"Memory Wall"\nLatencia y Consumo',
            ha='center', va='center', fontsize=8.2, fontweight='bold', color='#991B1B')

    # Consecuencia en Robótica (Debajo de Von Neumann)
    ax.text(5.1, 1.35, 'Desafío en Robótica en Tiempo Real: Bucle estricto a 100 Hz ($T_s \\leq 10$ ms).\nLa transferencia masiva de parámetros FP32 satura el bus, causa latencias variables y eleva la energía disipada.',
            ha='center', va='center', fontsize=8.8, color='#1E293B',
            bbox=dict(boxstyle='round,pad=0.4', facecolor='#FFFBEB', edgecolor='#FCD34D', lw=1.0))

    # ==========================================
    # FLECHA DE TRANSICIÓN HACIA LA SOLUCIÓN
    # ==========================================
    ax.annotate('', xy=(10.3, 3.15), xytext=(9.8, 3.15),
                arrowprops=dict(arrowstyle="-|>", color=c_qnn_b, lw=2.5, mutation_scale=16))
    ax.text(10.05, 3.45, 'Compresión\nNumérica', ha='center', va='bottom',
            fontsize=8.5, fontweight='bold', color=c_qnn_b)

    # ==========================================
    # PANEL DERECHO: PARADIGMA CUANTIZADO INT8 (SOLUCIÓN)
    # ==========================================
    rect_sol = patches.FancyBboxPatch((10.4, 0.7), 4.7, 4.9, boxstyle="round,pad=0.15",
                                     facecolor=c_qnn, edgecolor=c_qnn_b, lw=1.6)
    ax.add_patch(rect_sol)
    ax.text(12.75, 5.35, 'Solución: Redes Cuantizadas (INT8)',
            ha='center', va='center', fontsize=10.5, fontweight='bold', color='#14532D')

    # Beneficio 1: Reducción del ancho de palabra
    rect_b1 = patches.FancyBboxPatch((10.65, 3.85), 4.2, 1.25, boxstyle="round,pad=0.08",
                                     facecolor='white', edgecolor=c_qnn_b, lw=1.2)
    ax.add_patch(rect_b1)
    ax.text(12.75, 4.65, 'Compresión de Memoria: 74.4%',
            ha='center', va='center', fontsize=9.2, fontweight='bold', color='#15803D')
    ax.text(12.75, 4.15, 'FP32 (32 bits) $\\to$ INT8 (8 bits)\nReducción drástica del ancho de banda requerido.\nPesos residen en memoria caché L1/L2.',
            ha='center', va='center', fontsize=8.0, color='#334155')

    # Beneficio 2: Aceleración aritmética entera
    rect_b2 = patches.FancyBboxPatch((10.65, 2.45), 4.2, 1.25, boxstyle="round,pad=0.08",
                                     facecolor='white', edgecolor=c_qnn_b, lw=1.2)
    ax.add_patch(rect_b2)
    ax.text(12.75, 3.25, 'Aceleración y Eficiencia Aritmética',
            ha='center', va='center', fontsize=9.2, fontweight='bold', color='#15803D')
    ax.text(12.75, 2.75, 'Multiplicaciones y sumas enteras INT8/INT32.\nMenor área de silicio, menor consumo dinámico.\nInferencia C++ de baja latencia ($< 50$ $\\mu$s).',
            ha='center', va='center', fontsize=8.0, color='#334155')

    # Beneficio 3: Despliegue en Borde
    rect_b3 = patches.FancyBboxPatch((10.65, 1.05), 4.2, 1.25, boxstyle="round,pad=0.08",
                                     facecolor='white', edgecolor=c_qnn_b, lw=1.2)
    ax.add_patch(rect_b3)
    ax.text(12.75, 1.85, 'Viabilidad Temporal en Tiempo Real',
            ha='center', va='center', fontsize=9.2, fontweight='bold', color='#15803D')
    ax.text(12.75, 1.35, r'Cero asignaciones dinámicas en memoria.' + '\n' + r'Holgura frente al periodo nominal $T_s \leq 10$ ms.' + '\n' + r'Viabilidad en procesadores embebidos y FPGAs.',
            ha='center', va='center', fontsize=8.0, color='#334155')

    plt.tight_layout()
    out_path = os.path.join(OUTPUT_DIR, 'arquitectura_von_neumann_cuello_botella.png')
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    print(f"✅ Generado: {out_path}")

if __name__ == '__main__':
    create_von_neumann_figure()
