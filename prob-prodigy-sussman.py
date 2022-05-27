import ucpopy.globals as g
from ucpopy.structs import *
from ucpopy.ucpop import plan

g.templates = [
    P_STEP(
        id=[],
        action=["UNSTACK", "?SOB", "?SUNDEROB"],
        parms=["?SOB", "?SUNDEROB"],
        precond=[
            ":AND",
            ["OBJECT", "?SOB"],
            ["OBJECT", "?SUNDEROB"],
            ["ON", "?SOB", "?SUNDEROB"],
            ["CLEAR", "?SOB"],
            ["ARM-EMPTY"],
        ],
        add=[
            EFFECT(
                id=[],
                forall=[],
                precond=[],
                ranking=[],
                add=[[":NOT", ["ON", "?SOB", "?SUNDEROB"]]],
            ),
            EFFECT(
                id=[], forall=[], precond=[], ranking=[], add=[[":NOT", ["ARM-EMPTY"]]]
            ),
            EFFECT(
                id=[],
                forall=[],
                precond=[],
                ranking=[],
                add=[[":NOT", ["CLEAR", "?SOB"]]],
            ),
            EFFECT(
                id=[], forall=[], precond=[], ranking=[], add=[["CLEAR", "?SUNDEROB"]]
            ),
            EFFECT(id=[], forall=[], precond=[], ranking=[], add=[["HOLDING", "?SOB"]]),
        ],
        cache=[],
    ),
    P_STEP(
        id=[],
        action=["STACK", "?SOB", "?SUNDEROB"],
        parms=["?SOB", "?SUNDEROB"],
        precond=[
            ":AND",
            ["OBJECT", "?SOB"],
            ["OBJECT", "?SUNDEROB"],
            ["HOLDING", "?SOB"],
            ["CLEAR", "?SUNDEROB"],
        ],
        add=[
            EFFECT(
                id=[],
                forall=[],
                precond=[],
                ranking=[],
                add=[["ON", "?SOB", "?SUNDEROB"]],
            ),
            EFFECT(id=[], forall=[], precond=[], ranking=[], add=[["ARM-EMPTY"]]),
            EFFECT(id=[], forall=[], precond=[], ranking=[], add=[["CLEAR", "?SOB"]]),
            EFFECT(
                id=[],
                forall=[],
                precond=[],
                ranking=[],
                add=[[":NOT", ["CLEAR", "?SUNDEROB"]]],
            ),
            EFFECT(
                id=[],
                forall=[],
                precond=[],
                ranking=[],
                add=[[":NOT", ["HOLDING", "?SOB"]]],
            ),
        ],
        cache=[],
    ),
    P_STEP(
        id=[],
        action=["PUT-DOWN", "?OB"],
        parms=["?OB"],
        precond=[":AND", ["OBJECT", "?OB"], ["HOLDING", "?OB"]],
        add=[
            EFFECT(id=[], forall=[], precond=[], ranking=[], add=[["ON-TABLE", "?OB"]]),
            EFFECT(id=[], forall=[], precond=[], ranking=[], add=[["ARM-EMPTY"]]),
            EFFECT(id=[], forall=[], precond=[], ranking=[], add=[["CLEAR", "?OB"]]),
            EFFECT(
                id=[],
                forall=[],
                precond=[],
                ranking=[],
                add=[[":NOT", ["HOLDING", "?OB"]]],
            ),
        ],
        cache=[],
    ),
    P_STEP(
        id=[],
        action=["PICK-UP", "?OB1"],
        parms=["?OB1"],
        precond=[
            ":AND",
            ["OBJECT", "?OB1"],
            ["CLEAR", "?OB1"],
            ["ON-TABLE", "?OB1"],
            ["ARM-EMPTY"],
        ],
        add=[
            EFFECT(id=[], forall=[], precond=[], ranking=[], add=[["HOLDING", "?OB1"]]),
            EFFECT(
                id=[], forall=[], precond=[], ranking=[], add=[[":NOT", ["ARM-EMPTY"]]]
            ),
            EFFECT(
                id=[],
                forall=[],
                precond=[],
                ranking=[],
                add=[[":NOT", ["CLEAR", "?OB1"]]],
            ),
            EFFECT(
                id=[],
                forall=[],
                precond=[],
                ranking=[],
                add=[[":NOT", ["ON-TABLE", "?OB1"]]],
            ),
        ],
        cache=[],
    ),
]
g.axioms = []
g.dynamic_pred = ["ON-TABLE", "ON", "CLEAR", "HOLDING", "OBJECT", "ARM-EMPTY"]
initial = [
    ["OBJECT", "A"],
    ["OBJECT", "B"],
    ["OBJECT", "C"],
    ["ON-TABLE", "A"],
    ["ON-TABLE", "B"],
    ["ON", "C", "A"],
    ["CLEAR", "B"],
    ["CLEAR", "C"],
    ["ARM-EMPTY"],
]
goals = [":AND", ["ON", "A", "B"], ["ON", "B", "C"]]
a = plan(initial, goals)
a[0].display()
