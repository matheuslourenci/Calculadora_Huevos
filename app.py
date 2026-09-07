import streamlit as st

# Configuración de la página
st.set_page_config(page_title="Calculadora de Repostería", page_icon="🎂", layout="centered")

# 1. Tabla de equivalencias de moldes y cantidad de huevos por unidad (ACTUALIZADA)
MOLDES_HUEVOS = {
    "Mini": 0.5,
    "Gris": 1.0,
    "15cm / ♡ P": 1.5,
    "20cm / ♡ L": 2.5,
    "25cm": 5.0
}

# 2. Lista de recetas disponibles
RECETAS = [
    "Vainilla",
    "Chocolate",
    "Red Velvet",
    "Carrot Cake",
    "Café",
    "Coco",
    "Limón",
    "Plátano"
]

# Inicializar la sesión para guardar el acumulado
if "resumen_sesion" not in st.session_state:
    st.session_state.resumen_sesion = {}

st.title("🎂 Calculadora de Repostería")

# --- PASO 1: SELECCIÓN DE RECETA ---
st.subheader("1. Selecciona la receta")
receta_seleccionada = st.selectbox("Receta:", RECETAS)

# --- PASO 2: CANTIDAD DE MOLDES ---
st.subheader("2. Moldes a producir")
cantidades = {}

# Mostramos los moldes en 2 columnas
cols = st.columns(2)
for i, (molde, valor_h) in enumerate(MOLDES_HUEVOS.items()):
    col = cols[i % 2]
    cantidades[molde] = col.number_input(
        label=f"Moldes '{molde}' ({valor_h} h/u):",
        min_value=0.0,
        value=0.0,
        step=0.5,
        format="%.1f",
        key=f"input_{molde}"
    )

# --- PASO 3: CÁLCULO ---
st.markdown("---")
if st.button("🧮 Calcular para esta receta", type="primary", use_container_width=True):
    total_huevos = sum(cantidades[m] * MOLDES_HUEVOS[m] for m in cantidades)
    
    if total_huevos > 0:
        # Guardar en el acumulado de la sesión
        if receta_seleccionada in st.session_state.resumen_sesion:
            st.session_state.resumen_sesion[receta_seleccionada] += total_huevos
        else:
            st.session_state.resumen_sesion[receta_seleccionada] = total_huevos
            
        st.success(f"**{receta_seleccionada.upper()}**: Necesitas **{total_huevos} huevos**.")
        
        # Detalle de lo seleccionado
        with st.expander("Ver desglose del cálculo"):
            for m, cant in cantidades.items():
                if cant > 0:
                    st.write(f"• **{cant}** molde(s) '{m}' × {MOLDES_HUEVOS[m]} = **{cant * MOLDES_HUEVOS[m]} huevos**")
    else:
        st.warning("Indica al menos 1 molde para realizar el cálculo.")

# --- PASO 4: RESUMEN GENERAL ACUMULADO ---
if st.session_state.resumen_sesion:
    st.markdown("---")
    st.subheader("📊 Resumen Acumulado de la Jornada")
    
    total_jornada = 0.0
    for rec, h_total in st.session_state.resumen_sesion.items():
        st.write(f"• **{rec}**: {h_total} huevos")
        total_jornada += h_total
        
    st.info(f"👉 **GRAN TOTAL:** **{total_jornada} huevos**")
    
    if st.button("🗑️ Reiniciar jornada / Borrar acumulado", use_container_width=True):
        st.session_state.resumen_sesion = {}
        st.rerun()
