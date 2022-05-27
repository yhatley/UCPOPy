from __future__ import annotations
import sys
from typing import Optional, Union
from copy import deepcopy

import ucpopy.structs as st
from ucpopy.variable import (
    bind_variable,
    unify,
    add_bind,
    uniquify_var,
    is_variable,
    instantiate_term,
    new_bindings,
)
from ucpopy.plan_utils import (
    canonical,
    convert_eqn,
    compile_goal,
    instantiate_step,
)
import ucpopy.globals as g
from ucpopy.interface import bestf_search


# -----------------------------------------


def plan(
    initial: st.CONDITION,
    goals: st.CONDITION,
    flaw_fun=None,
    rank_fun=None,
    search_fun=bestf_search,
) -> Optional[st.PLAN]:
    g.flaw_fun = flaw_fun or g.default_flaw_fun
    rank_fun = rank_fun or g.default_rank_fun
    a_plan = ucpop(initial, goals, rank_fun, search_fun)
    return a_plan


def ucpop(init: st.CONDITION, goal: st.CONDITION, rank_fun, search_fun=bestf_search) -> Optional[st.PLAN]:
    ini_plan = init_plan(init, goal)
    return search_fun(ini_plan, plan_refinements, plan_test, rank_fun, g.search_limit)


def init_plan(init: st.CONDITION, goal: st.CONDITION) -> st.PLAN:
    goal = convert_eqn(goal)
    goal = compile_goal(goal, [])
    g = instantiate_term(goal, ":GOAL")
    return tweak_plan(
        None,
        reason=[":INIT"],
        new_steps=[
            st.P_STEP(id=":GOAL", precond=g, action=[], parms=[], add=[]),
            st.P_STEP(
                id=0,
                add=[st.EFFECT(id=0, add=init)],
                action=[],
                parms=[],
                precond=[],
                cache=[],
            ),
        ],
        flaws=[],
        ordering=[],
        bindings=new_bindings(),
        high_step=0,
        add_goal=st.OPENC(rank=[], condition=canonical(g), id=":GOAL"),
    )


def plan_test(plan: st.PLAN) -> bool:
    return not plan.flaws


def plan_refinements(plan: st.PLAN) -> list[st.PLAN]:
    flaws = g.default_flaw_fun(plan)
    new_plans = g.new_plan_fun(plan, flaws)
    return new_plans


def get_flaw(plan: st.PLAN) -> list[st.FLAW]:
    if unsafe := get_unsafe(plan):
        return unsafe
    elif opened := get_open(plan):
        return opened
    elif forall := get_forall(plan):
        return forall
    return []


def new_plans(plan: st.PLAN, f: st.FLAW) -> list[st.PLAN]:
    if isinstance(f, st.FACT):
        return handle_fact(f, plan)
    elif isinstance(f, st.OPENC):
        return handle_open(f, plan)
    elif isinstance(f, st.UNSAFE):
        return handle_unsafe_or_violation(f, plan)
    elif isinstance(f, st.UNIV_THREAT):
        return handle_univ_threat(f, plan)
    else:
        return []


def rank(plan: st.PLAN) -> int:
    ret = len(plan.links)
    for f in plan.flaws:
        if isinstance(f, st.OPENC):
            ret += 1
    return ret


def rank3(plan: st.PLAN) -> int:
    return len(plan.steps) + len(plan.flaws)


# def rank4(plan: st.PLAN):
#     def num_openc(plan: st.PLAN):
#         n = 0
#         for c in plan.flaws:
#             if isinstance(c, st.OPENC):
#                 if c.condition[0] != ':EQ' and c.condition[0] != ':NEQ':
#                     n += 1
#         return n
#     return len(plan.steps) + num_openc(plan)


def get_forall(plan: st.PLAN) -> list[st.FORALL]:
    if not g.d_forall:
        return [flaw for flaw in plan.flaws if isinstance(flaw, st.UNIV_THREAT)]
    else:
        for f in plan.flaws:
            if isinstance(f, st.UNIV_THREAT):
                vars = [
                    x for x in bind_variable(f.term, plan.bindings) if is_variable(x)
                ]
                if not vars:
                    return f
        return []


