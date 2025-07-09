import dearpygui.dearpygui as dpg

# Данные
data = {
    'p_crit': {'basic': {'N2': 3.394, 'CO2': 7.387, 'H2S': 8.937, 'C1': 4.604, 'C2': 4.884, 'C3': 4.246, 'iC4': 3.648, 'nC4': 3.797, 'iC5': 3.389, 'nC5': 3.7, 'C6': 3.104}, 'basic2': {'N2': 10.394, 'CO2': 7.387, 'H2S': 8.937, 'C1': 4.604, 'C2': 4.884, 'C3': 4.246, 'iC4': 3.648, 'nC4': 3.797, 'iC5': 3.389, 'nC5': 3.7, 'C6': 3.104}},
    't_crit': {'basic': {'N2': 126.19, 'CO2': 304.69, 'H2S': 373.59, 'C1': 190.59, 'C2': 305.42, 'C3': 369.79, 'iC4': 408.09, 'nC4': 425.19, 'iC5': 460.39, 'nC5': 469.59, 'C6': 507.5}},
    'acentric_factor': {'basic': {'N2': 0.04, 'CO2': 0.225, 'H2S': 0.1, 'C1': 0.013, 'C2': 0.0986, 'C3 ': 0.1524, 'iC4': 0.184, 'nC4': 0.201, 'iC5': 0.227, 'nC5': 0.251, 'C6': 0.252}},
    'molar_mass': {'basic': {'N2': 28.013, 'CO2': 44.01, 'H2S': 34.076, 'C1': 16.043, 'C2': 30.07, 'C3': 44.097, 'iC4': 58.124, 'nC4': 58.1, 'iC5': 72.151, 'nC5': 72.151, 'C6 ': 86.177}},
    'shift_parametr': {'basic': {'N2': -0.1927, 'CO2': -0.0817, 'H2S': -0.1288, 'C1': -0.1595, 'C2': -0.1134, 'C3': -0.0863, 'iC4': -0.0844, 'nC4': -0.094, 'iC5': -0.0608, 'nC5': -0.039, 'C6': -0.008}},
    'bips': {'basic': {}}
}

# Состояние приложения
state = {
    'selected_category': None,
    'table_id': None,
    'hint_text_id': None  # Для хранения id текста-подсказки
}

def create_table():
    """Создает компактную таблицу с данными выбранной категории"""
    # Удаляем старую таблицу, если она есть
    if state['table_id'] and dpg.does_item_exist(state['table_id']):
        dpg.delete_item(state['table_id'])
    
    # Скрываем подсказку, если она есть
    if state['hint_text_id'] and dpg.does_item_exist(state['hint_text_id']):
        dpg.hide_item(state['hint_text_id'])
    
    if not state['selected_category']:
        return
    
    category_data = data.get(state['selected_category'], {})
    subcategories = list(category_data.keys())
    components = set()
    
    for subcat in subcategories:
        components.update(category_data[subcat].keys())
    
    # Создаем компактную таблицу
    with dpg.table(parent="table_container", header_row=True, 
                  policy=dpg.mvTable_SizingFixedFit,  # Компактный режим
                  borders_innerH=True, borders_innerV=True, borders_outerH=True, borders_outerV=True,
                  row_background=True, reorderable=True, resizable=True,
                  tag="data_table") as table_id:
        state['table_id'] = table_id
        
        # Первый столбец - компоненты (фиксированная ширина)
        dpg.add_table_column(label="Component", width_fixed=True, width=80)
        
        # Столбцы для подкатегорий (минимальная ширина)
        for subcat in subcategories:
            dpg.add_table_column(label=subcat, width_fixed=True, width=100)
        
        # Заполняем таблицу данными
        for component in sorted(components):
            with dpg.table_row():
                dpg.add_text(component.strip())
                for subcat in subcategories:
                    value = category_data.get(subcat, {}).get(component, "")
                    dpg.add_text(str(value) if value != "" else "")

def on_category_select(sender, app_data):
    """Обработчик выбора категории"""
    state['selected_category'] = app_data
    create_table()

# Создаем GUI
dpg.create_context()
dpg.create_viewport(title='Data Viewer', width=1000, height=700)

with dpg.window(label="Main Window", width=1000, height=700):
    # Выпадающий список для выбора категории
    dpg.add_text("Select category:")
    dpg.add_combo(
        items=list(data.keys()),
        callback=on_category_select,
        width=200,
        tag="category_combo"
    )
    
    # Контейнер для таблицы с подсказкой по центру
    with dpg.child_window(tag="table_container", height=600, border=True):
        state['hint_text_id'] = dpg.add_text("Please select a category to view data", 
                                           pos=[400, 300])

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()