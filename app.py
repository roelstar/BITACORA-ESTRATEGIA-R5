import streamlit as st
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
from PIL import Image  # Para cargar el logo
import io
from fpdf import FPDF
df = pd.read_csv("operaciones.csv")


# ------------------- Configuración inicial -------------------
st.set_page_config(page_title="Bitácora Trading R5", layout="wide")

# Carga y muestra el logo
try:
    logo = Image.open("MiLogo.png")  # Cambia el nombre si tu archivo es otro
    st.image(logo, width=600)
except Exception as e:
    st.write("Logo no encontrado o error al cargar:", e)

# Título con fuente más pequeña
st.markdown(
    '<h2 style="font-size: 18px;">Bitácora Estrategia R5 By RoelStar (Ing. Rodolfo Ibarra Machuca)</h2>',
    unsafe_allow_html=True
)

# Archivos CSV
DATA_OPERACIONES = "operaciones.csv"
DATA_APORTES = "aportes_retiros.csv"

# ------------------- Inicializar DataFrames -------------------
try:
    df_operaciones = pd.read_csv(DATA_OPERACIONES)
except FileNotFoundError:
    df_operaciones = pd.DataFrame(columns=[
        "Fecha", "Hora", "Día", "Índice", "TipoOperacion",
        "StopLoss", "POI", "DondeCobre",
        "Lotaje", "Resultado", "ResultadoTipo",
        "ObsAntes", "ImgAntes", "ObsDespues", "ImgDespues"
    ])
    df_operaciones.to_csv(DATA_OPERACIONES, index=False)

try:
    df_aportes = pd.read_csv(DATA_APORTES)
except FileNotFoundError:
    df_aportes = pd.DataFrame(columns=["Fecha", "Tipo", "Monto"])
    df_aportes.to_csv(DATA_APORTES, index=False)

# ------------- Función para convertir Resultado a número -------------
def resultado_a_numero(x):
    try:
        return float(str(x).replace("+", "").strip())
    except:
        return 0.0

# ---------------- Registro Aportes / Retiros / Swaps ----------------
st.subheader("💵 Registro de Aportes, Retiros y Swaps")

with st.form("aporte_form", clear_on_submit=True):
    fecha_ap = st.date_input("Fecha del Movimiento")
    tipo_ap = st.radio("Tipo de Movimiento", ["Aporte", "Retiro", "Swap"])
    monto_ap = st.number_input("Monto ($)", value=0.0, format="%.2f")
    submitted_ap = st.form_submit_button("Registrar Movimiento")

if submitted_ap:
    nueva_ap = pd.DataFrame({"Fecha": [fecha_ap], "Tipo": [tipo_ap], "Monto": [monto_ap]})
    df_aportes = pd.concat([df_aportes, nueva_ap], ignore_index=True)
    df_aportes.to_csv(DATA_APORTES, index=False)
    st.success(f"✅ {tipo_ap} registrado correctamente.")

# ---------------- Registro Operaciones ----------------
st.subheader("📈 Registro de Nueva Operación")

