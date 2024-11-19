import subprocess
import platform
import mysql.connector
from mysql.connector import Error
from PyQt5.QtWidgets import QFileDialog
import os
import socket
import traceback
import mariadb
import re
from logics.DataClass import DataClass

class PrevDbStateChanger:

    def update_changelog_file_and_save(liquibase_initiator):
        print ("Updating changelog file")
        """
        Open a file explorer to select a new changeLogFile path, update the changeLogFile property
        of a LiquibasePropertyInitiator object, and save the updated properties to a liquibase.properties file.
        
        Parameters:
            liquibase_initiator (LiquibasePropertyInitiator): The instance to update.
        """
        # Open file dialog for the user to select a new changelog file
        prev_liquibase_filePath = liquibase_initiator.get_where_to_save()
        file_dialog = QFileDialog()
        new_changelog_file, _ = file_dialog.getOpenFileName(
            None, 
            "Select New ChangeLog File", 
            "", 
            "All Files (*);;XML Files (*.xml)"
        )
        print(new_changelog_file)
        DataClass.get_instance().set_temp_gen_xml_path(new_changelog_file)
        try:
            print("inside try of prrev db")
            host = DataClass.get_instance().get_host()
            database = DataClass.get_instance().get_origial_db_name()
            temp_db_string = PrevDbStateChanger.connect_maria_db(liquibase_initiator.username,liquibase_initiator.password,host,database, "temp_db",liquibase_initiator.url)
            print(temp_db_string)
        except Exception as e:
            print(f"Error creating temporary database: {e}")
    


        # If a file is selected, update the changeLogFile and save properties
        if new_changelog_file:
            liquibase_initiator.changeLogFile = PrevDbStateChanger.get_relative_path(prev_liquibase_filePath, new_changelog_file)
            liquibase_initiator.url = temp_db_string
            liquibase_initiator.save_liquibase_properties_with_file_path(prev_liquibase_filePath)
            liquibase_initiator.run_liquibase_update()
            
        else:
            print("No file selected.")
        gen_changelog_filePath = PrevDbStateChanger.replace_filename_in_path(liquibase_initiator.changeLogFile, "generated_changelog.xml")
        liquibase_initiator.changeLogFile = gen_changelog_filePath
        liquibase_initiator.save_liquibase_properties_by_replacing(prev_liquibase_filePath)
        DataClass.get_instance().set_temp_gen_xml_path(PrevDbStateChanger.replace_filename_in_path(new_changelog_file, "generated_changelog.xml"))
        liquibase_initiator.run_liquibase_command()
        

    

    import os

    def get_relative_path(liquibase_path, changelog_xml_path):
        """
        Returns the relative path of 'changelog_xml_path' relative to the directory of 'liquibase_path'.
        If 'liquibase_path' is a file, it extracts the directory path first.
        Replaces backslashes with forward slashes in the final output.
        """
        # If liquibase_path is a file, get its directory
        if os.path.isfile(liquibase_path):
            liquibase_path = os.path.dirname(liquibase_path)
        
        try:
            # Get relative path and replace backslashes with forward slashes
            relative_path = os.path.relpath(changelog_xml_path, start=liquibase_path).replace("\\", "/")
            return relative_path
        except Exception as e:
            print(f"Error calculating relative path: {e}")
            return None
        
    def replace_filename_in_path(path, new_filename):
        """Replace the filename in the provided path with a new filename."""
        # Get the directory of the existing path
        directory = os.path.dirname(path)
        # Join the directory with the new filename to form the updated path
        updated_path = os.path.join(directory, new_filename).replace("\\", "/")
        return updated_path
    

    def create_database_and_get_connection_url(host, port, username, password, database_name):
        """Connect to MariaDB, create a database, and return the connection string to the new database."""
        try:
            # Network reachability test
            print(f"Testing network reachability to {host}:{port}...")
            with socket.create_connection((host, port), timeout=10):
                print(f"Successfully reached {host}:{port}.")

            # Debugging connector configuration
            print("Attempting to connect to MariaDB server with mysql.connector...")  
            
            # Connect to the MariaDB server (no database specified initially)
            connection = mysql.connector.connect(
                host=host,
                port=port,
                user=username,
                password=password,
                auth_plugin='mysql_native_password',  # Explicitly set auth plugin
                ssl_disabled=True  # Disable SSL if not used
            )
            print("Connected to MariaDB server successfully.")  # Debugging output

            if connection.is_connected():
                cursor = connection.cursor()
                cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name}")
                cursor.close()
                connection.close()
                print(f"Database '{database_name}' created or already exists.")
                
                # Construct the connection string to the created database
                connection_string = f"mariadb://{username}:{password}@{host}:{port}/{database_name}"
                return connection_string

        except socket.error as e:
            print(f"Network error: Cannot reach {host}:{port}. Error: {e}")
            return None
        except Error as e:
            print("MySQL error:", e)
            print("Traceback:", traceback.format_exc())
            return None
        except Exception as e:
            print("Unexpected error encountered:", e)
            print("Traceback:", traceback.format_exc())
            return None
        
    def create_mariadb_database(host, user, password, new_database_name, port=3306):
        print("Creating database...")
        """
        Creates a new MariaDB database and returns the connection string.
        
        Parameters:
        host (str): Database host address
        user (str): Database username
        password (str): Database password
        new_database_name (str): Name for the new database
        port (int): Port number (default: 3306)
        
        Returns:
        str: Connection string for the new database
        
        Raises:
        Exception: If database creation fails
        """
        try:
            # First connect to MariaDB without specifying a database
            print("inside try..")
            
            connection = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                port=port
            )
            print("Connected to MariaDB server successfully.")
            
            if connection.is_connected():
                cursor = connection.cursor()
                
                # Create the new database
                cursor.execute(f"CREATE DATABASE IF NOT EXISTS {new_database_name}")
                
                # Close the initial connection
                cursor.close()
                connection.close()
                
                # Create and return the connection string
                connection_string = f"mysql+mysqlconnector://{user}:{password}@{host}:{port}/{new_database_name}"
                return connection_string
            else:
                raise Exception("Failed to connect to MariaDB server.")
        except Error as e:
            raise Exception(f"Error creating database: {e}")
            
        finally:
            if 'connection' in locals() and connection.is_connected():
                cursor.close()
                connection.close()

    def connect_maria_db(user, password, host, database, new_database_name,connection_string):
        try:
            print("inside connect maria db")
            print(host)
            conn = mariadb.connect(
                user=user,
                password=password,
                host=host,
                database=database
                )
            cursor = conn.cursor()
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {new_database_name}")
            DataClass.get_instance().set_temp_db_cursor(cursor)
            DataClass.get_instance().set_temp_db_name(new_database_name)
            pattern = r"(://[\d\.]+:\d+/)(\w+)$"
    
            # Replace the database name using the new database name
            new_connection_string = re.sub(pattern, r"\1" + new_database_name, connection_string)
            
            return new_connection_string
        
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")
            return None
        
    def extract_host_ip(connection_string):
        # Pattern to match the IP address in the connection string with flexible protocol
        print(connection_string)
        pattern = r"^(?:\w+://)([\d\.]+):\d+/"
        
        # Search for the pattern in the connection string
        match = re.search(pattern, connection_string)
        
        # Return the IP address if found, else return None
        return match.group(1) if match else None



    