import streamlit as st
from groq import Groq

st.set_page_config(page_title="mi chat de ia", page_icon="😒")

#basic config
Modelo= ['llama-3.1-8b-instant', 'llama-3.3-70b-versatile', 'deepseek-r1-distill-llama-70b']
st.set_page_config(page_title="mi chat de ia", page_icon="6",layout="centered")

st.title("MI PRIMERA APP CON STREAMLIT")

nombre = st.text_input("¿cual es tu nombre?")

if  st.button("saludar"):
    st.write(f"hola, {nombre}!thx")

def configurar_pagina():
    st.title("mi chat de ia")
    st.sidebar.title("configuracion de la ia")

    elegirModelo = st.sidebar.selectbox('elegi un modelo', options=Modelo, index=0)

    return elegirModelo

def crear_usuario_groq():
    clave_secreta = st.secrets["CLAVE_API"]
    return Groq(api_key=clave_secreta)
# modelo =configurar_pagina()

def configurar_modelo(cliente, modelo, mensajeDeEntrada):
        return cliente.chat.completions.create(
            model=modelo,
            messages=[{"role": "user", "content": mensajeDeEntrada}],
            stream=True
        )


def inicializar_estado():
        if "mensajes" not in st.session_state:
            st.session_state.mensajes = []

def actualizar_historial(rol, contenido, avatar):
    st.session_state.mensajes.append({"role": rol, "content": contenido,
    "avatar":avatar})

def mostrar_historial():
    for mensaje in st.session_state.mensajes:
        with st.chat_message(mensaje["role"], avatar=mensaje["avatar"]):
            st.markdown(mensaje["content"])

def area_chat():
    contenedorDelChat = st.container(height=400,border=True)
    # Abrimos el contenedor del chat y mostramos el historial.
    with contenedorDelChat:
        mostrar_historial()

def generar_respuesta(chat_completo):
    respuesta_completa = ""
    for frase in chat_completo:
        if frase.choices[0].delta.content:
            respuesta_completa  += frase.choices[0].delta.content
            yield frase.choices[0].delta.content
    return  respuesta_completa
     
          
def main():
    modelo = configurar_pagina()
    clienteUsuario = crear_usuario_groq()
    inicializar_estado()
    area_chat() # Función de esta clase
    mensaje = st.chat_input("Escribí tu mensaje:")
    # print(mensaje)
    # Tomamos el mensaje del usuario por el input.

    # Verificamos que el mensaje no esté vacío antes de configurar el modelo

    if mensaje:
        actualizar_historial("user", mensaje, "💕")
        chat_completo = configurar_modelo(clienteUsuario, modelo,mensaje)
        if chat_completo:
            with  st.chat_message("assistant"):
                respuesta_completa  = st.write_stream(generar_respuesta(chat_completo))
                actualizar_historial("assistant", respuesta_completa, "🤖")
                st.rerun()

if __name__ == "__main__":
    main()


          