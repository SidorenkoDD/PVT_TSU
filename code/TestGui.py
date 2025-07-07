import dearpygui.dearpygui as dpg
import dearpygui.demo as demo


# Основное окно
dpg.create_context()
dpg.create_viewport(title="Chemical Calculator", width=800, height=600)

import dearpygui.dearpygui as dpg

def menu_callback(sender, app_data, user_data):
    print(f"Выбран пункт: {user_data}")

dpg.create_context()
dpg.create_viewport(title="Window", width=800, height=600)

with dpg.window(label="Main window", tag="primary_window"):
    # Создаем строку меню
    with dpg.menu_bar():
        # Меню "Файл"
        with dpg.menu(label="File"):
            dpg.add_menu_item(label="Open", callback=menu_callback, user_data="Open")
            dpg.add_menu_item(label="Save", callback=menu_callback, user_data="Save")
            dpg.add_separator()
            dpg.add_menu_item(label="Exit", callback=lambda: dpg.stop_dearpygui())

        # Меню "Правка" с подменю
        with dpg.menu(label="Change"):
            dpg.add_menu_item(label="Copy", callback=menu_callback, user_data="Copy")
            dpg.add_menu_item(label="Paste", callback=menu_callback, user_data="Paste")
            with dpg.menu(label="More.."):
                dpg.add_menu_item(label="Cut", callback=menu_callback, user_data="Cut")
                dpg.add_menu_item(label="Del", callback=menu_callback, user_data="Del")

        # Меню "Справка"
        with dpg.menu(label="Info"):
            dpg.add_menu_item(label="Info", callback=menu_callback, user_data="Info")

# Настройка и запуск
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("primary_window", True)
dpg.start_dearpygui()
dpg.destroy_context()

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()