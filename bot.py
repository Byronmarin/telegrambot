import requests
import random
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

# Función para obtener una imagen aleatoria de Star Wars desde Pixabay
def get_random_star_wars_image():
    url = f"https://pixabay.com/api/?key={PIXABAY_API_KEY}&q=star+wars&image_type=photo"
    response = requests.get(url)

    # Verificamos si la respuesta fue exitosa
    if response.status_code == 200:
        data = response.json()

        # Verificamos si hay resultados
        if data["hits"]:
            # Seleccionamos una imagen aleatoria de los resultados
            random_image = random.choice(data["hits"])  # Elige una imagen aleatoria de la lista
            return random_image["webformatURL"]  # URL de la imagen seleccionada
        else:
            print("No se encontraron imágenes.")
            return None
    else:
        print(f"Error al obtener la imagen: {response.status_code}")
        return None

# Comando para enviar una imagen aleatoria de Star Wars
async def send_random_star_wars_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    image_url = get_random_star_wars_image()
    if image_url:
        await update.message.reply_photo(image_url)
    else:
        await update.message.reply_text("Lo siento, no pude obtener una imagen. Intenta de nuevo más tarde.")

# Token de tu bot de Telegram
BOT_TOKEN = "7486157301:AAGKMaVYQbq1S-HizfhAoTK1BjglysCjCfU"

if __name__ == "__main__":
    # Inicia el servidor Flask en un hilo aparte
    threading.Thread(target=run_server).start()

    # Configuración y ejecución del bot de Telegram
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Agregar el manejador para el comando /starwars
    app.add_handler(CommandHandler("starwars", send_random_star_wars_image))  # Comando /starwars

    print("Bot corriendo...")
    app.run_polling()
