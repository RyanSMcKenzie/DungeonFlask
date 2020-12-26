# DungeonFlask
A Dungeons &amp; Dragons character sheet Flask app.

# Motivation
I wanted to design a practical and useful application to help manage data for a family-favorite game. 
Erasing and rewriting or simply reprinting character sheets is a hassle, so storing your characters online
simplifies managing your characters.

# Language/Frameworks
Backend - Python3, Google Firestore
Frontend - HTML, Jinja, Bootstrap
Testing - TravisCI
Deployment - Docker, Google Cloud Run

# Features
1) Create an account, login and logout freely
2) Create and edit your character sheets - save your data on Google Firestore
3) Add and remove equipment, change your stats, level, anything you need
--- Development --
4) User data held in sessions to ensure backend and frontend communicate properly
5) Appropriate routes guarded by login requirement
6) Tested and integrated with TravisCI
7) Containerized with Docker
8) Continuous deployment on Google Cloud Run

# Try it out
Want to try it for yourself? Head over to the app [here](https://dungeon-flask-nvxsto2xda-uc.a.run.app).
