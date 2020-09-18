from flask import Flask, request
app = Flask(__name__)

top_menu_html = """
<nav>
<a href="/">Home</a>
<a href="/goals">Goals</a>
<a href="/league">League</a>
<a href="/teams">Teams</a>
</nav>
"""


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
            if visitant_team != local_team:
                league_dic[local_team][visitant_team] = None
    return league_dic, ranking_dic


def create_html_team_options():
    html = ""
    for team in teams:
        tag = "<option value=\"{}\">".format(team)
        tag += team
        tag += "</option>"
        html += tag
    return html


def create_html_team_select(team_type):
    team_list = create_html_team_options()
    html = "<select name={}>".format(team_type)
    html += team_list
    html += "</select>"
    return html


def create_html_set_goals(local, visitant):
    html = "<h1>{} vs {}</h1>".format(local, visitant)
    return html


teams = load_teams()
league, ranking = create_league()


@app.route('/')
def index():
    return top_menu_html


@app.route('/goals')
def select_teams(error=False):
    html = "<h1>Local Team</h1>"
    html += """<form method="post">"""
    html += create_html_team_select("local")
    html += "<h1>Visitant Team</h1>"
    html += create_html_team_select("visitant")
    html += "</br >"
    html += """<input type="submit">"""
    html += "</form >"
    if error:
        html += """<h1 style="color:red;">Error: Select different teams</h1>"""
    return top_menu_html + html


@app.route('/goals', methods=["POST"])
def select_teams_post():
    local_team = request.form["local"]
    visitant_team = request.form["visitant"]
    if local_team == visitant_team:
        return select_teams(True)
    else:
        html = create_html_set_goals(local_team, visitant_team)
        html += """<a href="/goals">Return</a>"""
        return html


@app.route('/league')
def view_league():
    return top_menu_html + """
    <h1>league Chart</h1>
    <p>{}</p>
    <a href="/">Return</a>
    """.format(league)


@app.route('/teams')
def team_list():
    return top_menu_html + """
    <h1>Team List</h1>
    <p>{}</p>
    <a href="/">Return</a>
    """.format(", ".join(teams))


if __name__ == '__main__':
    app.run()
