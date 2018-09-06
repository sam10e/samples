from flask import Flask, render_template, request, redirect
import pymysql
import config
import datetime

app = Flask(__name__)

connection = pymysql.connect(
    user=config.USER,
    host=config.HOST,
    port=3306,
    password=config.PASS,
    database=config.DB,
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)


# ========================================== HOME PAGE ======================================================
@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')


# ==================================================ADD INJURY PAGE ==================================================
@app.route('/injury/', methods=['GET'])
def new_injury():
    return render_template('addInjury.html')


@app.route('/injury/new', methods=['GET'])
def injury():
    playerID = request.args.get('playerID')
    date_input = request.args.get('injury_date')
    valid_input = False

    try:
        with connection.cursor() as cursor:
            sql = "SELECT firstName AS first, lastName AS last FROM nbaProfile WHERE id = %s"
            cursor.execute(sql, (playerID,))
            result = cursor.fetchone()
            if not result:
                return '<h1>This player is not in the database!<h1> <a href="/injury/">Try Again</a>'
            first = result['first']
            last = result['last']
    except ConnectionError:
        print('Connection Error')

    while valid_input is False:
        try:
            injury_date = request.args.get('injury_date')
            if '/' in injury_date:
                injury_date = injury_date.replace('/', '-')
            injury_date = injury_date.split('-')
            injury_year = injury_date[0]
            if int(injury_year) < 2000:
                raise ValueError
            injury_month = injury_date[1]
            injury_day = injury_date[2]

            injury_date_fixed = datetime.date(int(injury_year), int(injury_month), int(injury_day))

            valid_input = True

        except ValueError:
            print("Invalid date entered.")

    if int(injury_month) < 7:
        season = int(injury_year) - 1
    else:
        season = int(injury_year)

    player_id = request.args.get('playerID')

    team = request.args.get('team').upper()

    first_date = injury_date_fixed + datetime.timedelta(days=-9)

    conn = connection

    sql = "SELECT * from nbaSchedule where startDate between %s and %s AND (homeTeam = %s OR awayTeam = %s)"

    cursor = conn.cursor()

    cursor.execute(sql, (first_date, datetime.date(season + 1, 7, 1), team, team))

    no_result = False

    if cursor.rowcount == 0:
        no_result = True

    data = cursor.fetchall()

    cursor.close()

    game_found = False

    months = ['10', '11', '12']

    index = 0

    try:

        while game_found is False:

            date_framework = str(season) + months[index] + '%'

            cursor = conn.cursor()

            cursor.execute(
                "SELECT startDate from nbaSchedule where gameId like %s AND (homeTeam = %s OR awayTeam = %s) limit 1",
                (date_framework, team, team))

            if cursor.rowcount == 0:
                index = index + 1

                cursor.close()

            else:
                game_found = True

    except IndexError:
        print("Team not found for given season.")
        return '<h1>Team not found for given season.</h1>'

    season_start = cursor.fetchall()[0]['startDate']

    injury_game = None

    first_game = False

    minutes_played = 0

    rest_days = None

    if no_result is False:

        date_found = False

        games_missed = 0

        return_game = None

        game_index = 0

        temp_game = None

        temp_rest = None

        temp_minutes = None

        injury_game_date = None

        season_ending = False

        try:

            for game in data:

                game_id = game['gameId']

                score_cursor = conn.cursor()

                score_cursor.execute("SELECT minutes FROM nbaBoxScoresBasic WHERE gameId = %s AND playerId = %s",
                                     (game_id, player_id))

                if score_cursor.rowcount == 0:
                    if game_index == 0:
                        if game['startDate'] == season_start:
                            injury_game_date = str(injury_date_fixed)
                            date_found = True
                            first_game = True
                            rest_days = -1
                            minutes_played = 0
                    elif temp_game is not None:
                        date_found = True
                        injury_game = temp_game
                        rest_days = temp_rest
                        minutes_played = temp_minutes

                    if date_found is True:
                        games_missed = games_missed + 1
                    else:
                        if temp_game is not None:
                            games_missed = games_missed + 1
                            injury_game = temp_game
                            minutes_played = temp_minutes
                            rest_days = temp_rest

                else:
                    if date_found is False:
                        if game_index > 0:
                            if temp_game is not None:
                                temp_rest = game['startDate'] - temp_game['startDate'] + datetime.timedelta(days=-1)
                        temp_game = game
                        temp_minutes = int(score_cursor.fetchall()[0]['minutes'])
                    else:
                        if game['startDate'] >= injury_date_fixed:
                            return_game = game
                            break
                        else:
                            games_missed = 0
                            if game_index > 0:
                                if first_game is True:
                                    temp_rest = -1
                                else:
                                    temp_rest = game['startDate'] - temp_game['startDate'] + datetime.timedelta(days=-1)
                            temp_game = game
                            temp_minutes = int(score_cursor.fetchall()[0]['minutes'])

                game_index = game_index + 1

            if rest_days is None:
                raise NameError

            print("Season: " + str(season))

            if first_game is True:
                print("Injured during offseason/preseason.")
            else:
                if injury_game_date is None:
                    injury_game_date = str(injury_game['startDate'])
                if injury_game['homeTeam'] == team:
                    opponent = injury_game['awayTeam']
                else:
                    opponent = injury_game['homeTeam']

                print("Last game played: " + str(injury_game['startDate']) + " against " + opponent)
                print(
                        "Injury game page: " + 'https://www.basketball-reference.com/boxscores/' + injury_game['gameId']
                        + '.html')
                date_for_link = str(injury_game['startDate']).replace('-', '')
                print("ESPN scoreboard: " + 'http://www.espn.com/nba/scoreboard/_/date/' + date_for_link)
                print("ProSportsTransactions: " + 'https://www.prosportstransactions.com/basketball/'
                                                  'Search/SearchResults.php?Player=' + first.lower() + '+' +
                      last.lower() + '&Team=&BeginDate=&EndDate=&ILChkBx=yes&Submit=Search')

            if return_game is None:
                print("Injury was season-ending.")
                season_ending = True
                return_game = data[1]
                return_game['startDate'] = datetime.date(1000, 1, 1)
            else:
                print("Returned on " + str(return_game['startDate']))

            print("Games missed: " + str(games_missed))

            if rest_days != -1:
                print("Rest days: " + str(rest_days.days))
            else:
                print("Rest days: " + str(rest_days))

            print("Minutes played in last game: " + str(minutes_played))

        except ValueError:
            print("Invalid player ID or incorrect team.")
            return '<h1>Change player ID or team.</h1>'
        except NameError:
            print("Rest days not computable. Expand date range.")
            return '<h1>Rest days not computable. Expand date range.</h1>'

    else:
        print("No results using this date.")

    if rest_days != -1:
        return render_template('addInjury.html', first=first, last=last, playerid=playerID, first_date=first_date,
                               injury_date=injury_game_date, minutes_played=minutes_played, rest_days=rest_days.days,
                               return_game=return_game['startDate'], games_missed=games_missed, season=season,
                               season_ending=season_ending)
    else:
        return render_template('addInjury.html', first=first, last=last, playerid=playerID, first_date=first_date,
                               injury_date=injury_game_date, minutes_played=minutes_played, rest_days=rest_days,
                               return_game=return_game['startDate'], games_missed=games_missed, season=season,
                               season_ending=season_ending)


