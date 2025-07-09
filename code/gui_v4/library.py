# library.py
import dearpygui.dearpygui as dpg
import json
import yaml
from pathlib import Path
from db_reader import DBReader
from typing import Dict, Any


# class LibraryWindow:
#     def __init__(self):
#         self.db = DBReader()
#         self.keys = self.db.get_keys()
        
#     def create(self):
#         with dpg.window(
#             tag="popup_window",
#             label="DB Data",
#             width=800,
#             height=600,
#             modal=False,
#             no_close=True
#         ):
#             with dpg.group(horizontal=True):
#                 with dpg.group(width=200):
#                     dpg.add_text("Select db item:")
#                     dpg.add_listbox(
#                         tag='listbox_library',
#                         items=self.keys,
#                         num_items=min(15, len(self.keys)),
#                         width=180,
#                         callback=self.update_table
#                     )
#                     dpg.add_spacer(height=20)
#                     dpg.add_button(label='Add', callback=AddToDBWindow().show)
#                     dpg.add_button(
#                         label="Close",
#                         callback=lambda: dpg.delete_item("popup_window")
#                     )
#                 with dpg.group(tag="library_table_group"):
#                     if self.keys:
#                         self.show_table(self.keys[0])

#     def show_table(self, key: str):
#         if dpg.does_item_exist("library_table"):
#             dpg.delete_item("library_table")
            
#         data = self.db.get_data(key)
#         with dpg.table(
#             tag="library_table",
#             parent="library_table_group",
#             header_row=True,
#             borders_innerH=True,
#             borders_outerH=True,
#             borders_innerV=True,
#             borders_outerV=True,
#             width=550,
#             height=500
#         ):
#             if not data:
#                 dpg.add_text("No data available")
#                 return

#             dpg.add_table_column(label="Component")
#             dpg.add_table_column(label="Value")

#             for key, value in data.items():
#                 with dpg.table_row():
#                     dpg.add_text(str(key))
#                     dpg.add_text(json.dumps(value, indent=2) if isinstance(value, (dict, list)) else str(value))

#     def update_table(self, sender):
#         selected_key = dpg.get_value(sender)
#         self.show_table(selected_key)

# class LibraryWindow:
#     def __init__(self):
#         self.db = DBReader()
#         self.keys = self.db.get_keys()
#         self.table_id = None
#         self.hint_text_id = None
        
#     def create(self):
#         with dpg.window(
#             tag="popup_window",
#             label="DB Data",
#             width=1000,
#             height=700,
#             modal=False,
#             no_close=True
#         ):
#             with dpg.group(horizontal=True):
#                 # Левая панель - выбор категории
#                 with dpg.group(width=200):
#                     dpg.add_text("Select category:")
#                     dpg.add_listbox(
#                         tag='listbox_library',
#                         items=self.keys,
#                         num_items=min(15, len(self.keys)),
#                         width=180,
#                         callback=self.update_table
#                     )
#                     dpg.add_spacer(height=20)
#                     dpg.add_button(label='Add', callback=AddToDBWindow().show)
#                     dpg.add_button(
#                         label="Close",
#                         callback=lambda: dpg.delete_item("popup_window")
#                     )
                
#                 # Правая панель - таблица данных
#                 with dpg.child_window(tag="table_container", width=750, height=650):
#                     self.hint_text_id = dpg.add_text(
#                         "Please select a category to view data",
#                         pos=[300, 300]
#                     )

#     def create_table(self, category_data):
#         """Создает компактную таблицу с данными выбранной категории"""
#         # Удаляем старую таблицу, если она есть
#         if self.table_id and dpg.does_item_exist(self.table_id):
#             dpg.delete_item(self.table_id)
        
#         # Скрываем подсказку
#         if self.hint_text_id and dpg.does_item_exist(self.hint_text_id):
#             dpg.hide_item(self.hint_text_id)
        
#         if not category_data:
#             return
        
#         subcategories = list(category_data.keys())
#         components = set()
        
#         # Собираем все уникальные компоненты
#         for subcat in subcategories:
#             components.update(category_data[subcat].keys())
        
#         # Создаем компактную таблицу
#         with dpg.table(
#             parent="table_container",
#             header_row=True,
#             policy=dpg.mvTable_SizingFixedFit,
#             borders_innerH=True,
#             borders_innerV=True,
#             borders_outerH=True,
#             borders_outerV=True,
#             row_background=True,
#             reorderable=True,
#             resizable=True,
#             tag="data_table"
#         ) as table_id:
#             self.table_id = table_id
            
