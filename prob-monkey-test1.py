import ucpopy.globals as g
from ucpopy.structs import *
from ucpopy.ucpop import plan

g.templates = [
    P_STEP(
        id=[],
        action=["GETWATER", "?Y"],
        parms=["?Y"],
        precond=[
            ":AND",
            ["HASGLASS"],
            ["AT", "WATERFOUNTAIN", "?Y"],
            ["AT", "MONKEY", "?Y"],
            ["ONBOX", "?Y"],
        ],
        add=[EFFECT(id=[], forall=[], precond=[], ranking=[], add=[["HASWATER"]])],
        cache=[],
    ),
    P_STEP(
        id=[],
        action=["PICKGLASS", "?Y"],
        parms=["?Y"],
        precond=[":AND", ["AT", "GLASS", "?Y"], ["AT", "MONKEY", "?Y"]],
        add=[
            EFFECT(
                id=[],
                forall=[],
                precond=[],
                ranking=[],
                add=[[":NOT", ["AT", "GLASS", "?Y"]]],
            ),
            EFFECT(id=[], forall=[], precond=[], ranking=[], add=[["HASGLASS"]]),
        ],
        cache=[],
    ),
    P_STEP(
        id=[],
        action=["GRAB-BANANAS", "?Y"],
        parms=["?Y"],
        precond=[":AND", ["HASKNIFE"], ["AT", "BANANAS", "?Y"], ["ONBOX", "?Y"]],
        add=[EFFECT(id=[], forall=[], precond=[], ranking=[], add=[["HASBANANAS"]])],
        cache=[],
    ),
    P_STEP(
        id=[],
        action=["GET-KNIFE", "?Y"],
        parms=["?Y"],
        precond=[":AND", ["AT", "KNIFE", "?Y"], ["AT", "MONKEY", "?Y"]],
        add=[
            EFFECT(
                id=[],
                forall=[],
                precond=[],
                ranking=[],
                add=[[":NOT", ["AT", "KNIFE", "?Y"]]],
            ),
            EFFECT(id=[], forall=[], precond=[], ranking=[], add=[["HASKNIFE"]]),
        ],
        cache=[],
    ),
    P_STEP(
        id=[],
        action=["PUSH-BOX", "?X", "?Y"],
        parms=["?X", "?Y"],
        precond=[
            ":AND",
            [":NEQ", "?Y", "?X"],
            ["AT", "BOX", "?Y"],
            ["AT", "MONKEY", "?Y"],
            ["ON-FLOOR"],
        ],
        add=[
            EFFECT(
                id=[],
                forall=[],
                precond=[],
                ranking=[],
                add=[[":NOT", ["AT", "BOX", "?Y"]]],
            ),
            EFFECT(id=[], forall=[], precond=[], ranking=[], add=[["AT", "BOX", "?X"]]),
            EFFECT(
                id=[],
                forall=[],
                precond=[],
                ranking=[],
                add=[[":NOT", ["AT", "MONKEY", "?Y"]]],
            ),
            EFFECT(
                id=[], forall=[], precond=[], ranking=[], add=[["AT", "MONKEY", "?X"]]
            ),
        ],
        cache=[],
    ),
    P_STEP(
        id=[],
        action=["CLIMB", "?X"],
        parms=["?X"],
        precond=[":AND", ["AT", "BOX", "?X"], ["AT", "MONKEY", "?X"]],
        add=[
            EFFECT(
                id=[], forall=[], precond=[], ranking=[], add=[[":NOT", ["ON-FLOOR"]]]
            ),
            EFFECT(id=[], forall=[], precond=[], ranking=[], add=[["ONBOX", "?X"]]),
        ],
        cache=[],
    ),
    P_STEP(
        id=[],
        action=["GO-TO", "?X", "?Y"],
        parms=["?X", "?Y"],
        precond=[":AND", [":NEQ", "?Y", "?X"], ["ON-FLOOR"], ["AT", "MONKEY", "?Y"]],
        add=[
            EFFECT(
                id=[],
                forall=[],
                precond=[],
                ranking=[],
                add=[[":NOT", ["AT", "MONKEY", "?Y"]]],
            ),
            EFFECT(
                id=[], forall=[], precond=[], ranking=[], add=[["AT", "MONKEY", "?X"]]
            ),
        ],
        cache=[],
    ),
]
g.axioms = []
g.dynamic_pred = [
    "LOCATION",
    "HASBANANAS",
    "HASKNIFE",
    "AT",
    "HASGLASS",
    "ONBOX",
    "HASWATER",
    "ON-FLOOR",
]
initial = [
    ["LOCATION", "P1"],
    ["LOCATION", "P2"],
    ["LOCATION", "P3"],
    ["LOCATION", "P4"],
    ["AT", "MONKEY", "P1"],
    ["ON-FLOOR"],
    ["AT", "BOX", "P2"],
    ["AT", "BANANAS", "P3"],
    ["AT", "KNIFE", "P4"],
]
goals = ["HASBANANAS"]
a = plan(initial, goals)
a[0].display()
