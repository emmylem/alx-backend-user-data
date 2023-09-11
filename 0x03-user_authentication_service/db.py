#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Add a new user to the database."""
        new_user = User(email=email, hashed_password=hashed_password)
        self._session.add(new_user)
        self._session.commit()  # update the DataBase

        return user

    def find_user_by(self, **kwargs) -> User:
        """Find a user in the database based on keyword arguments."""
        try:
            # Create a query for the User table
            query = self._session.query(User)
            # Apply filters based on keyword arguments
            for k, v in kwargs.items():
                query = query.filter_by(**{key: value})

            # Retrieve the first result
            user = query.first()

            if user is None:
                raise NoResultFound("No user found for the given criteria")

            return user
        except InvalidRequestError as e:
            # Handle invalid query error
            self._session.rollback()
            raise e

    def update_user(self, user_id: int, **kwargs) -> None:
        """ update properties of an user """
        user = self.find_user_by(id=user_id)
        for i in kwargs.keys():
            if i not in User.__table__.columns.keys():
                raise ValueError

        for k, v in kwargs.items():
            setattr(user, k, v)

        self._session.commit()
