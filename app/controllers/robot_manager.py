import asyncio
import os
import sys
import signal
import psutil
import datetime
import subprocess
import json
import time
from typing import Dict

from fastapi import HTTPException, Response

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

from db import services


class RobotManager:
    """
    This class is responsible for managing the lifecycle of robot processes.
    It allows you to start and stop robot instances
    and handle errors during these operations.

    ## Example

    ```python
    from controllers import RobotManager

    robot = RobotManager()
    await robot.start()
    await robot.stop()
    ```
    """
    def __init__(self):
        self.project_root = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), '..')
        self.lock = asyncio.Lock()

    async def start(self, start_number: int = 0):
        """Starts a new robot instance.

            :param start_number: The initial number that the robot
                will display in the console. Defaults to 0.
            :return: A Response object containing a JSON message
                with the PID of the started robot(s).
            :raises HTTPException: If the robot script is not found or
                an error occurs while starting the process.
        """
        robot_script_path = os.path.join(self.project_root, 'robot',
                                         'robot_script.py')

        async with self.lock:
            try:
                venv_path = os.environ.get('VIRTUAL_ENV')

                if venv_path:
                    python_path = os.path.join(venv_path, 'scripts', 'python')
                else:
                    python_path = 'python'

                instance_bot = subprocess.Popen(
                    [python_path, robot_script_path, '--count',
                     str(start_number)],
                    creationflags=subprocess.CREATE_NEW_CONSOLE
                )

                message = f'Robot started successfully.'

                return Response(
                    content=json.dumps({'message': message}),
                    media_type="application/json", status_code=200)

            except FileNotFoundError:
                raise HTTPException(
                    status_code=404,
                    detail='Robot script not found.')

    async def _stop_and_update_robot(self, proc: Dict):
        """Stops a robot process and updates information in the database.

            :param proc: A dictionary containing information
                about the robot process (id, pid, start_date).
            """
        p = psutil.Process(proc.get("pid"))
        now_time = time.time()
        duration = int(now_time - p.create_time())
        await services.update_robot(proc.get("id"), duration)
        await self._stop_process(proc.get("pid"), proc.get("start_date"))

    async def _stop_robot_by_pid(self, pid: int) -> str:
        """Stops a robot by process ID.

            :param pid: The process ID of the robot.
            :return: A message indicating successful stop or error.
            :raises HTTPException: If the robot with the specified
                PID is not found or not running.
            """
        try:
            p = psutil.Process(pid=pid)
            if not p:
                raise HTTPException(
                    status_code=400,
                    detail={"message": f"Process with PID {pid} not found."}
                )

            tz = datetime.timezone.utc
            sql_datetime = datetime.datetime.fromtimestamp(p.create_time(),
                                                           tz=tz)
            prc = await services.get_process(sql_datetime, pid)
            if not prc:
                raise HTTPException(
                    status_code=400,
                    detail=f"Robot with PID {pid} not found among the running ones."
                )

            await self._stop_and_update_robot(prc)
            return f"Robot stopped. PID: {pid}"
        except psutil.NoSuchProcess as e:
            raise HTTPException(
                status_code=400,
                detail=f"Robot with PID {e} not found"
            )

    async def _stop_all_robots(self):
        """Stops all running robot processes."""
        processes = await services.get_processes()
        for proc in processes:
            try:
                await self._stop_and_update_robot(proc)
            except psutil.NoSuchProcess:
                pass
            await asyncio.sleep(0.03)

    async def stop(self, pid: int):
        """Stops a running robot instance.

            :param pid: The process ID of the robot to stop.
                If not provided, all running robots will be stopped.

            :return: A Response object containing a JSON message
                confirming the robot(s) stopped successfully.

            :raises HTTPException: If an error occurs while
                stopping the process(es).
        """
        async with self.lock:
            if not pid:
                await self._stop_all_robots()
                message = "All robots have been stopped!"
            else:
                message = await self._stop_robot_by_pid(pid)

        return Response(
            content=json.dumps({'message': message}),
            media_type="application/json",
            status_code=200
        )

    async def _stop_process(self, pid: int, start_date: str):
        """Stops the robot process by PID and start date.

        :param pid: Process ID
        :param start_date: Process start date
        """
        try:
            pr = psutil.Process(pid=pid)
        except psutil.NoSuchProcess:
            return

        tz = datetime.timezone.utc
        sql_datetime = datetime.datetime.fromtimestamp(pr.create_time(), tz=tz)

        if start_date == sql_datetime.replace(tzinfo=None):
            try:
                prc = subprocess.run(
                    ['taskkill', '/F', '/T', '/PID', str(pid)],
                    capture_output=True, text=True)
            except psutil.NoSuchProcess:
                pass
            except Exception as e:
                print(f'Exception: {type(e)}')
                raise HTTPException(
                    status_code=400,
                    detail=f'Failed to stop processes {pid}. '
                           f'Internal Server Error.')
