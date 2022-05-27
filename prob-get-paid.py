import ucpopy.globals as g
from ucpopy.structs import *
from ucpopy.ucpop import plan

g.templates = [
    P_STEP(
        id=[],
        action=["PUT-IN", "?X", "?L"],
        parms=["?X", "?L"],
        precond=[":NEQ", "?X", "B"],
        add=[
            EFFECT(
                id=[],
                forall=[],
                precond=[":AND", ["AT", "?X", "?L"], ["AT", "B", "?L"]],
                ranking=[],
                add=[["IN", "?X"]],
            )
        ],
        cache=[],
    ),
    P_STEP(
        id=[],
        action=["TAKE-OUT", "?X"],
        parms=["?X"],
        precond=[":NEQ", "?X", "B"],
        add=[
            EFFECT(
                id=[], forall=[], precond=[], ranking=[], add=[[":NOT", ["IN", "?X"]]]
            )
        ],
        cache=[],
    ),
    P_STEP(
        id=[],
        action=["MOV-B", "?M", "?L"],
        parms=["?M", "?L"],
        precond=[":AND", [":NEQ", "?M", "?L"], ["AT", "B", "?M"]],
        add=[
            EFFECT(
                id=[],
                forall=[],
                precond=["IN", "D"],
                ranking=[],
                add=[[":NOT", ["AT", "D", "?M"]]],
            ),
            EFFECT(
                id=[],
                forall=[],
                precond=["IN", "D"],
                ranking=[],
                add=[["AT", "D", "?L"]],
            ),
            EFFECT(
                id=[],
                forall=[],
                precond=["IN", "P"],
                ranking=[],
                add=[[":NOT", ["AT", "P", "?M"]]],
            ),
            EFFECT(
                id=[],
                forall=[],
                precond=["IN", "P"],
                ranking=[],
                add=[["AT", "P", "?L"]],
            ),
            EFFECT(
                id=[],
                forall=[],
                precond=[],
                ranking=[],
                add=[[":NOT", ["AT", "B", "?M"]]],
            ),
            EFFECT(id=[], forall=[], precond=[], ranking=[], add=[["AT", "B", "?L"]]),
        ],
        cache=[],
    ),
]
g.axioms = []
g.dynamic_pred = ["AT", "IN", "OBJECT", "PLACE"]
initial = [
    ["PLACE", "HOME"],
    ["PLACE", "OFFICE"],
    ["OBJECT", "P"],
    ["OBJECT", "D"],
    ["OBJECT", "B"],
    ["AT", "B", "HOME"],
    ["AT", "P", "HOME"],
    ["AT", "D", "HOME"],
    ["IN", "P"],
]
goals = [":AND", ["AT", "B", "OFFICE"], ["AT", "D", "OFFICE"], ["AT", "P", "HOME"]]
a = plan(initial, goals)
a[0].display()
