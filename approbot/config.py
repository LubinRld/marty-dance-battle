WINDOW_TITLE = "MartyApp"
BACKGROUND_STYLE = "background-color: #98d7d6;"
WINDOW_WIDTH = 440
WINDOW_HEIGHT = 500
WINDOW_ICON_PATH = "assets/Logo.png"

DEFAULT_COLOR_REFERENCES = {
    "Black" : (25,12,11), 
    "Purple" : (157,33,53),
    "Dark Blue" : (33,22,30),
    "Yellow" : (271,110,78),
    "Cyan" : (71,75,100),
    "Green" : (47,43,40),
    "Red" : (136,22,30)
    }

COLOR_TRANSLATION = {
    "Black": "N",
    "Purple": "P",
    "Dark Blue": "B",
    "Yellow": "Y",
    "Cyan": "C",
    "Green": "G",
    "Red": "R"
}

REAL_COLOR_RGB = {

    "Black" : "#000000",
    "Purple" : "#FF29F1",
    "Dark Blue" : "#0000F0",
    "Yellow": "#FFFF24",
    "Cyan" : "#1AF8FF",
    "Green" : "#1BF000",
    "Red" : "#FF291A"
}

BTN_SECONDARY_STYLE = """
    QPushButton {
        background-color: #34495E;
        color: white;
        font-weight: bold;
        border-radius: 6px;
        padding: 8px 15px;
        border: none;
    }
    QPushButton:hover {
        background-color: #2C3E50;
    }
    QPushButton:disabled {
        background-color: #BDC3C7;
        color: #7F8C8D;
    }
"""

BTN_PRIMARY_STYLE = """
    QPushButton {
        background-color: #2ECC71;
        color: white;
        font-weight: bold;
        border-radius: 6px;
        padding: 10px 20px;
        border: none;
    }
    QPushButton:hover {
        background-color: #27AE60;
    }
    QPushButton:disabled {
        background-color: #BDC3C7;
        color: #7F8C8D;
    }
"""

BTN_REF_DISCONNECTED_STYLE = """
    QPushButton {
        background-color: #E74C3C;
        color: white;
        font-weight: bold;
        border-radius: 6px;
        padding: 10px;
        border: none;
    }
    QPushButton:hover {
        background-color: #C0392B;
    }
"""

BTN_REF_CONNECTED_STYLE = """
    QPushButton {
        padding: 10px; 
        background-color: #2ECC71; 
        color: white; 
        font-weight: bold; 
        border-radius: 6px;
        border: none;
    }
    QPushButton:hover {
        background-color: #27AE60; /* Un vert un peu plus foncé au survol */
    }
"""

BTN_REF_WAITING_STYLE = """
    QPushButton {
        background-color: #F39C12; 
        color: white; 
        font-weight: bold; 
        border-radius: 6px;
        padding: 10px; 
        border: none;
    }
    QPushButton:hover {
        background-color: #D68910;
    }
"""

BTN_MOVEMENT_STYLE = """
    QPushButton {
        border: none;
        background: transparent;
    }

    QPushButton:pressed {
        padding-top: 3px;
        padding-left: 3px;
    }
"""

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

INPUT_STYLE = """
    QLineEdit, QComboBox {
        padding: 10px;
        font-size: 13px;
        border: 1px solid #cbd5e1;
        border-radius: 6px;
        background-color: #ffffff;
        color: #000000;  /* Force le texte de base en noir */
    }
    
    QLineEdit:focus, QComboBox:focus { 
        border: 2px solid #3b82f6; 
    }

    QComboBox QAbstractItemView {
        background-color: #ffffff;
        color: #000000;  /* Force le texte de la liste déroulante en noir */
        selection-background-color: #3b82f6; /* Couleur de surbrillance quand tu passes la souris */
        selection-color: #ffffff;
        border: 1px solid #cbd5e1;
    }
"""

CARD_STYLE = "background: transparent; border: none;"