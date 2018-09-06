# Data Entry Key 

## Useful websites
To find the injury data, use http://www.prosportstransactions.com/basketball/Search/Search.php

To look up box scores, play-by-play, and team schedules, use basketball-reference.com.  Googling the team name schedule and year will help you find what you're looking for (Ex. Utah Jazz schedule 2017)

To look up the game recaps, Google team vs team year (Ex. Jazz vs Lakers 2007) and a recap should pop up from ESPN or NBA.com

## Season Start Year
Put the year that the season began when the injury occurred.  If it occurred in the offseason, put the year of the offseason (or season that will begin).

## Date of Injury
If the injury happened in a game, put the date of that game.  If you are unsure if the injury happened in a game, put the date that is on prosportstransactions.com.  

## Return Date
If you leave this field blank, the default is '1000-01-01', which will let you know that the injury is ongoing and player hasn't returned yet, or you need to go back in and edit the injury with the return date after the player returns.  Put the date that the player is off the IL and cleared to play, or their first game back if date of IL is not given.

## Side of Body
If side of body is not given, just select none, even if you know that the injury had to have been on a side.

## Body Part
Select the body part that most closely corresponds with the choices given, or type in the part in other if not given.  If the specific body part lies in the general area of one of the radio buttons, select the body part the most closley corresponds, and put the specific body part in the description.  Ex. For hamstring, select Leg; For elbow, select Arm.

## Description
The standard way to input data here is: 'sub-body part' 'diagnosis'.  Examples include: 
```
MCL sprain
ACL tear
Hamstring strain
Sprain
Concussion
Middle finger fracture
Elbow dislocation
```

## Contact or Non-Contact
If you don't know, put unsure.  You will have to look back at the game recap to find if it was contact or non-contact.  If not given, put unsure.  If the injury occurred in practice, search for a news article to see what it was.

## Surgery, Season-Ending
If the injury led to surgery, check the surgery button and input the date of the surgery, if found.  Leave blank if you don't know the surgery date (will show as NULL in database).  If the injury ended their season, put season-ending. Be careful when clicking on these buttons, once you do, you can't unclick.  Just refresh the page if you accidentally click on one of them.

## Days of Rest
If the injury happened during the offseason, or during the first game of the season, put '-1' in this field.  If the game was a back-to-back, put 0.  When counting days of rest, put the number of days that aren't game days before the game of injury.

## Games Missed
Don't count the game that the injury occurred in.  Self-explanatory, just count how many games the player missed after the injury.  If the player hasn't returned from injury yet when entering their data, put -1 to know that you need to go back to change it.  Count playoff games missed.

## Minutes in Game Before Injury
Look at the box score to find out how many minutes the player played before exiting with the injury.  If they didn't get hurt during the game, put 0.  If you are unsure the player got hurt during the game and are unable to find it in the play-by-play, box score, or game recap, put 0.

## Severity
Put the Grade level of injury severity if given.  Otherwise, leave blank.
