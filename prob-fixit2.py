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
            ["JACKED", "?Y"],
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
            ["JACKED", "?Y"],
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
            ["JACKED", "?Y"],
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
            ["JACKED", "?Y"],
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
        precond=[":AND", ["HUB", "?X"], ["JACKED", "?X"]],
        add=[
            EFFECT(id=[], forall=[], precond=[], ranking=[], add=[["HAVE", "JACK"]]),
            EFFECT(
                id=[],
                forall=["?Y"],
                precond=["ON", "?Y", "?X"],
                ranking=[],
                add=[["ON", "?Y", "GROUND"]],
            ),
            EFFECT(
                id=[],
                forall=[],
                precond=[],
                ranking=[],
                add=[[":NOT", ["JACKED", "?X"]]],
            ),
        ],
        cache=[],
    ),
    P_STEP(
        id=[],
        action=["JACK-UP", "?Y"],
        parms=["?Y"],
        precond=[":AND", ["HUB", "?Y"], [":NOT", ["JACKED", "?Y"]], ["HAVE", "JACK"]],
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
                forall=["?X"],
                precond=["ON", "?X", "?Y"],
                ranking=[],
                add=[[":NOT", ["ON", "?X", "GROUND"]]],
            ),
            EFFECT(id=[], forall=[], precond=[], ranking=[], add=[["JACKED", "?Y"]]),
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
            [":NOT", ["JACKED", "?Y"]],
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
            [":NOT", ["JACKED", "?Y"]],
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
    "TOOL",
    "JACKED",
    "FREE",
    "IN",
    "HUB",
    "INTACT",
    "TIGHT",
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
    ["TOOL", "JACK"],
    ["TOOL", "PUMP"],
    ["TOOL", "WRENCH"],
    ["CONTAINER", "BOOT"],
    ["INTACT", "WHEEL2"],
    ["IN", "JACK", "BOOT"],
    ["IN", "PUMP", "BOOT"],
    ["IN", "WHEEL2", "BOOT"],
    ["IN", "WRENCH", "BOOT"],
    ["ON", "WHEEL1", "HUB"],
    ["ON", "WHEEL1", "GROUND"],
    ["TIGHT", "NUTS", "HUB"],
]
goals = [
    ":AND",
    [":NOT", ["OPEN", "BOOT"]],
    [":FORALL", ["TOOL", "?X"], ["IN", "?X", "BOOT"]],
    ["IN", "WHEEL1", "BOOT"],
    ["TIGHT", "NUTS", "HUB"],
    ["INFLATED", "WHEEL2"],
    ["ON", "WHEEL2", "HUB"],
]
a = plan(initial, goals)
a[0].display()
