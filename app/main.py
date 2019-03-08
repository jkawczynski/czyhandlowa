from typing import List

from flask import Flask, jsonify
from functools import lru_cache

import datetime

app = Flask(__name__)


shopping_sundays = (
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
)


@lru_cache()
def get_available_sundays() -> List[datetime.date]:
    """
    Get list of available shopping sundays in date format

    :return: List of shopping sundays
    """
    return [datetime.date(*date) for date in shopping_sundays]


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


@app.route("/")
def shopping_sunday():
    today = datetime.date.today()
    return jsonify({
        "is_shopping": is_shopping_sunday(get_next_sunday(today)),
        "next_shopping_sunday": get_next_shopping_sunday(today),
        "is_today_shopping_sunday": today.weekday() == 6,
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=80)