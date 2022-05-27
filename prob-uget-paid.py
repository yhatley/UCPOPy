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
        precond=[":AND", ["AT", "B", "?M"], [":NEQ", "?M", "?L"]],
        add=[
            EFFECT(
                id=[],
                forall=["?Z"],
                precond=[":AND", ["IN", "?Z"], [":NEQ", "?Z", "B"]],
                ranking=[],
                add=[[":NOT", ["AT", "?Z", "?M"]]],
            ),
            EFFECT(
                id=[],
                forall=["?Z"],
                precond=[":AND", ["IN", "?Z"], [":NEQ", "?Z", "B"]],
                ranking=[],
                add=[["AT", "?Z", "?L"]],
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
g.dynamic_pred = ["AT", "IN"]
initial = [["AT", "B", "HOME"], ["AT", "P", "HOME"], ["AT", "D", "HOME"], ["IN", "P"]]
goals = [":AND", ["AT", "B", "OFFICE"], ["AT", "D", "OFFICE"], ["AT", "P", "HOME"]]
a = plan(initial, goals)
a[0].display()
