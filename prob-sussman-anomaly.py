import ucpopy.globals as g
from ucpopy.structs import *
from ucpopy.ucpop import plan

g.templates = [
    P_STEP(
        id=[],
        action=["PUTON", "?X", "?Y", "?Z"],
        parms=["?X", "?Y", "?Z"],
        precond=[
            ":AND",
            ["ON", "?X", "?Z"],
            ["CLEAR", "?X"],
            ["CLEAR", "?Y"],
            [":NEQ", "?Y", "?Z"],
            [":NEQ", "?X", "?Z"],
            [":NEQ", "?X", "?Y"],
            [":NEQ", "?X", "TABLE"],
        ],
        add=[
            EFFECT(
                id=[],
                forall=[],
                precond=[":NEQ", "?Y", "TABLE"],
                ranking=[],
                add=[[":NOT", ["CLEAR", "?Y"]]],
            ),
            EFFECT(
                id=[],
                forall=[],
                precond=[":NEQ", "?Z", "TABLE"],
                ranking=[],
                add=[["CLEAR", "?Z"]],
            ),
            EFFECT(
                id=[],
                forall=[],
                precond=[],
                ranking=[],
                add=[[":NOT", ["ON", "?X", "?Z"]]],
            ),
            EFFECT(id=[], forall=[], precond=[], ranking=[], add=[["ON", "?X", "?Y"]]),
        ],
        cache=[],
    )
]
g.axioms = []
g.dynamic_pred = ["ON", "CLEAR", "BLOCK"]
initial = [
    ["BLOCK", "A"],
    ["BLOCK", "B"],
    ["BLOCK", "C"],
    ["BLOCK", "TABLE"],
    ["ON", "C", "A"],
    ["ON", "A", "TABLE"],
    ["ON", "B", "TABLE"],
    ["CLEAR", "C"],
    ["CLEAR", "B"],
    ["CLEAR", "TABLE"],
]
goals = [":AND", ["ON", "B", "C"], ["ON", "A", "B"]]
a = plan(initial, goals)
a[0].display()
