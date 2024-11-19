import sys
import webbrowser
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLineEdit, QLabel,
    QCheckBox, QHBoxLayout, QMessageBox, QSpacerItem, QSizePolicy,QFileDialog, QGridLayout
)
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtCore import Qt
from logics.LiquibasePropertyInitiator import LiquibasePropertyInitiator
import os
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtCore import pyqtSignal
from logics.DataClass import DataClass
from logics.PrevDbStateChanger import PrevDbStateChanger



class DbConnectorWindow(QWidget):
    liquibaseInitiatorCreated = pyqtSignal(object)
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.grid_layout = QGridLayout()
        # List of difference types (check boxes)
        self.difference_types = [
            "catalogs", "checkconstraints", "columns", "databasepackage",
            "databasepackagebody", "data", "foreignkeys", "functions",
            "indexes", "primarykeys", "sequences", "storedprocedures",
            "tables", "triggers", "uniqueconstraints", "views"
        ]
        self.checkboxes = {}

        for idx, diff_type in enumerate(self.difference_types):
            checkbox = QCheckBox(diff_type)
            self.checkboxes[diff_type] = checkbox
            row = idx // 3  # Two checkboxes per row
            col = idx % 3   # Alternating between column 0 and 1
            self.grid_layout.addWidget(checkbox, row, col)

        # Title Label
        title_label = QLabel("Database Connector", self)
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        # Username Input Field
        self.username_input = QLineEdit(self, placeholderText="admin")
        self.username_input.setPlaceholderText("Username")
        self.username_input.setText("admin")
        layout.addWidget(self.username_input)

        # URL Input Field
        self.url_input = QLineEdit(self, placeholderText="jdbc:mariadb://192.168.10.38:3306/fineract_tenants_sakib")
        self.url_input.setPlaceholderText("URL")
        self.url_input.setText("jdbc:mariadb://192.168.10.38:3306/fineract_tenants_sakib")
        # self.url_input.setFixedHeight(40)  # Set a fixed height to make it look normal
        layout.addWidget(self.url_input)

        # hostt Input Field
        self.host_input = QLineEdit(self, placeholderText="jdbc:mariadb://192.168.10.38:3306/fineract_tenants_sakib")
        self.host_input.setPlaceholderText("host")
        self.host_input.setText("192.168.10.38")
        # self.host_input.setFixedHeight(40)  # Set a fixed height to make it look normal
        layout.addWidget(self.host_input)

        # database Input Field
        self.database_input = QLineEdit(self, placeholderText="jdbc:mariadb://192.168.10.38:3306/fineract_tenants_sakib")
        self.database_input.setPlaceholderText("database")
        self.database_input.setText("fineract_tenants_sakib")
        # self.database_input.setFixedHeight(40)  # Set a fixed height to make it look normal
        layout.addWidget(self.database_input)


        # Password Input Field
        self.password_input = QLineEdit(self,placeholderText="@Ne7!n5")
        self.password_input.setPlaceholderText("Password")
        self.password_input.setText("@Ne7!n5")
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)

        # Driver String Input Field with Square Button
        driver_layout = QHBoxLayout()
        self.driver_string_input = QLineEdit(self, placeholderText="org.mariadb.jdbc.Driver")
        self.driver_string_input.setPlaceholderText("Driver String")
        self.driver_string_input.setText("org.mariadb.jdbc.Driver")
        driver_layout.addWidget(self.driver_string_input)

        # Small square button to open a link
        self.link_button = QPushButton("??", self)
        self.link_button.setFixedSize(20, 20)  # Small square button
        self.link_button.clicked.connect(self.open_link)
        driver_layout.addWidget(self.link_button)

        layout.addLayout(driver_layout)

        # Changelog file path input field
        file_layout = QHBoxLayout()
        self.changelog_input = QLineEdit(self, placeholderText="db/changelog/db.changelog-master.xml")
        self.changelog_input.setPlaceholderText("Changelog File Path")
        self.changelog_input.setText("db/changelog/db.changelog-master.xml")
        self.changelog_input.setText("db/changelog/db.changelog-master.xml")
        self.changelog_input.setFixedHeight(30)
        file_layout.addWidget(self.changelog_input)

        # Browse button to open file explorer
        self.browse_button = QPushButton("Browse", self)
        self.browse_button.setFixedSize(80, 30)
        self.browse_button.clicked.connect(self.open_file_explorer)
        file_layout.addWidget(self.browse_button)

        layout.addLayout(file_layout)

        # Show password checkbox
        self.show_password_checkbox = QCheckBox("Show Password", self)
        self.show_password_checkbox.stateChanged.connect(self.toggle_password_visibility)
        layout.addWidget(self.show_password_checkbox)

        # Horizontal layout for difference types
        diffLabelLayout = QHBoxLayout()

        # Label for checkboxes
        checkbox_label = QLabel("Select difference types:", self)
        diffLabelLayout.addWidget(checkbox_label)

        supeCheckbox = QCheckBox("Select All")
        supeCheckbox.stateChanged.connect(self.toggle_super_checkbox)
        diffLabelLayout.addWidget(supeCheckbox)

        layout.addLayout(diffLabelLayout)
        layout.addLayout(self.grid_layout)

        # Error message label
        self.error_label = QLabel("", self)
        self.error_label.setStyleSheet("color: red;")
        layout.addWidget(self.error_label)

        # Buttons layout (Next, Clear All and snapshot)
        button_layout = QHBoxLayout()

        # Spacer to push buttons to the right
        spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        button_layout.addItem(spacer)

        # Snapshot Button
        self.snapshot_button = QPushButton("Snapshot", self)
        self.snapshot_button.clicked.connect(self.direct_snapshot) #TODO: Implement snapshot functionality
        button_layout.addWidget(self.snapshot_button)

        # Clear Button
        self.clear_button = QPushButton("Clear All", self)
        self.clear_button.clicked.connect(self.clear_fields)
        button_layout.addWidget(self.clear_button)

        # Next Button
        self.next_button = QPushButton("Next", self)
        self.next_button.clicked.connect(self.validate_and_next)
        button_layout.addWidget(self.next_button)

        


        layout.addLayout(button_layout)
        self.setLayout(layout)

    def toggle_password_visibility(self):
        if self.show_password_checkbox.isChecked():
            self.password_input.setEchoMode(QLineEdit.Normal)
        else:
            self.password_input.setEchoMode(QLineEdit.Password)

    def clear_fields(self):
        self.url_input.clear()
        self.username_input.clear()
        self.password_input.clear()
        self.driver_string_input.clear()
        self.error_label.clear()
        self.changelog_input.clear()
        self.host_input.clear()
        self.database_input.clear()


        for checkbox in self.checkboxes.values():
            checkbox.setChecked(False)

    def toggle_super_checkbox(self):
        """Toggle all checkboxes based on the state of the super checkbox."""
        for checkbox in self.checkboxes.values():
            checkbox.setChecked(self.sender().isChecked())

    def open_link(self):
        """Open a predefined link in the system's default browser."""
        webbrowser.open("https://docs.liquibase.com/workflows/liquibase-community/adding-and-updating-liquibase-drivers.html")  # Replace with your desired link

    def validate_and_next(self):
        """Check if all fields are filled, otherwise show an error message."""
        if not self.url_input.text() or not self.username_input.text() or not self.password_input.text() or not self.driver_string_input.text() or not self.database_input.text() or not self.host_input.text():
            self.error_label.setText("All fields are required!")
        else:
            self.error_label.clear()
            """Collect input from form, validate, and create LiquibasePropertyInitiator object."""
            url = self.url_input.text().strip()
            username = self.username_input.text().strip()
            password = self.password_input.text().strip()
            driver = self.driver_string_input.text().strip()
            changelog_file = self.changelog_input.text().strip()

            # Validate that all required fields are filled
            if not url or not username or not password or not driver or not changelog_file:
                self.show_error_message("All fields must be filled.")
                return

            # Collect checked difference types
            diff_types = [key for key, checkbox in self.checkboxes.items() if checkbox.isChecked()]

            # Create LiquibasePropertyInitiator object
            liquibase_initiator = LiquibasePropertyInitiator(
                url=url,
                password=password,
                driver=driver,
                username=username,
                changeLogFile=changelog_file,
                diffTypes=diff_types
            )

            DataClass.get_instance().set_host(self.host_input.text())
            DataClass.get_instance().set_origial_db_name(self.database_input.text())

            liquibase_initiator.save_liquibase_properties()
            liquibase_initiator.run_liquibase_command()

            self.liquibaseInitiatorCreated.emit(liquibase_initiator)
            data_instance = DataClass.get_instance()
            data_instance.set_liquibase_initiator(liquibase_initiator)
            self.go_to_changelog()
    
    def direct_snapshot(self):
        """Check if all fields are filled, otherwise show an error message."""
        if not self.url_input.text() or not self.username_input.text() or not self.password_input.text() or not self.driver_string_input.text():
            self.error_label.setText("All fields are required!")
        else:
            self.error_label.clear()
            """Collect input from form, validate, and create LiquibasePropertyInitiator object."""
            url = self.url_input.text().strip()
            username = self.username_input.text().strip()
            password = self.password_input.text().strip()
            driver = self.driver_string_input.text().strip()
            changelog_file = self.changelog_input.text().strip()

            # Validate that all required fields are filled
            if not url or not username or not password or not driver or not changelog_file:
                self.show_error_message("All fields must be filled.")
                return

            # Collect checked difference types
            diff_types = [key for key, checkbox in self.checkboxes.items() if checkbox.isChecked()]

            # Create LiquibasePropertyInitiator object
            liquibase_initiator = LiquibasePropertyInitiator(
                url=url,
                password=password,
                driver=driver,
                username=username,
                changeLogFile=changelog_file,
                diffTypes=diff_types
            )

            # Save the liquibase.properties file and run the liquibase command
            liquibase_initiator.save_liquibase_properties()
            liquibase_initiator.run_liquibase_command()

            # Open the folder where the changelog file is located
            folder_path = os.path.dirname(changelog_file)  # Get the directory path from the changelog file
            if folder_path and os.path.exists(folder_path):  # Ensure the folder exists
                QDesktopServices.openUrl(QUrl.fromLocalFile(folder_path))

            # self.go_to_changelog()

    def go_to_changelog(self):
        """Logic to transition to ChangeLogWindow."""
        self.parent.show_changelog_window(self.changelog_input.text())

    def open_file_explorer(self):
        """Open the file explorer to select a folder and set the path."""
        options = QFileDialog.Options()
        folder_path = QFileDialog.getExistingDirectory(self, "Select Folder", "", options=options)
        DataClass.get_instance().set_current_xml_path(folder_path)
        if folder_path:
            self.changelog_input.setText(folder_path)
        else:
            # create a msgbox to show "No folder selected"
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("No folder selected.")




