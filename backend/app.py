import os
from flask import Flask, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from config import config
from models import db

def create_app(config_name=None):
    """Application factory"""
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')
    
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    CORS(app, origins=app.config['CORS_ORIGINS'])
    Migrate(app, db)
    
    # Register blueprints
    from routes.auth import auth_bp
    from routes.posts import posts_bp
    from routes.comments import comments_bp
    from routes.categories_tags import categories_bp, tags_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(posts_bp)
    app.register_blueprint(comments_bp)
    app.register_blueprint(categories_bp)
    app.register_blueprint(tags_bp)
    
    # Health check endpoint
    @app.route('/health')
    def health_check():
        return jsonify({
            'status': 'healthy',
            'service': 'mini-blog-api'
        }), 200
    
    # API info endpoint
    @app.route('/api')
    def api_info():
        return jsonify({
            'name': 'Mini Blog API',
            'version': '1.0.0',
            'endpoints': {
                'auth': '/api/auth',
                'posts': '/api/posts',
                'comments': '/api/comments',
                'categories': '/api/categories',
                'tags': '/api/tags'
            }
        }), 200
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Resource not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return jsonify({'error': 'Internal server error'}), 500
    
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({'error': 'Bad request'}), 400
    
    return app

if __name__ == '__main__':
    app = create_app()
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=app.config['DEBUG'])
