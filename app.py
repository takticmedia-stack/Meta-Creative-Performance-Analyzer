import streamlit as st
import pandas as pd
import plotly.express as px

# Configuración de la página
st.set_page_config(page_title="Meta Creative Performance Analyzer Dashboard", layout="wide")

# Inicializar o recuperar el estado de tipo_campaña
if 'tipo_campaña' not in st.session_state:
    st.session_state.tipo_campaña = "Ecommerce"

# ==============================================================================
# LAYOUT Y ESTILOS CSS (MEJORAS PROFESIONALES - ESTILO MINIMALISTA)
# ==============================================================================
st.markdown("""
<style>
/* 1. Tipografía y Tema General */
html, body, .stApp {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol";
    background-color: #ffffff; /* Fondo blanco puro */
    color: #1c1c1c; /* Texto principal gris oscuro profesional */
}
.stExpanderHeader {color: #1c1c1c !important;}
div[data-testid="stDataFrame"] {color: #1c1c1c;}
div[data-testid="stForm"] {background-color: #f7f9fc;}
div[data-testid="stRadio"] label {color: #1c1c1c;}
.stAlert {color: #1c1c1c !important;}

/* Encabezado sin fondo azul, centrado */
.hero-header-container {
    background-color: #ffffff; /* Fondo blanco */
    color: #1c1c1c; /* Texto oscuro */
    padding: 60px 0 30px 0; /* Padding ajustado */
    margin: -20px 0 0 0;
    text-align: center;
    box-shadow: none; /* Sin sombra para un look más limpio */
}

/* Tag "Meta Ads Analytics" */
.hero-tag {
    display: inline-block;
    background-color: #e6f0ff; /* Fondo azul muy claro */
    color: #004d99; /* Texto azul oscuro */
    padding: 8px 15px;
    border-radius: 20px;
    font-size: 0.9em;
    font-weight: 600;
    margin-bottom: 20px;
    backdrop-filter: none; /* Sin desenfoque */
    -webkit-backdrop-filter: none;
}
.hero-tag svg {
    vertical-align: middle;
    margin-right: 8px;
    font-size: 1.2em;
}

/* Título y subtítulo del hero-header */
.hero-title {
    font-size: 3.5rem;
    font-weight: 800;
    color: #1c1c1c; /* Negro para el título */
    margin-bottom: 15px;
    line-height: 1.2;
    letter-spacing: -1px;
}
.hero-subtitle {
    color: #4a4a4a; /* Gris oscuro para el subtítulo */
    font-size: 1.3rem;
    
    margin: 0 auto 30px auto;
    line-height: 1.5;
}

/* 3. Estilo de Contenedores y Carga de Archivos */
.file-uploader-title {
    font-size: 1.3rem;
    font-weight: 600;
    margin-top: 30px;
    margin-bottom: 15px;
    color: #1c1c1c;
    text-align: center;
}
.stFileUploader {
    border: 1px solid #e0e0e0; 
    border-radius: 12px;
    padding: 30px;
    text-align: center;
    background-color: #fcfcfc;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
    margin-top: 0px;
}
.business-type-label {
    font-size: 1.25rem;
    font-weight: 700;
    margin-bottom: 15px;
    color: #1c1c1c; /* Negro para el fondo blanco */
    text-align: center;
    margin-top: 30px;
}

/* 4. ESTILOS PARA LOS BOTONES DE SELECCIÓN */
div[data-testid="stColumn"] div.stButton > button {
    width: 100%;
    padding: 15px 20px;
    border-radius: 10px;
    border: 1px solid #cce0ff;
    background-color: #ffffff;
    color: #4a4a4a;
    font-weight: 600;
    font-size: 1.05rem;
    transition: all 0.2s;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

div[data-testid="stColumn"] div.stButton > button:hover:not(.active) {
    border-color: #007bff;
    color: #004d99;
    background-color: #f0f8ff;
}

div[data-testid="stColumn"] button.active {
    background-color: #e6f0ff !important;
    border: 7px solid #004d99 !important;
    color: #004d99 !important;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.25) !important;
    padding: 13px 18px;
}
            

/* 5. Estilo para las tarjetas de resultados (insights) */
.result-card {
    padding: 15px;
    border-radius: 10px;
    margin-bottom: 15px;
    color: white; /* Esto se ajustará por el color de la clase específica */
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    transition: transform 0.2s;
    border-left: 5px solid;
}
.result-card b {
    font-size: 1.1rem;
    font-weight: 700;
    display: block;
    margin-bottom: 5px;
}
/* Colores de las tarjetas con texto oscuro para fondo claro */
.color-Heroes { border-color: #28a745; background-color: #e9f7ec; color: #1e7e34; }
.color-Oportunidades { border-color: #17a2b8; background-color: #e9fafa; color: #0f6674; }
.color-Zombies { border-color: #ffc107; background-color: #fff9e6; color: #856404; }
.color-Villanos { border-color: #dc3545; background-color: #fcebeb; color: #a71d2a; }

.result-card .data-line {
    font-size: 0.95rem;
    color: #495057;
    line-height: 1.4;
}
.result-card i {
    font-size: 0.9em;
    display: block;
    margin-top: 8px;
    color: #6c757d;
}
.progress-bar-container {
    margin-top: 10px; 
    height: 10px; 
    background-color: #e9ecef; 
    border-radius: 5px; 
    overflow: hidden;
}
.progress-bar {
    height: 10px; 
    background-color: #007bff;
    border-radius: 5px;
}
.small-text {
    font-size: 0.8rem;
    color: #6c757d;
}

/* Ajuste de métricas */
div[data-testid="stMetricValue"] {
    font-size: 2.5rem !important;
    color: #004d99;
}
div[data-testid="stMetricLabel"] {
    font-size: 1rem;
    font-weight: 600;
    color: #5c5c5c;
}
</style>
""", unsafe_allow_html=True)

