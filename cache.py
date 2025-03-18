import os
import datetime


class Cache:
    def __init__(self):
        if not os.path.exists('./.cache/cache'):
            os.mkdir('./cache')

    def parse_cache(self):
        with open('./.cache/cache', 'r') as fp:
            for line in fp:
                cache_entry = self.parse_cache_entry(line)

                if cache_entry.expiry >= datetime.now():
                    self.entries[cache_entry.path] = cache_entry

    def parse_cache_entry(cache_line):
        return False