def handle_univ_threat(f: st.UNIV_THREAT, plan: st.PLAN) -> list[st.PLAN]:
    forall = f.forall
    a = f.term
    univ = {}
    exis = {}
    binds = unify(forall.type, a, plan.bindings)

    if binds:
        for b in binds[0]:
            if b[0] in forall.vars:
                univ[b[0]] = b[1]
            else:
                exis[b[0]] = b[1]
        eqn = v_sublis(univ, forall.condition)
        if a[0] in g.dynamic_pred:
            eqn = [":OR", [":NOT", a], [":AND", a, eqn]]
        if exis:
            eqn = [
                ":OR",
                ([":AND"] + [[":EQ", b[0], b[1]] for b in exis.items()] + [eqn]),
            ] + [[":NEQ", b[0], b[1]] for b in exis.items()]
        p = tweak_plan(
            plan,
            reason=[":FORALL", f],
            flaws=[fl for fl in plan.flaws if fl != f],
            add_goal=st.OPENC(rank=[], condition=eqn, id=forall.id),
        )
        return [p]
    else:
        p = tweak_plan(
            plan, reason=[":BOGUS"], flaws=[fl for fl in plan.flaws if fl != f]
        )
        return [p]


def get_open(plan: st.PLAN) -> list[st.OPENC]:
    for open_cond in plan.flaws:
        if isinstance(open_cond, st.OPENC) and plan.high_step > open_cond.src_limit:
            return open_cond
        if isinstance(open_cond, st.FACT):
            open_cond.bindings = open_cond.function(
                *[
                    bind_variable(x, plan.bindings) for x in open_cond.condition[1]
                ]  # [1:] ??
            )
            if ":NO-MATCH-ATTEMPTED" != open_cond.bindings:
                return open_cond
            else:
                return []
    return []


def handle_open(open_cond: st.FLAW, plan: st.PLAN, **aux) -> list[st.PLAN]:
    if isinstance(open_cond, st.OPENC) and open_cond.condition[0] == ":OR":
        return handle_or(open_cond, plan)
    elif ret := use_axiom(open_cond, plan):
        return [ret]
    elif g.delay_link:
        if open_cond.src_limit < -1:
            return reuse_step(open_cond, plan) + delay_openc(open_cond, plan)
        else:
            return (
                reuse_step(open_cond, plan)
                + add_step(open_cond, plan)
                + delay_openc(open_cond, plan)
            )
    else:
        return add_step(open_cond, plan) + reuse_step(open_cond, plan)


def handle_fact(fact: st.FACT, plan: st.PLAN) -> list[st.PLAN]:
    ret = []
    for tmp in fact.bindings:
        p = tweak_plan(
            plan,
            reason=[":FACT", fact.condition],
            flaws=[f for f in plan.fawls if f != fact],
            add_goal=st.OPENC(
                rank=[],
                condition=[":AND"] + [[":EQ", x[0], x[1]] for x in tmp],
                id=":GOAL",
            ),
        )
        if p:
            ret.append(p)
    return ret


def handle_or(goal: st.OPENC, plan: st.PLAN) -> list[st.PLAN]:
    ret = []
    for gc in goal.condition[1:]:
        p = tweak_plan(
            plan,
            reason=[":GOAL", gc, goal.id],
            flaws=[f for f in plan.flaws if f != goal],
            add_goal=st.OPENC(rank=[], condition=gc, id=goal.id),
        )
        if p:
            ret.append(p)
    return ret


def delay_openc(open_cond: st.OPENC, plan: st.PLAN) -> list[st.PLAN]:
    if open_cond.condition[0] == ":NOT":
        member = open_cond.condition[1][0]
    else:
        member = open_cond.condition[0]

    if member not in g.dynamic_pred:
        return []
    new_openc = deepcopy(open_cond)
    new_openc.src_limit = plan.high_step
    return [
        tweak_plan(
            plan,
            reason=[":DELAY-LINK", open_cond.condition, open_cond.id],
            flaws=[new_openc] + [f for f in plan.flaws if f != open_cond],
        )
    ]