# Función de callback para cambiar el estado
def set_campaign_type(tipo):
    st.session_state.tipo_campaña = tipo

# ==============================================================================
# UI PRINCIPAL Y SELECCIÓN DE NEGOCIO
# ==============================================================================

# Encabezado "Hero" simplificado y centrado (ahora sin fondo de color)
st.markdown("""
<div class="hero-header-container">
    <div class="hero-tag">
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-bar-chart-fill" viewBox="0 0 16 16">
          <path d="M1 11a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v3a1 1 0 0 1-1 1H2a1 1 0 0 1-1-1zm5-4a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v7a1 1 0 0 1-1 1H7a1 1 0 0 1-1-1zm5-5a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v10a1 1 0 0 1-1 1h-2a1 1 0 0 1-1-1z"/>
        </svg>
       Descubre tus creatividades ganadoras
    </div>
    <h1 class="hero-title"> Meta Creative Performance Analyzer</h1>
    <p class="hero-subtitle">
        Sube tu export de Meta Ads y analiza instantáneamente qué creatividades generan el mejor ROAS.
        <br>
        Comienza seleccionando tu tipo de negocio abajo.
    </p>
""", unsafe_allow_html=True)

# Etiqueta "Tipo de Negocio"
st.markdown('<p class="business-type-label">Tipo de Negocio</p>', unsafe_allow_html=True)


# Contenedor para centrar los botones
col_l, col_center, col_r = st.columns([1, 2, 1])

with col_center:
    # Columnas para que los botones queden uno al lado del otro
    btn_col1, btn_col2 = st.columns([1, 1], gap="small")

    button_group_selector = '[data-testid="stHorizontalBlock"]:nth-of-type(1)' 

    js_code_template = f"""
    <script>
    function updateActiveButton() {{
        const buttonGroup = document.querySelector('{button_group_selector}');
        if (!buttonGroup) return;

        const buttons = buttonGroup.querySelectorAll('button');
        if (buttons.length < 2) return;

        const currentType = "{st.session_state.tipo_campaña}";

        buttons.forEach((button) => {{
            const buttonLabel = button.textContent.trim();
            let isTargetButton = false;
            
            if (currentType === "Ecommerce" && buttonLabel.includes("Ecommerce")) {{
                isTargetButton = true;
            }} else if (currentType === "Leads" && buttonLabel.includes("Leads")) {{
                isTargetButton = true;
            }}

            if (isTargetButton) {{
                button.classList.add('active');
            }} else {{
                button.classList.remove('active');
            }}
        }});
    }}

    setTimeout(updateActiveButton, 50);
    </script>
    """
    st.markdown(js_code_template, unsafe_allow_html=True)
    
    with btn_col1:
        st.button(
            label="🏠 Ecommerce", 
            key="btn_ecommerce", 
            on_click=set_campaign_type, 
            args=("Ecommerce",),
            help="Analizar campañas enfocadas en Compras (ROAS)",
            use_container_width=True
        )
             
    with btn_col2:
        st.button(
            label="👥 Leads", 
            key="btn_leads", 
            on_click=set_campaign_type, 
            args=("Leads",),
            help="Analizar campañas enfocadas en Resultados (CPL)",
            use_container_width=True
        )

