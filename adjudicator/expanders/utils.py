

# base    -- List(Formula)
# formula -- Formula
# Add a formula to the base
# Checks if formula is already there first
def add_to_base(base, formula):
  if(not formula in base):
    base.append(formula)
    return True
  return False
