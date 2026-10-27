import re
import unicodedata
import streamlit as st

st.set_page_config(page_title="Ventanilla Única Municipal", page_icon="📄", layout="centered")

# Catálogo académico de referencia. Ajustar a la estructura real del municipio.
REGLAS = {
    "Secretaría de Planeación": [
        "suelo", "uso del suelo", "uso de suelo", "ordenamiento territorial",
        "ordenamiento urbano", "POT", "planeación", "urbanismo",
        "licencia urbanística", "licencia de construcción", "permiso de construcción",
        "demolición", "subdivisión de predios", "lote", "predio",
        "desarrollo urbano", "expansión urbana", "estratificación",
        "nomenclatura", "norma urbanística", "plan de desarrollo",
        "legalización de barrio", "reconocimiento de edificación", "vivienda",
        "mejoramiento de vivienda", "vivienda rural", "déficit habitacional",
    ],
    "Secretaría de Obras Públicas e Infraestructura": [
        "vía", "vías", "vía rural", "vías rurales", "carretera", "carreteras",
        "pavimento", "pavimentación", "pavimentar", "reparación de vía",
        "arreglo de vía", "mantenimiento vial", "mantenimiento de vías",
        "mejoramiento vial", "bache", "baches", "hueco", "huecos",
        "placa huella", "puente", "puentes", "andén", "obra pública",
        "infraestructura vial", "maquinaria amarilla", "cuneta",
        "señalización vial", "camino veredal", "camino rural",
        "muro de contención", "derrumbe en vía", "rehabilitación vial",
        "reparcheo", "reparación de calle", "vía terciaria",
    ],
    "Secretaría de Hacienda": [
        "impuesto", "impuestos", "predial", "impuesto predial", "tributo",
        "tributario", "tesorería", "pago de impuestos", "deuda tributaria",
        "factura de impuesto", "liquidación de impuesto", "cobro de impuesto",
        "acuerdo de pago", "retención", "paz y salvo tributario", "recaudo",
        "industria y comercio", "ICA", "avalúo catastral", "exención tributaria",
        "devolución de pago", "multas tributarias", "calendario tributario",
        "declaración tributaria", "presupuesto municipal", "beneficio tributario",
    ],
    "Secretaría de Salud": [
        "salud", "vacuna", "vacunación", "hospital", "centro de salud",
        "puesto de salud", "cita médica", "atención médica", "salud pública",
        "jornada de salud", "brigada de salud", "prevención de enfermedades",
        "medicamentos", "control sanitario", "vigilancia epidemiológica",
        "saneamiento básico", "salud mental", "régimen subsidiado",
        "aseguramiento en salud", "dengue", "salud materna", "nutrición infantil",
        "EPS", "campaña de vacunación", "vacunación infantil", "atención primaria",
    ],
    "Secretaría de Gobierno": [
        "convivencia", "seguridad ciudadana", "orden público",
        "inspección de policía", "problema vecinal", "conflicto vecinal",
        "ruido excesivo", "perturbación de la tranquilidad", "amenaza",
        "ocupación del espacio público", "permiso para evento", "evento público",
        "horario de establecimiento", "control de ruido", "alteración del orden",
        "querella policiva", "mediación comunitaria", "venta ambulante",
        "seguridad", "inspector de policía", "conflicto comunitario",
    ],
    "Secretaría de Desarrollo Social": [
        "adulto mayor", "persona mayor", "tercera edad", "centro vida",
        "centro día", "discapacidad", "persona con discapacidad",
        "población vulnerable", "familias vulnerables", "ayuda humanitaria",
        "subsidio social", "programa social", "ayuda económica",
        "transferencia monetaria", "infancia", "niñez", "adolescencia",
        "juventud", "mujer cabeza de hogar", "violencia contra la mujer",
        "equidad de género", "habitante de calle", "pobreza extrema",
        "seguridad alimentaria", "comedor comunitario", "Renta Ciudadana",
        "víctimas del conflicto", "desplazamiento", "inclusión social",
        "junta de acción comunal", "mujer rural", "persona cuidadora",
    ],
    "Secretaría de Educación, Cultura y Deporte": [
        "educación", "colegio", "escuela", "matrícula escolar", "estudiante",
        "docente", "profesor", "transporte escolar", "alimentación escolar",
        "beca educativa", "biblioteca", "cultura", "evento cultural",
        "patrimonio cultural", "artesanía", "música", "deporte", "recreación",
        "cancha deportiva", "escenario deportivo", "polideportivo",
        "torneo deportivo", "escuela de formación", "danza", "teatro",
        "festival", "infraestructura educativa", "deserción escolar",
        "educación rural", "mantenimiento de colegio",
    ],
    "Secretaría de Agricultura y Ambiente": [
        "agricultura", "campesino", "cultivo", "cosecha",
        "asistencia técnica agropecuaria", "asistencia agrícola", "ganadería",
        "productor rural", "pequeño productor", "semillas", "plagas de cultivos",
        "riego agrícola", "distrito de riego", "comercialización agrícola",
        "protección ambiental", "árbol", "tala de árboles", "reforestación",
        "residuos sólidos", "reciclaje", "contaminación", "vertimiento",
        "fuente hídrica", "río", "quebrada", "fauna silvestre", "flora",
        "cambio climático", "educación ambiental", "bienestar animal",
        "protección animal", "deforestación", "compostaje",
    ],
    "Secretaría de Servicios Públicos": [
        "acueducto", "alcantarillado", "agua potable", "falta de agua",
        "corte de agua", "fuga de agua", "servicio de agua", "servicios públicos",
        "aseo municipal", "recolección de basura", "alumbrado público",
        "luminaria dañada", "luz de la calle", "energía eléctrica",
        "gas domiciliario", "recolección de residuos", "limpieza de calles",
        "barrido de calles", "disposición de residuos", "tarifa de aseo",
        "cobro de acueducto", "daño en tubería", "falta de alumbrado",
        "luminaria apagada",
    ],
    "Secretaría General y Atención Ciudadana": [
        "derecho de petición", "petición", "solicitud de información",
        "certificado", "constancia", "copia de documento", "actualización de datos",
        "radicado", "radicación", "archivo municipal", "trámite administrativo",
        "respuesta a petición", "queja administrativa", "reclamo administrativo",
        "atención al ciudadano", "ventanilla única", "notificación",
        "correspondencia", "certificado de residencia", "certificado laboral",
        "copia de resolución", "estado de trámite", "copia de expediente",
        "solicitud de copia", "información general",
    ],
}

