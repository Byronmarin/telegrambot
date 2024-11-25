import requests
import random
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, JobQueue
import asyncio

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

# Función que se ejecutará cada segundo
async def auto_send_star_wars_image(context: ContextTypes.DEFAULT_TYPE):
    # Chat ID proporcionado
    chat_id = 1191192549  # Aquí usamos el chat ID proporcionado
    image_url = get_random_star_wars_image()
    if image_url:
        await context.bot.send_photo(chat_id=chat_id, photo=image_url)

# Configuración del bot
if __name__ == "__main__":
    # Token de tu bot de Telegram
    app = ApplicationBuilder().token("7486157301:AAGKMaVYQbq1S-HizfhAoTK1BjglysCjCfU").build()

    # Agregar el manejador para el comando /starwars
    app.add_handler(CommandHandler("starwars", send_random_star_wars_image))  # Comando /starwars

    # Iniciar el JobQueue para programar la tarea periódica
    job_queue = JobQueue()
    job_queue.set_application(app)
    job_queue.run_repeating(auto_send_star_wars_image, interval=1, first=0)  # Cada segundo

    print("Bot corriendo...")
    app.run_polling()
