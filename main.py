import requests
import zipfile
import os
import subprocess
import time
import socket

server_properties_base={"server-name":"DK Bedrock Server",
        "gamemode":"survival",
        "difficulty":"easy",
        "allow-cheats":False,
        "max-players":10,
        "online-mode":False,
        "white-list":False,
        "server-port":19132}

class Server:
    
    ip=""
    state=False
    
    def __init__(self, server_url, server_dir="bedrock-server", server_properties=server_properties_base):
        self.server_url=server_url
        self.server_dir=server_dir
        self.server_properties=server_properties
        self.process=None

    def download_server(self):
#        url = "https://minecraft.azureedge.net/bin-win/bedrock-server-1.20.81.01.zip"
        response = requests.get(self.server_url)
        zip_path = f"{self.server_dir}.zip"
        with open(zip_path, "wb") as file:
            file.write(response.content)
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(self.server_dir)
        os.remove(zip_path)

    def create_server_properties(self):
        properties = "/n".join(f"{key}={value}" for key, value in self.server_properties.items())
        with open(f"{self.server_dir}/server.properties",  "w") as file:
            file.write(properties)

    def start_server(self):
        self.process = subprocess.Popen(['bedrock-server/bedrock_server'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("Minecraft Bedrock сервер начинает свою работу...")
        time.sleep(30)
        print("Сервер запущен!")
        print(f"Адресс сервера: {self.get_server_adress()}")
    

    def send_command(self, command):
        if self.process:
            self.process.stdin.write(f"{command}\n".encode())
            self.process.stdin.flush()
        
    def stop_server(self):
        if self.process:
            self.send_command("stop")
            self.process.wait()
            print("Cервер остановлен!")

    def get_local_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
        finally:
            s.close()
        return ip
    
   
    







# 



# send_command("say Сервер запущен!")

# local_ip = get_local_ip()
# port = 19132
# server_address = f"{local_ip}:{port}"
# print(f"Адресс сервера: {server_address}")


