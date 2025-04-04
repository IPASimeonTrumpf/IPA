from app import create_app

from app.repositories.network_repository import create_network

app = create_app()

app.run(host='0.0.0.0', port=5000, debug=True)
