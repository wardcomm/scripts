import plotly.graph_objects as go

# fig = go.Figure(data=[go.Table(header=dict(values=['Symbol', 'Arithmetic','Example']),
#                  cells=dict(values=[[+,-,*,/,%], [ x + y, x - y, x * y, x % y]]))
#                      ])
# fig.show()

fig = go.Figure(data=[go.Table(header=dict(values=['A Scores', 'B Scores']),
                 cells=dict(values=[[100, 90, 80, 90], [95, 85, 75, 95]]))
                     ])
fig.show()

# arithmetic_operaters = {'''
# +     Addition    x + y

# -
# Subtraction
# x - y
# Try it »
# *
# Multiplication
# x * y
# Try it »
# /
# Division
# x / y
# Try it »
# %
# Modulus
# x % y
# Try it »
# **
# Exponentiation
# x ** y
# Try it »
# //
# Floor division
# x // y
# '''
# }

# print(arithmetic_operaters)
