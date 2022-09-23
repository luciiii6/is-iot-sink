import json

def check_json_format(doc):
    try:
        doc = json.loads(doc)
        return True
    except:
	    return False