def normalizar(texto):
    texto = texto.lower().strip()
    texto = unicodedata.normalize("NFD", texto)
    texto = "".join(c for c in texto if unicodedata.category(c) != "Mn")
    return re.sub(r"\s+", " ", texto)

def contiene_frase(texto, frase):
    patron = r"(?<!\w)" + re.escape(frase) + r"(?!\w)"
    return re.search(patron, texto) is not None

def sugerir_dependencia(asunto):
    if not isinstance(asunto, str) or not asunto.strip():
        return "Revisión manual", [], []
    texto = normalizar(asunto)
    coincidencias = []
    for dependencia, palabras in REGLAS.items():
        encontradas = [p for p in palabras if contiene_frase(texto, normalizar(p))]
        if encontradas:
            coincidencias.append((dependencia, encontradas))
    if len(coincidencias) == 1:
        dependencia, palabras = coincidencias[0]
        return dependencia, [dependencia], palabras
    dependencias = [d for d, _ in coincidencias]
    palabras = [p for _, lista in coincidencias for p in lista]
    return "Revisión manual", dependencias, palabras

st.title("📄 Ventanilla Única Municipal")
st.subheader("Clasificación preliminar de peticiones ciudadanas")
st.write("Escriba el asunto de una petición para obtener una sugerencia de dependencia.")
st.info("Prototipo académico basado en reglas y palabras clave. La sugerencia no reemplaza la revisión de un funcionario autorizado.")

asunto = st.text_area(
    "Asunto de la petición",
    placeholder="Ejemplo: Solicito pavimentación de la vía de mi barrio",
    height=120,
)

if st.button("Clasificar petición", type="primary", use_container_width=True):
    if not asunto.strip():
        st.warning("Escriba el asunto antes de continuar.")
    else:
        resultado, dependencias, palabras = sugerir_dependencia(asunto)
        st.divider()
        st.subheader("Resultado de la clasificación")
        if resultado == "Revisión manual":
            st.warning("Se requiere revisión manual para evitar una asignación incorrecta.")
            if dependencias:
                st.write("Áreas que podrían estar relacionadas:")
                for dependencia in dependencias:
                    st.write(f"- {dependencia}")
            else:
                st.write("No se encontraron coincidencias en el catálogo actual.")
        else:
            st.success(f"Dependencia sugerida: {resultado}")
        if palabras:
            st.caption("Palabras clave encontradas: " + ", ".join(palabras))
        st.info("La sugerencia es preliminar. Un funcionario autorizado debe revisar y confirmar la dependencia responsable.")

with st.expander("Consultar las dependencias incluidas"):
    for dependencia, palabras in REGLAS.items():
        st.markdown(f"**{dependencia}**")
        st.write(", ".join(palabras))

st.divider()
st.caption("Prototipo académico. Las dependencias y reglas son de referencia y deben adaptarse a la estructura de cada entidad.")
st.info(
    "Módulo académico para registrar y consultar peticiones. "
    "Utilice únicamente datos simulados mientras se configura "
    "la conexión segura con la base de datos."
)

st.subheader("Registrar una nueva petición")

with st.form("formulario_radicado"):
    numero_radicado = st.text_input(
        "Número de radicado",
        placeholder="Ejemplo: RAD-2026-001"
    )

    fecha_recepcion = st.date_input(
        "Fecha de recepción"
    )

    asunto_registro = st.text_area(
        "Asunto de la petición",
        placeholder="Escriba el asunto que se va a registrar"
    )

    dependencias_disponibles = list(REGLAS.keys()) + ["Revisión manual"]

    dependencia_registro = st.selectbox(
        "Dependencia responsable",
        options=dependencias_disponibles
    )

    estado_registro = st.selectbox(
        "Estado de la petición",
        options=[
            "Recibida",
            "En trámite",
            "Enviada",
            "Respondida",
            "Cerrada"
        ]
    )

    guardar_radicado = st.form_submit_button(
        "Guardar radicado",
        use_container_width=True
    )

if guardar_radicado:
    if not numero_radicado.strip():
        st.warning("Escriba el número de radicado.")
    elif not asunto_registro.strip():
        st.warning("Escriba el asunto de la petición.")
    else:
        st.warning(
            "El formulario está preparado, pero todavía no guarda "
            "registros en Supabase. Debemos completar la conexión "
            "y los permisos antes de habilitar el guardado."
        )
  st.warning(
            "El formulario está preparado, pero todavía no guarda "
            "registros en Supabase. Debemos completar la conexión "
            "y los permisos antes de habilitar el guardado."
        )