#             # Первый столбец - компоненты
#             dpg.add_table_column(label="Component", width_fixed=True, width=100)
            
#             # Столбцы для подкатегорий
#             for subcat in subcategories:
#                 dpg.add_table_column(label=subcat, width_fixed=True, width=100)
            
#             # Заполняем таблицу данными
#             for component in sorted(components):
#                 with dpg.table_row():
#                     dpg.add_text(component.strip())
#                     for subcat in subcategories:
#                         value = category_data.get(subcat, {}).get(component, "")
#                         dpg.add_text(str(value) if value != "" else "")

#     def update_table(self, sender):
#         selected_key = dpg.get_value(sender)
#         category_data = self.db.get_data(selected_key)
#         self.create_table(category_data)

import dearpygui.dearpygui as dpg
import json
from pathlib import Path


class LibraryWindow:
    def __init__(self):
        self.db = DBReader()
        self.keys = self.db.get_keys()
        print(self.keys)
        self.table_id = None
        self.hint_text_id = None
        self.selected_key = None
        self.window_tag = "popup_window"
        self.table_container_tag = "table_container"
        
    def create(self):
        # Удаляем старое окно если существует
        if dpg.does_item_exist(self.window_tag):
            dpg.delete_item(self.window_tag)
            
        with dpg.window(
            tag=self.window_tag,
            label="DB Data",
            width=1000,
            height=700,
            pos=[100, 100],
            modal=False,
            no_close=True
        ):
            with dpg.group(horizontal=True):
                # Левая панель - выбор категории
                with dpg.group(width=200):
                    dpg.add_text("Select category:")
                    # Используем combo вместо listbox для лучшего UX
                    dpg.add_combo(
                        tag='category_combo',
                        items=self.keys,
                        width=180,
                        callback=self.update_table
                    )
                    dpg.add_spacer(height=20)
                    dpg.add_button(label='Add')  # callback=AddToDBWindow().show временно убран
                    dpg.add_button(
                        label="Close",
                        callback=lambda: dpg.delete_item(self.window_tag)
                    )
                
                # Правая панель - таблица данных
                with dpg.child_window(
                    tag=self.table_container_tag, 
                    width=750, 
                    height=650,
                    border=True
                ):
                    self.hint_text_id = dpg.add_text(
                        "Please select a category to view data",
                        show=bool(self.keys)  # Показываем только если есть категории
                    )
            
            # Автоматически выбираем первую категорию при наличии данных
            if self.keys:
                self.selected_key = self.keys[0]
                dpg.set_value('category_combo', self.keys[0])
                self.update_table('category_combo', self.keys[0])

    def create_table(self, category_data):
        """Создает компактную таблицу с данными выбранной категории"""
        # Удаляем старую таблицу, если она есть
        if self.table_id and dpg.does_item_exist(self.table_id):
            dpg.delete_item(self.table_id)
            self.table_id = None
        
        # Скрываем подсказку
        if self.hint_text_id and dpg.does_item_exist(self.hint_text_id):
            dpg.hide_item(self.hint_text_id)
        
        if not category_data:
            # Если данных нет, показываем сообщение
            if self.hint_text_id and dpg.does_item_exist(self.hint_text_id):
                dpg.set_value(self.hint_text_id, "No data available for this category")
                dpg.show_item(self.hint_text_id)
            return
        
        subcategories = list(category_data.keys())
        
        # Если нет подкатегорий
        if not subcategories:
            if self.hint_text_id and dpg.does_item_exist(self.hint_text_id):
                dpg.set_value(self.hint_text_id, "No subcategories found")
                dpg.show_item(self.hint_text_id)
            return
        
        components = set()
        
        # Собираем все уникальные компоненты
        for subcat in subcategories:
            if category_data[subcat]:
                components.update(category_data[subcat].keys())
        
        # Если нет компонентов
        if not components:
            if self.hint_text_id and dpg.does_item_exist(self.hint_text_id):
                dpg.set_value(self.hint_text_id, "No components found")
                dpg.show_item(self.hint_text_id)
            return
        
        # Создаем компактную таблицу
        with dpg.table(
            parent=self.table_container_tag,
            header_row=True,
            policy=dpg.mvTable_SizingFixedFit,
            borders_innerH=True,
            borders_innerV=True,
            borders_outerH=True,
            borders_outerV=True,
            row_background=True,
            reorderable=True,
            resizable=True,
            scrollY=True,
            height=600,
            tag="data_table"
        ) as table_id:
            self.table_id = table_id
            
            # Первый столбец - компоненты
            dpg.add_table_column(label="Component", width_fixed=True, width=100)
            
            # Столбцы для подкатегорий
            for subcat in subcategories:
                dpg.add_table_column(label=subcat, width_fixed=True, width=100)
            
            # Заполняем таблицу данными
            for component in sorted(components):
                with dpg.table_row():
                    dpg.add_text(component.strip())
                    for subcat in subcategories:
                        comp_data = category_data.get(subcat, {})
                        value = comp_data.get(component) or comp_data.get(component.strip()) or ""
                        dpg.add_text(str(value) if value != "" else "")

    def update_table(self, sender, app_data):
        """Обработчик выбора категории"""
        selected_key = app_data
        if selected_key in self.keys:
            self.selected_key = selected_key
            category_data = self.db.get_data(selected_key)
            self.create_table(category_data)

