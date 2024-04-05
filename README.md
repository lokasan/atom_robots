# [GreenAtom Robots API (Test Task)](https://github.com/lokasan/atom_robots) &middot; [![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)]()

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

![TestTask API](https://downloader.disk.yandex.ru/preview/51b79d858b2a11bfbff04267cf1a6052ac1d6ea8881d8bce61980655d6ef620b/6610588b/Tn8cqT6OKWjUfW7Yoi0PhkTb_GbGRX8cFujzmy4MxO7gOtTV9glMpTNWd0KUyYncPV2Nn7Xu7q88JrHhfuGkLg%3D%3D?uid=0&filename=greenatom_testtask_doc.JPG&disposition=inline&hash=&limit=0&content_type=image%2Fjpeg&owner_uid=0&tknv=v2&size=2048x2048)

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
| Statistics for all robots                                                                                                                                                                                                                                                                                                                                                 |
|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| ![Statistics](https://downloader.disk.yandex.ru/preview/537d70856ac0704c58727c2fc9775864061fbd88a314ff598a56e62f4dec6265/661050a4/wUcBXhTZiOr3hg8TBmCGVwAFvZnkOy6T-TBRz6XYy4zXjAoOAtEpA4ruHXstCQ68fBS1we4Z_FP5FZlE4LDSKw%3D%3D?uid=0&filename=all_stats.JPG&disposition=inline&hash=&limit=0&content_type=image%2Fjpeg&owner_uid=0&tknv=v2&size=2048x2048) |
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
| Starting robot                                                                                                                                                                                                                                                                                                                                          |
|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| ![Start Robot from console](https://downloader.disk.yandex.ru/preview/1ad12ba80d5dd2bd36e170bab985ee648ff410f932880949e04032b8cfb57b2d/66105456/hY_5cPhDsuLUQO-Ra7FOjqLh9rBwBWciGSODJKeB18QZnrdVq61F52kzKSqqsJny9BOgFTqvBh94tr9usbN5DA%3D%3D?uid=0&filename=console_start.JPG&disposition=inline&hash=&limit=0&content_type=image%2Fjpeg&owner_uid=0&tknv=v2&size=2048x2048) |
3 - If you want to start counting from a different number, then use the following command
```bash
$ python robot_script.py -c 50
```
| Starting the robot with initial number                                                                                                                                                                                                                                                                                                                                                             |
|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| ![Robot from Console with initial number](https://downloader.disk.yandex.ru/preview/88bb0d65840eb9218100beebce3b9124039de6f41f35bd031a336a958989a7b5/66105514/q0815BD9jXCiYtXFXv5QCT6nuzgPWShNCxtrbx2bFcdlKLSOSAQoHxXXwTzC8CKOYkGsi-pfcVJ9bnD3Ql0cqQ%3D%3D?uid=0&filename=console_start_initial.JPG&disposition=inline&hash=&limit=0&content_type=image%2Fjpeg&owner_uid=0&tknv=v2&size=2048x2048) |
# Additional Notes
* The project uses a SQLite database (robots.db) to store information about robot runs.
* The API endpoints are tagged for better organization in the documentation.

# License
This project is licensed under the MIT License. See the [LICENSE](https://github.com/lokasan/atom_robots/blob/master/LICENSE) file for details.

# Contact
Contact
For questions or support, please contact [Email](mailto:borisostroumov@gmail.com).