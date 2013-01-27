asjson
======
Json dumps and loads with datetime and date support

    >>> from datetime import datetime, date
    >>> import asjson

    >>> src = {'created': [datetime(2013, 1, 27, 6, 48, 0, 38835), date(2013, 1, 27)]}

    >>> dump = asjson.dumps(src)
    >>> dump
    '{"created": ["2013-01-27T06:48:00.038835Z", "2013-01-27Z"]}'

    >>> loaded = asjson.loads(dump)
    >>> loaded
    {'created': [datetime.datetime(2013, 1, 27, 6, 48, 0, 38835), datetime.date(2013, 1, 27)]}
    >>> loaded == src
    True

Disable datetime support
------------------------

    >>> asjson.loads(dump, parse_datetime=False)
    {'created': ['2013-01-27T06:48:00.038835Z', datetime.date(2013, 1, 27)]}
    >>> asjson.loads(dump, parse_date=False)
    {'created': [datetime.datetime(2013, 1, 27, 6, 48, 0, 38835), '2013-01-27Z']}

Debug mode
----------
Shortcut for json.dumps(obj, indent=2, sort_keys=True, ensure_ascii=False)

    >>> asjson.dumps(src, debug=True)
    u'{\n  "created": [\n    "2013-01-27T06:48:00.038835Z",\n    "2013-01-27Z"\n  ]\n}'