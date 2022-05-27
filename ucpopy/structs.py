from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Literal, Optional, Union, TypeAlias
from ucpopy.variable import bind_variable



def car(lst):
    if not lst:
        return []
    else:
        return lst[0]


def cdr(lst):
    if not lst:
        return []
    else:
        return lst[1:]


def cadr(lst):
    return car(cdr(lst))


def caar(lst):
    return car(car(lst))


# ;;;;;;;;;;;;;;;;
# ;;; Topological Sort
# ;;; Returns correct order: first step at head
# ;;; Input: max is an integer
# ;;;    Ordering is a list of pairs (f l) where step number f must be before l
# ;;;    f, l <= max
# ;;; See Aho, Hopcoft, Ullman p70 for faster way
# (defun TOP-SORT (ordering max)
#   (let ((a (top-sort1 (copy-tree ordering) max))
#         (b nil))
#     (dotimes (i max (nconc a b))
#              (when (not (my-member (1+ i) a :test #'eql))
#                    (push (1+ i) b)))))

# ;;; Topological Sort util  -   This code is DESTRUCTIVE!  Pass it a copy!
# (defun TOP-SORT1 (ordering max)
#   (when ordering
#         (let ((as (mapcar #'cadr ordering)))
#           (do ((p ordering (cdr p)))
#               ((not (my-member (caar p) as))
#                (cons (caar p)
#                      (top-sort1 (delete-if #'(lambda (x)
# 					   (eql (car x) (caar p))) ordering)
#                                 (- max 1))))))))
def top_sort(ordering, max):
    """Returns correct order: first step at head
    Input: max is an integer
       Ordering is a list of pairs (f l) where step number f must be before l
       f, l <= max
    See Aho, Hopcoft, Ullman p70 for faster way"""
    a = top_sort1(ordering, max)
    b = []
    for i in range(max):
        if (i + 1) not in a:
            b = [(i + 1)] + b
    return a + b


def top_sort1(ordering, max):
    if ordering:
        as_ = [cadr(x) for x in ordering]
        p = ordering
        while caar(p) in as_:
            p = cdr(p)

        h = [caar(p)]
        t = top_sort1([x for x in ordering if car(x) != caar(p)], max - 1)
        return h + t
    else:
        return []


STEPID: TypeAlias = Union[int, Literal[':GOAL']]
CONDITION: TypeAlias = Union[str, list["CONDITION"]]


# (defstruct (var (:print-function print-variable))
#   name					; The variable's name
#   num)
@dataclass
class VAR:
    name: str
    num: int

    def __hash__(self):
        return hash((self.name, self.num))

    def __repr__(self):
        return f'{self.name}{self.num}'


# (defstruct (varset )
#   const         ;; the unique constant that codesignates with this varset.
#   cd-set        ;; the set of variables (and constant) that codesignate
#   ncd-set)	;; Vars & consts that must not codesignate with this set
@dataclass
class VARSET:
    const: Optional[str]
    cd_set: set[Union[str, VAR]]
    ncd_set: set[Union[str, VAR]]

    def __init__(self, const, cd_set, ncd_set):
        self.const = const if const else None
        self.cd_set = set(cd_set)
        self.ncd_set = set(ncd_set)


# (defstruct FLAW
#   (rank nil))
@dataclass
class FLAW:
    rank: Any


# (defstruct (OPENC (:include flaw)
#                   (:print-function print-open))
#   condition ;; open precondition {condx}
#   id ;; id of step which requires it
#   (src-limit -1))      ;; Do not link to any step less than this
@dataclass
class OPENC(FLAW):
    condition: CONDITION
    id: STEPID
    src_limit: int = -1

    def __init__(self, rank, condition, id, src_limit=-1):
        self.rank = rank
        self.condition = condition
        self.id = id
        self.src_limit = src_limit


