"""
    Dummy file to test out augmentation techniques
"""

import numpy as np

def k(s):
    return s + {2, 'a'}

x = {1, 1}
y = {1, 3, 4, 6}

x.intersection(y)
x.intersection(y + x + {1})
(k(x) + {1, 2} + k(x + k(y))).intersection(y)
(y + x).intersection(x + y)
(x + y).intersection(x + k(x))


(x + (k(y) + {2}).intersection(y)).intersection(x)
z = {1, 2} + (x + (k(y) + {2}).intersection(y)).intersection({1, 2})

pp = {1} + x.intersection(y) + {3, 4}

pp.intersection((x + (k(y) + {2})).intersection((x + (k(y) + k({2})))))
