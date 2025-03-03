from pony.orm import db_session

from .db import Country


@db_session
def create_countries():
    with open("db/countries.txt", "r") as f:
        countries = [c.strip().lower() for c in f.readlines()]
        db_countries = Country.select()
        for c in countries:
            if not db_countries.where(name=c).exists():
                Country(name=c)
