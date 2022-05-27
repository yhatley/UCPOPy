d_sep = True  # Use Peot and Smith's delay technique
d_forall = True

delay_link = False  # Are filter conditions used?

# Make DISABLE only introduce ordering constraints when set to T
ord_constrain_on_confront = False

# Cause ucpop to recognize a threat only when the threatening step's
# effect contradicts the link's label
positive_threats = False

# Cause ucpop to check for safety constraints
safety_p = False

# Cause ucpop to be aware of side effects.
# A step that possesses  side effects should not be instantiated
# as a new step by linking the side effects to an open condition.
side_effects = True

templates = []
axioms = []
facts = []
search_limit = 2000
safety_constraints = []
dynamic_pred = []
