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
    for local_team in teams:
        league_dic[local_team] = {}
        for visitant_team in teams:
            if visitant_team == local_team:
                league_dic[local_team][visitant_team] = "X"
            else:
                league_dic[local_team][visitant_team] = None
    return league_dic


def create_ranking():
    """Create ranking dic."""
    ranking_dic = {}
    for local_team in teams:
        ranking_dic[local_team] = 0
    return ranking_dic


def update_league(local_team, visitant_team, local_goals, visitant_goals):
    """Update goals on the league matrix."""
    league[local_team][visitant_team] = local_goals
    league[visitant_team][local_team] = visitant_goals


def update_ranking():
    """TODO: Work on a better function."""
    global ranking
    ranking = create_ranking()
    done_teams = []
    for local_team in league:
        for visitant_team in league[local_team]:
            if league[local_team][visitant_team] is not None:
                if local_team and visitant_team not in done_teams and local_team != visitant_team:
                    points = check_ranking_points(
                        league[local_team][visitant_team], league[visitant_team][local_team])
                    set_ranking_points(points, local_team, visitant_team)
        done_teams.append(local_team)


def check_ranking_points(local, visitant):
    """Check how many points did the local team win."""
    if local != None:
        if local > visitant:
            return 3
        elif local == visitant:
            return 1
        else:
            return 0
    else:
        return 0


def set_ranking_points(points, local_team, visitant_team):
    """Sum the points depending on the condition."""
    if points == 3:
        ranking[local_team] += points
    elif points == 1:
        ranking[local_team] += points
        ranking[visitant_team] += points
    else:
        ranking[local_team] += points
        ranking[visitant_team] += 3


teams = load_teams()
league = create_league()
ranking = create_ranking()


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
    update_ranking()
    return render_template("ranking.html", ranking=sorted(ranking.items(), key=lambda x: x[1], reverse=True))


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