def add_step(open_cond: st.OPENC, plan: st.PLAN) -> list[st.LINK]:
    new_step_num = plan.high_step + 1
    ret = []
    for templ in get_opers(open_cond.condition):
        ret += new_link(open_cond, instantiate_step(templ, new_step_num), plan)
    return ret


def get_opers(condition, **aux) -> list[st.P_STEP]:
    def test_templ(templ: st.P_STEP):
        for e in templ.add:
            for a in e.add:
                if a[0] == condition[0] and (
                    a[0] != ":NOT" or a[1][0] == condition[1][0]
                ):
                    return True
        return False

    ret = []
    for templ in g.templates:
        if test_templ(templ):
            ret.insert(0, templ)
    return ret


def reuse_step(open_cond: st.OPENC, plan: st.PLAN) -> list[st.LINK]:
    id = open_cond.id
    ret = []
    for prior_step in possibly_prior(id, plan):
        if prior_step < open_cond.src_limit:
            continue
        other_steps = [s for s in plan.steps if s.id == prior_step]
        ret += new_link(open_cond, other_steps[0] if other_steps else [], plan)
    return ret


def use_axiom(goal: st.OPENC, plan: st.PLAN, **aux) -> Optional[st.PLAN]:
    condition = goal.condition
    c = condition[1] if condition[0] == ":NOT" else condition
    id = goal.id

    ret = False
    new_goal = []

    for a in g.axioms:
        binds = unify(a.add, c, plan.bindings)
        if binds:
            ret = True
            gl = peel_goal(binds[0], a)
            b = [[":EQ", e[0], e[1]] for e in peel_binds(binds[0], a)]
            if b:
                new_goal.insert(0, [":AND"] + b + [g])
            else:
                new_goal.insert(0, gl)
    if len(new_goal) > 1:
        new_goal.insert(0, ":OR")
    elif len(new_goal) == 1:
        new_goal = new_goal[0]

    if condition[0] == ":NOT":
        new_goal = canonical([":NOT", new_goal])
    if ret:
        return tweak_plan(
            plan,
            reason=[":GOAL", new_goal, id],
            flaws=[fl for fl in plan.flaws if fl != goal],
            add_goal=st.OPENC(rank=[], condition=new_goal, id=id),
        )
    else:
        return []


def new_link(open_cond: st.OPENC, step: st.P_STEP, plan: st.PLAN) -> list[st.LINK]:
    condition = open_cond.condition
    id = open_cond.id
    ret = []
    if step.id == 0 and condition[0] == ":NOT":
        ret += new_cw_link(open_cond, id, plan, step.add[0])
    for effect in step.add:
        if not g.side_effects or effect.ranking != ":SIDE":
            for add_cond in effect.add:
                ret += new_link_x(
                    open_cond, step, plan, effect, add_cond, condition, id
                )
    return ret


def new_link_x(
    open_cond: st.OPENC,
    step: st.P_STEP,
    plan: st.PLAN,
    effect: st.EFFECT,
    add_cond,
    condition,
    id: st.STEPID,
    **aux,
):
    b = unify(add_cond, condition, plan.bindings)
    if not b:
        return []
    goal = peel_goal(b[0], effect)
    if effect.id > plan.high_step:
        if goal:
            goal = [":AND", goal, step.precond]
        else:
            goal = step.precond
    b = peel_binds(b[0], effect)
    new_l = st.LINK(effect.id, condition, id, effect)
    p = tweak_plan(
        plan,
        reason=[
            (":STEP" if effect.id > plan.high_step else ":LINK"),
            effect.id,
            add_cond,
        ],
        flaws=[f for f in plan.flaws if f != open_cond],
        new_steps=[step] if effect.id > plan.high_step else [],
        new_link=new_l,
        ordering=(
            plan.ordering
            if id == ":GOAL" or effect.id == 0
            else [[effect.id, id]] + plan.ordering
        ),
        bindings=add_bind(b, plan.bindings),
        add_goal=st.OPENC(rank=[], condition=goal, id=effect.id) if goal else [],
        high_step=max(effect.id, plan.high_step),
    )
    if p:
        x = p.other.get(":NEW-BINDINGS", None)
        if x:
            p.other[":NEW-BINDINGS"] = b + p.other[":NEW-BINDINGS"]
        else:
            p.other[":NEW-BINDINGS"] = b
        if g.safety_p:
            for v in detect_violatioin(p, new_l, step):
                p.flaws.insert(0, v)
        return [p]
    else:
        return []