with st.form("registro_form", clear_on_submit=True):
    col1, col2, col3 = st.columns(3)
    with col1:
        fecha = st.date_input("Fecha de la operación")
    with col2:
        hora = st.time_input("Hora (hh:mm)", value=datetime.now().time())
    with col3:
        dias_semana = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
        dia = st.selectbox("Día", dias_semana, index=datetime.now().weekday())

    indices_opciones = [
        "PAINX400", "PAINX600", "PAINX800", "PAINX999", "PAINX1200",
    "GAINX400", "GAINX600", "GAINX800", "GAINX999", "GAINX1200",
    "FLIPX1", "FLIPX2", "FLIPX3", "FLIPX4", "FLIPX5",
    "SFX VOL20", "SFX VOL40", "SFX VOL60", "SFX VOL80", "SFX VOL99",
    "FX VOL20", "FX VOL40", "FX VOL60", "FX VOL80", "FX VOL99",
    "CRASH300", "CRASH500", "CRASH600", "CRASH900", "CRASH1000",
    "BOOM300", "BOOM500", "BOOM600", "BOOM900", "BOOM1000",
    "STEP100.", "STEP200.", "STEP300.", "STEP400.", "STEP500.",
    "V.o.l.a.t.i.l.i.t.y.10 (1s)", "V.o.l.a.t.i.l.i.t.y.10", "V.o.l.a.t.i.l.i.t.y.100 (1s)", "V.o.l.a.t.i.l.i.t.y.100",
    "V.o.l.a.t.i.l.i.t.y.15 (1s)", "V.o.l.a.t.i.l.i.t.y.150 (1s)", "V.o.l.a.t.i.l.i.t.y.25 (1s)", "V.o.l.a.t.i.l.i.t.y.25",
    "V.o.l.a.t.i.l.i.t.y.250 (1s)", "V.o.l.a.t.i.l.i.t.y.30 (1s)", "V.o.l.a.t.i.l.i.t.y.50 (1s)", "V.o.l.a.t.i.l.i.t.y.50",
    "V.o.l.a.t.i.l.i.t.y.75 (1s)", "V.o.l.a.t.i.l.i.t.y.75", "V.o.l.a.t.i.l.i.t.y.90 (1s)",
    "DEX1500 DOWN", "DEX1500 UP", "DEX600 DOWN", "DEX600 UP",
    "DEX900 DOWN", "DEX900 UP",
    "D.r.i.f.t.Switch 10", "D.r.i.f.t.Switch 20", "D.r.i.f.t.Switch 30",
    "VolSwitch High", "VolSwitch Low", "VolSwitch Medium",
    "J.u.m.p.10", "J.u.m.p.100", "J.u.m.p.25", "J.u.m.p.50", "J.u.m.p.75",
    "C300", "C500", "C600", "C900", "C1000",
    "B300", "B500", "B600", "B900", "B1000",
    "VolFX20", "VolFX40", "VolFX60", "VolFX80", "VolFX99",
    "J10", "J100", "J25", "J50", "J75",
    "SpikeFX20", "SpikeFX40", "SpikeFX60", "SpikeFX80", "SpikeFX99",
    "V 10 (1s)", "V 10", "V 100 (1s)", "V 100",
    "V 15 (1s)", "V 150 (1s)", "V 25 (1s)", "V 25", "V 250 (1s)",
    "V 30 (1s)", "V 50 (1s)", "V 50", "V 75 (1s)", "V 75", "V 90 (1s)"

    ]
    indice = st.selectbox("Índice", indices_opciones)

    tipo_operacion = st.radio("Tipo de operación", ["Compra", "Venta"])

    col4, col5, col6 = st.columns(3)
    with col4:
        stop_loss = st.number_input("Stop Loss", value=0.0, format="%.2f")
    with col5:
        poi = st.number_input("POI (Precio objetivo)", value=0.0, format="%.2f")
    with col6:
        donde_cobre = st.number_input("Dónde cobré", value=0.0, format="%.2f")

    lotaje = st.number_input("Lotaje", value=0.0, format="%.2f")

    resultado_input = st.text_input("Resultado ($)")

    resultado_tipo = st.selectbox("Selecciona el tipo de resultado", ["SL", "Breakeven", "T.P.", "Manual"])

    obs_antes = st.text_area("Observaciones antes de operar")
    img_antes = st.text_input("Link imagen antes")
    obs_despues = st.text_area("Observaciones al cerrar")
    img_despues = st.text_input("Link imagen al cerrar")

    submitted = st.form_submit_button("Registrar operación")

if submitted:
    if resultado_input.strip() == "":
        st.error("❌ Debes ingresar el Resultado ($).")
    else:
        hora_str = hora.strftime("%H:%M")
        nueva = pd.DataFrame({
            "Fecha": [fecha],
            "Hora": [hora_str],
            "Día": [dia],
            "Índice": [indice],
            "TipoOperacion": [tipo_operacion],
            "StopLoss": [stop_loss],
            "POI": [poi],
            "DondeCobre": [donde_cobre],
            "Lotaje": [lotaje],
            "Resultado": [resultado_input],
            "ResultadoTipo": [resultado_tipo],
            "ObsAntes": [obs_antes],
            "ImgAntes": [img_antes],
            "ObsDespues": [obs_despues],
            "ImgDespues": [img_despues]
        })
        df_operaciones = pd.concat([df_operaciones, nueva], ignore_index=True)
        df_operaciones.to_csv(DATA_OPERACIONES, index=False)
        st.success(f"✅ Operación registrada correctamente con resultado tipo: {resultado_tipo}")

