from graphviz import Digraph

dot = Digraph(comment='Space Station Robot Signal Tree', format='png')

# Main Node
dot.node('A', 'Space Station')

# Level 1 Branches
dot.node('B', 'Robotic Arm')
dot.node('C', 'Production Line')
dot.node('D', 'Robots')

dot.edges(['AB', 'AC', 'AD'])

# Level 2 Branches (Robotic Arm)
dot.node('E', 'Object Manipulation')
dot.node('F', 'Maintenance')
dot.node('G', 'Experiment Assistance')

dot.edges(['BE', 'BF', 'BG'])

# Level 2 Branches (Production Line)
dot.node('H', 'Material Processing')
dot.node('I', 'Assembly')
dot.node('J', 'Quality Control')

dot.edges(['CH', 'CI', 'CJ'])

# Level 2 Branches (Robots)
dot.node('K', 'Social Companion')
dot.node('L', 'Pet')
dot.node('M', 'Chore')

dot.edges(['DK', 'DL', 'DM'])

# Render and Display
dot.render('space_station_signal_tree', view=True)
