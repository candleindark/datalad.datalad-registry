import click
from flask.cli import with_appcontext
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class URL(db.Model):  # type: ignore

    __tablename__ = "urls"

    url = db.Column(db.Text, primary_key=True)
    ds_id = db.Column(db.Text, nullable=True)
    annex_uuid = db.Column(db.Text)
    annex_key_count = db.Column(db.Integer)
    info_ts = db.Column(db.Integer)
    update_announced = db.Column(db.Integer)
    head = db.Column(db.Text)
    head_describe = db.Column(db.Text)
    branches = db.Column(db.Text)
    tags = db.Column(db.Text)
    git_objects_kb = db.Column(db.BigInteger)
    #: Whether initial data has been collected for this URL
    processed = db.Column(db.Boolean, default=False, nullable=False)

    def __repr__(self) -> str:
        return f"<URL(url={self.url!r}, ds_id={self.ds_id!r})>"


@click.command("init-db")
@with_appcontext
def init_db_command() -> None:
    db.create_all()
