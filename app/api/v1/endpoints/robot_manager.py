import asyncio
import os
import signal
import subprocess
import json
from fastapi import HTTPException, Response


class RobotManager:
    """
    This class manages the lifecycle of robot processes.
    """
    def __init__(self):
        self.instances_robots = {}

    async def start(self, start_number: int = 0):
        """
        Starts a new robot instance.

        :param start_number:The initial number that the robot
        will display in the console. Defaults to 0.

        :return: A Response object containing a JSON message
        with the PID of the started robot(s).

        :raises: HTTPException: If the robot script is not found or
        an error occurs while starting the process.
        """

        project_root = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                    '..', '..', '..', '..')
        robot_script_path = os.path.join(project_root, 'app', 'robot',
                                         'robot_script.py')

        try:
            instance_bot = subprocess.Popen(
                ['python', robot_script_path, '--count', str(start_number)],
                creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
            )

            process = self.instances_robots.get(instance_bot.pid, None)

            if process:
                process.send_signal(signal.CTRL_BREAK_EVENT)

            self.instances_robots[str(instance_bot.pid)] = instance_bot

            message =  f'Robot started successfully. Its PID: {instance_bot.pid}'

            return Response(
                content=json.dumps({'message': message}),
                media_type="application/json", status_code=200)

        except FileNotFoundError:
            raise HTTPException(
                status_code=404,
                detail='Robot script not found.')

    async def stop(self, pid: int):
        """
        Stops a running robot instance.

        :param pid: The process ID of the robot to stop.
        If not provided, all running robots will be stopped.

        :return: A Response object containing a JSON message
        confirming the robot(s) stopped successfully.

        :raises: HTTPException: If an error occurs while
        stopping the process(es).
        """
        if not len(self.instances_robots.items()):
            raise HTTPException(status_code=400,
                                detail=f'No robots are currently working!')

        if not pid:
            for pid, process in list(self.instances_robots.items()):
                try:
                    del self.instances_robots[pid]
                    process.send_signal(signal.CTRL_BREAK_EVENT)
                except Exception as e:
                    print(e)
                    raise HTTPException(
                        status_code=400,
                        detail=f'Failed to stop processes '
                               f'{process.pid}. '
                               f'Internal Server Error.')

            message = 'All robots have been stopped!'
            return Response(
                content=json.dumps({'message': message}),
                media_type="application/json", status_code=200)

        process = self.instances_robots.get(str(pid), None)

        if process:
            try:
                del self.instances_robots[str(pid)]
                process.send_signal(signal.CTRL_BREAK_EVENT)

                return Response(
                    content=json.dumps(
                        {'message': f'Robot stoped. Its PID: {pid}'}),
                    media_type="application/json", status_code=200)

            except ProcessLookupError:
                return HTTPException(status_code=400, detail={
                    'message': f'Process with PID {pid} not found.'})

            except Exception as e:
                raise HTTPException(status_code=400,
                                    detail=f'Failed to stop processes '
                                           f'{process.pid}. '
                                           f'Internal Server Error.')
        else:
            raise HTTPException(status_code=400,
                                detail=f'The robot with the passed '
                                       f'PID: {pid} is not among '
                                       f'the running ones')
