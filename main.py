import os
import uvicorn
from pyngrok import ngrok

from script.database import GPSDatabase
from script.app import App

NGROK_AUTH_PATH = "ngrok-auth.txt"

database = GPSDatabase()
app = App(database)

if __name__ == "__main__":
    host, port = '0.0.0.0', 9999
    public_url: ngrok.NgrokTunnel | None = None

    if os.path.exists(NGROK_AUTH_PATH):
        try:
            with open(NGROK_AUTH_PATH, 'r') as file:
                auth_token = file.read().strip()

            ngrok.set_auth_token(auth_token)
            public_url = ngrok.connect(str(port))

            print(
                f"Public URL: {public_url.public_url}\n",
                f"GPSLogger URL: {public_url.public_url}/api/gps"
            )
        except Exception as e:
            print("ngrok setup failed. defaulting to local network connections only.")
    else:
        print(f"{NGROK_AUTH_PATH} not found. defaulting to local network connections only.")

    try:
        uvicorn.run(app.fast_api, host=host, port=port)
    finally:
        if public_url and public_url.public_url:
            ngrok.disconnect(public_url.public_url)
            ngrok.kill()
