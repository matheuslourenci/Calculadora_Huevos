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

# Inicializar historial en la sesión
if "resumen_sesion" not in st.session_state:
    st.session_state.resumen_sesion = []

st.title("🎂 Calculadora de Repostería")

# --- PASO 1: SELECCIÓN DE RECETA ---
st.subheader("1. Selecciona la receta")
receta_seleccionada = st.selectbox("Receta:", RECETAS)

# --- PASO 2 Y 3: FORMULARIO DE MOLDES Y CÁLCULO ---
st.subheader("2. Moldes a producir")

# Usamos un formulario con clear_on_submit=True para que se limpien las casillas al enviar
with st.form(key="formulario_reposteria", clear_on_submit=True):
    cantidades = {}
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
    
    # Botón de envío del formulario
    boton_calcular = st.form_submit_button("🧮 Calcular y guardar para esta receta", type="primary", use_container_width=True)

# Lógica del cálculo tras pulsar el botón
if boton_calcular:
    total_huevos = sum(cantidades[m] * MOLDES_HUEVOS[m] for m in cantidades)
    
    if total_huevos > 0:
        desglose_moldes = {m: cant for m, cant in cantidades.items() if cant > 0}
        
        # Guardar registro en el historial de la sesión
        registro = {
            "receta": receta_seleccionada,
            "total_huevos": total_huevos,
            "desglose": desglose_moldes
        }
        st.session_state.resumen_sesion.append(registro)
        st.rerun()
    else:
        st.warning("Indica al menos 1 molde para realizar el cálculo.")

# --- RESULTADO DEL ÚLTIMO CÁLCULO ---
if st.session_state.resumen_sesion:
    ultimo = st.session_state.resumen_sesion[-1]
    st.success(f"✅ Añadido: **{ultimo['receta'].upper()}** ➔ **{ultimo['total_huevos']:.1f} huevos**.")
    with st.expander("Ver desglose del último cálculo"):
        for m, cant in ultimo["desglose"].items():
            st.write(f"• **{cant}** molde(s) '{m}' × {MOLDES_HUEVOS[m]} = **{cant * MOLDES_HUEVOS[m]:.1f} huevos**")

# --- PASO 4: RESUMEN GENERAL ACUMULADO DE LA JORNADA ---
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
        st.rerun()
