from __future__ import division
from pyomo.environ import *
from pyomo.opt import SolverFactory, SolverStatus, TerminationCondition

model = AbstractModel()

# SETS
model.I = Set()
model.J = Set()

# PARAMETERS
model.v = Param(model.I, model.J, default=0)
model.w = Param(model.I, model.J, default=0)
model.W = Param(model.J)

# VARIABLES
model.x = Var(model.I, model.J, domain=Binary)

# DATA
data = DataPortal()
data.load(filename="multiKnapsackData.dat")

# OBJECTIVE
def obj_rule(model):
    return sum(model.v[i,j] * model.x[i,j] for i in model.I for j in model.J)
model.obj = Objective(rule=obj_rule, sense=maximize)

# CONSTRAINTS
def total_weight_rule(model, j):
    return sum(model.w[i,j] * model.x[i,j] for i in model.I) <= model.W[j]
model.total_weight = Constraint(model.J, rule=total_weight_rule)

# SOLVER OPTIONS
opt = SolverFactory('glpk')

# SOLVE
instance = model.create(data)
results = opt.solve(instance, tee=False) #set tee=True if you want to see some solver output
instance.load(results)

solution_set = [(i,j) for i in instance.I for j in instance.J if instance.x[i,j].value == 1]
total_value = sum(instance.v[i,j] for (i,j) in solution_set)

print "solution_set:", solution_set
print "total_value:", total_value