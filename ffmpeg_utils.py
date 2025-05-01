import ffmpeg
import logging

logger = logging.getLogger(__name__)

def encode_video(input_path: str, output_path: str, custom_cmd: str = None) -> tuple[bool, str]:
    try:
        if not custom_cmd:
            custom_cmd = "c:v libx264 crf 23 preset fast"
        # Split the command into a list
        args = custom_cmd.split()
        # Convert to dictionary, removing leading dashes from keys
        ffmpeg_args = {}
        for i in range(0, len(args), 2):
            key = args[i].lstrip('-')  # Remove leading dash (e.g., "-c:v" -> "c:v")
            value = args[i + 1] if i + 1 < len(args) else None
            if value:
                ffmpeg_args[key] = value
        # Run FFmpeg
        stream = ffmpeg.input(input_path)
        stream = ffmpeg.output(stream, output_path, **ffmpeg_args, y="-y")
        ffmpeg.run(stream, quiet=True)
        return True, ""
    except ffmpeg.Error as e:
        logger.error(f"FFmpeg error: {e.stderr.decode()}")
        return False, e.stderr.decode()
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return False, str(e)
