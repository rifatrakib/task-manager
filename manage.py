import os

import uvicorn
from typer import Typer

app = Typer()


@app.command(name="startserver")
def start_server(mode: str = "development"):
    os.environ["MODE"] = mode
    uvicorn.run("server.main:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    app()
