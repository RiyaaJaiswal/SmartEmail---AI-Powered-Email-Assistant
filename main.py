from app import create_interface
import os

if __name__ == "__main__":
    interface = create_interface()
    port = int(os.environ.get("PORT", 7860))
    interface.launch(server_name="0.0.0.0", server_port=port, share=False)

