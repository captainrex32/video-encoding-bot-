import ffmpeg
import logging

logger = logging.getLogger(_name_)

def encode_video(input_path: str, output_path: str, custom_cmd: str = None) -> tuple[bool, str]:
    try:
        if not custom_cmd:
            custom_cmd = "-c:v libx264 -crf 23 -preset fast"
        args = custom_cmd.split()
        stream = ffmpeg.input(input_path)
        stream = ffmpeg.output(stream, output_path, **{k: v for k, v in zip(args[::2], args[1::2])}, y="-y")
        ffmpeg.run(stream, quiet=True)
        return True, ""
    except ffmpeg.Error as e:
        logger.error(f"FFmpeg error: {e.stderr.decode()}")
        return False, e.stderr.decode()
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return False, str(e)
