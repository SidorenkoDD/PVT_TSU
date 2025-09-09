from calculations.Composition.Composition import Composition
from calculations.VLE.Flash import FlashFactory
from calculations.PhaseDiagram.PhaseDiagram_v4 import PhaseDiagram
#from calculations.EOS import BaseEOS

class CompositionalVariantFactory:
    def __init__(self):
        self.counter = 0

    def create_variant(self, composition, eos):
        self.counter +=1
        return CompositionalVariant(f'Variant_{self.counter}',
                                    composition,
                                     eos)


class CompositionalVariant:

    def __init__(self, zi: Composition, eos: str = 'PREOS'):
        self._composition = zi
        self._eos = eos
        self._flash_results = {}
        self._compositional_variants_factory = CompositionalVariantFactory()
        self.compositional_variants = {}

    def flash(self, conditions, flash_type = 'TwoPhaseFlash'):
        self._flash_object = FlashFactory(self._composition, self._eos)
        flash_calculator = self._flash_object.create_flash(flash_type=flash_type)
        result = flash_calculator.calculate(conditions=conditions)

        self._flash_results[str(flash_type) + '_' + str(conditions.p)+'_' + str(conditions.t)] = result 
    
    
    def plot_phase_diagram(self, p_max = 40, t_min = 0, t_max = 200, t_step = 10):
        self.phase_diagram_obj = PhaseDiagram(self._composition, p_max= p_max, t_min= t_min, t_max= t_max, t_step= t_step)
        self.phase_diagram_obj.calc_phase_diagram(eos = self._eos)
        self.phase_diagram_obj.plot_phase_diagram()


class CompositionalVariantFactory:
    def __init__(self):
        self.counter = 0

    def create_variant(self, composition, eos):
        self.counter +=1
        return CompositionalVariant(composition,
                                     eos)

    