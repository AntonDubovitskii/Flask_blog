import os

from flask import render_template
from blog.app import create_app
from blog.extensions import db

app = create_app()


@app.cli.command("create-tags")
def create_tags():
    from blog.models import Tag
    for name in [
        "flask",
        "django",
        "python",
        "sqlalchemy",
        "news",
    ]:
        tag = Tag(name=name)
        db.session.add(tag)
    db.session.commit()

    print("Done! Tags created!")


@app.route('/', endpoint="index")
def start():
    return render_template("index.html")


@app.cli.command("create-admin")
def create_admin():
    from blog.models import User
    admin = User(username="Admin", is_staff=True, first_name="Anton", last_name="Dubovitskii", email="admin@mail.ru")
    admin.password = os.environ.get("ADMIN_PASSWORD") or "adminpass"

    db.session.add(admin)
    db.session.commit()

    print("Done! Created admin:", admin)


@app.cli.command("create-articles")
def create_articles():
    from blog.models import Article
    first = Article(
        title="The extinction of polar ferrets is a global problem.",
        body="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas eu dapibus leo. Proin non sem neque."
             "Donec nec accumsan ante. Proin venenatis nisl quis sapien aliquam malesuada. Maecenas turpis felis,"
             "porttitor eget pellentesque a, viverra id turpis. Quisque a magna eu nulla sodales maximus vitae"
    )
    second = Article(
        title="Will artificial intelligence replace clowns?",
        body="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas eu dapibus leo. Proin non sem neque."
             "Donec nec accumsan ante. Proin venenatis nisl quis sapien aliquam malesuada. Maecenas turpis felis, "
             "porttitor eget pellentesque a, viverra id turpis. Quisque a magna eu nulla sodales maximus vitae"
    )
    third = Article(
        title="At the G20 summit, three old men fell on the slippery floor.",
        body="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas eu dapibus leo. Proin non sem neque."
             "Donec nec accumsan ante. Proin venenatis nisl quis sapien aliquam malesuada. Maecenas turpis felis, "
             "porttitor eget pellentesque a, viverra id turpis. Quisque a magna eu nulla sodales maximus vitae"
    )

    db.session.add(first)
    db.session.add(second)
    db.session.add(third)
    db.session.commit()

    print("Done! Articles created!")

