"""Test cases for main module"""
import datetime
from unittest import TestCase, mock

from app.main import (
    get_available_sundays,
    is_shopping_sunday,
    get_next_sunday,
    get_next_shopping_sunday,
)


class ShoppingSundaysTestCase(TestCase):
    """Test case for `get_available_sundays`"""

    def test_shopping_sundays_are_valid_dates(self):
        """All dates from `shopping_sundays` should be sundays"""
        sundays = get_available_sundays()
        for sunday in sundays:
            self.assertEqual(sunday.weekday(), 6, f"{sunday} is not sunday")


class IsShoppingSunday(TestCase):
    """Test case for `is_shopping_sunday`"""

    shopping_sundays_mock = mock.patch(
        "app.main.get_available_sundays",
        return_value=[
            datetime.date(2019, 1, 1),
            datetime.date(2019, 1, 2),
            datetime.date(2019, 5, 12),
            datetime.date(2019, 6, 17),
            datetime.date(2019, 9, 20),
        ],
    )

    @shopping_sundays_mock
    def test_with_shopping_sunday(self, *args):
        """Should return true if given sunday is shopping sunday"""
        self.assertTrue(is_shopping_sunday(datetime.date(2019, 1, 2)))

    @shopping_sundays_mock
    def test_with_not_shopping_sunday(self, *args):
        """Should return false if given sunday is not shopping sunday"""
        self.assertFalse(is_shopping_sunday(datetime.date(2019, 1, 3)))


class GetNextSundayTestCase(TestCase):
    """Test case for `get_next_sunday`"""

    def test_get_next_sunday(self):
        """Should return next sunday for given date"""
        self.assertEqual(
            get_next_sunday(date=datetime.date(2019, 1, 1)), datetime.date(2019, 1, 6)
        )
        self.assertEqual(
            get_next_sunday(date=datetime.date(2019, 6, 12)), datetime.date(2019, 6, 16)
        )
        self.assertEqual(
            get_next_sunday(date=datetime.date(2019, 10, 20)),
            datetime.date(2019, 10, 27),
        )


class GetNextShoppingSunday(TestCase):
    """Test case for `get_next_shopping_sunday`"""

    @mock.patch(
        "app.main.get_available_sundays",
        return_value=[
            datetime.date(2019, 5, 12),
            datetime.date(2019, 6, 17),
            datetime.date(2019, 9, 20),
        ],
    )
    def test_get_next_shopping_sunday(self, *args):
        """Should return nearest shopping sunday for given date"""
        self.assertEqual(
            get_next_shopping_sunday(datetime.date(2019, 3, 10)),
            datetime.date(2019, 5, 12),
        )
        self.assertEqual(
            get_next_shopping_sunday(datetime.date(2019, 5, 12)),
            datetime.date(2019, 6, 17),
        )
        self.assertEqual(
            get_next_shopping_sunday(datetime.date(2019, 6, 10)),
            datetime.date(2019, 6, 17),
        )
        self.assertEqual(
            get_next_shopping_sunday(datetime.date(2019, 7, 10)),
            datetime.date(2019, 9, 20),
        )