# (defstruct (LINK (:print-function print-link))
#   id1
#   condition
#   id2
#   effect ;; effect linked to
# )
@dataclass
class LINK:
    id1: STEPID
    condition: CONDITION
    id2: STEPID
    effect: EFFECT = field(default_factory=list)


# (defstruct (UNSAFE (:include flaw)
#                    (:print-function print-unsafe))
#   link ;; id of threatened link
#   clobber-effect ;; effect which threatens it
#   clobber-condition ;; added condition which causes the threat
#   violation)           ;; for safety violation
@dataclass
class UNSAFE(FLAW):
    link: LINK  # id
    clobber_effect: "EFFECT"
    clobber_condition: CONDITION
    violation: Any


# (defstruct (FACT (:include flaw))
#   condition
#   function
#   (bindings nil))
@dataclass
class FACT(FLAW):
    condition: CONDITION
    function: Any
    bindings: list[list[VARSET]] = field(default_factory=list)


# (defstruct (P-STEP)
#   ID					; integer step number
#   action				; formula such as (puton ?X ?Y)
#   parms					; parameters
#   precond				; conditions like (clear ?X)
#   add					; effects asserted by step
#   (cache nil)				; A cache of existing steps
#   )
@dataclass
class P_STEP:
    id: STEPID
    action: list[str]
    parms: Optional[list]
    precond: Any
    add: list[EFFECT]
    cache: list[P_STEP] = field(default_factory=list)

# (defstruct (EFFECT (:print-function print-effect))
#   (ID nil) ; Effects associated step
#   (forall nil)
#   (precond nil) ; Preconditions of effect
#   (ranking nil) ; one of :primary, :side or nil (= N/A)
#   add)					; Added entry


@dataclass
class EFFECT:
    id: STEPID
    forall: Any = field(default_factory=list)
    precond: CONDITION = field(default_factory=list)
    ranking: Any = field(default_factory=list)
    add: list[CONDITION] = field(default_factory=list)


# (defstruct FORALL
#   ID ; integer step number
#   vars ; (forall *vars*
#   type ;         *type*
#   condition)				;         *condition*)
@dataclass
class FORALL:
    id: int
    vars: list[VAR]
    type: Any
    condition: CONDITION


# (defstruct (UNIV-THREAT (:include flaw))
#   forall
#   term
#   step)
@dataclass
class UNIV_THREAT(FLAW):
    forall: FORALL
    term: str
    step: Any


# ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

# (defstruct (STAT (:print-function print-stat))
#   algo ; tweak or strips
#   date ; when performed
#   prob-num ; identifier
#   num-init ; how many initial conditions
#   num-goal
#   plan-len ; how many steps
#   reached-max? ; terminated because of nodes?
#   complete? ; planner successful
#   time ; internal cpu time
#   visited ; nodes-visted
#   created ; calls to make-plan
#   q-len ; queue len at termination
#   ave-branch ; average branching factor
#   unify-count
#   rank-unifies
#   add-bindings)

# ;;;;;;;;;;;;;;;;;;;;;;;;
# ;;; Print out statistics from single run
# (defun DISPLAY-STAT (s &optional (st t) ignore)
#   (declare (ignore ignore))
#   (format st "~%~%~a Stats: Initial terms = ~2a;   Goals = ~2a;  ~a (~a steps)"
#           (stat-algo s) (stat-num-init s) (stat-num-goal s)
#           (if (stat-complete? s) "Success" "Failure")
#           (stat-plan-len s))
#   (format st "~%      Created ~a plans, but explored only ~a"
#           (stat-created s) (stat-visited s))
#   (format st "~%      CPU time: ~9,4F sec" (/ (stat-time s)
#                                               internal-time-units-per-second))
#   (format st "~%      Branching factor: ~6,3F" (stat-ave-branch s))
#   (format st "~%      Working Unifies: ~4a"
#           (- (stat-unify-count s) (stat-rank-unifies s)))
#   (format st "~%      Bindings Added: ~4a" (stat-add-bindings s)))

