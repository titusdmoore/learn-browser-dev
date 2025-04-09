import os
import datetime


class Cache:
    def __init__(self):
        if not os.path.exists('./.cache/cache'):
            os.mkdir('./cache')

        self.parse_cache()

    def parse_cache(self):
        with open('./.cache/cache', 'r') as fp:
            for line in fp:
                cache_entry = self.parse_cache_entry(line)

                if cache_entry.expiry >= datetime.now():
                    self.entries[cache_entry.path] = cache_entry

    def parse_cache_entry(cache_line):
        remote_path, expiry, cache_path = cache_line.split(",", 3)

    def cache_entry_to_string(cache_entry):
        return cache_entry.path + "," + cache_entry.expiry + ","
        + cache_entry.local_path

    def try_cache_hit(request):
        print("miss")
