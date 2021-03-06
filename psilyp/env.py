from symbol import *

List = list
Number = (int, float)


class Env(dict):
    "An environment: a dict of {'var':val} pairs, with an outer Env."
    def __init__(self, params=(), args=(), outer=None):
        # Bind param list to corresponding args, or single param to list of args
        self.outer = outer
        if isa(params, Symbol):
            self.update({params: list(args)})
        else:
            if len(args) != len(params):
                raise TypeError('expected %s, given %s, '
                                % (to_string(params), to_string(args)))
            self.update(zip(params, args))

    def find(self, var):
        "Find the innermost Env where var appears."
        if var in self:
            return self
        elif self.outer is None:
            raise LookupError(var)
        else:
            return self.outer.find(var)


def is_pair(x):
    return x != [] and isa(x, list)


def cons(x, y):
    return [x] + y


def add_globals(env):
    "Add some Lisp standard procedures."
    import sys, math, cmath, operator as op
    env.update(vars(math))
    env.update(vars(cmath))
    env.update({
     '+': op.add, '-': op.sub, '*': op.mul, '/': op.truediv, '**': op.pow,
     'not': op.not_, '>': op.gt, '<': op.lt, '>=': op.ge,
     '<=': op.le, '=': op.eq, 'equal?': op.eq, 'eq?': op.is_,
     'length': len, 'cons': cons, 'car': lambda x: x[0],
     'cdr': lambda x: x[1:], 'append': op.add,
     'list': lambda *x: list(x), 'list?': lambda x: isa(x, list),
     'null?': lambda x: x == [], 'symbol?': lambda x: isa(x, Symbol),
     'boolean?': lambda x: isa(x, bool), 'pair?': is_pair,
     'port?': lambda x: isa(x, file), 'apply': lambda proc, l: proc(*l),
     'map': lambda f, x: list(map(f, x)),
     'filter': lambda f, x: list(filter(f, x))})
    return env


isa = isinstance
global_env = add_globals(Env())
