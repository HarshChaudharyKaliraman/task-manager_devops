from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)


def init_db():
    conn = sqlite3.connect("tasks.db")

    conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


@app.route("/")
def home():
    conn = sqlite3.connect("tasks.db")
    conn.row_factory = sqlite3.Row

    tasks = conn.execute("SELECT * FROM tasks").fetchall()

    conn.close()

    return render_template("index.html", tasks=tasks)


@app.route("/add", methods=["POST"])
def add_task():
    task = request.form["task"].strip()

    if not task:
        return redirect("/")

    conn = sqlite3.connect("tasks.db")

    conn.execute("INSERT INTO tasks (task) VALUES (?)", (task,))

    conn.commit()
    conn.close()

    return redirect("/")


@app.route("/delete/<int:task_id>")
def delete_task(task_id):
    conn = sqlite3.connect("tasks.db")

    conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))

    conn.commit()
    conn.close()

    return redirect("/")


@app.route("/edit/<int:task_id>", methods=["POST"])
def edit_task(task_id):
    updated_task = request.form["task"]

    conn = sqlite3.connect("tasks.db")

    conn.execute("UPDATE tasks SET task = ? WHERE id = ?", (updated_task, task_id))

    conn.commit()
    conn.close()

    return redirect("/")


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=False)
