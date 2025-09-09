from pathlib import Path
import sys

# Добавляем корневую директорию в PYTHONPATH
root_path = Path(__file__).parent.parent.parent
sys.path.append(str(root_path))


from calculations.Composition.Composition import Composition
from calculations.VLE.Flash import FlashFactory
from calculations.Utils.Conditions import Conditions
from calculations.PhaseDiagram.PhaseDiagram_v4 import PhaseDiagram
from calculations.CompositionalModel.Variant import CompositionalVariantFactory



class CompositionalModel:
    def __init__(self,zi: Composition, eos: str = 'PREOS'):
        self._composition = zi
        self._eos = eos
        self._flash_results = {}
        self._compositional_variants_factory = CompositionalVariantFactory()
        self._compositional_variants = {}
        self._create_base_variant()

    def _create_base_variant(self):
        '''Creates base compositional variant'''
        self._compositional_variants['base'] = self._compositional_variants_factory.create_variant(self._composition, 'PREOS')

    def create_variant(self, name, composition, eos):
        self._compositional_variants[name] = self._compositional_variants_factory.create_variant(composition, eos)



if __name__ == '__main__':


    comp = Composition({'C1': 0.35, 'C2':0.1, 'C3': 0.05, 'nC5':0.05, 'C6': 0.05, 'iC4': 0.1,'C8':0.05, 'C9':0.05, 'C10': 0.05, 'C11': 0.05, 'C16':0.05, 'C44': 0.05},
                       c6_plus_bips_correlation= None,
                       c6_plus_correlations = {'critical_temperature': 'kesler_lee',
                                                        'critical_pressure' : 'rizari_daubert',
                                                        'acentric_factor': 'edmister',
                                                        'critical_volume': 'hall_yarborough',
                                                        'k_watson': 'k_watson',
                                                        'shift_parameter': 'jhaveri_youngren'}
                       )

    comp.show_composition_dataframes()

    #comp.edit_component_properties('C1', {'molar_mass': 0.1, 'critical_pressure': 500})

    #comp.show_composition_dataframes()

    comp_model = CompositionalModel(comp, eos = 'PREOS')

    conditions1 = Conditions(5, 50)
    # conditions2 = Conditions(7,50)

    comp_model.flash(conditions=conditions1)
    #print(comp_model.flash_results)
    
    # #comp_model.flash(conditions=conditions2)
    print(comp_model._flash_results)
    print(comp_model.show_flashes)


    



