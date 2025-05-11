from trilium_py.client import ETAPI
from env import trilium_server_url, env

password = env.str("TRILIUM_PASSWORD")
ea = ETAPI(trilium_server_url)
token = ea.login(password)
print(token)