@app.route('/manual/', methods=['GET'])
def new_injury2():
    return render_template('addinjury2.html')


@app.route('/manual/injury', methods=['GET'])
def add_injury_manual():
    playerID = request.args.get('playerID')
    try:
        with connection.cursor() as cursor:
            sql = "SELECT firstName AS first, lastName AS last FROM nbaProfile WHERE id = %s"
            cursor.execute(sql, (playerID,))
            result = cursor.fetchone()
            if not result:
                return '<h1>This player is not in the database!<h1> <a href="/injury/">Try Again</a>'
            first = result['first']
            last = result['last']
            print('player ID = ' + playerID)
    except ConnectionError:
        print('Connection Error')
    return render_template('addinjury2.html', first=first, last=last, playerid=playerID)


@app.route('/injury/new/submit', methods=['POST'])
def add_injury():
    playerID = request.form['playerID']
    season = request.form['season']
    injury_date = request.form['injury_date']
    return_date = request.form['return_date']
    side = request.form['side']
    part = request.form['part']
    description = request.form['description']
    occurrence = request.form['contact']
    surgery = request.form['surgery']
    ending = request.form['ending']
    rest = request.form['rest']
    games_missed = request.form['games_missed']
    minutes = request.form['minutes']
    severity = request.form['severity']
    surgeryDate = request.form['surgeryDate']
    try:
        with connection.cursor() as cursor:
            if return_date == "":
                return_date = '1000-01-01'
            if season == "" or injury_date == "" or part == "" or rest == "" or games_missed == "" or minutes == "":
                return '<h1>Must fill in required fields.  Click the back button in the browser to fill them in!!!</h1>'
            sql = """INSERT INTO nbaInjury (playerID, season, injuryDate, returnDate, side, bodyPart, description, 
            occurrence, surgery, seasonEnding, rest, gamesMissed, minutesPrior, severity)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""
            sql2 = """INSERT INTO nbaInjury (playerID, season, injuryDate, returnDate, side, bodyPart, description, 
            occurrence, surgery, seasonEnding, rest, gamesMissed, minutesPrior, severity, surgeryDate)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""

            if surgeryDate:
                cursor.execute(sql2, (playerID, season, injury_date, return_date, side, part, description,
                                      occurrence, surgery, ending, rest, games_missed, minutes, severity, surgeryDate))
            else:
                cursor.execute(sql, (playerID, season, injury_date, return_date, side, part, description,
                                     occurrence, surgery, ending, rest, games_missed, minutes, severity))
            connection.commit()
    except ConnectionError:
        print('Connection error: injury submission')
    print('Injury submitted')
    return redirect('/injury')


