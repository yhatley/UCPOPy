from __future__ import annotations
from typing import Union
import ucpopy.structs as st
from ucpopy.variable import instantiate_term, is_variable
import ucpopy.globals as g


def instantiate_step(step: st.P_STEP, num):
    def instantiate_effect(e):
        return st.EFFECT(
            id=num,
            forall=instantiate_term(e.forall, num),
            precond=instantiate_term(e.precond, num),
            add=instantiate_term(e.add, num),
        )

    s = [c for c in step.cache if c.id == num]
    if s:
        return s[0]
    else:
        new_step = st.P_STEP(
            id=num,
            action=instantiate_term(step.action, num),
            precond=instantiate_term(step.precond, num),
            add=[instantiate_effect(a) for a in step.add],
            parms=[],
        )
        step.cache.insert(0, new_step)
        return new_step


def convert_eqn(eqn: Union[list, str]):
    mapping = {
        "WHEN": ":WHEN",
        "AND": ":AND",
        "OR": ":OR",
        "NOT": ":NOT",
        "IMPLY": ":IMPLY",
        "EXISTS": ":EXISTS",
        "FORALL": ":FORALL",
        "EQ": ":EQ",
        "NEQ": ":NEQ",
    }
    if isinstance(eqn, list):
        for idx, elem in enumerate(eqn):
            eqn[idx] = convert_eqn(elem)
        return eqn
    elif isinstance(eqn, str):
        return mapping.get(eqn, eqn)


def canonical(eqn: Union[list, str], not_=False):
    if not eqn:
        if not_:
            return [":NOT", eqn]
        else:
            return eqn
    elif eqn[0] == ":NOT":
        return canonical(eqn[1], not not_)
    elif eqn[0] == ":OR":
        if not_:
            return [":AND"] + [canonical(e, not_) for e in eqn[1:]]
        else:
            return [":OR"] + [canonical(e, not_) for e in eqn[1:]]
    elif eqn[0] == ":AND":
        if not_:
            return [":OR"] + [canonical(e, not_) for e in eqn[1:]]
        else:
            return [":AND"] + [canonical(e, not_) for e in eqn[1:]]
    elif eqn[0] == ":FORALL":
        if not_:
            return [":EXISTS", eqn[1], eqn[2], canonical(eqn[3], not_)]
        else:
            return [":FORALL", eqn[1], eqn[2], canonical(eqn[3], not_)]
    elif eqn[0] == ":EXISTS":
        if not_:
            return [":FORALL", eqn[1], eqn[2], canonical(eqn[3], not_)]
        else:
            return [":EXISTS", eqn[1], eqn[2], canonical(eqn[3], not_)]
    elif eqn[0] == ":EQ":
        if not_:
            return [":NEQ"] + eqn[1:]
        else:
            return [":EQ"] + eqn[1:]
    elif eqn[0] == ":NEQ":
        if not_:
            return [":EQ"] + eqn[1:]
        else:
            return [":NEQ"] + eqn[1:]
    else:
        if not_:
            return [":NOT", eqn]
        else:
            return eqn


def compile_goal(eqn, vars):
    if eqn[0] == ":IMPLY":
        assert len(eqn) == 3
        return compile_goal([":OR", [":NOT", eqn[1]], eqn[2]])
    elif eqn[0] in (":AND", ":OR"):
        return [eqn[0]] + [compile_goal(e, vars) for e in eqn[1:]]
    elif eqn[0] == ":NOT":
        assert len(eqn) == 2
        return [":NOT", compile_goal(eqn[1], vars)]
    elif eqn[0] in (":EXISTS", ":FORALL"):
        vs = []
        # eqn = [":EXISTS" [TYPE "?X" "?Y"]  EXPRESSIONS...]
        for v in eqn[1][1:]:
            if is_variable(v) and v not in vars:
                vars.insert(0, v)
                vs.insert(0, v)
        assert vs
        if len(eqn) >= 2:
            return [eqn[0], vs, eqn[1]] + compile_goal(eqn[2], vars)
        else:
            return [eqn[0], vs, eqn[1]]
    else:
        return eqn


def merge(b, a, test, **aux):
    if not a:
        return b
    if not b:
        return a

    ret = []
    while a and b:
        if test(a[0], b[0]):
            ret.append(a.pop(0))
        else:
            ret.append(b.pop(0))
    if a:
        ret.extend(a)
    elif b:
        ret.extend(b)
    return ret


if __name__ == "__main__":
    from reader import CLLogReader, plist2dict

    lr = CLLogReader("MY-MERGE.log")
    iioo = lr.in_outs()

    for ((args, globs), outs) in iioo:
        import ipdb

        ipdb.set_trace()
        args = plist2dict(args)
        globs = plist2dict(globs)

        a = merge(**args)
        print(a)
        print(outs)
        assert a == outs
