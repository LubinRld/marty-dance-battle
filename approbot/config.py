WINDOW_TITLE = "MartyApp"
BACKGROUND_STYLE = "background-color: #98d7d6;"
WINDOW_WIDTH = 440
WINDOW_HEIGHT = 500
WINDOW_ICON_PATH = "approbot/Logo.png"

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

REAL_COLOR_RGB = {

    "Black" : "#000000",
    "Purple" : "#FF29F1",
    "Dark Blue" : "#0000F0",
    "Yellow": "#FFFF24",
    "Cyan" : "#1AF8FF",
    "Green" : "#1BF000",
    "Red" : "#FF291A"
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
        border: none;
        background: transparent;
    }

    QPushButton:pressed {
        padding-top: 3px;
        padding-left: 3px;
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
CARD_STYLE = """
    QWidget {
        background-color: #ffffff;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
    }
    QLabel { border: none; } /* Évite que les textes héritent de la bordure */
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

    /* 💡 C'EST CETTE RÈGLE QUI CORRIGE LA LISTE DÉROULANTE : */
    QComboBox QAbstractItemView {
        background-color: #ffffff;
        color: #000000;  /* Force le texte de la liste déroulante en noir */
        selection-background-color: #3b82f6; /* Couleur de surbrillance quand tu passes la souris */
        selection-color: #ffffff;
        border: 1px solid #cbd5e1;
    }
"""

BTN_LAUNCH_STYLE = """
    QPushButton {
        background-color: #10b981;
        color: white;
        font-size: 16px;
        font-weight: bold;
        border-radius: 8px;
        padding: 12px 40px;
    }
    QPushButton:hover { background-color: #059669; }
    QPushButton:disabled { background-color: #cbd5e1; color: #94a3b8; }
"""