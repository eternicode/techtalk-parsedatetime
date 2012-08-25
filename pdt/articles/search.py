from datetime import datetime, timedelta

from parsedatetime import parsedatetime as pdt, parsedatetime_consts as pdc

time_parser = pdt.Calendar(pdc.Constants())
def handle_time(s, matches):
    for negate, field, text, quoted in matches:
        if quoted:
            text = text[1:-1]
        data, parsed = time_parser.parse(text)

        data = list(data)
        now = datetime.now()
        # Sometimes, next year (now.year+1) is "parsed" out, but future dates are unusable
        if str(data[0]) not in text:
            while datetime(*data[:6]) > now:
                data[0] -= 1

        if not parsed: # not parsed
            continue
        elif parsed == 1: # parsed as date
            boundary = datetime(*data[:3])
            sod = boundary.replace(hour=0, minute=0, second=0, microsecond=0)
            eod = boundary.replace(hour=23, minute=59, second=59, microsecond=999999)
            range = (sod, eod)
        elif parsed in [2, 3]: # parsed as time, datetime
            boundary = datetime(*data[:6])

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

