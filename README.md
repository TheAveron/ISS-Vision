# ISS-explorer

## Description

This site his my final project to the Harvard's CS50 course.

This is a website made in python 3.12 with Flask that shows the current position of the iss around the world and it future trajectory.

There is also some complementary informations, like the crew actually on board, the speed, the altitude, and a calculator of the next three passes near your location (needs you to allow acces to geolocation of course).

I have separated all my files in different folders, putting the python scripts in a folder named "modules", and all the js and css in a folder callded static, separated in two subfolders. The html files are in a folder called "templates".

### Python files

The "app.py" file contain all the flask app core. I try to put there the minimal amount of code, puting everything in separate functions in ordered files, and import them in after.
In the "database.py" file, we have everything about the database gestion.
In "iss_info.py", we have all the functions related to the crew on board.
In "iss_traker.py", we have all the functions related to the position of the iss, and the metics of the spacecraft.
In "tle_fetcher.py", we get the tle information using external api for retrieving infos about the iss.
In "user_service.py" we have everything that concern the user logs, and map settings.

The similar logic is used in the js files, separating functions and infos according to the group of things they belong to.

For the html files, we have four part, one with the common things across the site, the "index.html" for the homepage, the "login.html" for the login page and "register.html" for the register page.

## Video Presentation

**[Video link](https://youtu.be/86QOJ3cgrl4)**

### Video transcription

Hello, my name is Victor, and this is the presentation of my final project of Harvard's CS50 course. It is Sunday the 8th of September two thousand twenty four, my github name is TheAveron, and my edx name is victor_1791. My project, called "Space Station Vision", is like its name says, a website for viewing where is the space station around the earth. on the homepage, we can see different information about the iss. First, on the right, we can see the actual speed of the station, its altitude and the crew currently on board. On the bottom right, we have a button that calculates the next three passes of the ISS over your location. Finally, we can change certain settings for the map, such as whether the iss_icon is shown and whether the trajectory is shown. We can also adjust the trajectory time, which defines how many hours of the trajectory we want to see. You can also create an account and to save theses settings for the next time you connect. I hope you enjoy using my project and thank you to your listening.
