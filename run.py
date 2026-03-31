from app.app import create_app
import os

app = create_app()

if __name__ == '__main__':
  host = os.environ.get('HOST', os.environ.get('FLASK_RUN_HOST', '127.0.0.1'))
  port = int(os.environ.get('PORT', os.environ.get('FLASK_RUN_PORT', 5001)))
  app.run(host=host, port=port)
  
