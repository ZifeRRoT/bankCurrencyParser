import os
from multiprocessing import Process
from config import headers
from dotenv import load_dotenv


def get_bank_modules():
    modules = next(os.walk("banks"))[2]
    modules = [__import__("banks.%s" % x[:-3], fromlist="start") for x in modules]
    # return [__import__("banks.oschadbank", fromlist="start")]
    return modules


def main():
    tasks = [Process(target=x.start(headers)) for x in get_bank_modules()]
    for task in tasks:
        task.start()


if __name__ == '__main__':
    load_dotenv()
    main()
