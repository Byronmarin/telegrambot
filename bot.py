import random
import aiohttp
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from flask import Flask
import threading

# Configuración del servidor Flask
app = Flask(__name__)

@app.route('/')
def home():
    return "El bot está activo."

def run_server():
    app.run(host='0.0.0.0', port=5000)

# Tu API Key de Pixabay
PIXABAY_API_KEY = "15904962-7777ccb3e4f3ad4e17d95f4df"

# Función asincrónica para obtener una imagen aleatoria basada en un tema desde Pixabay
async def get_random_image_by_topic(topic):
    url = f"https://pixabay.com/api/?key={PIXABAY_API_KEY}&q={topic}&image_type=photo"
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            # Verificamos si la respuesta fue exitosa
            if response.status == 200:
                data = await response.json()

                # Verificamos si hay resultados
                if data["hits"]:
                    # Seleccionamos una imagen aleatoria de los resultados
                    random_image = random.choice(data["hits"])
                    return random_image["webformatURL"]
                else:
                    print(f"No se encontraron imágenes para el tema: {topic}")
                    return None
            else:
                print(f"Error al obtener la imagen: {response.status}")
                return None

# Comando para enviar una imagen basada en un tema
async def send_image_by_topic(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:  # Verificamos si el usuario proporcionó un tema
        topic = " ".join(context.args)  # Combina palabras clave
        image_url = await get_random_image_by_topic(topic)
        if image_url:
            await update.message.reply_photo(image_url)
        else:
            await update.message.reply_text(f"Lo siento, no pude encontrar imágenes sobre el tema '{topic}'. Intenta con otro.")
    else:
        # Si no se proporciona un tema, el bot solicita uno
        await update.message.reply_text("Por favor, proporciona un tema para buscar imágenes. Ejemplo: /image naturaleza")

# Token de tu bot de Telegram (actualizado)
BOT_TOKEN = "7486157301:AAGKMaVYQbq1S-HizfhAoTK1BjglysCjCfU"

if __name__ == "__main__":
    # Inicia el servidor Flask en un hilo aparte
    threading.Thread(target=run_server).start()

    # Configuración y ejecución del bot de Telegram
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Agregar el manejador para el comando /image
    app.add_handler(CommandHandler("image", send_image_by_topic))  # Comando /image

    print("Bot corriendo...")
    app.run_polling()
