from menu import Menu, MenuItem
from django.urls import reverse
from . import views as budget_vw

# add items to the menu
Menu.add_item("budget", MenuItem("My Portfolio", url="/", weight=10))
Menu.add_item("budget", MenuItem("Budget Project", reverse(budget_vw.project_markdown), weight=10))
Menu.add_item("budget", MenuItem("Demo Dashboard", reverse(budget_vw.show_d3), weight=10))
Menu.add_item("budget", MenuItem("Demo Data", reverse(budget_vw.show_data), weight=10))
