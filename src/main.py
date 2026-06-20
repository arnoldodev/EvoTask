from models.db_config import criar_banco
from views.menu_view import menu_principal
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

criar_banco()
menu_principal()