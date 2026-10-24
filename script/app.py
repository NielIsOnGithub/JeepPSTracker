from fastapi import FastAPI, Request
from script.database import GPSDatabase

class App:
    def __init__(self, database: GPSDatabase) -> None:
        self.fast_api = FastAPI()
        self.database = database

        self.fast_api.add_api_route(
            path="/api/gps",
            endpoint=self.receive_gps_data,
            methods=["POST"]
        )

    async def receive_gps_data(self, request: Request):
        data = await request.json()

        try:
            device_id, device_type, latitude, longitude = data

            self.database.update(device_id, device_type, latitude, longitude)
                
            print(f"Received push from {device_id}: {latitude}, {longitude}")
            return {"status": "success", "message": "Location logged successfully"}
        except Exception as e:
            print(f"Error processing incoming phone stream: {e}")
            return {"status": "error", "message": str(e)}

