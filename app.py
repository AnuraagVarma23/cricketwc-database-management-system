from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
import config

app = Flask(__name__)

db = mysql.connector.connect(**config.db_config)

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "123456"

# Flash secret key for showing messages
app.secret_key = 'your_secret_key'  # You can set any secret key


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            return redirect(url_for("admin"))
        else:
            return render_template("login.html", error="Invalid username or password")
    return render_template("login.html")


@app.route("/admin")
def admin():
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM player")
    players = cursor.fetchall()

    cursor.execute("SELECT * FROM team")
    teams = cursor.fetchall()

    cursor.execute("SELECT * FROM matches")
    matches = cursor.fetchall()

    cursor.execute("SELECT * FROM umpire")
    umpires = cursor.fetchall()

    return render_template(
        "admin.html", players=players, teams=teams, matches=matches, umpires=umpires
    )


@app.route("/add_player_form", methods=['GET','POST'])
def add_player_form():
    return render_template("add_player.html")


@app.route("/edit_player_form/<player_id>", methods=["GET"])
def edit_player_form(player_id):
    """Render the edit form for the player with the given player_id."""
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM player WHERE player_id = %s", (player_id,))
    player = cursor.fetchone()
    cursor.close()
    
    if not player:
        flash("Player not found!", "error")
        return redirect(url_for("admin"))
    
    return render_template("edit_player.html", player=player)


@app.route("/edit_player", methods=["POST"])
def edit_player():
    player_id = request.form.get("player_id")
    player_name = request.form.get("player_name")
    dob = request.form.get("dob")
    type_of_player = request.form.get("type_of_player")
    total_runs = request.form.get("total_runs", 0)
    t20 = request.form.get("t20", 0)
    test = request.form.get("test", 0)
    odi = request.form.get("odi", 0)
    batting_average = request.form.get("batting_average", 0.0)
    no_of_sixes = request.form.get("no_of_sixes", 0)
    no_of_fours = request.form.get("no_of_fours", 0)
    economy = request.form.get("economy", 0.0)
    no_of_wickets = request.form.get("no_of_wickets", 0)
    highest_score = request.form.get("highest_score", 0)

    cursor = db.cursor()
    try:
        cursor.execute(
            """
            UPDATE player
            SET player_name = %s, dob = %s, type_of_player = %s, total_runs = %s, t20 = %s, test = %s, odi = %s,
                batting_average = %s, no_of_sixes = %s, no_of_fours = %s, economy = %s, no_of_wickets = %s,
                highest_run_scored = %s
            WHERE player_id = %s
            """,
            (
                player_name, dob, type_of_player, total_runs, t20, test, odi,
                batting_average, no_of_sixes, no_of_fours, economy, no_of_wickets,
                highest_score, player_id
            ),
        )
        db.commit()
        flash("Player updated successfully!", "success")
    except mysql.connector.Error as err:
        db.rollback()
        flash(f"Failed to update player: {str(err)}", "error")
    finally:
        cursor.close()

    return redirect(url_for("admin"))



@app.route("/add_player", methods=["POST"])
def add_player():
    player_name = request.form.get("player_name")
    dob = request.form.get("dob")
    type_of_player = request.form.get("type_of_player")
    total_runs = request.form.get("total_runs")
    t20 = request.form.get("t20")
    test = request.form.get("test")
    odi = request.form.get("odi")
    batting_average = request.form.get("batting_average")
    no_of_sixes = request.form.get("no_of_sixes")
    no_of_fours = request.form.get("no_of_fours")
    economy = request.form.get("economy")
    no_of_wickets = request.form.get("no_of_wickets")
    highest_score = request.form.get("highest_score")

    cursor = db.cursor()

    # Check if the player already exists with the same name
    cursor.execute("SELECT COUNT(*) FROM player WHERE player_name = %s", (player_name,))
    if cursor.fetchone()[0] > 0:
        flash('Player already exists with the same name!', 'error')
        return redirect(url_for('add_player_form'))

    cursor.execute("SELECT MAX(player_id) FROM player")
    result = cursor.fetchone()
    max_player_id = result[0]

    next_player_id = int(max_player_id[1:]) + 1 if max_player_id else 1
    new_player_id = "P" + str(next_player_id).zfill(3)

    try:
        cursor.execute(
            "INSERT INTO player (player_id, player_name, dob, type_of_player, total_runs, t20, test, odi, "
            "batting_average, no_of_sixes, no_of_fours, economy, no_of_wickets, highest_run_scored) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (new_player_id, player_name, dob, type_of_player, total_runs, t20, test, odi, batting_average, no_of_sixes,
             no_of_fours, economy, no_of_wickets, highest_score),
        )
        db.commit()
        flash('Player added successfully!', 'success')
    except mysql.connector.Error as err:
        db.rollback()
        flash(f"Failed to add player: {str(err)}", 'error')
    finally:
        cursor.close()

    return redirect(url_for("admin"))


