import asyncio
import argparse

parser = argparse.ArgumentParser(description='Asynchronous counter that prints '
                                             'numbers to the console every '
                                             'second, starting from a given '
                                             'initial value.')

parser.add_argument('-c', '--count', dest='count', default=0,
                    help='Initial counter value (default: 0)')

args = parser.parse_args()

async def print_number(start_number: int):
    """
    :param start_number: The initial value for the counter.
    """
    while True:
        print(start_number)
        start_number += 1
        await asyncio.sleep(1)

async def main():
    """
    Parses command-line arguments and starts the asynchronous counter.
    """
    try:
        await print_number(int(args.count))
    except ValueError:
        print('Error: --count argument must be a number.')

if __name__ == '__main__':
    asyncio.run(main())
