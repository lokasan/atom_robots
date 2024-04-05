import asyncio
import os
import sys
import signal
import psutil
import datetime
import subprocess
import json

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
                instance_bot = subprocess.Popen(
                    ['python', robot_script_path, '--count', str(start_number)],
                    creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
                )


                message =  f'Robot started successfully. Its PID: ' \
                           f'{instance_bot.pid}'

                return Response(
                    content=json.dumps({'message': message}),
                    media_type="application/json", status_code=200)

            except FileNotFoundError:
                raise HTTPException(
                    status_code=404,
                    detail='Robot script not found.')

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
                processes = await services.get_processes()
                for proc in processes:
                    await self._stop_process(proc.get('pid'),
                                             proc.get('start_date'))
                    await asyncio.sleep(0.03)
                message = 'All robots have been stopped!'
            else:
                p = psutil.Process(pid=pid)
                if p:
                    tz = datetime.timezone.utc
                    sql_datetime = datetime.datetime.fromtimestamp(
                        p.create_time(), tz=tz)
                    prc = await services.get_process(sql_datetime, pid)
                    if prc:
                        await self._stop_process(pid, prc.get('start_date'))
                        message = f'Robot stoped. Its PID: {pid}'
                    else:
                        raise HTTPException(
                            status_code=400,
                            detail=f'The robot with the passed PID: {pid} '
                                   f'is not among the running ones'
                        )
                else:
                    raise HTTPException(
                        status_code=400,
                        detail={
                            'message': f'Process with PID {pid} not found.'}
                    )

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
                os.kill(pid, signal.CTRL_BREAK_EVENT)
            except psutil.NoSuchProcess:
                pass
            except Exception:
                raise HTTPException(
                    status_code=400,
                    detail=f'Failed to stop processes {pid}. '
                           f'Internal Server Error.')
