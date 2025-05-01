import os
import time
import threading
from http.server import HTTPServer, SimpleHTTPRequestHandler
import logging
from pyrogram import Client, filters
from pyrogram.types import Message
from dotenv import load_dotenv
from ffmpeg_utils import encode_video

# Dummy port binding to satisfy Render
class DummyHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.w_close()

port = int(os.getenv("PORT", 5000))
server = HTTPServer(("0.0.0.0", port), DummyHandler)
server_thread = threading.Thread(target=server.serve_forever)
server_thread.daemon = True
server_thread.start()

# Load environment variables
load_dotenv()

# Bot configuration
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
SUDO_USERS = [int(uid) for uid in os.getenv("SUDO_USERS", "").split()]
DOWNLOAD_DIR = os.getenv("DOWNLOAD_DIR", "./downloads")
ENCODE_DIR = os.getenv("ENCODE_DIR", "./encoded")

# Ensure directories exist
os.makedirs(DOWNLOAD_DIR, exist_ok=True)
os.makedirs(ENCODE_DIR, exist_ok=True)

# Initialize bot
app = Client("VideoEncoderBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Start command
@app.on_message(filters.command("start") & filters.private)
async def start(client, message: Message):
    await message.reply_text("Welcome to the Video Encoder Bot! Send a video to encode, or use /setcode to specify a custom FFmpeg command.")

# Set custom FFmpeg code
@app.on_message(filters.command("setcode") & filters.private & filters.user(SUDO_USERS))
async def set_code(client, message: Message):
    if len(message.command) > 1:
        custom_code = " ".join(message.command[1:])
        with open("ffmpeg_custom.txt", "w") as f:
            f.write(custom_code)
        await message.reply_text(f"Custom FFmpeg code set: `{custom_code}`")
    else:
        await message.reply_text("Please provide an FFmpeg command. Example: /setcode c:v libx264 crf 23 preset fast")

# Handle video uploads
@app.on_message(filters.video & filters.private)
async def handle_video(client, message: Message):
    try:
        # Download video
        file_path = await message.download(file_name=os.path.join(DOWNLOAD_DIR, f"{message.video.file_id}.mp4"))
        output_path = os.path.join(ENCODE_DIR, f"encoded_{message.video.file_id}.mp4")

        # Get custom FFmpeg code or use default
        ffmpeg_cmd = None
        if os.path.exists("ffmpeg_custom.txt"):
            with open("ffmpeg_custom.txt", "r") as f:
                ffmpeg_cmd = f.read().strip()

        # Encode video
        await message.reply_text("Encoding your video, please wait...")
        success, error = encode_video(file_path, output_path, ffmpeg_cmd)

        if success:
            # Send encoded video
            await client.send_video(
                chat_id=message.chat.id,
                video=output_path,
                caption="Here is your encoded video!"
            )
            # Clean up
            os.remove(file_path)
            os.remove(output_path)
        else:
            await message.reply_text(f"Encoding failed: {error}")
    except Exception as e:
        logger.error(f"Error processing video: {e}")
        await message.reply_text("An error occurred while processing your video.")

# Run the bot
if __name__ == "__main__":
    app.run()