# (defun PRINT-STAT (s &optional (stream t) depth)
#   (declare (ignore depth))
#   (if *verbose*
#       (display-stat s stream)
#       (format stream "#Stats:<cpu time = ~,4F>"
#               (float (/ (stat-time s) internal-time-units-per-second)))))

# (defstruct (PLAN (:constructor make-plan*)
# 	    (:print-function print-plan))
#   steps					; list of steps
#   links					; list of causal links
#   flaws					; list of OPENCs and UNSAFEs
#   ordering				; list of (ID1 ID2)
#   foralls				; list of all forall preconditions
#   bindings				; binding constraints
#   high-step				; integer # of highest step in plan
#   (other nil)				; an alist of scr & debug stuff
#   )
@dataclass
class PLAN:
    steps: list[P_STEP]
    links: list[LINK]
    flaws: list[FLAW]
    ordering: list[tuple[int, int]]
    foralls: list[FORALL]
    bindings: list[list[VARSET]]
    high_step: int
    other: dict = field(default_factory=dict)

    def __init__(self, steps, links, flaws, ordering, foralls, bindings, high_step, other):
        self.steps = steps
        self.links = links
        self.flaws = flaws
        self.ordering = ordering
        self.foralls = foralls
        self.bindings = bindings
        self.high_step = high_step

        if isinstance(other, list):
            for i, elem in enumerate(other):
                # cons pair と cons list を区別していないためアドホックに分離
                if elem[0] != ':NEW-GOAL':
                    other[i] = [elem[0], elem[1:]]
                elif len(elem) == 1:
                    other[i] = [elem[0], []]
                # else:
                    # other[i] = [elem[0], elem[1:]]
        self.other = dict(other)

    def __lt__(self, other):
        return 0

    def display(plan: PLAN):
        steps = [None] * (plan.high_step + 1)
        order = top_sort(plan.ordering, plan.high_step)
        goal = []

        # initial
        step0 = [st for st in plan.steps if st.id == 0][0]
        added_cond = step0.add[0].add
        vars = [bind_variable(x, plan.bindings) for x in added_cond]
        print("Init   0 :", vars)
        for step_n in plan.steps:
            if step_n.id == ':GOAL':
                goal = step_n.precond
            else:
                steps[step_n.id] = step_n
        # steps
        for i in range(plan.high_step):
            sn = order[i]
            step = steps[sn]
            print("Step {:3d} : {}  Created {}".format(
                i + 1, 
                bind_variable(step.action, plan.bindings) if step else '',
                sn
            ))
            for ln in plan.links:
                if ln.id2 == sn:
                    print("         {} -> {}".format(
                        ln.id1,
                        bind_variable(ln.condition, plan.bindings)
                    ))
                    for u in plan.flaws:
                        if isinstance(u, UNSAFE) and ln == u.link:
                            print("<{}>".format(u.clobber_effect.id))
            for fl in plan.flaws:
                if isinstance(fl, OPENC) and fl.id == sn:
                    print("         -> {} ".format(
                        bind_variable(fl.condition, plan.bindings)
                    ))
        # goal
        print("Goal     :", goal)
        for ln in plan.links:
            if ln.id2 == ':GOAL':
                print("         {} -> {}".format(
                    ln.id1,
                    bind_variable(ln.condition, plan.bindings)
                ))
                for u in plan.flaws:
                    if isinstance(u, UNSAFE) and ln == u.link:
                        print("<{}>".format(u.clobber_effect.id))
        for fl in plan.flaws:
            if isinstance(fl, OPENC) and fl.id == ':GOAL':
                print("            => {}".format(
                    bind_variable(fl.condition, plan.bindings)
                ))
        # facts
        print("Facts:")
        for fl in plan.flaws:
            if isinstance(fl, FACT):
                print("  {}".format(bind_variable(fl.condition, plan.bindings)))
        # result
        if not plan.flaws:
            print("Complete!")

