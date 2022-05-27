import ucpopy.globals as g
from ucpopy.structs import *
from ucpopy.ucpop import plan

g.templates = [
    P_STEP(
        id=[],
        action=["DEBARK", "?X", "?Y"],
        parms=["?X", "?Y"],
        precond=[
            ":AND",
            ["AUTO", "?X"],
            ["PLACE", "?Y"],
            ["ON", "?X", "FERRY"],
            ["AT-FERRY", "?Y"],
        ],
        add=[
            EFFECT(id=[], forall=[], precond=[], ranking=[], add=[["EMPTY-FERRY"]]),
            EFFECT(id=[], forall=[], precond=[], ranking=[], add=[["AT", "?X", "?Y"]]),
            EFFECT(
                id=[],
                forall=[],
                precond=[],
                ranking=[],
                add=[[":NOT", ["ON", "?X", "FERRY"]]],
            ),
        ],
        cache=[],
    ),
    P_STEP(
        id=[],
        action=["SAIL", "?X", "?Y"],
        parms=["?X", "?Y"],
        precond=[
            ":AND",
            ["PLACE", "?X"],
            ["PLACE", "?Y"],
            ["AT-FERRY", "?X"],
            [":NEQ", "?X", "?Y"],
        ],
        add=[
            EFFECT(
                id=[],
                forall=[],
                precond=[],
                ranking=[],
                add=[[":NOT", ["AT-FERRY", "?X"]]],
            ),
            EFFECT(id=[], forall=[], precond=[], ranking=[], add=[["AT-FERRY", "?Y"]]),
        ],
        cache=[],
    ),
    P_STEP(
        id=[],
        action=["BOARD", "?X", "?Y"],
        parms=["?X", "?Y"],
        precond=[
            ":AND",
            ["AUTO", "?X"],
            ["PLACE", "?Y"],
            ["AT", "?X", "?Y"],
            ["AT-FERRY", "?Y"],
            ["EMPTY-FERRY"],
        ],
        add=[
            EFFECT(
                id=[],
                forall=[],
                precond=[],
                ranking=[],
                add=[[":NOT", ["EMPTY-FERRY"]]],
            ),
            EFFECT(
                id=[],
                forall=[],
                precond=[],
                ranking=[],
                add=[[":NOT", ["AT", "?X", "?Y"]]],
            ),
            EFFECT(
                id=[], forall=[], precond=[], ranking=[], add=[["ON", "?X", "FERRY"]]
            ),
        ],
        cache=[],
    ),
]
g.axioms = []
g.dynamic_pred = ["AUTO", "AT-FERRY", "PLACE", "ON", "AT", "EMPTY-FERRY"]
initial = [
    ["PLACE", "A"],
    ["PLACE", "B"],
    ["AUTO", "C1"],
    ["AUTO", "C2"],
    ["AT", "C1", "A"],
    ["AT", "C2", "A"],
    ["AT-FERRY", "A"],
    ["EMPTY-FERRY"],
]
goals = [":AND", ["AT", "C1", "B"], ["AT", "C2", "B"]]
a = plan(initial, goals)
a[0].display()
