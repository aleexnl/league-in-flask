from flask import Flask, request, redirect, url_for, render_template
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
            if visitant_team != local_team:
                league_dic[local_team][visitant_team] = None
    return league_dic, ranking_dic


def update_league(local_goals, visitant_goals, local_team, visitant_team):
    league[local_team][visitant_team] = local_goals
    league[visitant_team][local_team] = visitant_goals


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
    html += """
    <form method="post">
    <label>{} Goals: </label>
    <input name="local" type="number" value=0 required/>
    <br>
    <label>{} Goals: </label>
    <input name="visitant" type="number" value=0 required/>
    </br>
    <input type="submit"/>
    </form>
    """.format(local, visitant)
    return html


teams = load_teams()
league, ranking = create_league()


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/goals')
def select_teams(error=False):
    html = """<h1>Local Team</h1>
    <form method="post">"""
    html += create_html_team_select("local")
    html += "<h1>Visitant Team</h1>"
    html += create_html_team_select("visitant")
    html += """</br >
            <input type="submit">
            </form >"""
    if error:
        html += """<h1 style="color:red;">Error: Select different teams</h1>"""
    return html


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


@ app.route('/league')
def view_league():
    return """
    <h1>league Chart</h1>
    <p>{}</p>
    <a href="/">Return</a>
    """.format(league)


@ app.route('/teams')
def team_list():
    return """
    <h1>Team List</h1>
    <p>{}</p>
    <a href="/">Return</a>
    """.format(", ".join(teams))


if __name__ == '__main__':
    app.run()
