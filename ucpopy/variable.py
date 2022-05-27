from __future__ import annotations
from typing import Optional, Union
from collections import defaultdict
from copy import deepcopy
import ucpopy.structs as st


g_free_vsets = []
g_variable_cache: defaultdict[str, list[st.VAR]] = defaultdict(list)


def unify(cond1, cond2, bindings: list[list[st.VARSET]]) -> list[list[st.VARSET]]:
    if cond1[0] == ':NOT' and cond2[0] == ':NOT':
        cond1 = cond1[1]
        cond2 = cond2[1]
    if cond1[0] == cond2[0]:
        unifieds = unify_args(cond1[1:], cond2[1:], bindings)
        return unifieds
    return []


def unify_args(args1, args2, bindings: list[list[st.VARSET]]) -> list[list[st.VARSET]]:
    result: list[list[str]] = []
    a1 = []
    a2 = []
    cs = [deepcopy(bindings[0])]
    idx = 0

    if len(args1) != len(args2):
        return []

    for (b1, b2) in zip(args1, args2):
        a1 = get_vset(b1, cs)
        a2 = get_vset(b2, cs)
        if a1 != a2:
            result.insert(0, [a1.const if a1.const else b1] + [a2.const if a2.const else b2])
        c = combine_varset(a1, a2)
        if c:
            cs[0].insert(0, c)
            idx += 1
        else:
            # free_vsets(cs[0], bindings[0])
            return []
    # free_vsets(cs[0], bindings[0])
    return [result]


def bind_variable(var, bindings: list[list[st.VARSET]]):
    if not var:
        return []
    elif isinstance(var, list):
        return [bind_variable(x, bindings) for x in var]
    else:
        return sym_value(var, bindings)


def new_bindings():
    return new_cs()


def instantiate_term(term, num, alst={}):
    if isinstance(term, list):
        return [instantiate_term(t, num, alst) for t in term]
    elif is_variable(term):
        if term in alst:
            return alst[term][1:]
        else:
            return make_variable(term, num)
    else:
        return term


def add_bind(new_bind, bindings: list[list[st.VARSET]]) -> list[list[st.VARSET]]:
    if bindings:
        bindings = copy_cs(bindings)
        for pair in new_bind:
            if pair[0] == ':NOT':
                constr = constrain_neq(pair[1], pair[2], bindings)
            else:
                constr = constrain_eq(pair[0], pair[1], bindings)
            if not constr:
                return []
        return bindings


def new_cs():
    return [[]]


def copy_cs(cs: list[list[st.VARSET]]):
    return [deepcopy(cs[0])]


def constrain_eq(sym1: str, sym2: str, cs: list[list[st.VARSET]]):
    v1 = get_vset(sym1, cs)
    v2 = get_vset(sym2, cs)
    vs = combine_varset(v1, v2)
    if vs:
        if v1 != v2:
            cs[0].insert(0, vs)
        return True
    return []


def constrain_neq(sym1: str, sym2: str, cs: list[list[st.VARSET]]):
    r1 = get_vset(sym1, cs)
    v1 = restrict_varset(r1, sym2)
    r2 = get_vset(sym2, cs)
    v2 = restrict_varset(r2, sym1)
    if v1 and v2:
        cs[0].insert(0, v1)
        cs[0].insert(0, v2)
        return True
    return []


def codesignates(sym1: str, sym2: str, cs: list[list[st.VARSET]]):
    return sym2 in get_vset(sym1, cs).cd_set


# setが順不同
def sym_value(sym: str, cs: list[list[st.VARSET]]) -> str:
    if is_variable(sym):
        v = get_vset(sym, cs)
        if v.const:
            return v.const
        else:
            return list(v.cd_set)[0]
    else:
        return sym


def get_vset(sym: st.VAR, cs: list[list[st.VARSET]]) -> st.VARSET:
    if is_variable(sym):
        for vs in cs[0]:
            if sym in vs.cd_set:
                return vs
    else:
        for vs in cs[0]:
            if vs.const == sym:
                return vs
    ret_vset = make_empty_varset(sym)
    cs[0].insert(0, ret_vset)
    return ret_vset


def var_union(a, b):
    return set(a).union(b)


def var_intersect(a, b):
    return set(a).intersection(b)


def make_empty_varset(symb: str) -> st.VARSET:
    return new_varset(
        cd_set=[symb], const=([] if is_variable(symb) else symb), ncd_set=[]
    )


def combine_varset(a: st.VARSET, b: st.VARSET) -> Optional[st.VARSET]:
    if a == b:
        return a

    if not a.const or not b.const:
        cd_set = a.cd_set | b.cd_set
        ncd_set = a.ncd_set | b.ncd_set
        const = a.const if a.const else b.const
        if const not in ncd_set and not var_intersect(cd_set, ncd_set):
            return st.VARSET(const, cd_set, ncd_set)

    return []


def restrict_varset(vset: st.VARSET, restricter) -> Optional[st.VARSET]:
    if restricter not in vset.cd_set:
        return st.VARSET(const=vset.const, cd_set=vset.cd_set, ncd_set=var_union([restricter], vset.ncd_set))


def new_varset(const: Optional[str], cd_set: set[Union[str, st.VAR]], ncd_set: set[Union[str, st.VAR]]) -> st.VARSET:
    return st.VARSET(const=const, cd_set=cd_set, ncd_set=ncd_set)


def free_vsets(v1, v2):
    pass


def is_variable(thing: str) -> bool:
    if isinstance(thing, str) and thing[0] == '?':
        return True
    if isinstance(thing, st.VAR):
        return True
    return []


def uniquify_var(var: Union[st.VAR, str]) -> st.VAR:
    if isinstance(var, str):
        return st.VAR(name=var, num=None)
    else:
        return st.VAR(name=var.name, num=var.num)


def make_variable(var: str, num) -> st.VAR:
    global g_variable_cache
    vs = g_variable_cache[var]
    for v in vs:
        if num == v.num:
            return v
    vardata = st.VAR(name=var, num=num)
    g_variable_cache[var].insert(0, vardata)
    return vardata


if __name__ == '__main__':
    from reader import CLLogReader, plist2dict

    lr = CLLogReader('VARIABLE+.log')
    iioo = lr.in_outs()
    for ((args, globs), outs) in iioo:
        args = plist2dict(args)
        globs = plist2dict(globs)
        a = is_variable(**args)
        print(a)
        print(outs)
        assert a == bool(outs)
