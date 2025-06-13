from flask import Flask, request, render_template, redirect, url_for, flash
import psycopg2
import os

app = Flask(__name__)
app.secret_key = 'your-secret-key'
# Database connection
def get_db_connection():
    with open(os.environ.get("DB_PASSWORD_FILE")) as f:
        db_password = f.read().strip()
    conn = psycopg2.connect(
        host=os.environ.get("DB_HOST"),
        database=os.environ.get("DB_NAME"),
        user=os.environ.get("DB_USER"),
        password=db_password
    )
    return conn

def init_db():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS tasks (
        id SERIAL PRIMARY KEY,
        task TEXT NOT NULL,
        completed BOOLEAN NOT NULL DEFAULT FALSE
    )''')
    conn.commit()
    conn.close()

# Homepage route
@app.route('/', methods=['GET', 'POST'])
def home():
    init_db()
    if request.method == 'POST':
        task = request.form.get('task', '').strip()
        if not task:
            flash('Task cannot be empty!', 'error')
        else:
            conn = get_db_connection()
            c = conn.cursor()
            c.execute('INSERT INTO tasks (task, completed) VALUES (%s, FALSE)', (task,))
            conn.commit()
            conn.close()
            flash('Task added successfully!', 'success')

    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT id, task, completed FROM tasks ORDER BY id DESC')
    tasks = c.fetchall()
    conn.close()
    return render_template('index.html', tasks=tasks)

# Toggle task completion
@app.route('/toggle/<int:task_id>')
def toggle_task(task_id):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('UPDATE tasks SET completed = NOT completed WHERE id = %s', (task_id,))
    conn.commit()
    conn.close()
    flash('Task status updated!', 'success')
    return redirect(url_for('home'))

# Delete task
@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('DELETE FROM tasks WHERE id = %s', (task_id,))
    conn.commit()
    conn.close()
    flash('Task deleted successfully!', 'success')
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)