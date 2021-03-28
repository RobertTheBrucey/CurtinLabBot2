FROM python:3.8
RUN apt update && apt install -y libffi-dev iptables expect bash git && pip install discord paramiko
RUN git clone https://github.com/RobertTheBrucey/CurtinLabBot2.git && mv /CurtinLabBot2 /CurtinLabBot && cp /CurtinLabBot/BotFiles/BotFiles/start.sh /start.sh && chmod +x /start.sh
CMD ["/start.sh"]
