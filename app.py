from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors

app = Flask(__name__)
app.secret_key = 'your_secret_key'

app.config['MYSQL_HOST'] = '161.132.37.95'
app.config['MYSQL_USER'] = 'peti'
app.config['MYSQL_PASSWORD'] = 'peti34@@'
app.config['MYSQL_DB'] = 'strategic_planning'

mysql = MySQL(app)

@app.route('/login/', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE username = %s AND password = %s', (username, password))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            return redirect(url_for('home'))
        else:
            msg = 'Incorrect username/password!'
    return render_template('login.html', msg=msg)

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/home')
def home():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM plans')
        plans = cursor.fetchall()
        return render_template('home.html', username=session['username'], plans=plans)
    return redirect(url_for('login'))

@app.route('/create_plan', methods=['GET', 'POST'])
def create_plan():
    if 'loggedin' in session:
        if request.method == 'POST':
            mission = request.form['mission']
            vision = request.form['vision']
            values = request.form['values']
            objectives = request.form['objectives']
            internal_external_analysis = request.form['internal_external_analysis']
            value_chain = request.form['value_chain']
            participation_matrix = request.form['participation_matrix']
            porters_five_forces = request.form['porters_five_forces']
            pest = request.form['pest']
            strategy_identification = request.form['strategy_identification']
            came_matrix = request.form['came_matrix']
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('''INSERT INTO plans (mission, vision, valores, objectives, internal_external_analysis, value_chain, participation_matrix, porters_five_forces, pest, strategy_identification, came_matrix) 
                              VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''', 
                           (mission, vision, values, objectives, internal_external_analysis, value_chain, participation_matrix, porters_five_forces, pest, strategy_identification, came_matrix))
            mysql.connection.commit()
            return redirect(url_for('home'))
        return render_template('create_plan.html')
    return redirect(url_for('login'))

@app.route('/view_plan/<int:id>')
def view_plan(id):
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM plans WHERE id = %s', (id,))
        plan = cursor.fetchone()
        if plan:
            plan['valores'] = plan['valores'].split(',')
            plan['objectives'] = plan['objectives'].split(',')
            plan['internal_external_analysis'] = plan['internal_external_analysis'].split(',')
            plan['value_chain'] = plan['value_chain'].split(',')
            plan['participation_matrix'] = list(map(int, plan['participation_matrix'].split(',')))
            plan['porters_five_forces'] = plan['porters_five_forces'].split(',')
            return render_template('view_plan.html', plan=plan)
    return redirect(url_for('login'))

@app.route('/delete_plan/<int:id>', methods=['POST'])
def delete_plan(id):
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('DELETE FROM plans WHERE id = %s', (id,))
        mysql.connection.commit()
        return redirect(url_for('home'))
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)