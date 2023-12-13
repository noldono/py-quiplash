FROM python:3.11-slim
WORKDIR /app
COPY src/api/ /app/api/
COPY src/quip_server/ /app/quip_server/
COPY src/quip_model/ /app/quip_model/
RUN python3 -m pip install flask vtece4564-gamelib requests pygame pyautogui
CMD ["/usr/local/bin/python3", "-m", "api"]