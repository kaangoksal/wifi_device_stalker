"""
Author: Kaan Goksal
Date: Sometime around January 2018
Summary: This file stores the table structures for the client, accesspoint, clientsessions and so on. Nothing complex
just lots of busy work
"""

from sqlalchemy import Column, VARCHAR, TEXT, TIMESTAMP, func, Date, Integer
from dbModels.declerations import Base, engine, db_session


class Accesspoint_dbModel(Base):
    __tablename__ = 'access_points'

    access_point_bssid = Column(VARCHAR(30), primary_key=True)
    first_seen = Column(Date, server_default=func.now())
    tag = Column(TEXT) # Desing issue, we might have multiple tags, this undermines the search efficiency!

    def __init__(self, bssid):
        self.access_point_bssid = bssid

    @staticmethod
    def get_access_point(bssid):
        """
        Returns the access point from the db
        :param bssid: the mac address of the accesspoint
        :return: none if not registered, the database object if found in the database
        """
        fetched_access_point = db_session.query(Accesspoint_dbModel).filter_by(access_point_bssid=bssid).first()

        return fetched_access_point


class AccesspointSession_dbModel(Base):

    __tablename__ = 'accesspoint_sessions'
    id = Column(Integer, primary_key=True)
    bssid = Column(VARCHAR(30), nullable=False)
    session_start = Column(Date, nullable=False, server_default=func.now())
    session_end = Column(Date)
    connected_clients = Column(VARCHAR(40), nullable=False) # this is tied to another table
    spotted_channels = Column(VARCHAR(60), nullable=False) # this is tied to another table
    observed_rssi = Column(VARCHAR(60), nullable=False) # This is tied to another table

    def __init__(self, bssid, session_start=None):
        self.bssid = bssid
        if session_start is not None:
            self.session_start = session_start

    def end_session(self, end_time=None):
        if end_time is not None:
            self.session_end = end_time
        else:
            self.session_end = func.now()

    def end_session_with_save(self, session_object):
        """
        Record all the findings about the object here.
        :param session_object:
        :return:
        """
        pass

class WifiClient_dbModel(Base):
    """
    This class is just for storing and keeping a record of wifi clients
    """
    __tablename__ = 'wifi_clients'

    client_mac = Column(VARCHAR(30), primary_key=True)
    first_seen = Column(Date, server_default=func.now())
    tag = Column(TEXT)

    def __init__(self, client_mac):
        self.client_mac = client_mac

    @staticmethod
    def get_client(client_mac):
        """
        This function returns the client object or null if it doesn't exist
        :param client_mac:
        :return:
        """
        db_client = db_session.query(WifiClient_dbModel).filter_by(client_mac=client_mac).first()
        return db_client

#TODO change indexing for connected access_points and other aux tables


class WifiClientSession_dbModel(Base):

    __tablename__ = 'wifi_client_sessions'
    id = Column(Integer, primary_key=True)
    client_mac = Column(VARCHAR(30), nullable=False)
    session_start = Column(Date, nullable=False, server_default=func.now())
    session_end = Column(Date)
    connected_access_points = Column(VARCHAR(40), nullable=False) # this is tied to another table
    spotted_channels = Column(VARCHAR(60), nullable=False) # this is tied to another table
    observed_rssi = Column(VARCHAR(60), nullable=False) # This is tied to another table

    def __init__(self, client_mac, session_start=None):
        self.client_mac = client_mac
        if session_start is not None:
            self.session_start = session_start

    def end_session(self, end_time=None):
        if end_time is not None:
            self.session_end = end_time
        else:
            self.session_end = func.now()


class WifiClientSession_connected_access_points(Base):

    __tablename__ = 'client_connected_access_points'
    #todo Integer is limited please change this the long
    id = Column(Integer,primary_key=True,nullable=False)
    session_key = Column(VARCHAR(60), nullable=False)
    connected_access_point = Column(VARCHAR(40), nullable=False)
    date_observed = Column(Date, server_default=func.now())

    def __init__(self, session_key, connected_access_point, date_observed= None):
        self.session_key = session_key
        self.connected_access_point = connected_access_point
        if date_observed is not None:
            self.date_observed = date_observed

    @staticmethod
    def return_all_connected_access_points(session_key):
        """
        Fetches all the connected access_points from the table and returns them for a
        spesific session
        :param session_key:
        :return:
        """
        pass #TODO


class WifiClientSession_spotted_channels(Base):
    __tablename__ = 'client_spotted_channels'

    id = Column(Integer, primary_key=True, nullable=False)
    session_key = Column(VARCHAR(60),  nullable=False)
    spotted_channel = Column(Integer, nullable=False)
    date_observed = Column(Date, server_default=func.now())

    def __init__(self, session_key, spotted_channel, date_observed = None):
        self.session_key = session_key
        self.spotted_channel = spotted_channel
        if date_observed is not None:
            self.date_observed = date_observed

    @staticmethod
    def return_all_observed_channels(session_key):
        """
        Fetches all the observed channels given the session key
        :param session_key: session key of the session
        :return: a list of observed channel objects?
        """
        pass #TODO implement


class WifiClientSession_observed_rssi(Base):
    __tablename__ = 'observed_rssi'

    id = Column(Integer, primary_key=True, nullable=False)
    session_key = Column(VARCHAR(60), nullable=False)
    observed_rssi = Column(Integer, nullable=False)
    date_observed = Column(Date, server_default=func.now())

    def __init__(self, session_key, observed_rssi, date_observed=None):
        self.session_key = session_key
        self.observed_rssi = observed_rssi
        if date_observed is not None:
            self.date_observed = date_observed

    @staticmethod
    def return_all_observed_rssi(session_key):
        """
        Fetches all the observed rssi given the session key
        :param session_key: session key of the session
        :return: a list of rssi objects?
        """
        pass # TODO implement


Base.metadata.create_all(bind=engine)

