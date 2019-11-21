class DetailsModel:
  def __init__(self,ward_no,no_trees,population,co2_absorbtion,co2_emitted_population,co2_emitted_vehicles,co2_emitted_total,excessed_co2,tree_required):
    self.ward_no = ward_no
    self.no_trees = no_trees
    self.population = population
    self.co2_absorbtion = co2_absorbtion
    self.co2_emitted_population = co2_emitted_population
    self.co2_emitted_vehicles = co2_emitted_vehicles
    self.co2_emitted_total = co2_emitted_total
    self.excessed_co2 = excessed_co2
    self.tree_required = tree_required
  

  def toJSON(self):
    return {
      "ward_no": str(self.ward_no),
      "no_trees": str(self.no_trees),
      "population": str(self.population),
      "co2_absorbtion": str(self.co2_absorbtion),
      "co2_emitted_population": str(self.co2_emitted_population),
      "co2_emitted_vehicles": str(self.co2_emitted_vehicles),
      "co2_emitted_total": str(self.co2_emitted_total),
      "excessed_co2": str(self.excessed_co2),
      "tree_required": str(self.tree_required),
    }
