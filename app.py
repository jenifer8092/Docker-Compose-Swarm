"""
Punto de entrada principal de la aplicación.
"""
from ui.interface import create_interface


if __name__ == "__main__":
    app = create_interface()
    app.launch(server_name="0.0.0.0", server_port=7860)