@app.route("/delete_player/<player_id>", methods=["DELETE", "POST"])
def delete_player(player_id):
    cursor = db.cursor()
    try:
        cursor.execute("DELETE FROM player WHERE player_id = %s", (player_id,))
        db.commit()
        flash("Player deleted successfully", "success")
    except mysql.connector.Error as err:
        db.rollback()
        flash(f"Failed to delete player: {str(err)}", "error")
    finally:
        cursor.close()

    return redirect(url_for("admin"))


@app.route("/add_match_form")
def add_match_form():
    """Render the Add Match form."""
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT team_id, team_name FROM team")  # Fetch team details for dropdown
    teams = cursor.fetchall()
    cursor.close()
    return render_template("add_match.html", teams=teams)


@app.route("/add_match", methods=["POST"])
def add_match():
    """Add a new match."""
    team1 = request.form.get("team1")
    team2 = request.form.get("team2")
    match_date = request.form.get("match_date")
    location = request.form.get("location")

    cursor = db.cursor()
    cursor.execute("SELECT MAX(match_id) FROM matches")  # Generate the next match ID
    result = cursor.fetchone()
    max_match_id = result[0]

    next_match_id = int(max_match_id[1:]) + 1 if max_match_id else 1
    new_match_id = "M" + str(next_match_id).zfill(3)

    try:
        cursor.execute(
            "INSERT INTO matches (match_id, team1, team2, match_date, location) VALUES (%s, %s, %s, %s, %s)",
            (new_match_id, team1, team2, match_date, location),
        )
        db.commit()
        flash("Match added successfully!", "success")
    except mysql.connector.Error as err:
        db.rollback()
        flash(f"Failed to add match: {str(err)}", "error")
    finally:
        cursor.close()

    return redirect(url_for("admin"))


@app.route("/edit_match_form/<match_id>")
def edit_match_form(match_id):
    """Render the Edit Match form."""
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM matches WHERE match_id = %s", (match_id,))
    match = cursor.fetchone()

    cursor.execute("SELECT team_id, team_name FROM team")  # Fetch team details for dropdown
    teams = cursor.fetchall()
    cursor.close()

    return render_template("edit_match.html", match=match, teams=teams)


@app.route("/edit_match", methods=["POST"])
def edit_match():
    """Edit an existing match."""
    match_id = request.form.get("match_id")
    team1 = request.form.get("team1")
    team2 = request.form.get("team2")
    match_date = request.form.get("match_date")
    location = request.form.get("location")

    cursor = db.cursor()
    try:
        cursor.execute(
            """
            UPDATE matches
            SET team1 = %s, team2 = %s, match_date = %s, location = %s
            WHERE match_id = %s
            """,
            (team1, team2, match_date, location, match_id),
        )
        db.commit()
        flash("Match updated successfully!", "success")
    except mysql.connector.Error as err:
        db.rollback()
        flash(f"Failed to edit match: {str(err)}", "error")
    finally:
        cursor.close()

    return redirect(url_for("admin"))


@app.route("/delete_match/<match_id>", methods=["DELETE", "POST"])
def delete_match(match_id):
    """Delete a match."""
    cursor = db.cursor()
    try:
        cursor.execute("DELETE FROM matches WHERE match_id = %s", (match_id,))
        db.commit()
        flash("Match deleted successfully", "success")
    except mysql.connector.Error as err:
        db.rollback()
        flash(f"Failed to delete match: {str(err)}", "error")
    finally:
        cursor.close()

    return redirect(url_for("admin"))


@app.route("/")
def index():
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM player")
    players = cursor.fetchall()

    cursor.execute("SELECT * FROM team")
    teams = cursor.fetchall()

    cursor.execute("SELECT * FROM matches")
    matches = cursor.fetchall()

    cursor.execute("SELECT * FROM umpire")
    umpires = cursor.fetchall()

    return render_template(
        "index.html", players=players, teams=teams, matches=matches, umpires=umpires
    )


@app.route("/player/<player_id>")
def player(player_id):
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM player WHERE player_id = %s", (player_id,))
    player = cursor.fetchone()
    cursor.close()
    return render_template("player.html", player=player)


@app.route("/team/<team_id>")
def team(team_id):
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM team WHERE team_id = %s", (team_id,))
    team = cursor.fetchone()
    cursor.close()
    return render_template("team.html", team=team)


@app.route("/match/<match_id>")
def match(match_id):
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM matches WHERE match_id = %s", (match_id,))
    match = cursor.fetchone()
    cursor.close()
    return render_template("match.html", match=match)


@app.route("/umpire/<umpire_id>")
def umpire(umpire_id):
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM umpire WHERE umpire_id = %s", (umpire_id,))
    umpire = cursor.fetchone()
    cursor.close()
    return render_template("umpire.html", umpire=umpire)


if __name__ == "__main__":
    app.run(debug=True, port=3230)