def new_cw_link(open_cond: st.OPENC, id: st.STEPID, plan: st.PLAN, effect: st.EFFECT):
    condition = open_cond.condition
    bind_goals = []

    for e in effect.add:
        b = unify(condition[1], e, plan.bindings)
        if b:
            b = b[0]
            if not b:
                return []
            if len(b) == 1:
                new = [":NEQ", b[0][0], b[0][1]]
            else:
                new = [":OR"] + [[":NEQ", bi[0], bi[1]] for bi in b]
            bind_goals.insert(0, new)
    p = tweak_plan(
        plan,
        reason=[":CW-ASSUMPTION"],
        flaws=[f for f in plan.flaws if f != open_cond],
        new_link=st.LINK(id1=0, condition=condition, id2=id, effect=[]),
        add_goal=(
            st.OPENC(condition=[":AND"] + bind_goals, id=effect.id, rank=[])
            if bind_goals
            else []
        ),
    )
    if p:
        return [p]
    else:
        return []


def affects(cond1, cond2, bindings):
    if g.positive_threats:
        return unify(
            cond1[1] if cond1[0] == ":NOT" else cond1,
            cond2[1] if cond2[0] == ":NOT" else cond2,
            bindings,
        )
    else:
        if cond1[0] == ":NOT":
            return [] if cond2[0] == ":NOT" else unify(cond1[1], cond2, bindings)
        elif cond2[0] == ":NOT":
            return unify(cond1, cond2[1], bindings)
        else:
            return []


def get_unsafe(plan: st.PLAN):
    if not g.d_sep:
        for f in plan.flaws:
            if isinstance(f, st.UNSAFE):
                return f
        return []
    else:
        for unsafe_ln in plan.flaws:
            if isinstance(unsafe_ln, st.UNSAFE):
                if unsafe_ln.clobber_effect.id not in possibly_between(
                    unsafe_ln.link.id1, unsafe_ln.link.id2, plan
                ):
                    return unsafe_ln
                binds = affects(
                    unsafe_ln.clobber_condition, unsafe_ln.link.condition, plan.bindings
                )
                if not binds or not peel_binds(binds[0], unsafe_ln.clobber_effect):
                    return unsafe_ln
        return []


def handle_unsafe_or_violation(unsafe_ln: st.UNSAFE, plan: st.PLAN):
    if not unsafe_ln.violation:
        return handle_unsafe(unsafe_ln, plan)
    # else:
        # return handle_violation(unsafe_ln, plan)


def handle_unsafe(unsafe_ln: st.UNSAFE, plan: st.PLAN, **aux) -> list[st.PLAN]:
    binds = affects(
        unsafe_ln.clobber_condition, unsafe_ln.link.condition, plan.bindings
    )
    if binds and unsafe_ln.clobber_effect.id in possibly_between(
        unsafe_ln.link.id1, unsafe_ln.link.id2, plan
    ):
        return (
            disable(unsafe_ln, binds[0], plan)
            + demote(unsafe_ln, plan)
            + promote(unsafe_ln, plan)
        )
    else:
        flaws = [f for f in plan.flaws if f != unsafe_ln]
        return [tweak_plan(plan, reason=[":BOGUS"], flaws=flaws)]


