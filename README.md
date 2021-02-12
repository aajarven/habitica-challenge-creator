# Habitica Challenge Creator

A simple web app that allows creating challenges in Habitica.

## Input Format

Challenges are created based on text input. The challenge description is in format
```
[name]
[shortname]
[summary]
[description]
[group]
[categories]
[prize]
Tasks
[a number of tasks here]
End Tasks
```

See https://github.com/Memry/Challenge-Creator for full description of the input format.

### Example Challenge

```
Test challenge name
test short name
Summary here
And description here
2ff2c55f-b894-46c4-a8bd-d86e47b872ff
Getting Organized;Creativity
0
Tasks
Daily;Daily 1;An easy everyday task;Easy;1.1.2021;Weekly;1;SMTWHFA
Habit;Habit 1;A medium habit;Medium
Daily;Daily 2;A hard daily for weekdays;Hard;1.1.2021;Weekly;1;MTWHF
Habit;To-Do 1;A hard todo, due by the end of February;Hard;28.2.2021
Daily;To-Do 2;An easy daily to be done on the 15th of February;Easy;15.2.2021;Weekly;1;0
End Tasks
```

## Running the App for Development Use

### Requirements

Use python 3. I encourage you to use virtualenv:
```
virtualenv .venv -p python3
source .venv/bin/activate
```

Required packages can be installed based on `requirements.txt`:
```
pip install -r requirements.txt
```

### Running the App

To make your site available on `localhost:5000`, you need to run
```
flask run
```
or if you have a virtual machine without ports configured, possibly
```
flask run --host=0.0.0.0
```
instead. After that you should be able to view the page with your browser.
