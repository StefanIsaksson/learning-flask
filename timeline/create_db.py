#! /usr/bin/env python

from app import db


def initdb():
    db.create_all()
    print('Initialized the database')

def dropdb():
    db.drop_all()
    print('Dropped the database')


if __name__ == '__main__':
    dropdb()
    initdb()
