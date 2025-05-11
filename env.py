from environs import env

env.read_env()

trilium_token = env.str("TRILIUM_TOKEN")
trilium_server_url = env.str("TRILIUM_SERVER_URL")
