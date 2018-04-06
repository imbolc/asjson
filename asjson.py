'''
asjson
======
Json serialization with `datetime`, `date`,
`Decimal` and `bson.ObjectId` support

    >>> from datetime import datetime, date, timedelta, timezone
    >>> from decimal import Decimal
    >>> from bson import ObjectId
    >>> import asjson

    >>> data = {
    ...     'time': [
    ...         date(2018, 3, 6),
    ...         datetime(2018, 3, 6, 9, 38, 0, 1),
    ...         datetime(2018, 3, 6, 9, 38, 0, 1).replace(
    ...             tzinfo=timezone.utc),
    ...     ],
    ...     'decimal': Decimal('3.14'),
    ...     'objectid': ObjectId('a' * 24),
    ... }

We can make all the values json-appropriate without
dumping the structure to string.
It can be helpful in some cases, e.g. with passing it
into database json field.

    >>> asjson.encode(data)
    {'time': ['2018-03-06',
             '2018-03-06T09:38:00.000001',
             '2018-03-06T09:38:00.000001+00:00'],
         'decimal': '3.14',
         'objectid': 'aaaaaaaaaaaaaaaaaaaaaaaa'}

For dumping to string we can use `asjson.dumps` which takes
the same parameters as standard `json.dumps` does plus `debug`
which just a shortcut for
`json.dumps(..., indent=4, sort_keys=True, ensure_askii=False)`:

    >>> print(asjson.dumps(data, debug=True))
    {
        "decimal": "3.14",
        "objectid": "aaaaaaaaaaaaaaaaaaaaaaaa",
        "time": [
            "2018-03-06",
            "2018-03-06T09:38:00.000001",
            "2018-03-06T09:38:00.000001+00:00"
        ]
    }

'''
from datetime import datetime, date
from decimal import Decimal
import json
try:
    from bson import ObjectId
except ImportError:
    ObjectId = None


DEBUG = False


__version__ = '3.0.0'


def encode(data):
    '''Recursive encodes nested structures to json-appropriate format'''
    if isinstance(data, dict):
        return {k: encode(v) for k, v in data.items()}
    if isinstance(data, list):
        return [encode(v) for v in data]
    if isinstance(data, datetime):
        return data.isoformat()
    if isinstance(data, date):
        return data.isoformat()
    if isinstance(data, Decimal):
        return str(data)
    if ObjectId and isinstance(data, ObjectId):
        return str(data)
    return data


def dumps(data, *, debug=DEBUG, **kwargs):
    if debug:
        kwargs['indent'] = kwargs.get('indent', 4)
        kwargs['sort_keys'] = kwargs.get('sort_keys', True)
        kwargs['ensure_ascii'] = kwargs.get('ensure_ascii', False)
    return json.dumps(encode(data), **kwargs)


if __name__ == "__main__":
    import doctest
    doctest.testmod(optionflags=doctest.NORMALIZE_WHITESPACE)
