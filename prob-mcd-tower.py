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
            ["CLEAR", "?X"],
            ["CLEAR", "?Y"],
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
g.axioms = [
    EFFECT(
        id="IS-CLEAR",
        forall=["?X"],
        precond=[
            ":OR",
            [":EQ", "?X", "TABLE"],
            [":FORALL", ["?B"], ["ON", "?B", "?X"], [":NOT", []]],
        ],
        ranking=[],
        add=["CLEAR", "?X"],
    )
]
g.dynamic_pred = ["ABOVE", "ON", "CLEAR", "BLOCK"]
initial = [
    ["BLOCK", "A"],
    ["BLOCK", "B"],
    ["BLOCK", "C"],
    ["BLOCK", "TABLE"],
    ["CLEAR", "A"],
    ["ON", "A", "B"],
    ["ON", "B", "C"],
    ["ON", "C", "TABLE"],
    ["CLEAR", "TABLE"],
]
goals = [":AND", ["ON", "B", "C"], ["ON", "C", "A"]]
a = plan(initial, goals)
a[0].display()
