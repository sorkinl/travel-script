from numpy import Infinity
from ortools.linear_solver import pywraplp
from ortools.init import pywrapinit
import pandas as pd
from settings import df


def main():
    #df = pd.read_excel('table.xlsx')
    prices = df['Price'].tolist()
    # Create the linear solver with the GLOP backend.
    solver = pywraplp.Solver.CreateSolver('GLOP')
    # Create the variables x and y.
    list_of_vars = []
    for i in range(len(prices)):
        list_of_vars.append(solver.NumVar(0, 1, f'x{i}'))

    print('Number of variables =', solver.NumVariables())

    # Create a linear constraint, 0 <= x + y <= 2.
    ct = solver.Constraint(1, 1, 'ct')
    for i in range(len(list_of_vars)):
        ct.SetCoefficient(list_of_vars[i], 1)
    #ct.SetCoefficient(x, 1)
    #ct.SetCoefficient(y, 1)

    print('Number of constraints =', solver.NumConstraints())

    # Create the objective function, 3 * x + y.
    objective = solver.Objective()
    for i in range(len(prices)):
        objective.SetCoefficient(list_of_vars[i], prices[i])
    #objective.SetCoefficient(y, 1)
    objective.SetMinimization()

    solver.Solve()

    print('Solution:')
    print('Objective value =', objective.Value())
    for i in range(len(prices)):
        print(f'x{i} =', list_of_vars[i].solution_value())


if __name__ == '__main__':
    pywrapinit.CppBridge.InitLogging('basic_example.py')
    cpp_flags = pywrapinit.CppFlags()
    cpp_flags.logtostderr = True
    cpp_flags.log_prefix = False
    pywrapinit.CppBridge.SetFlags(cpp_flags)

    main()
