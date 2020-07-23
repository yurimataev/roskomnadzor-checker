from RoskomnadzorChecker import RoskomnadzorChecker

if __name__ == '__main__':
    checker = RoskomnadzorChecker()

    print ("Search fields include " + ', '.join(checker.FIELDS) + ". Use * to search all fields.")
    while True:
        field = input("Search field: ")
        if field == '*':
            break
        elif field in checker.FIELDS:
            break
        else:
            print ("Invalid field")

    pattern = input("Search pattern: ")

    matches = checker.findMatches(field, pattern)
    
    for match in matches:
        print(str(match))

    print()
    print('Entries matched: ' + str(len(matches)))
    