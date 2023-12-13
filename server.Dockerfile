FROM python:3.11-slim
WORKDIR /app
COPY src/quip_server/ /app/quip_server/
COPY src/quip_model/ /app/quip_model/
RUN apt-get update
RUN apt-get install python3-pygame -y
RUN python3 -m pip install flask vtece4564-gamelib requests pygame pyautogui

ENV DISPLAY=host.docker.internal:0.0

CMD ["/usr/local/bin/python3", "-m", "quip_server"]