# ---------------- Dashboard General ----------------
st.subheader("📊 Dashboard General")

if df_operaciones.empty:
    st.info("No hay operaciones registradas aún.")
else:
    df_operaciones = df_operaciones.copy()
    df_operaciones["FechaHora"] = pd.to_datetime(df_operaciones["Fecha"].astype(str) + " " + df_operaciones["Hora"])
    df_operaciones = df_operaciones.sort_values("FechaHora")

    df_operaciones["Resultado_num"] = df_operaciones["Resultado"].apply(resultado_a_numero)

    if not df_aportes.empty:
        df_aportes["Fecha"] = pd.to_datetime(df_aportes["Fecha"])
        aportes_total = df_aportes[df_aportes["Tipo"] == "Aporte"]["Monto"].sum()
        retiros_total = df_aportes[df_aportes["Tipo"] == "Retiro"]["Monto"].sum()
        swaps_total = df_aportes[df_aportes["Tipo"] == "Swap"]["Monto"].sum()
    else:
        aportes_total = 0.0
        retiros_total = 0.0
        swaps_total = 0.0

    operaciones_ganancia = df_operaciones["Resultado_num"].sum()

    saldo_actual = aportes_total - retiros_total - swaps_total + operaciones_ganancia

    if aportes_total > 0:
        rentabilidad_pct = ((saldo_actual - aportes_total) / aportes_total) * 100
    else:
        rentabilidad_pct = 0.0

    total_ops = len(df_operaciones)
    conteo_tipo = df_operaciones["ResultadoTipo"].value_counts()
    ticket_medio = operaciones_ganancia / total_ops if total_ops > 0 else 0.0
    efectividad = (conteo_tipo.get("T.P.", 0) / total_ops) * 100 if total_ops > 0 else 0.0
    eficiencia = (df_operaciones[df_operaciones["Resultado_num"] > 0].shape[0] / total_ops) * 100 if total_ops > 0 else 0.0

    st.write("### Resumen Financiero General")
    st.write(f"💰 **Aporte total:** ${aportes_total:.2f}")
    st.write(f"🔻 **Retiros totales:** -${retiros_total:.2f}")
    st.write(f"🔻 **Swaps totales:** -${swaps_total:.2f}")
    st.write(f"📈 **Ganancia/Pérdida operaciones:** ${operaciones_ganancia:.2f}")
    st.write(f"💵 **Saldo actual (capital real):** ${saldo_actual:.2f}")
    st.write(f"📊 **Rentabilidad acumulada:** {rentabilidad_pct:.2f}%")

    st.line_chart(df_operaciones.set_index("FechaHora")["Resultado_num"].cumsum())

# ---------------- Resumen Anual ----------------
st.subheader("📅 Resumen Anual (solo operaciones)")

