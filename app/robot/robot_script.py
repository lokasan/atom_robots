import asyncio
import argparse
import datetime
import logging
import signal
import psutil
import time
import sys
import os

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

from db import services

parser = argparse.ArgumentParser(description='Asynchronous counter that prints '
                                             'numbers to the console every '
                                             'second, starting from a given '
                                             'initial value.')

parser.add_argument('-c', '--count', dest='count', default=0,
                    help='Initial counter value (default: 0)')

args = parser.parse_args()

update_queue = asyncio.Queue()

terminate_flag = False

robot_id = 0

p = psutil.Process()

start_time = p.create_time()

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def handle_sigbreak(signum, frame):
    """Handles SIGBREAK and SIGINT signals to gracefully terminate the counter.

    :param signum: The signal number (e.g., signal.SIGBREAK, signal.SIGINT).
    :param frame: The current stack frame (not used in this handler).
    """
    global terminate_flag
    terminate_flag = True

    duration = int(time.time() - start_time)

    update_queue.put_nowait(services.update_robot(robot_id, duration))

    logger.info(f'The robot has been stopped. Duration of work: {duration} '
                f'seconds. Its PID is {p.pid}')


async def print_number(start_number: int):
    """Prints numbers to the console every second, starting from the given initial value.

    :param start_number: The initial value for the counter.
    """
    while not terminate_flag:
        print(start_number)
        start_number += 1
        await asyncio.sleep(1)


async def process_update_queue():
    """Processes tasks from the update queue asynchronously.

    This function continuously retrieves tasks from the `update_queue`
    and awaits their completion.
    :return:
    """
    while True:
        update_task = await update_queue.get()
        await update_task


async def main():
    """Parses command-line arguments, sets up the counter, and starts asynchronous tasks.

    This function handles argument parsing, creates a new robot entry
    in the database,
    sets up tasks for printing numbers and processing updates,
    and waits for their completion.
    """
    try:
        tz = datetime.timezone.utc
        sql_datetime = datetime.datetime.fromtimestamp(start_time,
                                                       tz=tz)
        start_time_str = sql_datetime.strftime('%Y-%m-%d %H:%M:%S')
        logger.info(f'The robot was launched with PID: {p.pid}')

        global robot_id
        await services.create_database()
        robot_id = await services.set_robot(sql_datetime, int(args.count), p.pid)
        update_task = asyncio.create_task(process_update_queue())
        print_task = asyncio.create_task(print_number(int(args.count)))

        await asyncio.wait([update_task, print_task],
                           return_when=asyncio.FIRST_COMPLETED)
    except ValueError:
        logger.error('Error: --count argument must be a number.')
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        logger.error('An error occurred with the process')


signal.signal(signal.SIGBREAK, handler=handle_sigbreak)
signal.signal(signal.SIGINT, handler=handle_sigbreak)

if __name__ == '__main__':
    asyncio.run(main())
