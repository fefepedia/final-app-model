import os
from flask import Flask, render_template, request
import json
import pyttsx3

app = Flask(__name__)

moves = []
games_played = 0
correct_moves = 0

def analyze_moves(moves):
    analysis = {}
    for move in moves:
        if move['result'] == 'correct':
            if move['operation'] in analysis:
                analysis[move['operation']] += 1
            else:
                analysis[move['operation']] = 1
    return analysis

@app.route('/', methods=['GET', 'POST'])
def dashboard():
    global moves
    global games_played
    global correct_moves
    if request.method == 'POST':
        val1 = int(request.form['val1'])
        val2 = int(request.form['val2'])
        vector = []
        vector.append(val1 + val2)
        vector.append(val1 - val2)
        vector.append(val1 * val2)
        if val2 != 0:
            vector.append(val1 / val2)
        else:
            vector.append(0)
        result = request.form['result']
        closest = float('inf')
        for v in vector:
            if v == result:
                closest = v
                break
            elif abs(v - result) < abs(closest - result):
                closest = v
        if closest == float('inf'):
            message = "Error in calculating"
            engine = pyttsx3.init()
            engine.say("Incorrect")
            engine.runAndWait()
            moves.append({'result': 'incorrect'})
        else:
            message = "The closest value to the result is " + str(closest)
            engine = pyttsx3.init()
            engine.say("Correct")
            engine.runAndWait()
            correct_moves += 1
            moves.append({'result': 'correct', 'operation': request.form['operation']})
        games_played += 1
    return render_template('dashboard.html', games_played=games_played, correct_moves=correct_moves, total_moves=len(moves))

@app.route('/reports')
def reports():
    analysis = analyze_moves(moves)
    return render_template('reports.html', analysis=analysis)

if __name__ == '__main__':
    app.run()

