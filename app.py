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
                league_dic[local_team][visitant_team] = ""
    return league_dic, ranking_dic


def update_league(local_team, visitant_team, local_goals, visitant_goals):
    """Update goals on the league matrix."""
    league[local_team][visitant_team] = local_goals
    league[visitant_team][local_team] = visitant_goals


teams = load_teams()
league, ranking = create_league()


@app.route('/')
def home():
    return render_template("index.html")


@ app.route('/league')
def league_grid():
    return render_template("league-chart.html", league=league, teams=teams)


@ app.route('/teams')
def team_list():
    return render_template("team-list.html", teams=teams)


@app.route('/goals')
def goals_input(error=None):
    return render_template("select-teams-goals.html", teams=teams, error=error)


@app.route('/ranking')
def ranking_chart(error=None):
    return render_template("ranking.html", ranking=ranking)


@app.route('/goals', methods=["POST"])
def goals_input_post():
    local_team = request.form["localTeam"]
    visitant_team = request.form["visitantTeam"]
    local_goals = request.form["localTeamScore"]
    visitant_goals = request.form["visitantTeamScore"]
    if local_team == visitant_team:
        return goals_input("sameTeams")
    else:
        update_league(local_team, visitant_team, local_goals, visitant_goals)
        return redirect(url_for("league_grid"))


if __name__ == '__main__':
    app.run()