if not df_operaciones.empty:
    df_operaciones["Año"] = pd.to_datetime(df_operaciones["Fecha"]).dt.year

    años_disponibles = sorted(df_operaciones["Año"].unique())
    año_seleccionado = st.selectbox("Selecciona año para resumen anual", años_disponibles, key="año_resumen_anual")

    resumen_anual = df_operaciones[df_operaciones["Año"] == año_seleccionado].copy()

    total_ops_anual = len(resumen_anual)
    ganancia_anual = resumen_anual["Resultado_num"].sum()
    ticket_medio_anual = ganancia_anual / total_ops_anual if total_ops_anual > 0 else 0.0
    efectividad_anual = (resumen_anual[resumen_anual["ResultadoTipo"] == "T.P."].shape[0] / total_ops_anual) * 100 if total_ops_anual > 0 else 0.0
    eficiencia_anual = (resumen_anual[resumen_anual["Resultado_num"] > 0].shape[0] / total_ops_anual) * 100 if total_ops_anual > 0 else 0.0

    st.write(f"📅 **Año {año_seleccionado}**")
    st.write(f"- Total operaciones: {total_ops_anual}")
    st.write(f"- Ganancia neta: ${ganancia_anual:.2f}")
    st.write(f"- Ticket medio: ${ticket_medio_anual:.2f}")
    st.write(f"- Efectividad (T.P.): {efectividad_anual:.2f}%")
    st.write(f"- Eficiencia: {eficiencia_anual:.2f}%")

    be_ano = resumen_anual[resumen_anual["ResultadoTipo"] == "Breakeven"].shape[0]
    ganadas_ano = resumen_anual[(resumen_anual["Resultado_num"] > 0) & (resumen_anual["ResultadoTipo"] != "Breakeven")].shape[0]
    perdidas_ano = resumen_anual[resumen_anual["Resultado_num"] < 0].shape[0]

    porc_ganadas_ano = (ganadas_ano / total_ops_anual * 100) if total_ops_anual else 0
    porc_perdidas_ano = (perdidas_ano / total_ops_anual * 100) if total_ops_anual else 0
    porc_be_ano = (be_ano / total_ops_anual * 100) if total_ops_anual else 0

    st.markdown(f"""
    **📌 Distribución anual de operaciones:**
    - 🟢 Ganadas: **{porc_ganadas_ano:.2f}%**
    - 🔴 Perdidas: **{porc_perdidas_ano:.2f}%**
    - ⚪ Breakeven: **{porc_be_ano:.2f}%**
    """)

    st.line_chart(resumen_anual.set_index("FechaHora")["Resultado_num"].cumsum())

    comentario_anual = ""

    if efectividad_anual < 40:
        comentario_anual += "⚠️ La efectividad (T.P.) es baja. Se recomienda revisar la estrategia de entrada para mejorar tasa de aciertos.\n"
    else:
        comentario_anual += "✅ La efectividad (T.P.) es aceptable.\n"

    if eficiencia_anual < 50:
        comentario_anual += "⚠️ La eficiencia (operaciones positivas) es baja. Considera mejorar la gestión de riesgo y filtros para reducir pérdidas.\n"
    else:
        comentario_anual += "✅ La eficiencia es buena.\n"

    if ticket_medio_anual < 10:
        comentario_anual += "⚠️ Ticket medio bajo; ganancias pequeñas por operación. Podrías evaluar ajustar objetivos o tamaños de posición.\n"
    else:
        comentario_anual += "✅ Ticket medio adecuado para la estrategia.\n"

    st.markdown("#### 📌 Comentarios Técnicos Anuales:")
    st.text(comentario_anual)

# ----------- Resumen Mensual -----------
st.subheader("📆 Resumen mensual")

df_operaciones["Mes"] = pd.to_datetime(df_operaciones["Fecha"]).dt.month

año_selec = st.selectbox("Selecciona año para resumen mensual", sorted(df_operaciones["Año"].unique()), index=0, key="año_selec_mes")
mes_selec = st.selectbox("Selecciona mes para resumen mensual", list(range(1,13)), index=datetime.now().month-1, key="mes_selec_mes")

filtro_mes = df_operaciones[(df_operaciones["Año"]==año_selec) & (df_operaciones["Mes"]==mes_selec)]

