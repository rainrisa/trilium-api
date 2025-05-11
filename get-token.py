from trilium_py.client import ETAPI
import os

server_url = os.getenv("TRILIUM_SERVER_URL")
password = os.getenv("TRILIUM_PASSWORD")
ea = ETAPI(server_url)
token = ea.login(password)
print(token)
