
## How to install

To create the exe file, download the project. 

- Create a virtual environment. 
- Setup the project in the virtual environment
- install pyQt5 and pyinstaller using `pip install`
- When you have run the program successfully a GUI will pop up looking like this - 

![App Screenshot](https://github.com/sakibesrat71/auto-db-migrator/blob/main/ss.png)

- Run the following command to export it as an executable. 
```bash
pyinstaller --onefile --windowed main.py
```
- This will generate 2 different folders in the directory. One is `./build` another is `./dist`.
-Your exe will be inside `./dist` named *main.exe*.
