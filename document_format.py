import sys

# Format the retrieved twitter data into CouchDB bulk document structure
def document_format(filePath):
    twitter_file = open(filePath, "r")
    twitter_string = twitter_file.read()
    twitter_file.close()

    twitter_list = twitter_string.split("\n")

    for count, json_obj in enumerate(twitter_list[1:len(twitter_list)], 1):
        if twitter_list[count] != "":
            twitter_list[count] = ","+json_obj

    new_twitter_string = '\n'.join(twitter_list)
    new_twitter_file = open(filePath, "w")
    new_twitter_file.write("{\n\"docs\": [\n")
    for i in new_twitter_string:
        new_twitter_file.write(i)
    new_twitter_file.write("\n]\n}")
    new_twitter_file.close()

"""
if __name__ == "__main__":
    filePath = sys.argv[1]
    document_format(filePath)
"""



