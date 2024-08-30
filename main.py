import argparse
import requests
import zipfile
import os
import shutil
import subprocess
import time
import socket
import json

server_properties_base = {
    "server-name": "DK Bedrock Server",
    "gamemode": "survival",
    "difficulty": "easy",
    "allow-cheats": False,
    "max-players": 10,
    "online-mode": False,
    "white-list": False,
    "server-port": 19132
}

class MinecraftServer:
    def __init__(self, server_dir="bedrock-server", server_properties=server_properties_base):
        self.server_dir = server_dir
        self.server_properties = server_properties
        self.process = None
        self.updater = MinecraftUpdater(server_dir=server_dir)
    
    def create_server_properties(self):
        properties = "\n".join(f"{key}={value}" for key, value in self.server_properties.items())
        with open(f"{self.server_dir}/server.properties", "w") as file:
            file.write(properties)

    def start_server(self):
        self.process = subprocess.Popen([f'{self.server_dir}/bedrock_server'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("Minecraft Bedrock сервер начинает свою работу...")
        time.sleep(30)
        print("Сервер запущен!")
        print(f"Адрес сервера: {self.get_server_address()}")

    def send_command(self, command):
        if self.process:
            self.process.stdin.write(f"{command}\n".encode())
            self.process.stdin.flush()

    def stop_server(self):
        if self.process:
            self.send_command("stop")
            self.process.wait()
            print("Сервер остановлен!")

    def stop_server_programmatically(self):
        if self.process:
            self.process.terminate()
            self.process.wait()
            print("Сервер остановлен!")

    def get_local_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
        finally:
            s.close()
        return ip

    def get_server_address(self):
        return f"{self.get_local_ip()}:{self.server_properties['server-port']}"

    def update_server(self):
        self.updater.run_update()

    def backup_server(self):
        backup_dir = "server_backup"
        if os.path.exists(backup_dir):
            shutil.rmtree(backup_dir)
        shutil.copytree(self.server_dir, backup_dir)
        print(f"Резервная копия сервера сохранена в {backup_dir}")

    def export_server_data(self, export_path="server_export"):
        if os.path.exists(export_path):
            shutil.rmtree(export_path)
        shutil.copytree(self.server_dir, export_path)
        print(f"Данные сервера экспортированы в {export_path}")

    def manage_whitelist(self, action, username):
        whitelist_path = f"{self.server_dir}/whitelist.json"
        if not os.path.exists(whitelist_path):
            with open(whitelist_path, 'w') as file:
                file.write('[]')
        
        with open(whitelist_path, 'r+') as file:
            whitelist = json.load(file)
            if action == "add":
                if username not in whitelist:
                    whitelist.append(username)
                    print(f"{username} добавлен в белый список.")
            elif action == "remove":
                if username in whitelist:
                    whitelist.remove(username)
                    print(f"{username} удален из белого списка.")
            file.seek(0)
            json.dump(whitelist, file)
            file.truncate()

    def assign_privilege(self, username):
        ops_path = f"{self.server_dir}/ops.json"
        if not os.path.exists(ops_path):
            with open(ops_path, 'w') as file:
                file.write('[]')

        with open(ops_path, 'r+') as file:
            ops = json.load(file)
            if username not in ops:
                ops.append(username)
                print(f"{username} назначен привилегированным пользователем.")
            file.seek(0)
            json.dump(ops, file)
            file.truncate()

    def monitor_server(self):
        self.send_command("tps")
        time.sleep(5) 
        print("Мониторинг состояния сервера запущен.")

    def notify_server(self, message):
        self.send_command(f"say {message}")
        print(f"Сообщение '{message}' отправлено на сервер.")

    def add_mod(self, mod_file_path):
        mods_dir = f"{self.server_dir}/mods"
        if not os.path.exists(mods_dir):
            os.makedirs(mods_dir)
        shutil.copy(mod_file_path, mods_dir)
        print(f"Модификация {mod_file_path} добавлена на сервер.")

    def set_resource_pack(self, resource_pack_path):
        resource_packs_dir = f"{self.server_dir}/resource_packs"
        if not os.path.exists(resource_packs_dir):
            os.makedirs(resource_packs_dir)
        shutil.copy(resource_pack_path, resource_packs_dir)
        print(f"Ресурс пак {resource_pack_path} установлен на сервер.")

class MinecraftUpdater:
    def __init__(self, server_dir="bedrock-server", backup_dir="backup"):
        self.server_dir = server_dir
        self.backup_dir = backup_dir
        self.download_url = None

    def get_latest_version_url(self):
        base_url = "https://minecraft.azureedge.net/bin-win/"
        version = self.get_latest_version_number()
        self.download_url = f"{base_url}bedrock-server-{version}.zip"
        return self.download_url

    def get_latest_version_number(self):
        return "1.21.22.01"

    def backup_current_server(self):
        if os.path.exists(self.backup_dir):
            shutil.rmtree(self.backup_dir)
        shutil.copytree(self.server_dir, self.backup_dir)
        print(f"Резервная копия сервера сохранена в {self.backup_dir}")

    def download_latest_version(self):
        if not self.download_url:
            self.get_latest_version_url()

        response = requests.get(self.download_url, stream=True)
        zip_path = f"{self.server_dir}.zip"
        with open(zip_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=128):
                file.write(chunk)
        print(f"Скачан {self.server_dir}.zip")
        return zip_path

    def update_server(self, zip_path):
        if os.path.exists(self.server_dir):
            shutil.rmtree(self.server_dir)

        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(self.server_dir)
        os.remove(zip_path)
        print(f"Сервер обновлен до последней версии в {self.server_dir}")

    def run_update(self):
        print("Начало процесса обновления...")
        self.backup_current_server()
        zip_path = self.download_latest_version()
        self.update_server(zip_path)
        print("Обновление завершено успешно!")
    

def main():
    parser = argparse.ArgumentParser(description="Управление сервером Minecraft Bedrock Edition.")
    parser.add_argument("action", choices=["start", "stop", "command", "update", "backup", "export", "whitelist", "privilege", "monitor", "notify", "addmod", "setpack"], help="Действие, которое необходимо выполнить с сервером.")
    parser.add_argument("--cmd", type=str, help="Команда для отправки на сервер (используйте с действием 'command').")
    parser.add_argument("--username", type=str, help="Имя пользователя для управления белым списком или привилегиями.")
    parser.add_argument("--file", type=str, help="Файл для добавления на сервер (модификация или ресурс пак).")
    parser.add_argument("--message", type=str, help="Сообщение для отправки на сервер.")
    args = parser.parse_args()

    server = MinecraftServer()

    if args.action == "update":
        server.update_server()
    elif args.action == "start":
        server.create_server_properties()
        server.start_server()
    elif args.action == "stop":
        server.stop_server_programmatically()
    elif args.action == "command":
        if args.cmd:
            server.send_command(args.cmd)
        else:
            print("Необходимо указать команду для выполнения.")
    elif args.action == "backup":
        server.backup_server()
    elif args.action == "export":
        server.export_server_data()
    elif args.action == "whitelist":
        if args.username:
            server.manage_whitelist("add", args.username)
        else:
            print("Необходимо указать имя пользователя для добавления в белый список.")
    elif args.action == "privilege":
        if args.username:
            server.assign_privilege(args.username)
        else:
            print("Необходимо указать имя пользователя для назначения привилегий.")
    elif args.action == "monitor":
        server.monitor_server()
    elif args.action == "notify":
        if args.message:
            server.notify_server(args.message)
        else:
            print("Необходимо указать сообщение для отправки на сервер.")
    elif args.action == "addmod":
        if args.file:
            server.add_mod(args.file)
        else:
            print("Необходимо указать путь к файлу модификации.")
    elif args.action == "setpack":
        if args.file:
            server.set_resource_pack(args.file)
        else:
            print("Необходимо указать путь к ресурс паку.")

if __name__ == "__main__":
    main()
