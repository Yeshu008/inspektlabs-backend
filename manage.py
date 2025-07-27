import click
from flask.cli import FlaskGroup
from app import create_app, db
from flask_migrate import upgrade, migrate, init,downgrade,stamp
import os

app = create_app()
cli = FlaskGroup(app)

@cli.command("init-db")
@click.option('--message', '-m', default="Initial migration", help='Migration message')
def init_db(message):
    """Initializes migrations folder, runs first migration and upgrades DB"""
    migrations_folder = os.path.join(os.getcwd(), "migrations")

    if not os.path.exists(migrations_folder):
        print("📁 Initializing migrations folder...")
        init()
    else:
        print("✅ Migrations folder already exists")

    print(f"🔁 Creating migration with message: '{message}'")
    migrate(message=message)

    print("⬆️ Applying migration...")
    upgrade()

    print("✅ Database initialized and up-to-date")


@cli.command("create-all")
def create_all():
    """Creates all database tables (without migrations)"""
    db.create_all()
    print("✅ Tables created using SQLAlchemy")


@cli.command("drop-all")
def drop_all():
    """Drops all database tables"""
    confirm = input("⚠️ Are you sure you want to drop all tables? [y/N]: ")
    if confirm.lower() == 'y':
        db.drop_all()
        print("🗑️ All tables dropped")
    else:
        print("❌ Cancelled")


@cli.command("migrate-db")
def make_migration():
    """Creates a new migration script"""
    print("🔁 Creating new migration...")
    migrate()
    print("✅ Migration script created")


@cli.command("upgrade-db")
def upgrade_db():
    """Applies migrations to upgrade the database"""
    print("⬆️ Applying migrations...")
    upgrade()
    print("✅ Database upgraded")


@cli.command("downgrade-db")
@click.argument("revision", required=False)
def downgrade_db(revision=None):
    """Downgrades the database. If no revision is given, downgrades one step."""
    revision = revision or "-1"
    print(f"⬇️ Downgrading database to revision: {revision} ...")
    downgrade(revision)
    print(f"✅ Downgraded to {revision}")



@cli.command("reset-db")
def reset_db():
    """Drops and recreates the DB schema using migrations"""
    print("♻️ Resetting DB using migrations...")
    db.drop_all()
    upgrade()
    print("✅ DB reset with latest schema")


@cli.command("stamp-head")
def stamp_head():
    """Mark DB with latest migration without applying it"""
    stamp()
    print("🔖 Database stamped with current migration head")


if __name__ == '__main__':
    cli()
