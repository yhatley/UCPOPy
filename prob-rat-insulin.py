import ucpopy.globals as g
from ucpopy.structs import *
from ucpopy.ucpop import plan

g.templates = [
    P_STEP(
        id=[],
        action=["SCREEN", "?X", "?Y", "?Z"],
        parms=["?X", "?Y", "?Z"],
        precond=[
            ":AND",
            ["BACTERIUM", "?X"],
            ["ANTIBIOTIC", "?Z"],
            [":NEQ", "?X", "?Y"],
            [":NEQ", "?Y", "?Z"],
            [":NEQ", "?X", "?Z"],
            ["RESISTS", "?Z", "?Y"],
            ["CONTAINS", "?Y", "?X"],
        ],
        add=[EFFECT(id=[], forall=[], precond=[], ranking=[], add=[["PURE", "?X"]])],
        cache=[],
    ),
    P_STEP(
        id=[],
        action=["TRANSFORM", "?X", "?Y"],
        parms=["?X", "?Y"],
        precond=[
            ":AND",
            ["BACTERIUM", "?Y"],
            [":NEQ", "?X", "?Y"],
            ["CLEAVABLE", "?X"],
            ["ACCEPTS", "?X", "?Y"],
        ],
        add=[
            EFFECT(
                id=[],
                forall=[],
                precond=[],
                ranking=[],
                add=[[":NOT", ["CLEAVABLE", "?X"]]],
            ),
            EFFECT(
                id=[], forall=[], precond=[], ranking=[], add=[["CONTAINS", "?X", "?Y"]]
            ),
        ],
        cache=[],
    ),
    P_STEP(
        id=[],
        action=["CLEAVE", "?X"],
        parms=["?X"],
        precond=["CLEAVABLE", "?X"],
        add=[
            EFFECT(
                id=[],
                forall=[],
                precond=[],
                ranking=[],
                add=[[":NOT", ["CLEAVABLE", "?X"]]],
            ),
            EFFECT(id=[], forall=[], precond=[], ranking=[], add=[["CLEAVED", "?X"]]),
        ],
        cache=[],
    ),
    P_STEP(
        id=[],
        action=["LIGATE", "?X", "?Y"],
        parms=["?X", "?Y"],
        precond=[":NEQ", "?X", "?Y"],
        add=[
            EFFECT(
                id=[],
                forall=[],
                precond=[
                    ":AND",
                    ["CLEAVED", "?X"],
                    ["CLEAVED", "?Y"],
                    [":NEQ", "?X", "LINKER"],
                ],
                ranking=[],
                add=[[":NOT", ["CLEAVED", "?Y"]]],
            ),
            EFFECT(
                id=[],
                forall=[],
                precond=[
                    ":AND",
                    ["CLEAVED", "?X"],
                    ["CLEAVED", "?Y"],
                    [":NEQ", "?X", "LINKER"],
                ],
                ranking=[],
                add=[[":NOT", ["CLEAVED", "?X"]]],
            ),
            EFFECT(
                id=[],
                forall=[],
                precond=[
                    ":AND",
                    ["CLEAVED", "?X"],
                    ["CLEAVED", "?Y"],
                    [":NEQ", "?X", "LINKER"],
                ],
                ranking=[],
                add=[["CLEAVABLE", "?Y"]],
            ),
            EFFECT(
                id=[],
                forall=[],
                precond=[
                    ":AND",
                    ["CLEAVED", "?X"],
                    ["CLEAVED", "?Y"],
                    [":NEQ", "?X", "LINKER"],
                ],
                ranking=[],
                add=[["CONTAINS", "?X", "?Y"]],
            ),
            EFFECT(
                id=[],
                forall=[],
                precond=[":AND", ["DOUBLE-STRAND", "?Y"], [":EQ", "?X", "LINKER"]],
                ranking=[],
                add=[["CLEAVABLE", "?Y"]],
            ),
        ],
        cache=[],
    ),
    P_STEP(
        id=[],
        action=["DIGEST", "?X"],
        parms=["?X"],
        precond=["HAIR-PIN", "?X"],
        add=[
            EFFECT(
                id=[],
                forall=[],
                precond=[],
                ranking=[],
                add=[[":NOT", ["HAIR-PIN", "?X"]]],
            ),
            EFFECT(
                id=[], forall=[], precond=[], ranking=[], add=[["DOUBLE-STRAND", "?X"]]
            ),
        ],
        cache=[],
    ),
    P_STEP(
        id=[],
        action=["POLYMERIZE", "?X"],
        parms=["?X"],
        precond=["SINGLE-STRAND", "?X"],
        add=[
            EFFECT(
                id=[],
                forall=[],
                precond=[],
                ranking=[],
                add=[[":NOT", ["SINGLE-STRAND", "?X"]]],
            ),
            EFFECT(id=[], forall=[], precond=[], ranking=[], add=[["HAIR-PIN", "?X"]]),
        ],
        cache=[],
    ),
    P_STEP(
        id=[],
        action=["SEPARATE", "?X"],
        parms=["?X"],
        precond=["CONNECTED-CDNA-MRNA", "?X"],
        add=[
            EFFECT(
                id=[],
                forall=[],
                precond=[],
                ranking=[],
                add=[[":NOT", ["CONNECTED-CDNA-MRNA", "?X"]]],
            ),
            EFFECT(
                id=[], forall=[], precond=[], ranking=[], add=[["SINGLE-STRAND", "?X"]]
            ),
        ],
        cache=[],
    ),
    P_STEP(
        id=[],
        action=["REVERSE-TRANSCRIBE", "?X"],
        parms=["?X"],
        precond=["MRNA", "?X"],
        add=[
            EFFECT(
                id=[],
                forall=[],
                precond=[],
                ranking=[],
                add=[["CONNECTED-CDNA-MRNA", "?X"]],
            )
        ],
        cache=[],
    ),
]
g.axioms = []
g.dynamic_pred = [
    "RESISTS",
    "MOLECULE",
    "MRNA",
    "HAIR-PIN",
    "CLEAVED",
    "DOUBLE-STRAND",
    "BACTERIUM",
    "PURE",
    "CONNECTED-CDNA-MRNA",
    "ACCEPTS",
    "SINGLE-STRAND",
    "CONTAINS",
    "CLEAVABLE",
    "ANTIBIOTIC",
]
initial = [
    ["MOLECULE", "INSULIN-GENE"],
    ["MOLECULE", "E-COLI-EXOSOME"],
    ["MOLECULE", "JUNK-EXOSOME"],
    ["MOLECULE", "LINKER"],
    ["BACTERIUM", "E-COLI"],
    ["BACTERIUM", "JUNK"],
    ["ANTIBIOTIC", "ANTIBIOTIC-1"],
    ["MRNA", "INSULIN-GENE"],
    ["CLEAVABLE", "E-COLI-EXOSOME"],
    ["CLEAVABLE", "JUNK-EXOSOME"],
    ["ACCEPTS", "JUNK-EXOSOME", "JUNK"],
    ["ACCEPTS", "E-COLI-EXOSOME", "E-COLI"],
    ["RESISTS", "ANTIBIOTIC-1", "E-COLI-EXOSOME"],
]
goals = [
    ":EXISTS",
    ["BACTERIUM", "?Y"],
    [
        ":EXISTS",
        ["MOLECULE", "?X"],
        [
            ":AND",
            ["CONTAINS", "INSULIN-GENE", "?X"],
            ["CONTAINS", "?X", "?Y"],
            ["PURE", "?Y"],
        ],
    ],
]
a = plan(initial, goals)
a[0].display()
