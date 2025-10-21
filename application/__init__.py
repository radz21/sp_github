from flask import Flask,  session
from flask_socketio import SocketIO, os
from flask_uploads import UploadSet, configure_uploads, IMAGES
socketio = SocketIO()


def create_app(debug=True):
    """Create an application."""
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '&^##*($top_secret&&#(@(@":f'
    app.debug = debug
    IMAGE_FOLDER = os.path.join('static', 'image')

    
    app.config['UPLOADED_PHOTOS_DEST'] = 'static/image'
    app.config['UPLOAD_FOLDER'] = IMAGE_FOLDER

    photos = UploadSet('photos', IMAGES)
    configure_uploads(app, photos)
    
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    socketio.init_app(app)
    return app
