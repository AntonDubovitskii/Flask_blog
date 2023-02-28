from blog.app import create_app, db
from flask import render_template

app = create_app()


@app.route('/')
def start():
    return render_template("index.html")


@app.cli.command("init-db")
def init_db():
    db.create_all()
    print("Done!")


@app.cli.command("create-users")
def create_users():
    from blog.models import User
    admin = User(username="admin", is_staff=True)
    sam = User(username="sam")

    db.session.add(admin)
    db.session.add(sam)
    db.session.commit()

    print("Done! Created users:", admin, sam)