# =================================================REMOVE INJURY PAGE ==================================================
@app.route('/injury/delete', methods=['GET'])
def remove_injury():
    return render_template('removeInjury.html')


@app.route('/injury/delete/submit', methods=['POST'])
def remove_injury_submit():
    form_id = request.form['injuryID']
    try:
        with connection.cursor() as cursor:
            sql = """DELETE FROM nbaInjury WHERE id = %s"""
            cursor.execute(sql, (form_id,))
            connection.commit()
    except ConnectionError:
        print("Oops! Could not connect")
    print('Requesting the DELETE PLAYER page : injury deleted: %s' % form_id)
    return redirect('/injury/delete')


# ========================================= NEW PLAYER PAGE ========================================================
@app.route('/player/', methods=['GET'])
def player():
    try:
        with connection.cursor() as cursor:
            sql = 'SELECT COUNT(*) AS count FROM nbaProfile;'
            cursor.execute(sql)
            result = cursor.fetchone()
            print(result)
            counter = result['count']
        return render_template('newPlayer.html', value=counter)
    except ConnectionError:
        print('Oops! Could not connect')


@app.route('/player/new/', methods=['POST'])
def new_player():
    playerid = request.form['playerID']
    fname = request.form['fname']
    lname = request.form['lname']
    height = request.form['height']
    weight = request.form['weight']
    pos = request.form['position']
    shootingHand = request.form['hand']
    birthDate = request.form['birthDate']
    birthPlace = request.form['birthPlace']
    college = request.form['college']
    highSchool = request.form['highSchool']
    draftYear = request.form['draftYear']
    draftNum = request.form['draftNum']
    race = request.form['race']
    try:
        with connection.cursor() as cursor:
            sql = """INSERT INTO nbaProfile (id, firstName, lastName, height, weight, positions, shootingHand, birthDate, 
                                          birthPlace, college, highSchool, race, draftYear, draftNum)
                      VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            cursor.execute(sql,
                           (playerid, fname, lname, height, weight, pos, shootingHand, birthDate, birthPlace, college,
                            highSchool, race, draftYear, draftNum))
            connection.commit()
    except ConnectionError:
        print("Oops! Could not connect")
    print('Requesting the NEW PLAYER page : new player created: %s %s' % (fname, lname))
    return redirect('/player/')


# ================================================== REMOVE PLAYER PAGE ==============================================
@app.route('/player/delete/', methods=['GET'])
def remove_player_page():
    return render_template('removePlayer.html')


@app.route('/player/delete/submit', methods=['POST'])
def remove_player():
    form_id = request.form['playerID']
    try:
        with connection.cursor() as cursor:
            sql = """DELETE FROM nbaProfile WHERE id = %s"""
            cursor.execute(sql, (form_id,))
            connection.commit()
    except ConnectionError:
        print("Oops! Could not connect")
    print('Requesting the DELETE PLAYER page : player deleted: %s' % form_id)
    return redirect('/player/delete')


# ====================================================DISPLAY PLAYER INJURIES =======================================
@app.route('/display/', methods=['GET'])
def display_injuries_page():
    return render_template('displayInjury.html')


@app.route('/display/info/', methods=['GET'])
def display_injuries():
    playerID = request.args.get('playerID')
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM nbaInjury WHERE playerID = %s"
            cursor.execute(sql, (playerID,))
            results = cursor.fetchall()
            sql2 = "SELECT firstName, lastName FROM nbaProfile WHERE id = %s"
            cursor.execute(sql2, (playerID,))
            name = cursor.fetchone()
            first = name['firstName']
            last = name['lastName']
    except ConnectionError:
        print('Connection Error')
    return render_template('displayInjury.html', results=results, first=first, last=last)


# ============================================================ RUN APP =============================================
if __name__ == '__main__':
    app.run()
