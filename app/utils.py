class BlockedBySiteError(Exception):
    pass

def parse_time(t):
    minutes, seconds = t.split(':')
    return int(minutes) * 60 + float(seconds)