def disable(
    unsafe_ln: st.UNSAFE, binds: list[list[str]], plan: st.PLAN
) -> list[st.PLAN]:
    effect = unsafe_ln.clobber_effect
    if g.ord_constrain_on_confront:
        ord = []
        if unsafe_ln.link.id1 > 0:
            ord += [[unsafe_ln.link.id1, effect.id]]
        if isinstance(unsafe_ln.link.id2, int):
            ord += [[effect.id, unsafe_ln.link.id2]]
        ord += plan.ordering
    else:
        ord = plan.ordering

    b = [[":EQ", x[0], x[1]] for x in peel_binds(binds, effect)]
    if b:
        goal = [":AND"] + b + [peel_goal(binds, effect)]
    else:
        goal = peel_goal(binds, effect)
    p = tweak_plan(
        plan,
        reason=[":GOAL", [":NOT", goal], effect.id],
        ordering=ord,
        flaws=[f for f in plan.flaws if f != unsafe_ln],
        add_goal=st.OPENC(condition=canonical([":NOT", goal]), id=effect.id, rank=[]),
    )

    if g.d_sep and b:
        print(
            "Disable D-SEP and continue" "D-SEP does not appear to be working.\n",
            "Try evaluating (setq *d-sep* nil) before evaluating this query.",
            file=sys.stderr,
        )
        g.d_sep = False

    if p:
        return [p]
    else:
        return []


def demote(unsafe_ln: st.UNSAFE, plan: st.PLAN) -> list[st.PLAN]:
    clobber_id = unsafe_ln.clobber_effect.id
    id = unsafe_ln.link.id1
    demotable = clobber_id in possibly_prior(id, plan)
    if demotable:
        return [
            tweak_plan(
                plan,
                reason=[":ORDER", clobber_id, id],
                flaws=[f for f in plan.flaws if f != unsafe_ln],
                ordering=[[clobber_id, id]] + plan.ordering,
            )
        ]
    else:
        return []


def promote(unsafe_ln: st.UNSAFE, plan: st.PLAN) -> list[st.PLAN]:
    clobber_id = unsafe_ln.clobber_effect.id
    link = unsafe_ln.link
    id = link.id2
    promotable = id in possibly_prior(clobber_id, plan)
    if promotable:
        return [
            tweak_plan(
                plan,
                reason=[":ORDER", id, clobber_id],
                flaws=[f for f in plan.flaws if f != unsafe_ln],
                ordering=[[id, clobber_id]] + plan.ordering,
            )
        ]
    else:
        return []


def test_link(plan: st.PLAN, link: st.LINK) -> list[st.UNSAFE]:
    new_unsafe = []
    bind2 = plan.bindings
    between_ids = set(possibly_prior(link.id2, plan)).intersection(
        possibly_after(link.id1, plan)
    )
    for step in plan.steps:
        if step.id in between_ids:
            for effect in step.add:
                for add_cond in effect.add:
                    if affects(add_cond, link.condition, bind2):
                        new_unsafe.insert(
                            0, st.UNSAFE([], link, effect, add_cond, violation=[])
                        )
    return new_unsafe


def test_effects(plan: st.PLAN, effects: list[st.EFFECT], **aux) -> list[st.UNSAFE]:
    ret = []
    if not effects:
        return ret
    prior = possibly_prior(effects[0].id, plan)
    after = possibly_after(effects[0].id, plan)
    for ln in plan.links:
        if ln.id1 in prior and ln.id2 in after:
            for effect in effects:
                for c in effect.add:
                    if affects(c, ln.condition, plan.bindings):
                        unsafe = st.UNSAFE(
                            link=ln,
                            clobber_effect=effect,
                            clobber_condition=c,
                            rank=[],
                            violation=[],
                        )
                        ret.insert(0, unsafe)
    return ret


def possibly_between(s1: st.STEPID, s2: st.STEPID, plan: st.PLAN) -> list[int]:
    return list(set(possibly_after(s1, plan)) & set(possibly_prior(s2, plan)))


def possibly_prior(step_id: st.STEPID, plan: st.PLAN):
    """plan.stepのstep_idで示されるP_STEPよりも前に実行される可能性があるStepを返す"""
    if step_id == 0:
        return []
    after_of = ["bad"] * (plan.high_step + 1)
    poss_prior = []
    if isinstance(step_id, int):
        after_of[step_id] = []
    for s in plan.steps:
        if isinstance(s.id, int):
            after_of[s.id] = []
    if isinstance(step_id, int):
        for x, y in plan.ordering:
            after_of[x] = [y] + after_of[x]
        # step_idから後にあるP_STEPを削除（'after'というマークを入れておく）
        idx = 0
        c = [step_id]
        while c[idx:]:
            elem = c[idx]
            if isinstance(after_of[elem], list):
                c += after_of[elem]
                after_of[elem] = "after"
            idx += 1
    for n in range(1 + plan.high_step):
        if isinstance(after_of[0], list):
            poss_prior = [n] + poss_prior
        after_of.pop(0)
    return poss_prior


