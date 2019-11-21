class TreeNeededModel:
  def __init__(self, ward_no, no_trees, no_trees_needed):
    self.ward_no = ward_no    
    self.no_trees = no_trees    
    self.no_trees_needed = no_trees_needed

  def toJSON(self):
    return {"ward_no": str(self.ward_no), "no_trees": str(self.no_trees), "no_trees_needed": str(self.no_trees_needed)}
