import sys
import os

from fastapi import APIRouter

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             '..', '..', '..'))

if __package__ is None or __package__ == "":
    from consts import TAGS_METADATA, ROBOT_MANAGEMENT, ROBOT_STATISTICS
else:
    from .consts import TAGS_METADATA, ROBOT_MANAGEMENT, ROBOT_STATISTICS
from controllers import RobotManager
from db import services

router = APIRouter()

robot = RobotManager()

@router.on_event('startup')
async def startup_event():
    "Create database on SQlite"
    await services.create_database()

@router.post('/start', tags=[ROBOT_MANAGEMENT])
async def start(start_number: int = 0):
    """Starts a new robot instance with the specified start number.

        Multiple robot instances will share the same console window and
        output their values sequentially.

        :param start_number:
            The initial number that the robot will display in the console.
            Defaults to 0.
        :return: A JSON response containing a message with the PID of the
        started robot.
        :raises FileNotFoundError: If the robot script is not found
        (404 Not Found).

         ## Example
         Start a new robot instance with initial number is 0
         ```
         POST /start
         ```
         Start a new robot instance with an arbitrary initial value
         ```
         POST /start?start_number=1234
         ```
    """
    return await robot.start(start_number)

@router.post('/stop', tags=[ROBOT_MANAGEMENT])
async def stop(pid: int = 0):
    """Stops a running robot instance.

    This endpoint allows you to terminate a specific robot process
    or stop all currently running robots.

    :param pid: The process ID (PID) of the robot to stop.
        If not provided (or set to 0), all running robots will be stopped.

    :return: JSONResponse: A JSON response indicating the result of the stop
        operation.
            **On Success:**
                * If a specific PID is provided and the robot is found:
                    ```json
                    {"message": "Robot with PID {pid} stopped successfully."}
                    ```
                * If no PID is provided or set to 0 (stopping all robots):
                    ```json
                    {"message": "All robots have been stopped!"}
                    ```
            **On Failure:**
                * 400 Bad Request:
                    * If there are no robots currently running.
                    * If an error occurs while stopping the process(es).
                    * If the robot with the specified PID is not found
                        among the running ones.
                    The response will include a detailed error message.

    :raises HTTPException: Raised with appropriate status codes and messages
    for error conditions as described above.

    ## Example
    Stop a specific robot with PID 1234:
    ```
    POST /stop?pid=1234
    ```
    Stop all running robots:
    ```
    POST /stop
    ```
    """
    return await robot.stop(pid)


@router.get('/stats', tags=[ROBOT_STATISTICS])
async def stats(offset: int = 0, limit: int = 20, order_by: str = 'asc'):
    """Retrieves robot run statistics with pagination and sorting.

        :param offset: Offset from the beginning of the result set.
        :param limit: Maximum number of records to return.
        :param order_by: Sorting direction: 'asc' (ascending) or 'desc'.
        :return: A JSON response containing a list of dictionaries.

        The structure of each robot run dictionary is as follows:
            * **id (int):** Robot run ID.
            * **start_date (datetime):** Date and time of the robot run start.
            * **pid (int):** Process id of the robot run.
            * **duration (float):** Duration of the robot run.
            * **start_number (int):** Robot run number.
        ## Example
        Get the first 20 robot runs in ascending order:
        ```
        GET /stats
        ```
        Get the next 10 robot runs in descending order, starting from the
        21st record:
        ```
        GET /stats?offset=20&limit=10&order_by=desc
        ```
    """
    return await services.get_stats(offset, limit, order_by)