def possibly_after(step_id: st.STEPID, plan: st.PLAN):
    """plan.stepのstep_idで示されるP_STEPよりも後に実行される可能性があるStepを返す"""
    if step_id == ":GOAL":
        return []
    before_of = ["bad"] * (plan.high_step + 1)
    poss_after = [":GOAL"]
    for s in plan.steps:
        if isinstance(s.id, int):
            before_of[s.id] = []
    if 0 < step_id:
        for x, y in plan.ordering:
            before_of[y] = [x] + before_of[y]
        # step_idから後にあるP_STEPを削除（'before'というマークを入れておく）
        idx = 0
        c = [step_id]
        while c[idx:]:
            elem = c[idx]
            if isinstance(before_of[elem], list):
                c += before_of[elem]
                before_of[elem] = "before"
            idx += 1
    for n in range(1 + plan.high_step):
        if len(before_of) > 1 and isinstance(before_of[1], list):
            poss_after = [n + 1] + poss_after
        before_of.pop(0)
    return poss_after


def tweak_plan(
    plan: Optional[st.PLAN],
    reason: str,
    new_steps=[],
    new_link=[],
    flaws=":SAME",
    ordering=":SAME",
    bindings=":SAME",
    high_step=":SAME",
    add_goal: st.OPENC = [],
):
    if plan:
        new_plan = deepcopy(plan)
    else:
        new_plan = st.PLAN([], [], [], [], [], [], [], {})

    new_plan.other = {
        ":REASON": reason,
        ":NEW-GOAL": add_goal,
    }

    if flaws != ":SAME":
        new_plan.flaws = flaws
    if ordering != ":SAME":
        new_plan.ordering = ordering
    if bindings != ":SAME":
        new_plan.bindings = bindings
    if high_step != ":SAME":
        new_plan.high_step = high_step

    if add_goal and new_plan:
        new_plan = handle_goal(add_goal.condition, add_goal.id, new_plan)
    if new_plan:
        if new_link:
            new_plan.links.insert(0, new_link)
        for new_step in new_steps:
            new_plan.steps.insert(0, new_step)
        return new_unsafes(new_plan, new_link, new_steps)
    return []


def new_unsafes(plan: st.PLAN, new_link: Optional[st.LINK], new_steps: st.P_STEP):
    if new_link:
        for u in test_link(plan, new_link):
            plan.flaws.insert(0, u)
    for new_step in new_steps:
        if not test_step(new_step, plan):
            return []
    return plan


def test_step(new_step: st.P_STEP, plan1: st.PLAN):
    for u in test_effects(plan1, new_step.add):
        plan1.flaws.insert(0, u)
    for f in plan1.foralls:
        for e in new_step.add:
            for a in e.add:
                binds = unify(f.type, a, plan1.bindings)
                if binds:
                    ut = st.UNIV_THREAT(forall=f, term=a, step=new_step.id, rank=[])
                    plan1.flaws.insert(0, ut)
    return plan1


def handle_goal(eqn, id, plan: st.PLAN, **aux) -> Optional[st.PLAN]:
    def new_goal(n):
        if n == [":NOT", []]:
            raise
        if not n:
            return False
        for o in plan.flaws:
            if isinstance(o, st.OPENC) and o.id == id:
                if o.condition == n:
                    return False
                if is_negates(o.condition, n):
                    raise
        for ln in plan.links:
            if id == ln.id2:
                if ln.condition == n:
                    return False
                if is_negates(ln.condition, n):
                    raise
        return True

    bs = []

    def handle_goal_x(e) -> list[st.FLAW]:
        if e and e[0] == ":EQ":
            bs.insert(0, [e[1], e[2]])
            return []
        elif e and e[0] == ":NEQ":
            bs.insert(0, [":NOT", e[1], e[2]])
            return []
        elif e and e[0] == ":AND":
            return sum([handle_goal_x(ei) for ei in e[1:]], [])
        elif e and e[0] == ":FORALL":
            return handle_forall(e, id, plan)
        elif e and e[0] == ":EXISTS":
            return handle_goal_x(handle_exists(e))
        else:
            temp = [fact for fact in g.facts if fact[0] == e[0]]
            if temp:
                return [st.FACT(rank=[], condition=e, function=temp[0][1:])]
            elif new_goal(e):
                return [st.OPENC(rank=[], condition=e, id=id)]
            else:
                return []

    try:
        fs = handle_goal_x(eqn)
        plan.other[":NEW-BINDINGS"] = bs
        bs = add_bind(bs, plan.bindings)
        if bs:
            plan.bindings = bs
            plan.flaws = fs + plan.flaws
            return plan
        else:
            return []
    except:
        return []


