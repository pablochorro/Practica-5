import streamlit as st
from config.conexion import obtener_conexion


def mostrar_examenes():
    st.header("Exámenes")

    # Formulario para registrar un examen
    with st.form("form_examen"):
        nombre = st.text_input("Nombre del examen")
        descripcion = st.text_input("Descripción")
        precio = st.number_input(
            "Precio",
            min_value=0.01,
            step=0.01
        )

        guardar = st.form_submit_button("Guardar examen")

    if guardar:
        if nombre.strip() == "":
            st.warning("Debe ingresar el nombre del examen.")

        else:
            conexion = None
            cursor = None

            try:
                conexion = obtener_conexion()

                if conexion is None:
                    return

                cursor = conexion.cursor()

                consulta = """
                    INSERT INTO EXAMEN
                    (Nombre, Descripcion, Precio)
                    VALUES (%s, %s, %s)
                """

                cursor.execute(
                    consulta,
                    (nombre.strip(), descripcion.strip(), float(precio))
                )

                conexion.commit()

                st.success("Examen registrado correctamente.")

            except Exception as error:
                if conexion is not None:
                    conexion.rollback()

                st.error(f"Error al registrar el examen: {error}")

            finally:
                if cursor is not None:
                    cursor.close()

                if conexion is not None and conexion.is_connected():
                    conexion.close()

    # Listado de exámenes
    st.subheader("Exámenes disponibles")

    conexion = None
    cursor = None

    try:
        conexion = obtener_conexion()

        if conexion is not None:
            cursor = conexion.cursor(dictionary=True)

            cursor.execute("""
                SELECT Id_Examen, Nombre, Descripcion, Precio
                FROM EXAMEN
            """)

            filas = cursor.fetchall()

            if filas:
                st.dataframe(filas, use_container_width=True)
            else:
                st.info("Aún no hay exámenes registrados.")

    except Exception as error:
        st.error(f"Error al consultar los exámenes: {error}")

    finally:
        if cursor is not None:
            cursor.close()

        if conexion is not None and conexion.is_connected():
            conexion.close()

