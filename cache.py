import os


class Cache:
    def __init__(self):
        if not os.path.exists('./.cache/cache'):
            os.mkdir('./cache')

    def parse_cache(self):
        print("cache read")
