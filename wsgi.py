import sys
import os

path_root = os.path.dirname(os.path.abspath(__file__))
if path_root not in sys.path:
    sys.path.append(path_root)
    
app_folder = os.path.join(path_root, 'app')
if app_folder not in sys.path:
    sys.path.append(app_folder)

os.environ['FLASK_APP'] = 'app'

from app import create_app
application = create_app()