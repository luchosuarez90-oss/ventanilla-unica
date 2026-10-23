  "Revisión manual",
        [d for d, _ in coincidencias],
        [p for _, palabras in coincidencias for p in palabras]
    )


st.title("📄 Ventanilla Única Municipal")
st.subheader("Clasificación preliminar de peticiones ciudadanas")

st.write(
    "Ingrese el asunto de una petición para obtener una sugerencia "
    "de la dependencia que podría atenderla."
)

st.info(
    "Prototipo académico basado en reglas y palabras clave. "
    "La clasificación no reemplaza la revisión de un funcionario."
)

asunto = st.text_area(
    "Asunto de la petición",
    placeholder="Ejemplo: Solicito pavimentación de la vía de mi barrio",
    height=120
)

if st.button("Clasificar petición", type="primary",
             use_container_width=True):
    if not asunto.strip():
        st.warning("Escriba el asunto antes de continuar.")
    else:
        resultado, coincidencias, palabras = sugerir_dependencia(asunto)

        st.divider()
        st.subheader("Resultado")

        if resultado == "Revisión manual":
            st.warning(
                "Se requiere revisión manual para evitar una asignación "
                "incorrecta."
            )

            if coincidencias:
                st.write("Áreas que podrían estar relacionadas:")
                for dependencia in coincidencias:
                    st.write(f"- {dependencia}")
            else:
                st.write(
                    "No se encontraron coincidencias en el catálogo actual."
                )
        else:
            st.success(f"Dependencia sugerida: {resultado}")

        if palabras:
            st.caption("Palabras clave encontradas: " + ", ".join(palabras))

        st.info(
            "La sugerencia es preliminar. Un funcionario autorizado "
            "debe revisar y confirmar la dependencia responsable."
        )

with st.expander("Consultar las dependencias incluidas"):
    for dependencia, palabras in REGLAS.items():
        st.markdown(f"**{dependencia}**")
        st.write(", ".join(palabras))

st.divider()
st.caption(
    "Prototipo académico. Las dependencias y reglas son de referencia "
    "y deben adaptarse a la estructura de cada entidad."
)
