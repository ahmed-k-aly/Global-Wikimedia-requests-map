import json

json_file = open('wikipedia.json', 'r')
data: dict = json.load(json_file)
newDict: dict = {}
# Loop through all pages.
    # Loop through all entries per page.
        # put all entries in one page together in an array.
        # find max element from mean in that array.
        # return that entry only as {page: {time: requests}} or {page: (time, requests)}
    # put that entry into the main dict as returned above.
# loop through that dict in search of the 10 highest values.