class AddToDBWindow:
    def __init__(self):
        
        self.json_data: Dict[str, Any] = {}
        self.input_widgets = []

    def add_field_callback(self):
        """Добавляет новое поле для ввода ключа и значения"""
        with dpg.group(horizontal=True, parent="fields_group"):
            key_input = dpg.add_input_text(hint="Key", width=150)
            value_input = dpg.add_input_text(hint="Value", width=150)
            dpg.add_button(label="×", callback=lambda: self.remove_field(key_input, value_input))
            self.input_widgets.append((key_input, value_input))

    def remove_field(self, key_input, value_input):
        """Удаляет поле ввода"""
        for widget in [key_input, value_input]:
            dpg.delete_item(widget)
        self.input_widgets.remove((key_input, value_input))

    def collect_data(self):
        """Собирает данные из всех полей ввода"""
        global json_data
        json_data = {}
        for key_input, value_input in self.input_widgets:
            key = dpg.get_value(key_input)
            value = dpg.get_value(value_input)
            if key:  # Игнорируем пустые ключи
                # Пытаемся преобразовать значение в число или булево
                try:
                    value = int(value)
                except ValueError:
                    try:
                        value = float(value)
                    except ValueError:
                        if value.lower() == "true":
                            value = True
                        elif value.lower() == "false":
                            value = False
                json_data[key] = value
        return json_data

    def save_json_callback(self):
        """Обработчик сохранения JSON"""
        data = self.collect_data()
        if not data:
            dpg.set_value("status", "Error: No data!")
            return
        
        with dpg.file_dialog(
            directory_selector=False,
            show=True,
            modal=True,
            height=400,
            callback=lambda s, a: self.write_json(s, a, data),
            tag="file_dialog_id"
        ):
            dpg.add_file_extension(".json", color=(0, 255, 0, 255))
            dpg.add_file_extension(".*")

    def write_json(self, sender, app_data, user_data):
        """Записывает JSON в файл"""
        if app_data["file_path_name"]:
            filepath = app_data["file_path_name"]
            if not filepath.endswith('.json'):
                filepath += '.json'
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(user_data, f, indent=4, ensure_ascii=False)
                dpg.set_value("status", f"File saved: {filepath}")


    def show_data_callback(self):
        """Показывает собранные данные"""
        data = self.collect_data()
        dpg.set_value("output", json.dumps(data, indent=4, ensure_ascii=False))

    def show(self):
        if dpg.does_item_exist("add_json_window"):
            dpg.delete_item("add_json_window")
    
        with dpg.window(label="JSON Generator", tag="add_json_window", width=800, height=600, no_close=True):
            # Кнопки управления
            with dpg.group(horizontal=True):
                dpg.add_button(label="+ Add row",callback=self.add_field_callback)
                dpg.add_button(label="Show JSON", callback=self.show_data_callback)
                dpg.add_button(label="Save JSON", callback=self.save_json_callback)
                dpg.add_button(label='Import library data from JSON',)
            
            # Группа для динамических полей
            dpg.add_text("Data:")
            dpg.add_separator()
            dpg.add_group(tag="fields_group")

                # Область вывода
            dpg.add_text("Result:")
            dpg.add_input_text(multiline=True, tag="output", width=700, height=300)
            dpg.add_text("", tag="status")

            dpg.add_button(label="Close", callback=lambda: dpg.delete_item("add_json_window"))
            # Добавляем 3 поля по умолчанию
        for _ in range(3):
            self.add_field_callback()
            


