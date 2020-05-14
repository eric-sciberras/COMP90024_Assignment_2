import json
import pickle
import logging

# logging.basicConfig()
# logging.getLogger().setLevel(logging.DEBUG)

output_file_path = "debug.json"

def export_tweet(tweet):
    with open(output_file_path, "a") as f:
        f.write(json.dumps(tweet)+"\n")


def load_checkpoint(city):
    value = None
    try:
        value = pickle.load(open("checkpoint.pickle", "rb"))[city]
    except (OSError, IOError):
        logging.info(f'No Checkpoint file found')
    except KeyError:
        logging.info(f'No value for {city} found')
    except Exception as e:
        logging.error(f'{repr(e)}')
    logging.info(f'Value: {str(value)}')
    return value

def save_checkpoint(city, last_id):
    try:
        checkpoint = pickle.load(open("checkpoint.pickle", "rb"))
    except (OSError, IOError):
        logging.info(f'No Checkpoint file found')
        checkpoint = {}
    except Exception as e:
        logging.error(f'{repr(e)}')
    finally:
        checkpoint[city] = last_id
        pickle.dump(checkpoint, open("checkpoint.pickle", "wb"))
        return
