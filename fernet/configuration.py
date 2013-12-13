__author__ = 'spersinger'

class Configuration:
    @staticmethod
    def run():
        Configuration.enforce_ttl = True
        Configuration.ttl = 60

Configuration.run()
