asjson
======
json.dumps with datetime, date and bson.ObjectId support

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