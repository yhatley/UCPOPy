import ucpopy.globals as g
from ucpopy.structs import *
from ucpopy.ucpop import plan

g.templates = [
    P_STEP(
        id=[],
        action=["TURN-FAUCET", "?HOW"],
        parms=["?HOW"],
        precond=[],
        add=[
            EFFECT(
                id=[],
                forall=[],
                precond=[":AND", [":EQ", "?HOW", "ON"], [":NOT", ["GOOD-PLUMBING"]]],
                ranking=[],
                add=[["HOLEY-WALLS"]],
            ),
            EFFECT(
                id=[],
                forall=["?S"],
                precond=[":AND", [":NEQ", "?S", "?HOW"], ["WATER", "?S"]],
                ranking=[],
                add=[[":NOT", ["WATER", "?S"]]],
            ),
            EFFECT(id=[], forall=[], precond=[], ranking=[], add=[["WATER", "?HOW"]]),
        ],
        cache=[],
    ),
    P_STEP(
        id=[],
        action=["FIX", "?IT"],
        parms=["?IT"],
        precond=["OBJECT", "?IT"],
        add=[
            EFFECT(
                id=[],
                forall=[],
                precond=[":AND", [":EQ", "?IT", "PLUMBING"], ["WATER", "OFF"]],
                ranking=[],
                add=[["GOOD-PLUMBING"]],
            ),
            EFFECT(
                id=[],
                forall=[],
                precond=[
                    ":AND",
                    [":EQ", "?IT", "WALL"],
                    [":NOT", ["GOOD-PLUMBING"]],
                    ["WATER", "OFF"],
                ],
                ranking=[],
                add=[[":NOT", ["HOLEY-WALLS"]]],
            ),
            EFFECT(
                id=[],
                forall=[],
                precond=[":AND", [":EQ", "?IT", "WALL"], ["GOOD-PLUMBING"]],
                ranking=[],
                add=[[":NOT", ["HOLEY-WALLS"]]],
            ),
        ],
        cache=[],
    ),
]
g.axioms = []
g.dynamic_pred = ["HOLEY-WALLS", "GOOD-PLUMBING", "WATER", "OBJECT"]
initial = [["OBJECT", "WALL"], ["OBJECT", "PLUMBING"], ["HOLEY-WALLS"], ["WATER", "ON"]]
goals = [":AND", ["WATER", "ON"], [":NOT", ["HOLEY-WALLS"]]]
a = plan(initial, goals)
a[0].display()
