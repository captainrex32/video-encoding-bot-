# Video Encoder Telegram Bot

A Telegram bot that encodes videos using FFmpeg. Deploy it on Render to encode videos with default or custom settings.

## How to Set Up
1.  *Deploy to Render*:
   - Sign up at https://render.com.
   - Create a new Web Service, connect your GitHub repo, and select Docker.
   - Add these environment variables in Render:
     - API_ID: Your Telegram API ID.
     - API_HASH: Your Telegram API Hash.
     - BOT_TOKEN: Your bot’s token.
     - SUDO_USERS: Your Telegram User ID.
   - Deploy the service.

2. *Use the Bot*:
   - Start your bot on Telegram (e.g., @YourVideoEncoderBot).
   - Send /start to check if it works.
   - Send a video to encode it.
   - As admin, use /setcode to set custom FFmpeg commands (e.g., /setcode -c:v libx265 -crf 28 -preset fast).

## Notes
- Videos must be under 2GB (Telegram’s limit).
- Encoding takes time, especially on Render’s free tier.
- Only you (the admin) can set custom FFmpeg commands.

## License
MIT

## Features
- Custom encoding
- more features soon..
