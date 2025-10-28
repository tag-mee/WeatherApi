from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, Response
import requests
from dicttoxml import dicttoxml

app = FastAPI()

API_KEY = "31371bc5c3msh34f399b07961d46p192883jsn2ba7562e3194"
API_HOST = "weatherapi-com.p.rapidapi.com"
API_URL = f"https://{API_HOST}/current.json"

HEADERS = {
    "X-RapidAPI-Key": API_KEY,
    "X-RapidAPI-Host": API_HOST
}


def fetch_weather(city: str) -> dict:

    params = {"q": city}
    response = requests.get(API_URL, headers=HEADERS, params=params)
    response.raise_for_status()
    data = response.json()

    return {
        "Weather": f"{data['current']['temp_c']} C",
        "Latitude": str(data['location']['lat']),
        "Longitude": str(data['location']['lon']),
        "City": f"{data['location']['name']} {data['location']['country']}"
    }


@app.post("/getCurrentWeather")
async def get_current_weather(request: Request):
    body = await request.json()
    city = body.get("city")
    output_format = body.get("output_format", "json").lower()

    if not city:
        return JSONResponse(status_code=400, content={"error": "City is required"})

    try:
        weather_data = fetch_weather(city)
    except requests.RequestException as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

    if output_format == "xml":
        xml_data = dicttoxml(weather_data, custom_root='root', attr_type=False)
        return Response(content=xml_data, media_type="application/xml")

    return JSONResponse(content=weather_data)