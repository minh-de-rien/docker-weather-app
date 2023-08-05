FROM python:3.9
WORKDIR /app/weather-server/
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
WORKDIR /app/weather-server/src
COPY src/ .
EXPOSE 5000
CMD [ "python3", "weather_server.py" ]