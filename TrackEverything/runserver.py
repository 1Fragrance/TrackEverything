from src import create_app
import sys
import os

'''
Should exec:
    export FLASK_CONFIG=development && export FLASK_APP=run.py
Then:
    import os
    config_name = os.getenv('FLASK_CONFIG')
    app = create_app(config_name)
'''

app = create_app('development')

if __name__ == '__main__':
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.append(BASE_DIR)

    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)
