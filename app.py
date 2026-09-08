import streamlit as st

# Configuración de la página
st.set_page_config(page_title="Calculadora de Repostería", page_icon="🎂", layout="centered")

# 1. Tabla de equivalencias de moldes y cantidad de huevos por unidad
MOLDES_HUEVOS = {
    "Mini": 0.5,
    "Gris": 1.0,
    "15cm / ♡ P": 1.5,
    "20cm / ♡ L": 2.5,
    "25cm": 5.0,
    "Plancha": 3.0,
    "Cupcake": 0.1
}

# 2. Lista de recetas disponibles
RECETAS = [
    "Vainilla",
    "Chocolate",
    "Red Velvet",
    "Carrot Cake",
    "Café",
    "Coco",
    "Limón"
]

# Inicializar estados en la sesión
if "resumen_sesion" not in st.session_state:
    st.session_state.resumen_sesion = []

if "ultimo_calculo" not in st.session_state:
    st.session_state.ultimo_calculo = None

def limpiar_cantidades():
    """Función para poner a 0 todas las casillas de moldes."""
    for molde in MOLDES_HUEVOS.keys():
        st.session_state[f"input_{molde}"] = 0.0

st.title("🎂 Calculadora de Repostería")

# --- PASO 1: SELECCIÓN DE RECETA ---
st.subheader("1. Selecciona la receta")
receta_seleccionada = st.selectbox("Receta:", RECETAS)

# --- PASO 2: CANTIDAD DE MOLDES ---
col_head1, col_head2 = st.columns([2, 1])
with col_head1:
    st.subheader("2. Moldes a producir")
with col_head2:
    st.button("🔄 Limpiar moldes", on_click=limpiar_cantidades, use_container_width=True)

cantidades = {}

# Mostramos los moldes en 2 columnas
cols = st.columns(2)
for i, (molde, valor_h) in enumerate(MOLDES_HUEVOS.items()):
    col = cols[i % 2]
    cantidades[molde] = col.number_input(
        label=f"'{molde}' ({valor_h} h/u):",
        min_value=0.0,
        value=0.0,
        step=0.5,
        format="%.1f",
        key=f"input_{molde}"
    )

# --- PASO 3: CÁLCULO ---
st.markdown("---")
if st.button("🧮 Calcular y guardar para esta receta", type="primary", use_container_width=True):
    total_huevos = sum(cantidades[m] * MOLDES_HUEVOS[m] for m in cantidades)
    
    if total_huevos > 0:
        desglose_moldes = {m: cant for m, cant in cantidades.items() if cant > 0}
        
        # Guardar registro en la sesión
        registro = {
            "receta": receta_seleccionada,
            "total_huevos": total_huevos,
            "desglose": desglose_moldes
        }
        st.session_state.resumen_sesion.append(registro)
        st.session_state.ultimo_calculo = registro
        
        # Limpiar casillas para el siguiente cálculo
        limpiar_cantidades()
        st.rerun()
    else:
        st.warning("Indica al menos 1 molde para realizar el cálculo.")

# --- RESULTADO DEL ÚLTIMO CÁLCULO ---
if st.session_state.ultimo_calculo:
    calc = st.session_state.ultimo_calculo
    st.success(f"✅ ¡Añadido! **{calc['receta'].upper()}**: **{calc['total_huevos']:.1f} huevos**.")
    with st.expander("Ver desglose del último cálculo"):
        for m, cant in calc["desglose"].items():
            st.write(f"• **{cant}** molde(s) '{m}' × {MOLDES_HUEVOS[m]} = **{cant * MOLDES_HUEVOS[m]:.1f} huevos**")

# --- PASO 4: RESUMEN GENERAL ACUMULADO ---
if st.session_state.resumen_sesion:
    st.markdown("---")
    st.subheader("📊 Resumen Acumulado de la Jornada")
    
    total_jornada = 0.0
    resumen_por_receta = {}
    
    # Agrupar por receta
    for reg in st.session_state.resumen_sesion:
        rec = reg["receta"]
        h_total = reg["total_huevos"]
        resumen_por_receta[rec] = resumen_por_receta.get(rec, 0.0) + h_total
        total_jornada += h_total
        
    for rec, h_total in resumen_por_receta.items():
        st.write(f"• **{rec}**: {h_total:.1f} huevos")
        
    st.info(f"👉 **GRAN TOTAL DE LA SESIÓN:** **{total_jornada:.1f} huevos**")
    
    if st.button("🗑️ Reiniciar jornada / Borrar acumulado", use_container_width=True):
        st.session_state.resumen_sesion = []
        st.session_state.ultimo_calculo = None
        limpiar_cantidades()
        st.rerun()