def replace_in_tree(new, old, tree):
    """Replace tree element.  tree is implemented with list."""
    for idx, child in enumerate(tree):
        if isinstance(child, list):
            replace_in_tree(new, old, child)
        else:
            if child == old:
                tree[idx] = new


def peel_goal(binds: list[tuple[str, str]], effect: st.EFFECT):
    if effect.forall:
        ret = deepcopy(effect.precond)
        for b in binds:
            if b[0] in effect.forall:
                replace_in_tree(b[1], b[0], ret)
        return ret
    else:
        return effect.precond


def peel_binds(binds: list[tuple[str, str]], effect: st.EFFECT):
    ret = []
    for b in binds:
        if b[0] not in effect.forall:
            ret.append(b)
    return ret


def is_negates(n1: list, n2: list) -> bool:
    if n1[0] == ":NOT":
        p1 = n1
        p2 = n2
    else:
        p1 = n2
        p2 = n1

    return p1[0] == ":NOT" and p1[1] == p2


def handle_forall(goal, id: st.STEPID, plan: st.PLAN) -> list[st.UNIV_THREAT]:
    priors = possibly_prior(id, plan)
    ft = goal[2]
    forall = st.FORALL(id, goal[1], ft, goal[3])
    plan.foralls.insert(0, forall)

    ret = []
    for s in plan.steps:
        if s.id not in priors:
            continue
        for e in s.add:
            for a in e.add:
                binds = unify(ft, a, plan.bindings)
                if binds:
                    ret.append(
                        st.UNIV_THREAT(forall=forall, term=a, step=s.id, rank=[])
                    )
    return ret


def handle_exists(goal):
    alst = {x: uniquify_var(x) for x in goal[1]}
    return v_sublis(alst, [":AND", goal[2], goal[3]])


def v_sublis(alst: dict[st.VAR, str], e: Union[list, st.VAR, str]):
    if isinstance(e, list):
        return [v_sublis(alst, ei) for ei in e]
    elif is_variable(e):
        if isinstance(alst, dict):
            if e in alst:
                return alst[e]
            else:
                return e
        elif isinstance(alst, list):  # alist
            rep = [v for (k, v) in alst if k == e]
            if rep:
                return rep[0]
            else:
                return e
    else:
        return e


g.default_flaw_fun = get_flaw
g.default_rank_fun = rank3
g.new_plan_fun = new_plans


if __name__ == "__main__":
    from reader import CLLogReader, plist2dict

    lr = CLLogReader("log-{}/{}".format("mcd-sussman", "TWEAK-PLAN.log"))
    iioo = lr.in_outs()

    for i, ((args, globs), correct) in enumerate(iioo):
        args = plist2dict(args)
        globs = plist2dict(globs)

        # global variables
        if "*new_plan_fun*" in globs:
            del globs["*new_plan_fun*"]

        for key, value in globs.items():
            g.__dict__[key.replace("*", "")] = value

        if "not" in args:
            args["not_"] = args["not"]
            del args["not"]
        if "test" in args:
            from interface import cartest

            args["test"] = cartest
        if "search_fun" in args:
            del args["search_fun"]

        output = tweak_plan(**args)
        if output is None:
            output = []
        print(output)
        print(correct)
        if output != correct:
            print(i)
            import ipdb

            ipdb.set_trace()
            output = tweak_plan(**args)
