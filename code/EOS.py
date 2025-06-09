import math as m
import yaml

class EOS:


    def __init__(self, zi:dict):
        self.zi = zi

        with open('code/db.yaml', 'r') as yaml_file:
            self.db = yaml.safe_load(yaml_file)


    def calc_a(self, component):
        '''
        Вспомогательная функция для расчета параметра а уравнения состояния
        params:
        component - компонент, для которого будет расчитан параметр а 
        '''
        omega_a = 0.45724
        return omega_a * m.pow(self.db['critical_temperature'][component], 2) * m.pow(8.314, 2) / self.db['critical_pressure'][component]



    def calc_b(self, component):
        omega_b = 0.0778
        return omega_b * 8.314 * self.db['critical_temperature'][component] / self.db['critical_pressure'][component]



    def db_print(self):
        print(self.db)


if __name__ == '__main__':
    eos = EOS({'C1':0.25, 'C2': 0.5, 'C3': 0.25})
    print(eos.calc_a('C1'))

