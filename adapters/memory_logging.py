class MemoryLogging():
    def __init__(self):
        self.logs = []

    def debug(self, message):
        self.logs.append(('DEBUG', message))

    def info(self, message):
        self.logs.append(('INFO', message))

    def warning(self, message):
        self.logs.append(('WARNING', message))

    def error(self, message):
        self.logs.append(('ERROR', message))

    def dump(self):
        return self.logs


memory_logging = MemoryLogging()