meses = ["", "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
         "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]

if filtro_mes.empty:
    st.warning("No hay operaciones ese mes.")
else:
    total_ops = len(filtro_mes)
    ganancia = filtro_mes["Resultado_num"].sum()
    ticket_medio = ganancia / total_ops if total_ops > 0 else 0.0
    efectividad = (filtro_mes[filtro_mes["ResultadoTipo"]=="T.P."].shape[0]/total_ops)*100
    eficiencia = (filtro_mes[filtro_mes["Resultado_num"]>0].shape[0]/total_ops)*100

    conteo_tipos = filtro_mes["ResultadoTipo"].value_counts()

    st.write(f"📅 **{meses[mes_selec]} {año_selec}**")
    st.write(f"- Total operaciones: {total_ops}")
    st.write(f"- Ganancia neta: ${ganancia:.2f}")
    st.write(f"- Ticket medio: ${ticket_medio:.2f}")
    st.write(f"- Efectividad (T.P.): {efectividad:.2f}%")
    st.write(f"- Eficiencia: {eficiencia:.2f}%")

    # Total operaciones del mes
    total_ops_mes = len(filtro_mes)

    # Cantidad de breakeven basado en tipo "B.E."
    be_mes = filtro_mes[filtro_mes["ResultadoTipo"] == "B.E."].shape[0]

    # Cantidad de ganadas: resultado positivo (mayor que 0) y que no sean breakeven
    ganadas_mes = filtro_mes[(filtro_mes["Resultado_num"] > 0) & (filtro_mes["ResultadoTipo"] != "B.E.")].shape[0]

    # Cantidad de perdidas: resultado negativo (menor que 0)
    perdidas_mes = filtro_mes[filtro_mes["Resultado_num"] < 0].shape[0]

    # Porcentajes mensuales
    porc_ganadas_mes = (ganadas_mes / total_ops_mes * 100) if total_ops_mes else 0
    porc_perdidas_mes = (perdidas_mes / total_ops_mes * 100) if total_ops_mes else 0
    porc_be_mes = (be_mes / total_ops_mes * 100) if total_ops_mes else 0

    st.markdown(f"""
    **📌 Distribución mensual de operaciones:**
    - 🟢 Ganadas: **{porc_ganadas_mes:.2f}%**
    - 🔴 Perdidas: **{porc_perdidas_mes:.2f}%**
    - ⚪ Breakeven: **{porc_be_mes:.2f}%**
    """)

    st.write("#### 📋 Distribución de resultados:")
    st.write(f"✅ T.P.: {conteo_tipos.get('T.P.',0)}")
    st.write(f"❌ SL: {conteo_tipos.get('SL',0)}")
    st.write(f"🔹 Breakeven: {conteo_tipos.get('Breakeven',0)}")
    st.write(f"✏️ Manual: {conteo_tipos.get('Manual',0)}")

    st.write("#### 📊 Índices operados en el mes:")

    conteo_indices = (
        filtro_mes["Índice"]
        .value_counts()
        .reset_index()
    )
    conteo_indices.columns = ["Índice", "Cantidad"]
    conteo_indices["Cantidad"] = conteo_indices["Cantidad"].astype(int)
    conteo_indices["Porcentaje"] = (conteo_indices["Cantidad"] / total_ops * 100).round(2)

    st.table(conteo_indices)

    if not conteo_indices.empty:
        indice_mas_operado = conteo_indices.iloc[0]["Índice"]
        cantidad_mas_operado = conteo_indices.iloc[0]["Cantidad"]
        porcentaje_mas_operado = conteo_indices.iloc[0]["Porcentaje"]

        st.write("#### 📊 Índice más operado en el mes:")
        st.write(f"- **{indice_mas_operado}** con {cantidad_mas_operado} operaciones ({porcentaje_mas_operado:.2f}% del total)")

    st.line_chart(filtro_mes.set_index("FechaHora")["Resultado_num"].cumsum())

    # Comentarios técnicos para resumen mensual
    comentario_mensual = ""

    if efectividad < 40:
        comentario_mensual += "⚠️ Efectividad mensual baja, se sugiere analizar condiciones de entrada y optimizar filtros.\n"
    else:
        comentario_mensual += "✅ Efectividad mensual aceptable.\n"

    if eficiencia < 50:
        comentario_mensual += "⚠️ Eficiencia mensual baja, considerar ajustes en gestión de pérdidas y stops.\n"
    else:
        comentario_mensual += "✅ Eficiencia mensual adecuada.\n"

    if ticket_medio < 10:
        comentario_mensual += "⚠️ Ticket medio mensual bajo; analizar tamaño de posición y objetivos.\n"
    else:
        comentario_mensual += "✅ Ticket medio mensual positivo.\n"

    st.markdown("#### 📌 Comentarios Técnicos Mensuales:")
    st.text(comentario_mensual)

# ---------------- Tabla operaciones mes seleccionado ----------------
if not df_operaciones.empty:
    filtro_mes_tabla = filtro_mes.copy()
    filtro_mes_tabla_display = filtro_mes_tabla[[
        "Fecha", "Hora", "Día", "Índice", "TipoOperacion", "StopLoss",
        "POI", "DondeCobre", "Lotaje", "Resultado", "ResultadoTipo",
        "ObsAntes", "ImgAntes", "ObsDespues", "ImgDespues"
    ]]
    st.subheader("📄 Tabla resumen operaciones mes seleccionado")
    st.dataframe(filtro_mes_tabla_display)

# ---------------- Gráficas comparativas por año ----------------
st.subheader("📊 Evolución mensual durante el año")

if not df_operaciones.empty:
    # Crear columnas de año y mes si no existen
    if "Año" not in df_operaciones.columns:
        df_operaciones["Año"] = pd.to_datetime(df_operaciones["Fecha"]).dt.year
    if "Mes" not in df_operaciones.columns:
        df_operaciones["Mes"] = pd.to_datetime(df_operaciones["Fecha"]).dt.month

    año_seleccion = st.selectbox(
        "Selecciona el año para comparar evolución mensual",
        sorted(df_operaciones["Año"].unique())
    )

    # Filtrar el año seleccionado
    df_anual = df_operaciones[df_operaciones["Año"] == año_seleccion].copy()

    # Agrupar por mes
    resumen_mensual = df_anual.groupby("Mes").agg(
        Ganancia_Neta=("Resultado_num", "sum"),
        Ticket_Medio=("Resultado_num", lambda x: x.sum() / len(x) if len(x) > 0 else 0),
        Efectividad=("ResultadoTipo", lambda x: (x.eq("T.P.").sum() / len(x))*100 if len(x) > 0 else 0)
    ).reset_index()

    # Asegurar que todos los meses aparezcan (1 al 12)
    todos_meses = pd.DataFrame({"Mes": range(1, 13)})
    resumen_mensual = todos_meses.merge(resumen_mensual, on="Mes", how="left").fillna(0)

    # Etiquetas de meses
    meses = [
        "Ene", "Feb", "Mar", "Abr", "May", "Jun",
        "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"
    ]
    resumen_mensual["Mes_nombre"] = resumen_mensual["Mes"].apply(lambda x: meses[x-1])

    # Mostrar gráficas en 3 columnas
    col1, col2, col3 = st.columns(3)

    with col1:
        st.write("📈 **Ganancia Neta por Mes**")
        st.bar_chart(data=resumen_mensual.set_index("Mes_nombre")["Ganancia_Neta"])

    with col2:
        st.write("💵 **Ticket Medio por Mes**")
        st.bar_chart(data=resumen_mensual.set_index("Mes_nombre")["Ticket_Medio"])

    with col3:
        st.write("🎯 **Efectividad (%) por Mes**")
        st.bar_chart(data=resumen_mensual.set_index("Mes_nombre")["Efectividad"])


# ---------------- Exportar Reporte PDF ----------------
from fpdf import FPDF

st.subheader("📥 Exportar reportes PDF")

if not df_operaciones.empty:
    if st.button("Exportar reporte mensual en PDF"):
        # Obtener el mes seleccionado
        mes_nombre = meses[mes_selec - 1]

        # Crear tabla de índices usados
        conteo_indices = (
            filtro_mes["Índice"]
            .value_counts()
            .reset_index()
        )
        conteo_indices.columns = ["Índice", "Cantidad"]

        # Convertir a numérico para evitar errores en operaciones
        conteo_indices["Cantidad"] = pd.to_numeric(conteo_indices["Cantidad"], errors='coerce').fillna(0)

        conteo_indices["Porcentaje"] = (conteo_indices["Cantidad"] / total_ops * 100).round(2)

        # Crear PDF
        pdf = FPDF()
        pdf.add_page()

        # Intentar poner logo arriba
        try:
            pdf.image("MiLogo.png", x=60, y=8, w=103)  # Ajusta tamaño y posición si quieres
        except Exception as e:
            pass  # Si no hay logo o error, no pasa nada

        pdf.set_font("Arial", "B", 16)
        pdf.cell(0, 50, "Reporte Mensual - Bitácora Trading R5", ln=True, align="C")

        pdf.set_font("Arial", "", 12)
        pdf.ln(5)
        pdf.cell(0, 10, f"Mes: {mes_nombre} {año_selec}", ln=True)
        pdf.cell(0, 10, f"Total operaciones: {total_ops}", ln=True)
        pdf.cell(0, 10, f"Ganancia neta: ${ganancia:.2f}", ln=True)
        pdf.cell(0, 10, f"Saldo actual calculado: ${saldo_actual:.2f}", ln=True)
        pdf.cell(0, 10, f"Ticket medio: ${ticket_medio:.2f}", ln=True)
        pdf.cell(0, 10, f"Efectividad (T.P.): {efectividad:.2f}%", ln=True)
        pdf.cell(0, 10, f"Eficiencia: {eficiencia:.2f}%", ln=True)
        pdf.cell(0, 10, f"Índice más operado: {conteo_indices.iloc[0]['Índice']}", ln=True)

        pdf.ln(5)
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 10, "Distribución de resultados:", ln=True)
        pdf.set_font("Arial", "", 12)
        pdf.cell(0, 10, f"T.P.: {conteo_tipos.get('T.P.', 0)}", ln=True)
        pdf.cell(0, 10, f"SL: {conteo_tipos.get('SL', 0)}", ln=True)
        pdf.cell(0, 10, f"Breakeven: {conteo_tipos.get('Breakeven', 0)}", ln=True)
        pdf.cell(0, 10, f"Manual: {conteo_tipos.get('Manual', 0)}", ln=True)

        pdf.ln(5)
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 10, "Índices operados:", ln=True)
        pdf.set_font("Arial", "", 12)

        for idx, row in conteo_indices.iterrows():
            pdf.cell(0, 10, f"- {row['Índice']}: {row['Cantidad']} ({row['Porcentaje']}%)", ln=True)

        # Obtener contenido PDF como bytes
        pdf_bytes = pdf.output(dest="S").encode("latin1")

        # Descargar con Streamlit
        st.download_button(
            label="📄 Descargar PDF",
            data=pdf_bytes,
            file_name=f"reporte_{mes_nombre}_{año_selec}.pdf",
            mime="application/pdf"
        )

