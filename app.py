from flask import Flask
app = Flask(__name__)
teams = []


@app.route('/')
def input_teams():
    return """
    <h1>ADD A TEAM</h1>
    <form method="post">
        <label for="team_name">Team name:</label>
        <input type="text" name="team_name" id="team_name" />
        <br>
        <input type="submit">
    </form>
    """


@app.route('/', methods=['POST'])
def method_name():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
