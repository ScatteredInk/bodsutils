import sys
import json
from bodsutils import bods_schema, test_valid_bods

def main():
    schema = bods_schema()
    for jsonline in sys.stdin:
        test_valid_bods(json.loads(jsonline), schema)
if __name__=='__main__':
    sys.exit(main())