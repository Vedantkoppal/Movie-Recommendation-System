import eventlet
eventlet.monkey_patch()
from app import app

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Fetch Render's port
    app.run(host="0.0.0.0", port=port)