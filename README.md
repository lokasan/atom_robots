# [GreenAtom Robots API (Test Task)](https://github.com/lokasan/atom_robots) &middot; [![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/lokasan/atom_robots/blob/master/LICENSE)

## Description

This project implements a RESTful API using FastAPI to manage asynchronous robot processes. It allows you to:

* **Start robots:** Initiate new robot instances with a specified starting number.
* **Stop robots:** Terminate individual robots by their process ID (PID) or stop all running robots. 
* **View statistics:** Retrieve paginated and sorted statistics about robot runs, including start time, duration, and starting number.

## Getting Started

### Prerequisites

* Python 3.7 or later
* Required libraries (installed automatically):
    * fastapi
    * uvicorn
    * sqlalchemy
    * aiosqlite

## Installation
### A few steps
1 - Cloning a git repository
```bash
$ git clone https://github.com/lokasan/atom_robots.git
```
2 - Go to the root folder of the project
```bash
$ cd atom_robots
```
3 - Installing dependencies for the project
```bash
$ pip install -r requirements.txt
```
4 - Start the web server
```bash
$ uvicorn main:app --reload
```

## API Reference
The API documentation is available at http://127.0.0.1:8000/docs. It provides a detailed overview of the available endpoints, parameters, and responses.

![TestTask API](https://i.ibb.co/MpXgHdQ/greenatom-testtask-doc.jpg)

## Usage Examples

### Starting a Robot
* Start a robot with the default starting number (0):
```bash
curl -X POST http://127.0.0.1:8000/start
```
|Starting a Robot                                                                                                                                                                                              |
|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| ![Start Robot](https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExYnB2OGY3ODcxY2lydnl3cWVnZjQ3YzZrOXpoemtqYWtqODVqbmJ3NiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/t2KGnX9X6yVJrSISvV/giphy.gif) |
* Start a robot with a specific starting number (e.g., 42):
```bash
curl -X POST http://127.0.0.1:8000/start?start_number=42
```
| Starting a Robot with the initial number                                                                                                                                                                 |
|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| ![Strat Robot With Number](https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExOWZqcGdqMGcxeTNiY3hseGZ2OWZiM2l1aHhtb2NwdWs5bHNuZTJqdSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/a8boC9yUjnB6v2GWB4/giphy.gif) |
### Stopping a Robot
* Stop a robot by its PID (e.g., 23896):
```bash
curl -X POST http://127.0.0.1:8000/stop?pid=23896
```
| Stopping a Robot with pid                                                                                                                                                          |
|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| ![Stop Robot](https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExbXVoMzExemgwZm1xYWYyOXNlMHd4MHRnYm1qd3FhaHA4bXpyaHZtaCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/RgF8tyh10ogIqj0rZd/giphy.gif) |
* Stop all running robots:
```bash
curl -X POST http://127.0.0.1:8000/stop
```
| Stopping all running Robots                                                                                                                                                                      |
|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| ![Stop All Robots](https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExZWE5N2Y2cDM3a2p4NXplb240bnVka3djaGhrd2lkOGY3OTRieTJudiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/717hFnBJvIZfihrYe0/giphy.gif) |
### Viewing Statistics
* This **GET** request displays statistics on robot launches

Get statistics for the first 20 robot runs:
```bash
curl http://127.0.0.1:8000/stats
```
| Statistics for all robots                                                                                                                                                                                                                                                                                                                                                |
|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| ![Statistics](https://i.ibb.co/yPqHYXs/all-stats.jpg)                                                                                                                                                                                                                                                      |
* You can use multiple parameters in a query to display process information: 
  * **offset** - is responsible for how many records need to be skipped
  * **limit** - is responsible for how many records to display
  * **order_by** - is responsible for sorting order - (**asc** or **desc**). Default: asc 
```bash
curl http://127.0.0.1:8000/stats?offset=2&limit=10&order_by=desc
```
| Statistics with query parameters                                                                                                                                                                        |
|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| ![Statistics with params](https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExejN5MTVyYXVmaHA1enoycjk5MnpoMzVwaHBianU2MWVtMjFqMWNyeCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/9gfxWD3f4f7xzD1mXo/giphy.gif) |
## Usage Examples of Console
* The robot can work independently of the web server

1 - Navigate from the project root folder to the following path
```bash
$ cd app/robot
```
2 - Start the robot, the initial count number will be 0
```bash
$ python robot_script.py
```
| Starting robot                                                          |
|-------------------------------------------------------------------------|
| ![Start Robot from console](https://i.ibb.co/d6C9KGP/console-start.jpg) |

3 - If you want to start counting from a different number, then use the following command
```bash
$ python robot_script.py -c 50
```
| Starting the robot with initial number                                                                                                                                                                                                                                                                                                                                                      |
|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| ![Robot from Console with initial number](https://i.ibb.co/hHGcBGY/console-start-initial.jpg)                                                                                                                                                                                                                                                                                            |
# Additional Notes
* The project uses a SQLite database (robots.db) to store information about robot runs.
* The API endpoints are tagged for better organization in the documentation.

# License
This project is licensed under the MIT License. See the [LICENSE](https://github.com/lokasan/atom_robots/blob/master/LICENSE) file for details.

# Contact
Contact
For questions or support, please contact [Email](mailto:borisostroumov@gmail.com).