import ucpopy.globals as g
from ucpopy.structs import *
from ucpopy.ucpop import plan

g.templates = [
    P_STEP(
        id=[],
        action=["MOVE", "?FROM", "?TO"],
        parms=["?FROM", "?TO"],
        precond=[
            ":AND",
            ["LOCATION", "?FROM"],
            ["LOCATION", "?TO"],
            [":NEQ", "?FROM", "?TO"],
            ["AT", "ROBOT", "?FROM"],
            ["CONNECTED", "?FROM", "?TO"],
        ],
        add=[
            EFFECT(
                id=[],
                forall=["?X"],
                precond=[":AND", ["GRASPING", "?X"], ["OBJECT", "?X"]],
                ranking=[],
                add=[[":NOT", ["AT", "?X", "?FROM"]]],
            ),
            EFFECT(
                id=[],
                forall=["?X"],
                precond=[":AND", ["GRASPING", "?X"], ["OBJECT", "?X"]],
                ranking=[],
                add=[["AT", "?X", "?TO"]],
            ),
            EFFECT(
                id=[],
                forall=[],
                precond=[],
                ranking=[],
                add=[[":NOT", ["AT", "ROBOT", "?FROM"]]],
            ),
            EFFECT(
                id=[], forall=[], precond=[], ranking=[], add=[["AT", "ROBOT", "?TO"]]
            ),
        ],
        cache=[],
    ),
    P_STEP(
        id=[],
        action=["DROP", "?X"],
        parms=["?X"],
        precond=[":AND", ["OBJECT", "?X"], [":NEQ", "?X", "ROBOT"], ["GRASPING", "?X"]],
        add=[
            EFFECT(
                id=[],
                forall=[],
                precond=[],
                ranking=[],
                add=[[":NOT", ["GRASPING", "?X"]]],
            ),
            EFFECT(id=[], forall=[], precond=[], ranking=[], add=[["EMPTY-HANDED"]]),
        ],
        cache=[],
    ),
    P_STEP(
        id=[],
        action=["PICKUP", "?X", "?LOC"],
        parms=["?X", "?LOC"],
        precond=[
            ":AND",
            ["OBJECT", "?X"],
            ["LOCATION", "?LOC"],
            [":NEQ", "?X", "ROBOT"],
            ["EMPTY-HANDED"],
            ["AT", "?X", "?LOC"],
            ["AT", "ROBOT", "?LOC"],
        ],
        add=[
            EFFECT(
                id=[],
                forall=[],
                precond=[],
                ranking=[],
                add=[[":NOT", ["EMPTY-HANDED"]]],
            ),
            EFFECT(id=[], forall=[], precond=[], ranking=[], add=[["GRASPING", "?X"]]),
        ],
        cache=[],
    ),
]
g.axioms = []
g.dynamic_pred = ["LOCATION", "AT", "EMPTY-HANDED", "OBJECT", "GRASPING", "CONNECTED"]
initial = [
    ["LOCATION", "RM1"],
    ["LOCATION", "RM2"],
    ["OBJECT", "BOX1"],
    ["OBJECT", "BOX2"],
    ["OBJECT", "ROBOT"],
    ["CONNECTED", "RM1", "RM2"],
    ["CONNECTED", "RM2", "RM1"],
    ["AT", "BOX1", "RM2"],
    ["AT", "BOX2", "RM2"],
    ["EMPTY-HANDED"],
    ["AT", "ROBOT", "RM1"],
]
goals = ["AT", "BOX1", "RM1"]
a = plan(initial, goals)
a[0].display()
