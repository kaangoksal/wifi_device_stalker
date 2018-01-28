from sqlalchemy import Column, VARCHAR, TEXT, TIMESTAMP, func, Date, Integer
from dbModels.declerations import Base

#TODO change indexing for connected access_points and other aux tables

class WifiClientSession_dbModel(Base):
    __tablename__ = 'wifi_client_sessions'

    client_mac = Column(VARCHAR(30), primary_key=True)
    session_start = Column(Date, nullable=False, server_default=func.now())
    session_end = Column(Date)
    connected_access_points = Column(VARCHAR(40), nullable=False) # this is tied to another table
    spotted_channels = Column(VARCHAR(60), nullable=False) # this is tied to another table
    observed_rssi = Column(VARCHAR(60), nullable=False) # This is tied to another table

    def __init__(self, client_mac, session_start=None):
        self.client_mac = client_mac
        if session_start is not None:
            self.session_start = session_start

    def end_session(self, end_time =None):
        if end_time is not None
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
    __tablename__ = 'client_spotted_channels'

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
        pass  # TODO implement