# Cierre del div hero-header-container
st.markdown("</div>", unsafe_allow_html=True)

# Forzar a que Streamlit reconozca la variable de estado
tipo_campaña = st.session_state.tipo_campaña

# Área de subida de CSV
st.markdown('<p class="file-uploader-title">Sube tu CSV de Meta Ads</p>', unsafe_allow_html=True)
uploaded_file = st.file_uploader("", type="csv", help="Asegúrate de que tu CSV incluye las columnas de Nombre del Anuncio, Gasto, CPC, CTR y Resultados/Compras.")


# ==============================================================================
# LÓGICA DE ANÁLISIS (SIN CAMBIOS EN FUNCIONALIDAD)
# ==============================================================================

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # Columnas según tipo de campaña
    if tipo_campaña == "Leads":
        metric = "Resultados"
        cpc_col = "CPC (costo por clic en el enlace)"
        ctr_col = "CTR (porcentaje de clics en el enlace)"
        gasto_col = "Importe gastado (EUR)" 
    else:
        metric = "Compras"
        cpc_col = "CPC (costo por clic en el enlace)"
        ctr_col = "CTR (porcentaje de clics en el enlace)"
        roas_col = "ROAS (retorno de la inversión en publicidad)"
        gasto_col = "Importe gastado (EUR)" 

    # Validar columnas
    required_cols = ["Nombre del anuncio", metric, cpc_col, ctr_col, gasto_col]
    if tipo_campaña == "Ecommerce":
        required_cols.append(roas_col)
    
    # Comprobación de columnas y manejo de errores
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        st.error(f"Faltan las columnas obligatorias para '{tipo_campaña}': {', '.join(missing_cols)}")
        st.stop()


    # Filtrar filas vacías
    df = df[df[metric].notnull()]
    total_metric = df[metric].sum()
    df["Porcentaje del total"] = df[metric] / total_metric * 100

    # Medianas para evaluación
    costo_med = df[cpc_col].median()
    gasto_total = df[gasto_col].sum()

    # Clasificación Héroes / Oportunidades / Zombies / Villanos
    insights = []
    for i, row in df.iterrows():
        porcentaje = row["Porcentaje del total"]
        gasto_frac = row[gasto_col] / gasto_total if gasto_total > 0 else 0

        # Reglas de clasificación
        if porcentaje > 20:
            categoria = "Héroes"
            color = "color-Heroes" # Usamos la clase CSS
            texto = "Top volumen y CPC bajo → mantener y escalar."
        elif row[cpc_col] < costo_med and gasto_frac < 0.2:
            categoria = "Oportunidades"
            color = "color-Oportunidades" # Usamos la clase CSS
            texto = "Buen CPL y baja inversión → posible escalar."
        elif porcentaje < 5 and gasto_frac < 0.1 and row[cpc_col] < df[cpc_col].median() and row[ctr_col] > df[ctr_col].median():
            categoria = "Zombies"
            color = "color-Zombies" # Usamos la clase CSS
            texto = "Bajo volumen y gasto pero engagement alto → probar en testeo."
        else:
            categoria = "Villanos"
            color = "color-Villanos" # Usamos la clase CSS
            texto = "CPL alto o inversión considerable → revisar o evitar."

        roas_value = row[roas_col] if tipo_campaña == "Ecommerce" and roas_col in row else None

        insights.append({
            "Nombre": row["Nombre del anuncio"],
            metric: row[metric],
            "CPC": row[cpc_col],
            "CTR": row[ctr_col],
            "ROAS": roas_value,
            "Porcentaje del total": porcentaje,
            "Categoria": categoria,
            "ColorClass": color, # Almacenamos la clase CSS en lugar del código HEX
            "Texto": texto,
            "Gasto": row[gasto_col]
        })

    insights_df = pd.DataFrame(insights)

    # ==============================================================================
    # SECCIÓN DE RESULTADOS
    # ==============================================================================
    st.header(f"Resultados de Análisis ({tipo_campaña})")

    # Gráfico de secciones (Sección 1: Distribución)
    col_chart, col_summary = st.columns([2, 1])

    with col_chart:
        # Usaremos colores más limpios en el gráfico
        color_map={"Héroes":"#28a745","Oportunidades":"#17a2b8","Zombies":"#ffc107","Villanos":"#dc3545"}
        pie_counts = insights_df["Categoria"].value_counts().reset_index()
        pie_counts.columns = ["Categoria", "Cantidad"]
        fig = px.pie(
            pie_counts,
            names="Categoria",
            values="Cantidad",
            color="Categoria",
            color_discrete_map=color_map,
            title="Distribución de creatividades por categoría"
        )
        # Aseguramos un tema profesional y limpio para Plotly
        fig.update_layout(
            paper_bgcolor="#fcfcfc", 
            plot_bgcolor="white", 
            font_color="#1c1c1c",
            title_font_size=20,
            margin=dict(t=50, b=0, l=0, r=0)
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col_summary:
        st.subheader("Métricas Clave")
        st.metric(label=f"Total {metric}", value=f"{total_metric:,.0f}")
        # Formato a 2 decimales:
        st.metric(label="Gasto Total (€)", value=f"{gasto_total:,.2f} €")
        # Formato a 2 decimales:
        st.metric(label=f"Mediana {cpc_col}", value=f"{costo_med:,.2f}")
        if tipo_campaña == "Ecommerce":
            # Formato a 2 decimales:
            st.metric(label="ROAS Promedio", value=f"{insights_df['ROAS'].mean():,.2f}")


    st.markdown("---")
    st.subheader("Clasificación Detallada de Creatividades")

    # Mostrar tarjetas por categoría con desplegables
    for cat in ["Héroes", "Oportunidades", "Zombies", "Villanos"]:
        cat_df = insights_df[insights_df["Categoria"] == cat]
        
        # Mostrar siempre el expander
        with st.expander(f"✨ {cat} ({len(cat_df)} creatividades)", expanded=(cat=="Héroes")):
            if cat_df.empty:
                st.info("No hay creatividades en esta categoría.")
            else:
                for i, info in cat_df.iterrows():
                    # Formato a 2 decimales para ROAS, Gasto, CPC y CTR en la tarjeta
                    roas_text = f"| ROAS: {info['ROAS']:.2f}" if info.get("ROAS") is not None else ""
                    
                    st.markdown(
                        f"""
                        <div class="result-card {info['ColorClass']}">
                            <b>{info['Nombre']}</b>
                            <p class="data-line">
                                {metric}: {info[metric]} ({info['Porcentaje del total']:.1f}%) | Gasto: {info['Gasto']:.2f}€
                            </p>
                            <p class="data-line">
                                CPC: {info['CPC']:.2f} | CTR: {info['CTR']:.2f}% {roas_text}
                            </p>
                            <i>{info['Texto']}</i>
                            <div class="progress-bar-container">
                                <div class="progress-bar" style="width:{min(int(info['Porcentaje del total']),100)}%;"></div>
                            </div>
                            <small class="small-text">Porcentaje de {metric} del total: {info['Porcentaje del total']:.1f}%</small>
                        </div>
                        """, unsafe_allow_html=True
                    )

    # Tabla completa opcional
    with st.expander("Ver tabla completa"):
        # Formato del DataFrame para mostrar 2 decimales
        formatted_df = insights_df.copy()
        # Eliminamos la columna de ColorClass antes de mostrar la tabla
        formatted_df = formatted_df.drop(columns=['ColorClass'])
        
        for col in ["CPC", "CTR", "ROAS", "Gasto"]:
            if col in formatted_df.columns:
                formatted_df[col] = formatted_df[col].apply(lambda x: f"{x:,.2f}" if pd.notnull(x) else x)
        
        st.dataframe(formatted_df.sort_values(by=metric, ascending=False))