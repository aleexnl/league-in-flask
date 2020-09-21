from flask import Flask, request, redirect, url_for, render_template
app = Flask(__name__)


def load_teams():
    """Load teams and append to list from file."""
    team_list = []
    file = open("teams.cfg", "r")
    for team in file:
        team_list.append(team.rstrip("\n"))
    return team_list


def create_league():
    """ Creates the league matrix."""
    league_dic = {}
    ranking_dic = {}
    for local_team in teams:
        league_dic[local_team] = {}
        ranking_dic[local_team] = 0
        for visitant_team in teams:
            if visitant_team == local_team:
                league_dic[local_team][visitant_team] = "X"
            else:
                league_dic[local_team][visitant_team] = None
    return league_dic, ranking_dic


def update_league(local_goals, visitant_goals, local_team, visitant_team):
    league[local_team][visitant_team] = local_goals
    league[visitant_team][local_team] = visitant_goals


teams = load_teams()
league, ranking = create_league()


@app.route('/')
def index():
    return render_template("index.html")


@ app.route('/league')
def view_league():
    return render_template("league-chart.html", league=league, teams=teams)


@ app.route('/teams')
def team_list():
    return render_template("team-list.html", teams=teams)


@app.route('/goals')
def select_teams(error=False):
    return render_template("select-teams-goals.html", teams=teams)


@app.route('/goals', methods=["POST"])
def select_teams_post():
    local_team = request.form["local"]
    visitant_team = request.form["visitant"]
    if local_team == visitant_team:
        return select_teams(True)
    else:
        return redirect(url_for('set_goals', local=local_team, visitant=visitant_team))


@ app.route('/set_goals<local>vs<visitant>')
def set_goals(local, visitant):
    html = create_html_set_goals(local, visitant)
    html += """<a href="/goals">Return</a>"""
    return html


@ app.route('/set_goals<local>vs<visitant>', methods=["POST"])
def set_goals_post(local, visitant):
    update_league(request.form["local"],
                  request.form["visitant"], local, visitant)
    return "Hello World!"


if __name__ == '__main__':
    app.run()
