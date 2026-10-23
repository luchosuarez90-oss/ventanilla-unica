import streamlit as st

st.set_page_config(
    page_title="Ventanilla Única",
    page_icon="📄",
    layout="centered"
)

REGLAS = {
    "Secretaría de Hacienda": [
        "impuesto", "predial", "tributario",
        "pago de impuestos"
    ],
    "Secretaría de Planeación": [
        "uso del suelo", "licencia de construcción",
        "mantenimiento de vía", "via rural",
        "infraestructura", "planeación"
    ],
    "Secretaría de Salud": [
        "salud", "hospital", "cita médica",
        "servicios de salud"
    ],
    "Secretaría de Gobierno": [
        "convivencia", "orden público",
        "seguridad ciudadana", "espacio público"
    ],
    "Secretaría General": [
        "copia de documento", "actualización de datos",
        "respuesta a petición anterior",
        "trámite administrativo", "servicios públicos",
        "programa social"
    ]
}

def sugerir_dependencia(asunto):
    if not isinstance(asunto, str) or not asunto.strip():
        return "Revisión manual"

    texto = asunto.lower()
    coincidencias = []

    for dependencia, palabras in REGLAS.items():
        if any(palabra in texto for palabra in palabras):
            coincidencias.append(dependencia)

    if len(coincidencias) == 1:
        return coincidencias[0]

    return "Revisión manual"


st.title("📄 Ventanilla Única")
st.subheader("Clasificación preliminar de peticiones")

st.write(
    "Escriba el asunto de la petición para obtener "
    "una sugerencia de dependencia."
)

asunto = st.text_area(
    "Asunto de la petición",
    placeholder="Ejemplo: Solicitud de revisión del impuesto predial"
)

if st.button("Clasificar petición", type="primary"):
    if not asunto.strip():
        st.warning("Escriba el asunto antes de continuar.")
    else:
        resultado = sugerir_dependencia(asunto)

        if resultado == "Revisión manual":
            st.warning(
                "La petición requiere revisión manual "
                "por un funcionario autorizado."
            )
        else:
            st.success(f"Dependencia sugerida: {resultado}")

        st.info(
            "Esta es una sugerencia preliminar. "
            "La asignación debe ser revisada y confirmada "
            "por un funcionario autorizado."
        )
