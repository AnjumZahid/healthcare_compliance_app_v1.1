import multiprocessing
import time
from services.mcp_server import run_server

# 🚀 Start FDA server in background
def start_fda_server():
    p = multiprocessing.Process(target=run_server, daemon=True)
    p.start()
    time.sleep(2)  # wait for server startup
    return p