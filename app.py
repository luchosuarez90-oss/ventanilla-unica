import streamlit as st
import unicodedata

st.set_page_config(
    page_title="Ventanilla Única",
    page_icon="📄",
    layout="centered"
)

# Palabras clave para orientar las peticiones
REGLAS = {
    "Secretaría de Hacienda": [
        "impuesto", "predial", "tributario", "pago de impuestos",
        "deuda tributaria", "pago predial", "factura de impuesto",
        "liquidacion de impuesto", "cobro de impuesto",
        "acuerdo de pago", "retencion", "tesoreria"
    ],
    "Secretaría de Planeación": [
        "uso del suelo", "uso de suelo", "licencia de construccion",
        "permiso de construccion", "construccion de vivienda",
        "mantenimiento de via", "mantenimiento de vias",
        "via rural", "vias rurales", "reparacion de via",
        "reparacion de vias", "mejoramiento de via",
        "mejoramiento de vias", "carretera", "carreteras",
        "pavimentacion", "infraestructura", "planeacion",
        "ordenamiento territorial", "licencia urbanistica",
        "demarcacion", "anden", "alcantarillado",
        "acueducto", "vivienda", "obra publica",
        "espacio urbano", "esquema de ordenamiento"
    ],
    "Secretaría de Salud": [
        "salud", "hospital", "cita medica", "servicios de salud",
        "vacunacion", "saneamiento", "control sanitario",
        "centro de salud", "epidemia", "atencion medica",
        "salud publica", "medicamentos"
    ],
    "Secretaría de Gobierno": [
        "convivencia", "orden publico", "seguridad ciudadana",
        "espacio publico", "ruido", "alteracion del orden",
        "conflicto vecinal", "problemas de convivencia",
        "seguridad", "reunion comunitaria", "permiso de evento",
        "ocupacion del espacio publico", "inspeccion de policia"
    ],
    "Secretaría General": [
        "copia de documento", "actualizacion de datos",
        "respuesta a peticion anterior", "tramite administrativo",
        "servicios publicos", "programa social",
        "certificado", "constancia", "solicitud de informacion",
        "derecho de peticion", "radicado", "archivo",
        "documento administrativo", "copia de expediente",
        "atencion al ciudadano", "informacion general"
    ]
}


def normalizar(texto):
    texto = texto.lower().strip()
    texto = unicodedata.normalize("NFD", texto)
    return "".join(
        caracter for caracter in texto
        if unicodedata.category(caracter) != "Mn"
    )


def sugerir_dependencia(asunto):
    if not isinstance(asunto, str) or not asunto.strip():
        return "Revisión manual", []

    texto = normalizar(asunto)
    coincidencias = []

    for dependencia, palabras in REGLAS.items():
        for palabra in palabras:
            if normalizar(palabra) in texto:
                coincidencias.append(dependencia)
                break

    if len(coincidencias) == 1:
        return coincidencias[0], coincidencias

    return "Revisión manual", coincidencias


# Interfaz
st.title("📄 Ventanilla Única")
st.subheader("Clasificación preliminar de peticiones")

st.write(
    "Escriba el asunto de una petición ciudadana para obtener "
    "una sugerencia de la dependencia que podría atenderla."
)

st.info(
    "Este prototipo utiliza reglas y palabras clave. "
    "No reemplaza la revisión de un funcionario autorizado."
)

asunto = st.text_area(
    "Asunto de la petición",
    placeholder=(
        "Ejemplo: Solicitud de reparación de una vía rural "
        "en mal estado"
    ),
    height=120
)

if st.button("Clasificar petición", type="primary",
             use_container_width=True):

    if not asunto.strip():
        st.warning("Escriba el asunto antes de continuar.")

    else:
        resultado, coincidencias = sugerir_dependencia(asunto)

        st.divider()
        st.subheader("Resultado de la clasificación")

        if resultado == "Revisión manual":
            st.warning(
                "La petición requiere revisión manual por un "
                "funcionario autorizado."
            )

            if len(coincidencias) > 1:
                st.write(
                    "Se encontraron coincidencias en varias "
                    "dependencias:"
                )
                for dependencia in coincidencias:
                    st.write(f"- {dependencia}")

            elif len(coincidencias) == 1:
                st.write(
                    "Se encontró una coincidencia, pero no fue "
                    "suficiente para asignar la dependencia con "
                    "seguridad."
                )

            else:
                st.write(
                    "No se encontraron palabras clave conocidas. "
                    "Se recomienda revisar el asunto y ampliar "
                    "las reglas si es necesario."
                )

        else:
            st.success(f"Dependencia sugerida: {resultado}")

        st.caption(
            "La sugerencia es preliminar. La asignación definitiva "
            "debe ser revisada y confirmada por un funcionario "
            "autorizado."
        )

with st.expander("Consultar las áreas contempladas"):
    for dependencia in REGLAS:
        st.write(f"• {dependencia}")

st.divider()
st.caption(
    "Prototipo académico de apoyo a la orientación de peticiones. "
    "Los resultados dependen de las reglas programadas."
)
