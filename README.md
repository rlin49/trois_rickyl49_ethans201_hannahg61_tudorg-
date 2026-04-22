# Accro aux Jeux Vidéo by Trois

## NOTE: BECAUSE OUR DATA FILE IS BOTH SMALL AND PROPRIETARY WE HAVE CHOSEN TO KEEP IT IN THE REPO INSTEAD OF MAKING USERS REDOWNLOAD THE ORIGINAL CSV AND THEN RUN THE PROGRAM TO CONVERT THAT INTO A JSON FILE

Ricky (PM): Database functions, frontend

Ethan: User handling (creating profiles, making reviews, etc)

Hannah: Frontend, graphs

Tudor: Database sanitation, APIs, backend

# description
Users are given game information and have to guess total sales, which updates a graph showing their guesses vs actual sales, growing each round. On their own profile, users can rank their favorite games while also seeing their accuracy in games. Users will be able to view other players profiles, while also seeing the top players and top rated games.

#### Visit our live site at [167.71.85.43](http://167.71.85.43)



# Install Guide:

## Requirements:
  - python3 & git installed

### Clone repo:

  ``` git clone git@github.com:rlin49/trois_rickyl49_ethans201_hannahg61_tudorg-.git ```


### Cd into repo:

 ``` cd trois_rickyl49_ethans201_hannahg61_tudorg- ```


### Set up virtual environment:

``` python -m venv {{venv_path}} ```


### Activate virtual environment:

  - Linux/Mac:
    ``` source {{venv_path}}/bin/activate ```

  - Windows:
    ``` {{venv_path}}\Scripts\activate ```


### Install requirements:

  ``` $pip install -r requirements.txt ```



# Launch Codes:

### Activate virtual environment:

  - Linux/Mac:

    ``` {{venv_path}}/bin/activate ```

  - Windows:

    ``` {{venv_path}}\Scripts\activate ```


### Cd into app folder:

  ``` cd trois_rickyl49_ethans201_hannahg61_tudorg-/app ```

### Run \_\_init\_\_.py

  ``` python __init__.py ```

### FEATURE SPOTLIGHT
* You can access other people's profile through the search page. 
* You can access the gamepage where someone wrote a review through their profile.
* You can favorite games.

### KNOWN BUGS/ISSUES
* Submitting ratings/reviews and/or reloading the page too quickly in a short amount of time may cause issues and lock the database. Only known recourse is to remove the database file located at /app/Data/database.db, and then in /app run populate_db.py. App should work fine after but previous data will obviously have been wiped.
