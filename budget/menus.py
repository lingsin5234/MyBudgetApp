from menu import Menu, MenuItem
from django.urls import reverse
from . import views as budget_vw

# add items to the menu
Menu.add_item("budget", MenuItem("Home", reverse(budget_vw.show_d3), weight=10))
Menu.add_item("budget", MenuItem("Budget Data", reverse(budget_vw.show_data), weight=10))
