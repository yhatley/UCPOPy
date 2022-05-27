import ucpopy.globals as g
from ucpopy.structs import *
from ucpopy.ucpop import plan

g.templates = [
    P_STEP(
        id=[],
        action=["INFLATE", "?X"],
        parms=["?X"],
        precond=[
            ":AND",
            ["WHEEL", "?X"],
            ["HAVE", "PUMP"],
            [":NOT", ["INFLATED", "?X"]],
            ["INTACT", "?X"],
        ],
        add=[
            EFFECT(id=[], forall=[], precond=[], ranking=[], add=[["INFLATED", "?X"]])
        ],
        cache=[],
    ),
    P_STEP(
        id=[],
        action=["PUT-ON-WHEEL", "?X", "?Y"],
        parms=["?X", "?Y"],
        precond=[
            ":AND",
            ["WHEEL", "?X"],
            ["HUB", "?Y"],
            [":NEQ", "?X", "?Y"],
            ["HAVE", "?X"],
            ["FREE", "?Y"],
            ["UNFASTENED", "?Y"],
            [":NOT", ["ON-GROUND", "?Y"]],
        ],
        add=[
            EFFECT(
                id=[], forall=[], precond=[], ranking=[], add=[[":NOT", ["FREE", "?Y"]]]
            ),
            EFFECT(
                id=[], forall=[], precond=[], ranking=[], add=[[":NOT", ["HAVE", "?X"]]]
            ),
            EFFECT(id=[], forall=[], precond=[], ranking=[], add=[["ON", "?X", "?Y"]]),
        ],
        cache=[],
    ),
    P_STEP(
        id=[],
        action=["REMOVE-WHEEL", "?X", "?Y"],
        parms=["?X", "?Y"],
        precond=[
            ":AND",
            ["WHEEL", "?X"],
            ["HUB", "?Y"],
            [":NEQ", "?X", "?Y"],
            [":NOT", ["ON-GROUND", "?Y"]],
            ["ON", "?X", "?Y"],
            ["UNFASTENED", "?Y"],
        ],
        add=[
            EFFECT(
                id=[],
                forall=[],
                precond=[],
                ranking=[],
                add=[[":NOT", ["ON", "?X", "?Y"]]],
            ),
            EFFECT(id=[], forall=[], precond=[], ranking=[], add=[["FREE", "?Y"]]),
            EFFECT(id=[], forall=[], precond=[], ranking=[], add=[["HAVE", "?X"]]),
        ],
        cache=[],
    ),
    P_STEP(
        id=[],
        action=["DO-UP", "?X", "?Y"],
        parms=["?X", "?Y"],
        precond=[
            ":AND",
            ["NUT", "?X"],
            ["HUB", "?Y"],
            [":NEQ", "?X", "?Y"],
            ["HAVE", "WRENCH"],
            ["UNFASTENED", "?Y"],
            [":NOT", ["ON-GROUND", "?Y"]],
            ["HAVE", "?X"],
        ],
        add=[
            EFFECT(
                id=[], forall=[], precond=[], ranking=[], add=[[":NOT", ["HAVE", "?X"]]]
            ),
            EFFECT(
                id=[],
                forall=[],
                precond=[],
                ranking=[],
                add=[[":NOT", ["UNFASTENED", "?Y"]]],
            ),
            EFFECT(
                id=[], forall=[], precond=[], ranking=[], add=[["LOOSE", "?X", "?Y"]]
            ),
        ],
        cache=[],
    ),
    P_STEP(
        id=[],
        action=["UNDO", "?X", "?Y"],
        parms=["?X", "?Y"],
        precond=[
            ":AND",
            ["NUT", "?X"],
            ["HUB", "?Y"],
            [":NEQ", "?X", "?Y"],
            [":NOT", ["ON-GROUND", "?Y"]],
            [":NOT", ["UNFASTENED", "?Y"]],
            ["HAVE", "WRENCH"],
            ["LOOSE", "?X", "?Y"],
        ],
        add=[
            EFFECT(
                id=[],
                forall=[],
                precond=[],
                ranking=[],
                add=[[":NOT", ["LOOSE", "?X", "?Y"]]],
            ),
            EFFECT(
                id=[],
                forall=[],
                precond=[],
                ranking=[],
                add=[[":NOT", ["ON", "?X", "?Y"]]],
            ),
            EFFECT(
                id=[], forall=[], precond=[], ranking=[], add=[["UNFASTENED", "?Y"]]
            ),
            EFFECT(id=[], forall=[], precond=[], ranking=[], add=[["HAVE", "?X"]]),
        ],
        cache=[],
    ),
    P_STEP(
        id=[],
        action=["JACK-DOWN", "?X"],
        parms=["?X"],
        precond=[":AND", ["HUB", "?X"], [":NOT", ["ON-GROUND", "?X"]]],
        add=[
            EFFECT(id=[], forall=[], precond=[], ranking=[], add=[["HAVE", "JACK"]]),
            EFFECT(id=[], forall=[], precond=[], ranking=[], add=[["ON-GROUND", "?X"]]),
        ],
        cache=[],
    ),
    P_STEP(
        id=[],
        action=["JACK-UP", "?Y"],
        parms=["?Y"],
        precond=[":AND", ["HUB", "?Y"], ["ON-GROUND", "?Y"], ["HAVE", "JACK"]],
        add=[
            EFFECT(
                id=[],
                forall=[],
                precond=[],
                ranking=[],
                add=[[":NOT", ["HAVE", "JACK"]]],
            ),
            EFFECT(
                id=[],
                forall=[],
                precond=[],
                ranking=[],
                add=[[":NOT", ["ON-GROUND", "?Y"]]],
            ),
        ],
        cache=[],
    ),
    P_STEP(
        id=[],
        action=["TIGHTEN", "?X", "?Y"],
        parms=["?X", "?Y"],
        precond=[
            ":AND",
            ["NUT", "?X"],
            ["HUB", "?Y"],
            [":NEQ", "?X", "?Y"],
            ["HAVE", "WRENCH"],
            ["LOOSE", "?X", "?Y"],
            ["ON-GROUND", "?Y"],
        ],
        add=[
            EFFECT(
                id=[],
                forall=[],
                precond=[],
                ranking=[],
                add=[[":NOT", ["LOOSE", "?X", "?Y"]]],
            ),
            EFFECT(
                id=[], forall=[], precond=[], ranking=[], add=[["TIGHT", "?X", "?Y"]]
            ),
        ],
        cache=[],
    ),
    P_STEP(
        id=[],
        action=["LOOSEN", "?X", "?Y"],
        parms=["?X", "?Y"],
        precond=[
            ":AND",
            ["NUT", "?X"],
            ["HUB", "?Y"],
            [":NEQ", "?X", "?Y"],
            ["HAVE", "WRENCH"],
            ["TIGHT", "?X", "?Y"],
            ["ON-GROUND", "?Y"],
        ],
        add=[
            EFFECT(
                id=[],
                forall=[],
                precond=[],
                ranking=[],
                add=[[":NOT", ["TIGHT", "?X", "?Y"]]],
            ),
            EFFECT(
                id=[], forall=[], precond=[], ranking=[], add=[["LOOSE", "?X", "?Y"]]
            ),
        ],
        cache=[],
    ),
    P_STEP(
        id=[],
        action=["PUT-AWAY", "?X", "?Y"],
        parms=["?X", "?Y"],
        precond=[
            ":AND",
            ["CONTAINER", "?Y"],
            [":NEQ", "?X", "?Y"],
            ["HAVE", "?X"],
            ["OPEN", "?Y"],
        ],
        add=[
            EFFECT(
                id=[], forall=[], precond=[], ranking=[], add=[[":NOT", ["HAVE", "?X"]]]
            ),
            EFFECT(id=[], forall=[], precond=[], ranking=[], add=[["IN", "?X", "?Y"]]),
        ],
        cache=[],
    ),
    P_STEP(
        id=[],
        action=["FETCH", "?X", "?Y"],
        parms=["?X", "?Y"],
        precond=[
            ":AND",
            ["CONTAINER", "?Y"],
            [":NEQ", "?X", "?Y"],
            ["IN", "?X", "?Y"],
            ["OPEN", "?Y"],
        ],
        add=[
            EFFECT(
                id=[],
                forall=[],
                precond=[],
                ranking=[],
                add=[[":NOT", ["IN", "?X", "?Y"]]],
            ),
            EFFECT(id=[], forall=[], precond=[], ranking=[], add=[["HAVE", "?X"]]),
        ],
        cache=[],
    ),
    P_STEP(
        id=[],
        action=["CLOSE", "?X"],
        parms=["?X"],
        precond=[":AND", ["CONTAINER", "?X"], ["OPEN", "?X"]],
        add=[
            EFFECT(
                id=[], forall=[], precond=[], ranking=[], add=[[":NOT", ["OPEN", "?X"]]]
            )
        ],
        cache=[],
    ),
    P_STEP(
        id=[],
        action=["OPEN", "?X"],
        parms=["?X"],
        precond=[
            ":AND",
            ["CONTAINER", "?X"],
            [":NOT", ["LOCKED", "?X"]],
            [":NOT", ["OPEN", "?X"]],
        ],
        add=[EFFECT(id=[], forall=[], precond=[], ranking=[], add=[["OPEN", "?X"]])],
        cache=[],
    ),
    P_STEP(
        id=[],
        action=["CUSS"],
        parms=[],
        precond=[],
        add=[
            EFFECT(
                id=[], forall=[], precond=[], ranking=[], add=[[":NOT", ["ANNOYED"]]]
            )
        ],
        cache=[],
    ),
]
g.axioms = []
g.dynamic_pred = [
    "OPEN",
    "HAVE",
    "ON",
    "NUT",
    "LOOSE",
    "TIGHT",
    "FREE",
    "IN",
    "HUB",
    "INTACT",
    "ON-GROUND",
    "CONTAINER",
    "WHEEL",
    "LOCKED",
    "UNFASTENED",
    "INFLATED",
    "ANNOYED",
]
initial = [
    ["WHEEL", "WHEEL1"],
    ["WHEEL", "WHEEL2"],
    ["HUB", "HUB"],
    ["NUT", "NUTS"],
    ["CONTAINER", "BOOT"],
    ["INTACT", "WHEEL2"],
    ["HAVE", "JACK"],
    ["HAVE", "PUMP"],
    ["HAVE", "WHEEL1"],
    ["HAVE", "WRENCH"],
    ["OPEN", "BOOT"],
    ["INFLATED", "WHEEL2"],
    ["ON", "WHEEL2", "HUB"],
    ["TIGHT", "NUTS", "HUB"],
    ["ON-GROUND", "HUB"],
]
goals = [
    ":AND",
    ["IN", "JACK", "BOOT"],
    ["IN", "PUMP", "BOOT"],
    ["IN", "WHEEL1", "BOOT"],
    ["IN", "WRENCH", "BOOT"],
    ["INFLATED", "WHEEL2"],
    ["ON", "WHEEL2", "HUB"],
    ["TIGHT", "NUTS", "HUB"],
]
a = plan(initial, goals)
a[0].display()
