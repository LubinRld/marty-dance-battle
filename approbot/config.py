WINDOW_TITLE = "MartyApp"
BACKGROUND_STYLE = "background-color: #98d7d6;"
WINDOW_WIDTH = 440
WINDOW_HEIGHT = 500

DEFAULT_COLOR_REFERENCES = {
    "Black" : (25,12,11), 
    "Purple" : (122,26,40),
    "Dark Blue" : (33,22,30),
    "Yellow" : (271,110,78),
    "Cyan" : (71,75,100),
    "Green" : (47,43,40),
    "Red" : (105,17,21)
    }

COLOR_TRADUCTION = {
    "Black": "N",
    "Purple": "P",
    "Dark Blue": "B",
    "Yellow": "Y",
    "Cyan": "C",
    "Green": "G",
    "Red": "R"
}

INPUT_MARTY_IP_STYLE = """
    QLineEdit {
        padding: 8px;
        font-size: 14px;
        border: 2px solid #3498DB;
        border-radius: 6px;
        color: #000000;
        background-color: #45c2e8;
    }
    QLineEdit:focus {
        border: 2px solid #2980B9;
    }
"""

BTN_CONNEXION_STYLE = """
    QPushButton {
        padding: 8px;
        background-color: #45c2e8;
        color: black;
        border: 2px solid #3498DB;
        border-radius: 15px;
    }
    QPushButton:hover {
        background-color: #3498DB;
        color: white;
    }
"""

BTN_MOVEMENT_STYLE = """
    QPushButton {
        padding: 15px;
        background-color: #3498DB;
        color: white;
        font-weight: bold;
        border-radius: 10px;
    }
    QPushButton:hover {
        background-color: #2980B9;
    }
"""

INPUT_REF_IP_STYLE = """
    QLineEdit {
        color: black;
        padding: 8px;
        font-size: 14px;
        border: 2px solid #E74C3C;
        border-radius: 6px;
        background-color: white;
    }
    QLineEdit:focus {
        border: 2px solid #C0392B;
    }
"""