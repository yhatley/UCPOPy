import ucpopy.globals as g
from ucpopy.structs import *
from ucpopy.ucpop import plan

g.templates = [
    P_STEP(
        id=[],
        action=["PUTON", "?X", "?Y", "?D"],
        parms=["?X", "?Y", "?D"],
        precond=[
            ":AND",
            [":NEQ", "?X", "?Y"],
            [":NEQ", "?X", "TABLE"],
            [":NEQ", "?D", "?Y"],
            ["ON", "?X", "?D"],
            [
                ":OR",
                [":EQ", "?X", "TABLE"],
                [":FORALL", ["?B"], ["BLOCK", "?B"], [":NOT", ["ON", "?B", "?X"]]],
            ],
            [
                ":OR",
                [":EQ", "?Y", "TABLE"],
                [":FORALL", ["?B"], ["BLOCK", "?B"], [":NOT", ["ON", "?B", "?Y"]]],
            ],
        ],
        add=[
            EFFECT(
                id=[],
                forall=["?E"],
                precond=[
                    ":AND",
                    ["ABOVE", "?X", "?E"],
                    [":NEQ", "?Y", "?E"],
                    [":NOT", ["ABOVE", "?Y", "?E"]],
                ],
                ranking=[],
                add=[[":NOT", ["ABOVE", "?X", "?E"]]],
            ),
            EFFECT(
                id=[],
                forall=["?C"],
                precond=[":OR", [":EQ", "?Y", "?C"], ["ABOVE", "?Y", "?C"]],
                ranking=[],
                add=[["ABOVE", "?X", "?C"]],
            ),
            EFFECT(
                id=[],
                forall=[],
                precond=[],
                ranking=[],
                add=[[":NOT", ["ON", "?X", "?D"]]],
            ),
            EFFECT(id=[], forall=[], precond=[], ranking=[], add=[["ON", "?X", "?Y"]]),
        ],
        cache=[],
    )
]
g.axioms = []
g.dynamic_pred = ["ABOVE", "ON", "BLOCK"]
initial = [
    ["BLOCK", "A"],
    ["BLOCK", "B"],
    ["BLOCK", "C"],
    ["BLOCK", "TABLE"],
    ["ON", "C", "A"],
    ["ON", "B", "TABLE"],
    ["ON", "A", "TABLE"],
]
goals = [":AND", ["ON", "B", "C"], ["ON", "A", "B"]]
a = plan(initial, goals)
a[0].display()
