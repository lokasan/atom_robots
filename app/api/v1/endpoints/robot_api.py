from fastapi import FastAPI
from robot_manager import RobotManager

app = FastAPI()

robot = RobotManager()

@app.post('/start')
async def start(start_number: int = 0):
    return await robot.start(start_number)

@app.post('/stop')
async def stop(pid: int = 0):
    return await robot.stop(pid)
