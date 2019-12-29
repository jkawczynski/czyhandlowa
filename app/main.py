import datetime
from functools import lru_cache
from typing import List

from flask import Flask, jsonify, render_template
from flask.json import JSONEncoder
from flask_caching import Cache

SHOPPING_SUNDAYS = (
    (2019, 1, 27),
    (2019, 2, 24),
    (2019, 3, 31),
    (2019, 4, 14),
    (2019, 4, 28),
    (2019, 5, 26),
    (2019, 6, 30),
    (2019, 7, 28),
    (2019, 8, 25),
    (2019, 9, 29),
    (2019, 10, 27),
    (2019, 11, 24),
    (2019, 12, 15),
    (2019, 12, 22),
    (2019, 12, 29),
    (2020, 1, 26),
    (2020, 4, 5),
    (2020, 4, 26),
    (2020, 6, 28),
    (2020, 8, 30),
    (2020, 12, 13),
    (2020, 12, 20),
)


class ISODateJSONEncoder(JSONEncoder):
    """
    JSON Encoder which converts `datetime.date` objects to ISOFormat
    """

    def default(self, obj):
        try:
            if isinstance(obj, datetime.date):
                return obj.isoformat()
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)
        return JSONEncoder.default(self, obj)


app = Flask(__name__)
app.json_encoder = ISODateJSONEncoder
cache = Cache(app, config={'CACHE_TYPE': 'simple'})


@lru_cache()
def get_available_sundays() -> List[datetime.date]:
    """
    Get list of available shopping sundays in date format

    :return: List of shopping sundays
    """
    return [datetime.date(*date) for date in SHOPPING_SUNDAYS]


def is_shopping_sunday(date: datetime.date) -> bool:
    """
    Check whether given date is shopping sunday

    :param date: Input date
    :return: bool - Is shopping sunday or not
    """
    return date in get_available_sundays()


def get_next_shopping_sunday(date: datetime.date) -> datetime.date:
    """
    Get next shopping sunday for given date

    :param date: Input date
    :return: Next shopping sunday
    """
    nearest_day_delta = min(
        [
            (sunday - date)
            for sunday in get_available_sundays()
            if (sunday - date).days > 0
        ]
    )
    return date + nearest_day_delta


def get_next_sunday(date: datetime.date) -> datetime.date:
    """
    Get next sunday for given date

    :param date: Input date
    :return: Next sunday date
    """
    if date.weekday() == 6:
        return date + datetime.timedelta(7)
    return date + datetime.timedelta((6 - date.weekday()) % 7)


def get_context():
    today = datetime.date.today()
    return {
        "is_today_shopping_sunday": is_shopping_sunday(today),
        "is_next_sunday_shopping": is_shopping_sunday(get_next_sunday(today)),
        "next_shopping_sunday": get_next_shopping_sunday(today),
    }


@app.route("/", methods=("GET",))
def index():
    return render_template('index.html', context=get_context())


@cache.cached(timeout=60)
@app.route("/api", methods=("GET",))
def shopping_sunday():
    return jsonify(get_context())


@cache.cached()
@app.route("/api/shopping_sundays", methods=("GET",))
def list_shopping_sundays():
    return jsonify(get_available_sundays())


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=80)
