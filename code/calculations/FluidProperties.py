import pandas as pd
from PhaseEquilibrium import PhaseEquilibrium 
import yaml
class FluidProperties:
    
    
    def __init__(self, p, t, equil_obj: PhaseEquilibrium):
        
        with open('code/calculations/db.yaml', 'r') as db_file:
            self.db = yaml.safe_load(db_file)
        
        
        self.equil_obj = equil_obj


        if __name__ == '__main__':
            self.p = p
            self.t = t + 273.14

        else:
            self.p = p
            self.t = t



    # Метод расчета молекулярной массы
    ## Для расчета молекулярной массы газовой фазы
    @property
    def molecular_mass_vapour(self):
        m_to_sum = []
        for component in self.equil_obj.yi_v.keys():
            m_to_sum.append(self.equil_obj.yi_v[component] * self.db['molar_mass'][component])
        return sum(m_to_sum)


    # Метод расчета молекулярной массы
    ## Для расчета молекулярной массы жидкой фазы
    @property
    def molecular_mass_liquid(self):
        m_to_sum = []
        for component in self.equil_obj.xi_l.keys():
            m_to_sum.append(self.equil_obj.xi_l[component] * self.db['molar_mass'][component])
        return sum(m_to_sum)
    

    # Методы расчета объема
    ## Расчет объема для газовой фазы
    @property
    def vapour_volume(self):
        return self.equil_obj.fv * ((8.314 * self.t * self.equil_obj.eos_vapour.choosen_eos_root/ self.p) - self.equil_obj.eos_vapour.shift_parametr)


    ## Расчет объема для жидкой фазы
    @property
    def liquid_volume(self):
        return (1 - self.equil_obj.fv) * ((8.314 * self.t *self.equil_obj.eos_liquid.choosen_eos_root/ self.p) - self.equil_obj.eos_liquid.shift_parametr)
    

    # Методы расчета плотности
    ## Расчет плотности для газовой фазы
    @property
    def vapour_density(self):
        return self.molecular_mass_vapour * self.equil_obj.fv / self.vapour_volume


    ## Расчет плотности для жидкой фазы
    @property
    def liquid_density(self):
        return self.molecular_mass_liquid * (1 - self.equil_obj.fv) / self.liquid_volume


    def calc_all_properties(self):
        result_dict = {'MW_vapour': self.molecular_mass_vapour, 'MW_liquid': self.molecular_mass_liquid, 'V_vapour': self.vapour_volume, 'V_liquid': self.liquid_volume,
                       'Den_vapour': self.vapour_density, 'Den_liquid': self.liquid_density}
        return result_dict
    


if __name__ == '__main__':
    ...