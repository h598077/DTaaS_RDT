from yafem import nodes
from yafem.elem import MCK
from yafem.elem import beam2d
from yafem import model
import numpy as np
import json

def eval_yafem_model(pars=None,modes=2):
    if pars == None:
        pars = {}
    pars.setdefault('b',29e-3)
    pars.setdefault('h',1e-3)
    pars.setdefault('E',210e9)
    pars.setdefault('Rho',7850)
    pars.setdefault('L',0.530)
    pars.setdefault('l',0.170)
    pars.setdefault('l1',0.030)
    pars.setdefault('l2',0.135)
    pars.setdefault('k',3.5e3)
    pars.setdefault('m',4.8e-3)
    pars.setdefault('default_field', 'default_value')

    A = pars['b']*pars['h'] 
    I = pars['b']*pars['h']**3/12

    l3 = pars['L'] - pars['l'] - pars['l1'] - pars['l2']

    # nodal parameters
    nodes_pars = {}
    nodes_pars['nodal_data'] = np.array([[0,0.0,0.0                               ,0.0],
                                         [1,0.0,pars['l']                         ,0.0],
                                         [2,0.0,pars['l']+l3                      ,0.0], # mass 1
                                         [3,0.0,pars['l']+l3+pars['l2']           ,0.0], # mass 2
                                         [4,0.0,pars['l']+l3+pars['l2']+pars['l1'],0.0]])

    # node object
    my_nodes = nodes(nodes_pars)

    # accelerometers
    my_element_mass_pars = {}
    my_element_mass_pars['M'] = np.array([[pars['m'],0],[0,pars['m']]])
    my_element_mass_pars['K'] = np.zeros((2,2))
    my_element_mass_pars['dofs'] = np.array([[2,0],[3,0]])
    my_element_mass = MCK(my_nodes,my_element_mass_pars)

    # soil spring
    my_element_spring_pars = {}
    my_element_spring_pars['K'] = np.array([[pars['k']]])
    my_element_spring_pars['dofs'] = np.array([[1,0]])
    my_element_spring = MCK(my_nodes,my_element_spring_pars)

    my_element_beam2d1_pars = {}
    my_element_beam2d1_pars['E'] = pars['E']
    my_element_beam2d1_pars['Rho'] = pars['Rho']
    my_element_beam2d1_pars['A'] = A
    my_element_beam2d1_pars['I'] = I
    my_element_beam2d1_pars['nodal_labels'] = np.array([0,1])
    my_element_beam2d1 = beam2d(my_nodes,my_element_beam2d1_pars)

    my_element_beam2d2_pars = {}
    my_element_beam2d2_pars['E'] = pars['E']
    my_element_beam2d2_pars['Rho'] = pars['Rho']
    my_element_beam2d2_pars['A'] = A
    my_element_beam2d2_pars['I'] = I
    my_element_beam2d2_pars['nodal_labels'] = np.array([1,2])
    my_element_beam2d2 = beam2d(my_nodes,my_element_beam2d2_pars)

    my_element_beam2d3_pars = {}
    my_element_beam2d3_pars['E'] = pars['E']
    my_element_beam2d3_pars['Rho'] = pars['Rho']
    my_element_beam2d3_pars['A'] = A
    my_element_beam2d3_pars['I'] = I
    my_element_beam2d3_pars['nodal_labels'] = np.array([2,3])
    my_element_beam2d3 = beam2d(my_nodes,my_element_beam2d3_pars)

    my_element_beam2d4_pars = {}
    my_element_beam2d4_pars['E'] = pars['E']
    my_element_beam2d4_pars['Rho'] = pars['Rho']
    my_element_beam2d4_pars['A'] = A
    my_element_beam2d4_pars['I'] = I
    my_element_beam2d4_pars['nodal_labels'] = np.array([3,4])
    my_element_beam2d4 = beam2d(my_nodes,my_element_beam2d4_pars)

    # list of all elements
    my_elements = [my_element_mass,my_element_spring,my_element_beam2d1,my_element_beam2d2,my_element_beam2d3,my_element_beam2d4]

    # list of all elements
    my_elements = [my_element_mass,my_element_spring,my_element_beam2d1,my_element_beam2d2,my_element_beam2d3,my_element_beam2d4]

    # model parameters
    model_pars = {}
    model_pars['dofs_c'] = np.array([[0,0],[0,1]]) # node 0 is pinned
    model_pars['damping_model'] = 'proportional'
    model_pars['alpha'] = 2.0
    model_pars['beta'] = 0.1

    # modal analysis
    my_model = model(my_nodes, my_elements,model_pars)

    omega,phi = my_model.compute_modal(modes)
    return omega, phi

omega, phi = eval_yafem_model(pars=None,modes=2)
print(omega, phi)