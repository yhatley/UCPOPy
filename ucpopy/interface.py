from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, Any
import ucpopy.structs as st
from ucpopy.plan_utils import merge


@dataclass
class Domain:
    name: str
    operators: Any
    axioms: Any
    facts: Any
    safety: Any


@dataclass
class Problem:
    name: str
    domain: Domain
    inits: Any
    goal: Any
    rank_fun: Any
    flaw_fun: Any


def cartest(x, y):
    return x[0] < y[0]


def bestf_search(initial_state, daughters_fn, goal_p, rank_fn, limit) -> Optional[st.PLAN]:
    branches = []
    search_queue = [[0, initial_state]]
    while search_queue:
        if not search_queue:
            current_state = []
        else:
            current_state = search_queue.pop(0)[1]

        if not current_state or goal_p(current_state) or limit < 0:
            return current_state, (0 if not branches else sum(branches) / len(branches))
        children = [[rank_fn(c), c] for c in daughters_fn(current_state)]
        num_children = len(children)
        branches.insert(0, num_children)
        limit -= num_children
        search_queue = merge(search_queue, sorted(children), cartest)
