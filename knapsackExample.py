from __future__ import division
from pyomo.environ import *
from pyomo.opt import SolverFactory, SolverStatus, TerminationCondition

model = AbstractModel()

# SETS
model.I = Set()

# PARAMETERS
model.v = Param(model.I, default=0)
model.w = Param(model.I, default=0)
model.W = Param()

# VARIABLES
model.x = Var(model.I, domain=Binary)

# DATA
data = DataPortal()
data.load(filename="knapsackData.dat")

# OBJECTIVE
def obj_rule(model):
    return summation(model.v, model.x)
model.obj = Objective(rule=obj_rule, sense=maximize)

# CONSTRAINTS
def total_weight_rule(model):
    return summation(model.w, model.x) <= model.W
model.total_weight = Constraint(rule=total_weight_rule)

# SOLVER OPTIONS
opt = SolverFactory('glpk')

# SOLVE
instance = model.create(data)
results = opt.solve(instance, tee=False) #set tee=True if you want to see some solver output
instance.load(results)

solution_set = [i for i in instance.I if instance.x[i].value == 1]
total_value = sum(instance.v[i] for i in solution_set)

print "solution_set:", solution_set
print "total_value:", total_value
