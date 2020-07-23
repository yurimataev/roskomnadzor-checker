# Roskomnadzor Checker

This Python module makes use of the wonderful API made available by [Roskomsvoboda](https://roskomsvoboda.org/) to search the blacklist of Roskomnadzor (Russia's censorship agency). This is handy if you are worried about being blacklisted by the Russian government, as they aren't always great at communicating such actions.

## Usage

To use the CLI:

    python roskom-cli.py

If you're using it in your code, the RoskomnadzorChecker class has the following methods:

    checker = RoskomnadzorChecker()
    matches = checker.findMatches('fieldname', 'string')
    # or
    matches = checker.findMatchesRegex('fieldname', r'regex pattern')

`matches` will be a list
