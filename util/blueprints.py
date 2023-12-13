import routes


def register_blueprints(app):
    app.register_blueprint(routes.user)
    app.register_blueprint(routes.author)
    app.register_blueprint(routes.book)
    app.register_blueprint(routes.genre)
    app.register_blueprint(routes.image)
    app.register_blueprint(routes.auth)