# ---------------- Eliminar Operaciones ----------------
st.subheader("🗑️ Eliminar una operación registrada")

if not df_operaciones.empty:
    # Creamos un selector con el índice y un resumen de cada operación
    df_operaciones_reset = df_operaciones.reset_index(drop=False)
    df_operaciones_reset["Resumen"] = (
        df_operaciones_reset["index"].astype(str) + " | " +
        df_operaciones_reset["Fecha"].astype(str) + " - " +
        df_operaciones_reset["Índice"].astype(str) + " - " +
        df_operaciones_reset["ResultadoTipo"].astype(str) + " ($" +
        df_operaciones_reset["Resultado"].astype(str) + ")"
    )

    seleccion = st.selectbox(
        "Selecciona una operación para eliminar",
        options=[""] + df_operaciones_reset["Resumen"].tolist()
    )

    if seleccion != "":
        idx_str = seleccion.split(" | ")[0]
        idx = int(idx_str)

        if st.button("❌ Confirmar eliminación de esta operación"):
            df_operaciones = df_operaciones.drop(index=idx).reset_index(drop=True)
            df_operaciones.to_csv(DATA_OPERACIONES, index=False)
            st.success("✅ Operación eliminada correctamente.")
            st.experimental_rerun()


import streamlit as st
import pandas as pd

# Cargar el archivo CSV
archivo = "operaciones.csv"
df = pd.read_csv(archivo)

st.subheader("📸 Visualizar Imágenes de las Operaciones")

# Verificar columnas que contienen imágenes
columnas_imagen = [col for col in df.columns if "img" in col.lower() or "imagen" in col.lower()]

if not columnas_imagen:
    st.warning("No se encontraron columnas con enlaces de imagen.")
else:
    fila_max = len(df) - 1  # Porque si empiezas desde 0, el máximo es len - 1
    fila_seleccionada = st.number_input(
        "Selecciona el número de fila para ver imágenes",
        min_value=0,
        max_value=fila_max,
        step=1
    )

    index = fila_seleccionada  # Ya coincide directamente

    for columna in columnas_imagen:
        enlace = df.at[index, columna] if columna in df.columns else None

        st.markdown(f"### 🔹 {columna} (Fila {fila_seleccionada})")

        if pd.notna(enlace) and isinstance(enlace, str) and enlace.startswith("http"):
            st.image(enlace, caption=columna, use_container_width=True)
            st.markdown(f"[🔗 Abrir imagen en nueva pestaña]({enlace})", unsafe_allow_html=True)
        else:
            st.info("No hay imagen válida en esta celda.")
