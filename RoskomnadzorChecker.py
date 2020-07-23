import urllib.request
import json
import datetime
import re

class RoskomnadzorChecker(object):
    """This module loads a JSON feed containing the full Roskomnadzor
    blacklist and enables searching using either string matching or
    regex.

    Methods:
        findMatches(field, pattern) -- simple string match of field for pattern
        findMatchesRegex(field, pattern) -- analogous regex matching
    """
    FIELDS = ('ip', 'link', 'page', 'date', 'gos_organ', 'postanovlenie')

    def __init__(self, verbose):
        self.verbose = verbose
        self.startTime = datetime.datetime.now()

        # We have to specify a browser-like user agent to prevent from being blocked
        req = urllib.request.Request(
          'https://reestr.rublacklist.net/api/v2/current/json',
          headers={'User-Agent': 'Mozilla/5.0'}
        )

        # Load the data
        response = urllib.request.urlopen(req)
        raw_data = response.read()
        self._timeForOperation('Downloaded in')
        data = json.loads(raw_data)
        self._timeForOperation('Parsed JSON in')

        # Check to make sure data is current
        currDate = str(datetime.date.today())
        if not currDate in data.keys():
            raise RoskomnadzorCheckerError('Feed is out-of-date ' + currDate + ' ' + str(data.keys()))

        self.data = data[currDate]

    def findMatches(self, field, pattern):
        # This method checks our data for entries where a specified field
        # includes a string (pattern). '*' means all fields.
        self._checkValidField(field)
        matches = []
        for entry in self.data:
            if field == '*':
                if pattern in str(entry):
                    matches.append(entry)
            else:
                if pattern in str(entry[field]):
                    matches.append(entry)

        return matches

    def findMatchesRegex(self, field, pattern):
        # This method checks our data for entries where a specified field 
        # matches a regular expresion. '*' means all fields.
        self._checkValidField(field)
        matches = []
        for entry in self.data:
            if field == '*':
                if re.match(pattern, str(entry)):
                    matches.append(entry)
            else:
                if re.match(pattern, str(entry[field])):
                    matches.append(entry)

        return matches

    def _timeForOperation(self, message):
        # Prints how long has passed since the last time this method was run
        if self.verbose:
            timeStr = str(datetime.datetime.now() - self.startTime)
            print(message + ' ' + timeStr)
            self.startTime = datetime.datetime.now()

    def _checkValidField(self, field):
        # Checks if a field is in our list of valid fields
        if not field in self.FIELDS:
            raise RoskomnadzorCheckerError(field + ' is not a valid field!')

class RoskomnadzorCheckerError(Exception):
    """Exception for this module.

    Attributes:
        message -- explanation of the error
    """
    def __init__(self, message):
        self.message = message