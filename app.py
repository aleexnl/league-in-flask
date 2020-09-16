from flask import Flask, request
app = Flask(__name__)


def load_teams():
    team_list = []
    file = open("teams.cfg", "r")
    for team in file:
        team_list.append(team.rstrip("\n"))
    return team_list


def create_league():
    """ Creates the league matrix. """
    league_dic = {}
    ranking_dic = {}
    for local_team in teams:
        league_dic[local_team] = {}
        ranking_dic[local_team] = 0
        for visitant_team in teams:
            league_dic[local_team][visitant_team] = None
    return league_dic, ranking_dic


teams = load_teams()
league, ranking = create_league()


@app.route('/')
def set_goals():
    return "Hello World!"


@app.route('/league')
def view_league():
    return """
    <h1>league Chart</h1>
    <p>{}</p>
    <a href="/">Return</a>
    """.format(league)


@app.route('/team-list')
def team_list():
    return """
    <h1>Team List</h1>
    <p>{}</p>
    <a href="/">Return</a>
    """.format(", ".join(teams))


if __name__ == '__main__':
    app.run()
