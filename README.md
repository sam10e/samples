# nba-injury-form
NBA Injury database form.  This form helps you to manually input data about injuries and players into the nbaInjury tables in the BYU Stats Department database.  If you can't find a way to webscrape the data, this is a great way to get the data into the database so you don't have to type up a bunch of SQL code.  This does it for you!

## What you'll need
#### PyCharm from JetBrains
#### Python 3
#### MySQL Workbench/MySQL Shell
#### Access to the Sports Stats Database at BYU
#### VPN access to the BYU statistics department
#### Google Chrome
#### Files from this Git Repo
##### You also need to install the different Flask and python packages included at the top of the app.py file.  You can do this in the code by clicking the red light bulbs on the IDE.

## How to get it working on your computer
This form works by running the application on your local machine.  You can use any web developing IDE or program.  I used PyCharm from JetBrains so that's how I will describe how to get the application up and running.  I'm also assuming you have access to the BYU stats database and have VPN access thru the Stats Department.  It won't update any databases if you don't have that all set up thru Dr. Fellingham/the Stats Department.  

## CREATE A config.py FILE with your USER, PASS, DB, and HOST or else it won't connect.  Create it in the working directory with app.py

```
HOST='hostname'
USER='yourusername'
PASS='yourpassword'
DB='nameofteststatsdb'
```

## Running the Form
After installing PyCharm onto your computer, download the files or copy all of the code over so you have the files on your computer. Start the new project in PyCharm using the files from the Git Repo. The magic happens from the app.py file.  At the top right of PyCharm, there is a box with a dropdown.  This pulls up the Run/Debug Configuration window.  Add a Flask Server by clicking the green plus button at the top left.  Set the "Target" as the path to app.py.  Click Apply and Ok.  Run the app by having Flask Server (whatever you named it) as the main app configuration and press the green arrow up on the top by the dropdown you selected earlier.  This will run the app on the localhost and you can click on the link at the bottom (http://127.0.0.1:5000/) that the app creates which will open up a webpage on Google Chrome (assuming you have Google Chrome installed).

## Using the Form Application
After clicking on the link, you will be taken to the homepage.  There, you can select an option of what you would like to add or remove from the database.  Currently, there are only options to add an injury, add a player, or remove a player.

### Add injury
Type in the playerID of the player you wish to add injury information to.  You will be taken to a page with all of the form data to add the injury.  The * symbol are next to fields that are required for you to fill out or else the server will through an error.  When you click submit, the information will be added to the database.  There isn't anything setup yet to have you verify that everything is correct, so make sure you have everything correct before you submit.  You will be directed back to the injury page to select a new playerID.

### Remove Injury
Just type in the injuryID number into the field given and it will remove that injury from the nbaInjuryTest table.


### Add New Player
This is to add a player to the database that isn't already in there.  Web scraping is easier to add the information, but in case you have only a few players to add, this can prove useful. This will only update the nbaProfileTest table for now until we finalize a couple of things. If you want to leave a value blank, just type in NULL.  This might not work for draft pick, in which case just type in 0.  PlayerIDs should be the first 5 letters of their last name, first 2 letters of first name, and copy number (01 for most).  

```
PlayerID:  jamesle01 for LeBron James.
```

### Remove Player
Same as remove injury.  Type in the playerID into the field given and it will remove that player from the nbaProfileTest table.

## Using MySQL Shell
To get the shell up and running so you can look at your database, install and open the shell.  Run \sql to make it so sql commands are accepted.  **Make sure you are connected to the VPN**.
```
\sql
```
Then run \connect mysql://user@host (user and host given by stats department). 
```
\connect mysql://user@host
```

Type in your password to the database that you created thru the department.  Run USE dbname; to select the correct database to work with.  Database is the one from the test one from the BYU database.
```
USE databasename;
```
At this point, you should be able to run SQL queries to look at your database tables.

### Author
**Sam Tenney**
