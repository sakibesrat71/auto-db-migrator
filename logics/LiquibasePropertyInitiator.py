from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLineEdit, QLabel,
    QCheckBox, QHBoxLayout, QMessageBox, QSpacerItem, QSizePolicy,QFileDialog, QGridLayout
)
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QDesktopServices
import subprocess
import platform
import os
from logics.PrevDbStateChanger import PrevDbStateChanger
class LiquibasePropertyInitiator:
    def __init__(self, url: str, password: str, driver: str, username: str, changeLogFile: str, diffTypes: list):
        self.url = url
        self.password = password
        self.driver = driver
        self.username = username
        self.changeLogFile = changeLogFile
        self.diffTypes = diffTypes

    def get_where_to_save(self):
        """Open file explorer for the user to select where to save the liquibase.properties file."""
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(
            None, "Save Liquibase Properties File", "", "Properties Files (*.properties);;All Files (*)", options=options
        )
        return file_path


    def save_liquibase_properties(self):
        """Generate and save liquibase.properties file using the attributes of the current instance."""
        
        # Build the content for liquibase.properties
        

        # Open file explorer for saving the file
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(
            None, "Save Liquibase Properties File", "", "Properties Files (*.properties);;All Files (*)", options=options
        )
        self.changeLogFile = PrevDbStateChanger.get_relative_path(file_path, self.changeLogFile)

        properties_content = f"""url={self.url}
username={self.username}
password={self.password}
driver={self.driver}
changeLogFile={self.changeLogFile}
diffTypes={','.join(self.diffTypes)}
"""

        # If the user selects a file path, save the properties content to the file
        if file_path:
            try:
                self.saved_path = file_path
                with open(file_path, 'w') as file:
                    file.write(properties_content)
                print(f"Liquibase properties saved successfully to {file_path}")
            except Exception as e:
                print(f"An error occurred while saving the file: {e}")
        else:
            print("No file selected.")
            

    def save_liquibase_properties_with_file_path(self,file_path):
        """Generate and save liquibase.properties file using the attributes of the current instance."""
        
        # Build the content for liquibase.properties
        properties_content = f"""url={self.url}
username={self.username}
password={self.password}
driver={self.driver}
changeLogFile={self.changeLogFile}
diffTypes={','.join(self.diffTypes)}
"""

        # # Open file explorer for saving the file
        # options = QFileDialog.Options()
        # file_path, _ = QFileDialog.getSaveFileName(
        #     None, "Save Liquibase Properties File", "", "Properties Files (*.properties);;All Files (*)", options=options
        # )

        # If the user selects a file path, save the properties content to the file
        if file_path:
            try:
                self.saved_path = file_path
                with open(file_path, 'w') as file:
                    file.write(properties_content)
                print(f"Liquibase properties saved successfully to {file_path}")
            except Exception as e:
                print(f"An error occurred while saving the file: {e}")

    def save_liquibase_properties_by_replacing(self, file_path):
        """Generate and save liquibase.properties file using the attributes of the current instance."""
        
        # Build the content for liquibase.properties
        properties_content = f"""url={self.url}
    username={self.username}
    password={self.password}
    driver={self.driver}
    changeLogFile={self.changeLogFile}
    diffTypes={','.join(self.diffTypes)}
    """

        # If the file exists, delete the previous one to replace it with the current one
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                print(f"Previous file at {file_path} deleted.")
            except Exception as e:
                print(f"An error occurred while deleting the previous file: {e}")
                return
        
        # Now create (or recreate) the file with the updated properties
        try:
            with open(file_path, 'w') as file:
                file.write(properties_content)
            print(f"Liquibase properties saved successfully to {file_path}")
            self.saved_path = file_path
        except Exception as e:
            print(f"An error occurred while saving the file: {e}")

    def run_liquibase_command(self):
        """Open terminal or command line and run 'liquibase generateChangeLog'."""
        
        # Get the directory path from the file_path
        directory = self.saved_path.rsplit('/', 1)[0] if '/' in self.saved_path else self.saved_path.rsplit('\\', 1)[0]

        # Command to run liquibase generateChangeLog
        command = 'liquibase generateChangeLog'

        try:
            # Check the current operating system
            if platform.system() == 'Windows':
                # For Windows, open cmd and execute the command in the directory
                process = subprocess.Popen(f'cd /d "{directory}" && {command}', 
                                           stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            else:
                # For Linux/MacOS, use bash and execute the command in the directory
                process = subprocess.Popen(f'cd "{directory}" && {command}', 
                                           stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

            # Capture the output and errors
            output, error = process.communicate()
            output_message = output.decode('utf-8') if output else "Command executed successfully"
            error_message = error.decode('utf-8') if error else ""

            # Display the result in a QMessageBox
            self.show_message_box(output_message, error_message)

        except Exception as e:
            self.show_message_box("", str(e))

    def run_liquibase_update(self):
        """Open terminal or command line and run 'liquibase update'."""
        
        # Get the directory path from the file_path
        directory = self.saved_path.rsplit('/', 1)[0] if '/' in self.saved_path else self.saved_path.rsplit('\\', 1)[0]

        # Command to run liquibase generateChangeLog
        command = 'liquibase update'

        try:
            # Check the current operating system
            if platform.system() == 'Windows':
                # For Windows, open cmd and execute the command in the directory
                process = subprocess.Popen(f'cd /d "{directory}" && {command}', 
                                           stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            else:
                # For Linux/MacOS, use bash and execute the command in the directory
                process = subprocess.Popen(f'cd "{directory}" && {command}', 
                                           stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

            # Capture the output and errors
            output, error = process.communicate()
            output_message = output.decode('utf-8') if output else "Command executed successfully"
            error_message = error.decode('utf-8') if error else ""

            # Display the result in a QMessageBox
            self.show_message_box(output_message, error_message)

        except Exception as e:
            self.show_message_box("", str(e))

    def show_message_box(self, output_message, error_message):
        """Show the command output and errors in a QMessageBox with a custom button."""
        msg = QMessageBox()
        msg.setWindowTitle("Liquibase Command Output")
        msg.resize(1000, 800)

        if output_message:
            msg.setText(f"Output:\n{output_message}")
        if error_message:
            msg.setDetailedText(f"Error:\n{error_message}")

        # Add a custom button "Liquibase not recognised?"
        liquibase_help_button = QPushButton("Liquibase not recognised?")
        msg.addButton(liquibase_help_button, QMessageBox.ActionRole)

        # Open a relevant URL when the button is clicked
        def open_help_link():
            QDesktopServices.openUrl(QUrl("https://docs.liquibase.com/start/install/home.html"))

        liquibase_help_button.clicked.connect(open_help_link)

        msg.exec_()
