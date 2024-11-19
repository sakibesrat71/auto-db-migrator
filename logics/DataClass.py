# data_class.py

class DataClass:
    _instance = None
    _liquibase_initiator = None
    _temp_gen_xml_path = None
    _current_xml_path = None
    _temp_db_cursor = None
    _temp_db_name = None
    _host = None
    _origial_db_name = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()  # Create the singleton instance if it doesn't exist
        return cls._instance

    def set_liquibase_initiator(self, initiator):
        print("set_liquibase_initiator called")
        self._liquibase_initiator = initiator

    def get_liquibase_initiator(self):
        print("get_liquibase_initiator called")
        return self._liquibase_initiator
    
    def set_temp_gen_xml_path(self, path):
        self._temp_gen_xml_path = path
    
    def get_temp_gen_xml_path(self):
        return self._temp_gen_xml_path
    
    def set_current_xml_path(self, path):
        self._current_xml_path = path
    
    def get_current_xml_path(self):
        return self._current_xml_path
    
    def set_temp_db_cursor(self, cursor):
        self._temp_db_cursor = cursor
    
    def get_temp_db_cursor(self):
        return self._temp_db_cursor
    
    def set_temp_db_name(self, db_name):
        self._temp_db_name = db_name

    def get_temp_db_name(self):
        return self._temp_db_name
    
    def set_host(self, host):
        self._host = host
    
    def get_host(self):
        return self._host

    def set_origial_db_name(self, db_name):
        self._origial_db_name = db_name
    
    def get_origial_db_name(self):
        return self._origial_db_name
    

    # Prevent direct instantiation
    def __new__(cls, *args, **kwargs):
        if cls._instance is not None:
            raise Exception("This class is a singleton!")
        return super(DataClass, cls).__new__(cls, *args, **kwargs)
