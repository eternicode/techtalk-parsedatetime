import re
from datetime import datetime, timedelta

from parsedatetime import parsedatetime as pdt, parsedatetime_consts as pdc

from .utils import words2ints


time_parser = pdt.Calendar(pdc.Constants())
within_re = re.compile(r'within\s+(\d+(?:\.\d+)?)\s*(years?|yrs?|y|months?|mon?s?|da?ys?|d|hours?|hrs?|h|minutes?|mins?|m|seconds?|secs?|s)')
def handle_time(s, matches):
    for negate, field, text, quoted in matches:
        if quoted:
            text = text[1:-1]
        text = words2ints(text)
        data, parsed = time_parser.parse(text)

        data = list(data)
        now = datetime.now()
        # Sometimes, next year (now.year+1) is "parsed" out, but future dates are unusable
        if str(data[0]) not in text:
            while datetime(*data[:6]) > now:
                data[0] -= 1

        limit = re.search(r'before|after', text.lower())
        limit = limit.group(0) if limit else 'date'

        if not parsed: # not parsed
            continue
        elif parsed == 1: # parsed as date
            boundary = datetime(*data[:3])
            sod = boundary.replace(hour=0, minute=0, second=0, microsecond=0)
            eod = boundary.replace(hour=23, minute=59, second=59, microsecond=999999)
            range = dict(
                date = (sod, eod),
                after = (eod, datetime.max),
                before = (datetime(1900, 1, 1), sod),
            )[limit]
        elif parsed in [2, 3]: # parsed as time, datetime
            boundary = datetime(*data[:6])

            if limit in ['before', 'after']:
                # Allow before/after queries to specify specific times
                range = dict(
                    before = (datetime(1900, 1, 1), boundary),
                    after = (boundary, datetime.max)
                )[limit]

            elif within_re.search(text):
                magnitude, unit = within_re.search(text).groups()
                magnitude = float(magnitude)
                if unit[:2] == 'mo':
                    unit = 'o'
                unit = unit[0]
                delta = dict(
                    y = timedelta(days=365.25*magnitude),
                    o = timedelta(days=30.5*magnitude),
                    d = timedelta(days=magnitude),
                    h = timedelta(seconds=3600*magnitude),
                    m = timedelta(seconds=60*magnitude),
                    s = timedelta(seconds=magnitude),
                )[unit]
                range = (bound-delta, bound+delta)

            else:
                # chances are nothing actually happened at that specific time,
                # so we add different ranges of fuzz based on how specific their
                # query was.
                if boundary.second:
                    # 1-minute fuzz for seconds resolution
                    delta = timedelta(seconds=30)
                elif boundary.minute:
                    # 10-minute fuzz for minute resolution
                    delta = timedelta(seconds=300)
                elif boundary.hour:
                    # 2-hour fuzz for hour resolution
                    delta = timedelta(seconds=3600)
                else:
                    # 5-hour fuzz for day resolution (which should be parsed as
                    # a date, above, anyway...)
                    delta = timedelta(seconds=9000)
                range = (boundary-delta, boundary+delta)

        filter = (
            dict(created__gte=range[0], created__lte=range[1])
            if field == 'created' else
            dict(modified__gte=range[0], modified__lte=range[1])
        )
        s = getattr(s, 'exclude' if negate else 'filter')(**filter)
    return s


syntaxes = {
    # pattern: handler
    r'(-?)(created|modified):(([\'"]?)[^\4]+(?:\4)|\S+)': handle_time,
}

