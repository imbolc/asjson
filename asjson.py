'''
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
    u'{\\n  "created": [\\n    "2013-01-27T06:48:00.038835Z",\\n    "2013-01-27Z"\\n  ]\\n}'
'''
import re
import sys
import datetime
try:
    import simplejson as json
except ImportError:
    try:
        import json
    except ImportError:
        import simplejson

__version__ = '1.2.1'

DATE_RE = re.compile(r'^(\d{4})-(\d{2})-(\d{2})Z$')
DATETIME_RE = re.compile(
    r'^(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2})(?:\.(\d{1,6}))?Z$')
DEBUG = False

if sys.version_info >= (3, 0):
    basestring = str

def dumps(obj, debug=False, **kwargs):
    if debug or DEBUG:
        kwargs['indent'] = kwargs.get('indent', 2)
        kwargs['sort_keys'] = kwargs.get('sort_keys', True)
        kwargs['ensure_ascii'] = kwargs.get('ensure_ascii', False)
    return Encoder(**kwargs).encode(obj)

def loads(s, **kwargs):
    return Decoder(**kwargs).decode(s)


class Encoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat() + 'Z'
        elif isinstance(obj, datetime.date):
            return obj.isoformat() + 'Z'
        else:
            return super(Encoder, self).default(obj)


class Decoder(json.JSONDecoder):
    def __init__(self, parse_datetime=True, parse_date=True, **kwargs):
        self.parse_datetime = parse_datetime
        self.parse_date = parse_date
        super(Decoder, self).__init__(**kwargs)

    def decode(self, s, **kwargs):
        obj = super(Decoder, self).decode(s, **kwargs)
        if self.parse_datetime or self.parse_date:
            return _decode(obj, {'parse_datetime': self.parse_datetime,
                'parse_date': self.parse_date})
        return obj

def _decode(obj, opts):
    if isinstance(obj, basestring):
        return decode_datetime(obj, opts)
    if isinstance(obj, dict):
        r = {}
        for k in obj:
            r[k] = _decode(obj[k], opts)
        return r
    elif isinstance(obj, list):
        return [_decode(v, opts) for v in obj]
    return obj

def decode_datetime(obj, opts):
    if opts.get('parse_datetime'):
        dt_result = DATETIME_RE.match(obj)
        if dt_result:
            try:
                return datetime.datetime(*map(lambda x: int(x) if x else 0,
                    dt_result.groups()))
            except Exception:
                pass
    if opts.get('parse_date'):
        dt_result = DATE_RE.match(obj)
        if dt_result:
            try:
                return datetime.date(*map(int, dt_result.groups()))
            except Exception:
                pass
    return obj


if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)
