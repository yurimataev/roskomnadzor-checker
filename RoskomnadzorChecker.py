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

    def __init__(self):
        # We have to specify a browser-like user agent to prevent from being blocked
        req = urllib.request.Request(
          'https://reestr.rublacklist.net/api/v2/current/json',
          headers={'User-Agent': 'Mozilla/5.0'}
        )

        # Load the data
        response = urllib.request.urlopen(req)
        data = json.loads(response.read())

        # Check to make sure data is current
        currDate = str(datetime.date.today())
        if not currDate in data.keys():
            raise JsonDataError('Feed is out-of-date ' + currDate + ' ' + str(data.keys()))

        self.data = data[currDate]

    def findMatches(self, field, pattern):
        # This method checks our data for entries where a specified field
        # includes a string (pattern). '*' means all fields.
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
        matches = []
        for entry in self.data:
            if field == '*':
                if re.match(pattern, str(entry)):
                    matches.append(entry)
            else:
                if re.match(pattern, str(entry[field])):
                    matches.append(entry)

        return matches


class JsonDataError(Exception):
    """Exception raised for errors in the JSON feed.

    Attributes:
        message -- explanation of the error
    """
    def __init__(self, message):
        self.message = message