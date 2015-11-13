'''
asjson
======
json.dumps with datetime, date and bson.ObjectId support

    >>> from datetime import datetime, date
    >>> import asjson
    >>> import bson

    >>> asjson.dumps([datetime(2013, 1, 27, 6, 48, 0, 38835),
    ...               bson.ObjectId('aaaaaaaaaaaaaaaaaaaaaaaa')])
    '["2013-01-27T06:48:00.038835", "aaaaaaaaaaaaaaaaaaaaaaaa"]'



Debug mode
----------
Shortcut for json.dumps(obj, indent=4, sort_keys=True, ensure_ascii=False)

    >>> asjson.dumps({'foo': 1, 'bar': 2}, debug=True)
    '{\\n    "bar": 2,\\n    "foo": 1\\n}'
'''
import json
from datetime import datetime, date
try:
    from bson import ObjectId
except ImportError:
    ObjectId = None


__version__ = '2.0.0'


class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        if isinstance(obj, date):
            return obj.isoformat()
        if ObjectId and isinstance(obj, ObjectId):
            return str(obj)
        return super().default(obj)


def dumps(data, debug=False, **kwargs):
    if debug:
        kwargs['indent'] = kwargs.get('indent', 4)
        kwargs['sort_keys'] = kwargs.get('sort_keys', True)
        kwargs['ensure_ascii'] = kwargs.get('ensure_ascii', False)
    return JSONEncoder(**kwargs).encode(data)


if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)
