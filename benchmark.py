#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import time
import datetime

def main():
    print( '=== Compare iso-formated string to datetime converters' )
    args = [datetime.datetime.now().isoformat() + 'Z']
    funcs = [
        iso_to_datetime_old_py,
        iso_to_datetime_py_26,
        iso_to_datetime_re_1,
        iso_to_datetime_re_2,
    ]
    benchmark(funcs, args=args)


def iso_to_datetime_old_py(s):
    '''ISO -> datetime with datetime.strptime in py < 2.6'''
    parts = s[:-1].split('.')
    dt = datetime.datetime.strptime(parts.pop(0), '%Y-%m-%dT%H:%M:%S')
    if parts:
        ms = int(parts[0].replace('Z', ''))
        dt = dt.replace(microsecond=ms)
    return dt

def iso_to_datetime_py_26(s):
    '''ISO -> datetime with datetime.strptime in py >= 2.6'''
    if '.' in s:
        return datetime.datetime.strptime(s, '%Y-%m-%dT%H:%M:%S.%fZ')
    else:
        return datetime.datetime.strptime(s, '%Y-%m-%dT%H:%M:%SZ')

iso_re_1 = re.compile('[^\d]')
def iso_to_datetime_re_1(s):
    '''ISO -> datetime with regexp method 1'''
    if len(s) > 19 and s[10] == 'T' and s.count('-') == s.count(':') == 2:
        return datetime.datetime(*map(int, iso_re_1.split(s)[:-1]))

iso_re_2 = re.compile(
    r'^(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2})(?:\.(\d{1,6}))?Z$')
def iso_to_datetime_re_2(obj):
    '''ISO -> datetime with regexp method 2 (used currently)'''
    dt_result = iso_re_2.match(obj)
    if dt_result:
        return datetime.datetime(*map(int, dt_result.groups()))

def benchmark(funcs, run_count=10000, args=None, kwargs=None,
        check_results=True):
    args = args or []
    kwargs = kwargs or {}
    fname = lambda f: f.__doc__ or f.__name__
    longest_name = max(len(fname(f)) for f in funcs)
    for f in funcs:
        f.name = ('%%-%is' % longest_name) % fname(f)

    if check_results:
        for f in funcs:
            r0 = funcs[0](*args, **kwargs)
            r = f(*args, **kwargs)
            assert r == r0, '%s returned %s (%s)\n %s returned %s (%s)' % (
                    f.name, r, type(r), funcs[0].name, r0, type(r0))

    for f in funcs:
        start = time.time()
        for i in range(run_count):
            result = f(*args, **kwargs)
        finish = time.time() - start
        print( '%s\t%s sec.\t%s' % (f.name, finish, result) )
        time.sleep(1)



if __name__ == '__main__':
    main()
