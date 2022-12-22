from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
def init_db(app, conf):
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://{}:{}@{}:{}/{}".format(
        conf.DB_USER, conf.DB_PASS, conf.DB_HOST, conf.DB_PORT, conf.DB_NAME)
    db.init_app(app)
    with app.app_context():
        db.create_all()