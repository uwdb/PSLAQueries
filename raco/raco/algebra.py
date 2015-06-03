from raco import expression
from raco import scheme
from raco.utility import Printable, real_str

from abc import ABCMeta, abstractmethod
import copy
import operator
import math
from raco.expression import StateVar
from functools import reduce


# BEGIN Code to generate variables names
var_id = 0


def reset():
    global var_id
    var_id = 0


def gensym():
    global var_id
    var_id += 1
    return "V%s" % var_id
# END Code to generate variables names


# Global constants
DEFAULT_CARDINALITY = 10000


class RecursionError(ValueError):
    pass


class SchemaError(Exception):
    pass


class Operator(Printable):

    """Operator base class"""
    __metaclass__ = ABCMeta

    def __init__(self):
        self.bound = None
        # Extra code to emit to cleanup
        self.cleanup = ""
        self.alias = self
        self._trace = []

    @abstractmethod
    def apply(self, f):
        """ apply function f to its children. """

    @abstractmethod
    def children(self):
        """Return all the children of this operator."""

    @abstractmethod
    def scheme(self):
        """Return the scheme of the tuples output by this operator."""

    def walk(self):
        """Return an iterator over the tree of operators."""
        yield self
        for c in self.children():
            for x in c.walk():
                yield x

    @abstractmethod
    def num_tuples(self):
        """Return the expected number of tuples output by this operator."""

    def postorder(self, f):
        """Postorder traversal, applying a function to each operator.  The
        function returns an iterator"""
        for c in self.children():
            for x in c.postorder(f):
                yield x
        for x in f(self):
            yield x

    def preorder(self, f):
        """Preorder traversal, applying a function to each operator.  The
        function returns an iterator"""
        for x in f(self):
            yield x
        for c in self.children():
            for x in c.postorder(f):
                yield x

    def collectParents(self, parent_map=None):
        """Construct a dict mapping children to parents. Used in
        optimization"""
        if parent_map is None:
            parent_map = {}
        for c in self.children():
            parent_map.setdefault(c, []).append(self)
            c.collectParents(parent_map)

    def __copy__(self):
        raise RuntimeError("Shallow copy not supported for operators")

    def __eq__(self, other):
        return self.__class__ == other.__class__

    def __str__(self):
        if len(self.children()) > 0:
            return "%s%s" % (self.shortStr(), real_str(self.children()))
        return self.shortStr()

    def __hash__(self):
        h = str(self.__class__).__hash__()
        for i, c in enumerate(self.children()):
            h ^= (c.__hash__() << i)

        return h

    def copy(self, other):
        self._trace = [pair for pair in other.gettrace()]
        self.bound = None

    def trace(self, key, val):
        self._trace.append((key, val))

    def gettrace(self):
        """Return a list of trace messages"""
        return self._trace

    def set_alias(self, alias):
        """Set a user-defined identifier for this operator.  Used in
        optimization and transformation of plans"""
        self.alias = alias

    @abstractmethod
    def shortStr(self):
        """Returns a short string describing the current operator and its
        arguments, but not its children. Consider:

           query = "A(x) :- R(x,3)."
           logicalplan = dlog.fromDatalog(query)
           (label, root_op) = logicalplan[0]

           str(root_op) returns "Project($0)[Select($1 = 3)[Scan(R)]]"

           shortStr(root_op) should return "Project($0)" """

    def collectGraph(self, graph=None):
        """Collects the operator graph for a given query. Input parameter graph
        has the format {'nodes': list(), 'edges': list()}, initialized to empty
        lists by default. An input graph will be mutated."""

        # Initialize graph if necessary
        if graph is None:
            graph = {'nodes': list(), 'edges': list()}

        # Cycle detection - continue, but don't re-add this node to the graph
        if id(self) in [id(n) for n in graph['nodes']]:
            return graph

        # Add this node to the graph
        graph['nodes'].append(self)
        # Add all edges
        graph['edges'].extend([(x, self) for x in self.children()])
        for x in self.children():
            # Recursively add children and edges to the graph. This mutates
            # graph
            x.collectGraph(graph)

        # Return the graph
        return graph

    def resolveAttribute(self, ref):
        """Return a tuple of (column_name, type) for a given AttributeRef."""
        assert isinstance(ref, expression.AttributeRef), ref
        return self.scheme().resolve(ref)


class ZeroaryOperator(Operator):

    """Operator with no arguments"""

    def __init__(self):
        Operator.__init__(self)

    def __eq__(self, other):
        return self.__class__ == other.__class__

    def children(self):
        return []

    def apply(self, f):
        """Apply a function to your children"""
        return self

    def copy(self, other):
        """Deep copy"""
        Operator.copy(self, other)

    def compileme(self, resultsym):
        """Compile this operator, storing its result in resultsym"""
        raise NotImplementedError("{op}.compileme".format(op=type(self)))

    def __repr__(self):
        return "{op}()".format(op=self.opname())


class UnaryOperator(Operator):

    """Operator with one argument"""

    def __init__(self, input):
        self.input = input
        Operator.__init__(self)

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.input == other.input

    def children(self):
        return [self.input]

    def scheme(self):
        """Default scheme is the same as the input.  Usually overriden"""
        return self.input.scheme()

    def apply(self, f):
        """Apply a function to your children"""
        self.input = f(self.input)
        return self

    def copy(self, other):
        """deep copy"""
        self.input = other.input
        Operator.copy(self, other)

    def compileme(self, inputsym):
        """Compile this operator with specified input and output symbol
        names"""
        raise NotImplementedError("{op}.compileme".format(op=type(self)))

    def __repr__(self):
        return "{op}({inp!r})".format(op=self.opname(), inp=self.input)


class BinaryOperator(Operator):

    """Operator with two arguments"""

    def __init__(self, left, right):
        self.left = left
        self.right = right
        Operator.__init__(self)

    def __eq__(self, other):
        return (self.__class__ == other.__class__
                and self.left == other.left
                and self.right == other.right)

    def children(self):
        return [self.left, self.right]

    def apply(self, f):
        """Apply a function to your children"""
        self.left = f(self.left)
        self.right = f(self.right)
        return self

    def copy(self, other):
        """deep copy"""
        self.left = other.left
        self.right = other.right
        Operator.copy(self, other)

    def compileme(self, leftsym, rightsym):
        """Compile this operator with specified left, right, and output symbol
        names"""
        raise NotImplementedError("{op}.compileme".format(op=type(self)))

    def __repr__(self):
        return "{op}({l!r}, {r!r})".format(op=self.opname(), l=self.left,
                                           r=self.right)


class NaryOperator(Operator):

    """Operator with N arguments.  e.g., multi-way joins in one step."""

    def __init__(self, args=None):
        Operator.__init__(self)

        if args is None:
            self.args = []
        else:
            self.args = args

    def add(self, op):
        """Add a child operator to the end of the child argument list."""
        self.args.append(op)

    def children(self):
        return self.args

    def copy(self, other):
        """deep copy"""
        self.args = [a for a in other.args]
        Operator.copy(self, other)

    def apply(self, f):
        """Apply a function to your children"""
        self.args = [f(arg) for arg in self.args]
        return self

    def compileme(self, resultsym, argsyms):
        """Compile this operator with specified children and output symbol
        names"""
        raise NotImplementedError("{op}.compileme".format(op=type(self)))

    def __repr__(self):
        return "{op}({ch!r})".format(op=self.opname(), ch=self.args)


class NaryJoin(NaryOperator):

    """Logical Nary Join operator"""

    def __init__(self, children=None, conditions=None, output_columns=None):
        # TODO: conditions is not actually an expression, it's a list of
        # pairs of UnnamedAttributeRefs that represent equijoins. This is
        # wrong -- it should be a single expression like in Join.
        #
        # Should be able to:
        #    assert isinstance(condition, racoExpression).
        self.conditions = conditions
        self.output_columns = output_columns
        NaryOperator.__init__(self, children)

    def __eq__(self, other):
        return (NaryOperator.__eq__(self, other)
                and self.conditions == other.conditions)

    def num_tuples(self):
        # TODO: use AGM bound (P10 in http://arxiv.org/pdf/1310.3314v2.pdf)
        return DEFAULT_CARDINALITY

    def scheme(self):
        combined = reduce(operator.add, [c.scheme() for c in self.children()])
        # do projection
        if self.output_columns:
            combined = [combined[attr.get_position(combined)]
                        for attr in self.output_columns]
        return scheme.Scheme(combined)

    def copy(self, other):
        """deep copy"""
        self.conditions = other.conditions
        self.output_columns = other.output_columns
        NaryOperator.copy(self, other)

    def shortStr(self):
        return "%s(%s)" % (self.opname(), real_str(self.conditions,
                                                   skip_out=True))


"""Logical Relational Algebra"""


class Union(BinaryOperator):

    """Set union."""

    def __init__(self, left=None, right=None):
        BinaryOperator.__init__(self, left, right)

    def num_tuples(self):
        # a heuristic
        return int((self.left.num_tuples() + self.right.num_tuples()) / 2)

    def scheme(self):
        """Same semantics as SQL: Assume first schema "wins" and throw an
        error if they don't match during evaluation"""
        return self.left.scheme()

    def shortStr(self):
        return self.opname()


class UnionAll(BinaryOperator):

    """Bag union."""

    def __init__(self, left=None, right=None):
        BinaryOperator.__init__(self, left, right)

    def num_tuples(self):
        return self.left.num_tuples() + self.right.num_tuples()

    def copy(self, other):
        """deep copy"""
        BinaryOperator.copy(self, other)

    def scheme(self):
        return self.left.scheme()

    def shortStr(self):
        return self.opname()


class Intersection(BinaryOperator):

    """Set intersection."""

    def __init__(self, left=None, right=None):
        BinaryOperator.__init__(self, left, right)

    def num_tuples(self):
        return min(self.left.num_tuples(), self.right.num_tuples())

    def scheme(self):
        return self.left.scheme()

    def shortStr(self):
        return self.opname()


class Difference(BinaryOperator):

    """Set difference"""

    def __init__(self, left=None, right=None):
        BinaryOperator.__init__(self, left, right)

    def num_tuples(self):
        left_num = self.left.num_tuples()
        right_num = self.right.num_tuples()
        return left_num - math.floor(min(right_num, left_num * 0.5))

    def scheme(self):
        return self.left.scheme()

    def shortStr(self):
        return self.opname()


class CompositeBinaryOperator(BinaryOperator):

    """Join-like operations whose output schema combines its input schemas."""

    @abstractmethod
    def add_equijoin_condition(self, col0, col1):
        """Attempt to add a selection filter to this operation.

        Returns a (possibly modified) operator or None if the columns do not
        refer to different children of the join/cross-product.
        """

    @staticmethod
    def get_equijoin_condition(col0, col1):
        """Return a boolean expression representing an equijoin."""

        return expression.EQ(expression.UnnamedAttributeRef(col0),
                             expression.UnnamedAttributeRef(col1))


class CrossProduct(CompositeBinaryOperator):

    """Logical Cross Product operator"""

    def __init__(self, left=None, right=None):
        BinaryOperator.__init__(self, left, right)

    def num_tuples(self):
        return self.left.num_tuples() * self.right.num_tuples()

    def copy(self, other):
        """deep copy"""
        BinaryOperator.copy(self, other)

    def shortStr(self):
        return self.opname()

    def scheme(self):
        """Return the scheme of the result."""
        return self.left.scheme() + self.right.scheme()

    def add_equijoin_condition(self, col0, col1):
        """Convert the cross-product into a join whenever possible."""
        condition = self.get_equijoin_condition(col0, col1)
        return Join(condition, self.left, self.right)


class Join(CompositeBinaryOperator):

    """Logical Join operator"""

    def __init__(self, condition=None, left=None, right=None):
        self.condition = condition
        BinaryOperator.__init__(self, left, right)

    def __eq__(self, other):
        return (BinaryOperator.__eq__(self, other)
                and self.condition == other.condition)

    def num_tuples(self):
        # this is black magic
        return int(self.left.num_tuples() * self.right.num_tuples() / 10)

    def copy(self, other):
        """deep copy"""
        self.condition = other.condition
        BinaryOperator.copy(self, other)

    def shortStr(self):
        return "%s(%s)" % (self.opname(), self.condition)

    def scheme(self):
        """Return the scheme of the result."""
        return self.left.scheme() + self.right.scheme()

    def add_equijoin_condition(self, col0, col1):
        condition = self.get_equijoin_condition(col0, col1)
        self.condition = expression.AND(self.condition, condition)
        return self

    def __repr__(self):
        return "{op}({cond!r}, {l!r}, {r!r})".format(op=self.opname(),
                                                     cond=self.condition,
                                                     l=self.left,
                                                     r=self.right)


def resolve_attribute_name(user_name, scheme, sexpr, index):
    """Resolve an attribute/column into a name.

    :param user_name: A user-provided string name.  Can be None.
    :type user_name: string
    :param scheme: The schema of the operator's input.
    :type scheme: raco.Scheme
    :param sexpr: The scalar expression describing the column's contents.
    :type sexpr: raco.expression.Expression
    :param index: The numeric index of the column
    :type index: int
    :returns: A string representing the column name
    """

    # We always give preference to a user-provided name
    if user_name:
        return user_name

    # If the column contains a simple attribute reference, infer the column
    # name from the input schema.  However, do not pass along an auto-gen
    # column name.
    elif isinstance(sexpr, expression.AttributeRef):
        inferred_name = scheme.resolve(sexpr)[0]
        if not inferred_name.startswith('_COLUMN'):
            return inferred_name

    # Otherwise, just concoct a column name based on the column index.
    return '_COLUMN%d_' % index


class Apply(UnaryOperator):

    def __init__(self, emitters=None, input=None):
        """Create new attributes from expressions with optional rename.

        :param emitters: list of tuples of the form:
            (column_name, raco.expression.Expression).
            column_name can be None, in which case the system will infer a
            name based on the expression
        :type emitters: list of tuples
        """

        if emitters is not None:
            in_scheme = input.scheme()
            self.emitters = \
                [(resolve_attribute_name(name, in_scheme, sexpr, index), sexpr)
                 for index, (name, sexpr) in enumerate(emitters)]
        UnaryOperator.__init__(self, input)

    def __eq__(self, other):
        return (UnaryOperator.__eq__(self, other) and
                self.emitters == other.emitters)

    def num_tuples(self):
        return self.input.num_tuples()

    def copy(self, other):
        """deep copy"""
        self.emitters = other.emitters
        UnaryOperator.copy(self, other)

    def scheme(self):
        """scheme of the result."""
        input_scheme = self.input.scheme()
        new_attrs = [(name, expr.typeof(input_scheme, None))
                     for (name, expr) in self.emitters]
        return scheme.Scheme(new_attrs)

    def shortStr(self):
        estrs = ",".join(["%s=%s" % (name, str(ex))
                          for name, ex in self.emitters])
        return "%s(%s)" % (self.opname(), estrs)

    def get_names(self):
        """Get the names of the columns emitted by this Apply."""
        return [e[0] for e in self.emitters]

    def get_unnamed_emit_exprs(self):
        """Get the emit expressions for this Apply after ensuring that all
        attribute references are UnnamedAttributeRefs."""
        emits = [e[1] for e in self.emitters]
        return expression.ensure_unnamed(emits, self.input)

    def __repr__(self):
        return "{op}({emt!r}, {inp!r})".format(op=self.opname(),
                                               emt=self.emitters,
                                               inp=self.input)


class StatefulApply(UnaryOperator):
    inits = None
    updaters = None
    state_scheme = None
    emitters = None

    def __init__(self, emitters=None, state_modifiers=None, input=None):
        """Create new attributes from expressions with additional state passed
        from tuple to tuple.

        :param emitters: list of tuples of the form:
                (column_name, raco.expression.Expression).
                column_name can be None, in which case the system will infer a
                name based on the expression
            :type emitters: list of tuples
        :param state_modifiers: State variables maintained by the StatefulApply
        operator.
        :type state_modifiers: list of StateVar tuples
        """

        if state_modifiers is not None:
            self.inits = [(x.name, x.init_expr) for x in state_modifiers]
            self.updaters = [(x.name, x.update_expr) for x in state_modifiers]

            self.state_scheme = scheme.Scheme()
            for (name, expr) in self.inits:
                self.state_scheme.addAttribute(name, expr.typeof(None, None))

        if emitters is not None:
            in_scheme = input.scheme()
            self.emitters = \
                [(resolve_attribute_name(name, in_scheme, sexpr, index), sexpr)
                 for index, (name, sexpr) in enumerate(emitters)]

        UnaryOperator.__init__(self, input)

    def __eq__(self, other):
        return (super(StatefulApply, self).__eq__(self, other) and
                self.emitters == other.emitters and
                self.updaters == other.updaters and
                self.inits == other.inits)

    def __repr__(self):
        # the next line is because of the refactoring that we do in __init__
        state_mods = [StateVar(a, b, d)
                      for ((a, b), (c, d)) in zip(self.inits, self.updaters)]
        return "{op}({emt!r}, {sm!r}, {inp!r})".format(op=self.opname(),
                                                       emt=self.emitters,
                                                       sm=state_mods,
                                                       inp=self.input)

    def num_tuples(self):
        return self.input.num_tuples()

    def copy(self, other):
        """deep copy"""
        self.emitters = other.emitters
        self.updaters = other.updaters
        self.inits = other.inits
        self.state_scheme = other.state_scheme
        UnaryOperator.copy(self, other)

    def scheme(self):
        """scheme of the result."""
        input_scheme = self.input.scheme()
        new_attrs = [(name, expr.typeof(input_scheme, self.state_scheme))
                     for (name, expr) in self.emitters]
        return scheme.Scheme(new_attrs)

    def shortStr(self):
        estrs = ",".join(["%s=%s" % (name, str(ex))
                          for name, ex in self.emitters])
        return "%s(%s)" % (self.opname(), estrs)


# TODO: Non-scheme-mutating operators
class Distinct(UnaryOperator):

    """Remove duplicates from the child operator"""

    def __init__(self, input=None):
        UnaryOperator.__init__(self, input)

    def num_tuples(self):
        # TODO: better heuristics?
        return self.input.num_tuples()

    def scheme(self):
        """scheme of the result"""
        return self.input.scheme()

    def shortStr(self):
        return self.opname()


class Limit(UnaryOperator):

    def __init__(self, count=None, input=None):
        UnaryOperator.__init__(self, input)
        self.count = count

    def __eq__(self, other):
        return UnaryOperator.__eq__(self, other) and self.count == other.count

    def __repr__(self):
        return "{op}({cnt!r}, {inp!r})".format(op=self.opname(),
                                               cnt=self.count,
                                               inp=self.input)

    def num_tuples(self):
        return self.count

    def copy(self, other):
        self.count = other.count
        UnaryOperator.copy(self, other)

    def scheme(self):
        return self.input.scheme()

    def shortStr(self):
        return "%s(%s)" % (self.opname(), self.count)


class Select(UnaryOperator):

    """Logical selection operator"""

    def __init__(self, condition=None, input=None):
        self.condition = condition
        UnaryOperator.__init__(self, input)

    def __eq__(self, other):
        return (UnaryOperator.__eq__(self, other)
                and self.condition == other.condition)

    def num_tuples(self):
        return int(self.input.num_tuples() * 0.5)

    def shortStr(self):
        if isinstance(self.condition, dict):
            cond = self.condition["condition"]
        else:
            cond = self.condition
        return "%s(%s)" % (self.opname(), cond)

    def __repr__(self):
        return "{op}({cond!r}, {inp!r})".format(op=self.opname(),
                                                cond=self.condition,
                                                inp=self.input)

    def copy(self, other):
        """deep copy"""
        self.condition = other.condition
        UnaryOperator.copy(self, other)

    def scheme(self):
        """scheme of the result."""
        return self.input.scheme()

    def get_unnamed_condition(self):
        """Get the filter condition for this Select after ensuring that all
        attribute references are UnnamedAttributeRefs."""
        return expression.ensure_unnamed(self.condition, self.input)


class Project(UnaryOperator):

    """Logical projection operator"""

    def __init__(self, columnlist=None, input=None):
        self.columnlist = columnlist
        UnaryOperator.__init__(self, input)

    def __eq__(self, other):
        return (UnaryOperator.__eq__(self, other)
                and self.columnlist == other.columnlist)

    def num_tuples(self):
        return self.input.num_tuples()

    def shortStr(self):
        return "%s(%s)" % (self.opname(), real_str(self.columnlist,
                                                   skip_out=True))

    def __repr__(self):
        return "{op}({col!r}, {inp!r})".format(op=self.opname(),
                                               col=self.columnlist,
                                               inp=self.input)

    def copy(self, other):
        """deep copy"""
        self.columnlist = other.columnlist
        UnaryOperator.copy(self, other)

    def scheme(self):
        """scheme of the result. Raises a TypeError if a name in the project
        list is not in the source schema"""
        attrs = [self.input.resolveAttribute(attref)
                 for attref in self.columnlist]
        return scheme.Scheme(attrs)

    def get_unnamed_column_list(self):
        """Get the column list for this Project after ensuring that all
        attribute references are UnnamedAttributeRefs."""
        return expression.ensure_unnamed(self.columnlist, self.input)


class GroupBy(UnaryOperator):

    """Logical GroupBy operator

    :param grouping_list: A list of expressions in a "group by" clause
    :param aggregate_list: A list of aggregate expressions (e.g., MIN, MAX)
    :param input: The input operator
    :param state_modifiers: A list of StateVar tuples associated with the
    user-defined aggregates.
    """

    def __init__(self, grouping_list=None, aggregate_list=None, input=None,
                 state_modifiers=None):
        self.grouping_list = grouping_list or []
        self.aggregate_list = aggregate_list or []

        if state_modifiers is not None:
            self.inits = [(x.name, x.init_expr) for x in state_modifiers]
            self.updaters = [(x.name, x.update_expr) for x in state_modifiers]

            self.state_scheme = scheme.Scheme()
            for name, expr in self.inits:
                self.state_scheme.addAttribute(name, expr.typeof(None, None))
        else:
            self.inits = []
            self.updaters = []
            self.state_scheme = scheme.Scheme()

        UnaryOperator.__init__(self, input)

    def num_tuples(self):
        if not self.grouping_list:
            return 1
        return self.input.num_tuples()

    def shortStr(self):
        return "%s(%s; %s)" % (self.opname(),
                               real_str(self.grouping_list, skip_out=True),
                               real_str(self.aggregate_list, skip_out=True))

    def __repr__(self):
        # the next line is because of the refactoring that we do in __init__
        state_mods = [StateVar(a, b, d)
                      for ((a, b), (c, d)) in zip(self.inits, self.updaters)]

        return "{op}({gl!r}, {al!r}, {inp!r}, {sm!r})".format(
            op=self.opname(), gl=self.grouping_list, al=self.aggregate_list,
            inp=self.input, sm=state_mods)

    def copy(self, other):
        """deep copy"""
        self.grouping_list = other.grouping_list
        self.aggregate_list = other.aggregate_list
        self.updaters = other.updaters
        self.inits = other.inits
        self.state_scheme = other.state_scheme

        UnaryOperator.copy(self, other)

    def column_list(self):
        return self.grouping_list + self.aggregate_list

    def get_unnamed_grouping_list(self):
        """Get the grouping list for this GroupBy after ensuring that all
        attribute references are UnnamedAttributeRefs."""
        return expression.ensure_unnamed(self.grouping_list, self.input)

    def get_unnamed_aggregate_list(self):
        """Get the aggregate list for this GroupBy after ensuring that all
        attribute references are UnnamedAttributeRefs."""
        return expression.ensure_unnamed(self.aggregate_list, self.input)

    def get_unnamed_update_exprs(self):
        """Get the update list for this GroupBy after ensuring that all
        attribute references are UnnamedAttributeRefs."""
        ups = [expr for _, expr in self.updaters]
        return expression.ensure_unnamed(ups, self.input)

    def scheme(self):
        """scheme of the result."""
        in_scheme = self.input.scheme()
        # Note: user-provided column names are supplied by a subsequent Apply
        # invocation; see raco/myrial/groupby.py
        schema = scheme.Scheme()
        for index, sexpr in enumerate(self.column_list()):
            name = resolve_attribute_name(None, in_scheme, sexpr, index)
            _type = sexpr.typeof(in_scheme, self.state_scheme)
            schema.addAttribute(name, _type)
        return schema


class OrderBy(UnaryOperator):

    """ Logical Sort operator
    """

    def __init__(self, input=None, sort_columns=None, ascending=None):
        UnaryOperator.__init__(self, input)
        self.sort_columns = sort_columns
        self.ascending = ascending

    def num_tuples(self):
        return self.input.num_tuples()

    def shortStr(self):
        ascend_string = ['+' if a else '-' for a in self.ascending]
        sort_string = ','.join('{col}{asc}'.format(col=c, asc=a)
                               for c, a in zip(self.sort_columns,
                                               ascend_string))
        return "%s(%s)" % (self.opname(), sort_string)

    def copy(self, other):
        """deep copy"""
        self.sort_columns = other.sort_columns
        self.ascending = other.ascending
        UnaryOperator.copy(self, other)

    def scheme(self):
        return self.input.scheme()


class ProjectingJoin(Join):

    """Logical Projecting Join operator"""

    def __init__(self, condition=None, left=None, right=None,
                 output_columns=None):
        self.output_columns = output_columns
        Join.__init__(self, condition, left, right)

    def __eq__(self, other):
        return (Join.__eq__(self, other)
                and self.output_columns == other.output_columns)

    def shortStr(self):
        if self.output_columns is None:
            return Join.shortStr(self)
        return "%s(%s; %s)" % (self.opname(), self.condition,
                               real_str(self.output_columns, skip_out=True))

    def __repr__(self):
        return "{op}({cond!r}, {l!r}, {r!r}, {oc!r})"\
            .format(op=self.opname(), cond=self.condition,
                    l=self.left, r=self.right, oc=self.output_columns)

    def copy(self, other):
        """deep copy"""
        self.output_columns = other.output_columns
        Join.copy(self, other)

    def scheme(self):
        """Return the scheme of the result."""
        if self.output_columns is None:
            return Join.scheme(self)

        def get_col(pos, left_sch, right_sch):
            if pos < len(left_sch):
                return left_sch.getName(pos), left_sch.getType(pos)
            else:
                pos -= len(left_sch)
                assert pos < len(right_sch)
                return right_sch.getName(pos), right_sch.getType(pos)

        left_sch = self.left.scheme()
        right_sch = self.right.scheme()

        combined = left_sch + right_sch
        return scheme.Scheme([get_col(p.get_position(combined),
                                      left_sch, right_sch)
                              for p in self.output_columns])

    def add_equijoin_condition(self, col0, col1):
        # projects are pushed after selections
        raise NotImplementedError()


class Shuffle(UnaryOperator):

    """Send the input to the specified servers"""

    def __init__(self, child=None, columnlist=None, shuffle_type=None):
        UnaryOperator.__init__(self, child)
        self.columnlist = columnlist
        self.shuffle_type = shuffle_type

    def num_tuples(self):
        return self.input.num_tuples()

    def shortStr(self):
        return "%s(%s)" % (self.opname(), real_str(self.columnlist,
                                                   skip_out=True))

    def copy(self, other):
        self.columnlist = other.columnlist
        self.shuffle_type = other.shuffle_type
        UnaryOperator.copy(self, other)

    class ShuffleType(object):
        """Enum of supported shuffling types."""
        SingleFieldHash, MultiFieldHash, IdentityHash = range(3)


class HyperCubeShuffle(UnaryOperator):

    """HyperCube Shuffle for multiway join"""

    def __init__(self, child=None, hashed_columns=None,
                 mapped_hc_dims=None, hyper_cube_dims=None,
                 cell_partition=None):
        """ Keyword arguments:
            child -- child operator.
            hashed_columns -- list of columns to be hashed.
            mapped_hc_dims --  mapped dimensions in HC of hashed columns.
            hyper_cube_dims -- size of dimensions of hyper cube.
            cell_partition -- partition of the HC cells for this shuffle.
        """
        UnaryOperator.__init__(self, child)
        self.hashed_columns = hashed_columns
        self.mapped_hc_dimensions = mapped_hc_dims
        self.hyper_cube_dimensions = hyper_cube_dims
        self.cell_partition = cell_partition

    def num_tuples(self):
        return self.input.num_tuples()

    def shortStr(self):
        return "%s(%s)" % (self.opname(), real_str(self.hashed_columns,
                                                   skip_out=True))

    def copy(self, other):
        self.hashed_columns = other.hashed_columns
        self.mapped_hc_dimensions = other.mapped_hc_dimensions
        self.hyper_cube_dimensions = other.hyper_cube_dimensions
        self.cell_partition = other.cell_partition
        UnaryOperator.copy(self, other)


class Collect(UnaryOperator):

    """Send input to one server"""

    def __init__(self, child=None, server=None):
        UnaryOperator.__init__(self, child)
        self.server = server

    def num_tuples(self):
        return self.input.num_tuples()

    def shortStr(self):
        return "%s(@%s)" % (self.opname(), self.server)

    def copy(self, other):
        self.server = other.server
        UnaryOperator.copy(self, other)


class Broadcast(UnaryOperator):

    """Send input to all servers"""

    def num_tuples(self):
        return self.input.num_tuples()

    def shortStr(self):
        return self.opname()


class Split(UnaryOperator):
    """An in-memory pipeline between two operators. Typically used in
    multi-threaded systems for IPC between threads executing different
    operator subtrees."""

    def num_tuples(self):
        return self.input.num_tuples()

    def shortStr(self):
        return self.opname()


class PartitionBy(UnaryOperator):

    """Send input to a server indicated by a hash of specified columns."""

    def __init__(self, columnlist=None, input=None):
        self.columnlist = columnlist
        UnaryOperator.__init__(self, input)

    def __eq__(self, other):
        return (UnaryOperator.__eq__(self, other)
                and self.columnlist == other.columnlist)

    def num_tuples(self):
        return self.input.num_tuples()

    def shortStr(self):
        return "%s(%s)" % (self.opname(), real_str(self.columnlist,
                                                   skip_out=True))

    def copy(self, other):
        """deep copy"""
        self.columnlist = other.columnlist
        UnaryOperator.copy(self, other)

    def scheme(self):
        """scheme of the result. Raises a TypeError if a name in the project
        list is not in the source schema"""
        return self.input.scheme()


class Fixpoint(Operator):

    def __init__(self, body=None):
        self.body = body

    def children(self):
        return [self.body]

    def num_tuples(self):
        raise NotImplementedError("{op}.num_tuples".format(op=type(self)))

    def __str__(self):
        return "%s[%s]" % (self.shortStr(), self.body)

    def shortStr(self):
        return """Fixpoint"""

    def apply(self, f):
        """Apply a function to your children"""
        self.body.apply(f)
        return self

    def scheme(self):
        if self.body:
            return self.body.scheme()
        else:
            raise RecursionError("No Scheme defined yet for fixpoint")

    def loopBody(self, plan):
        self.body = plan


class State(ZeroaryOperator):

    """A placeholder operator for a recursive plan"""

    def __init__(self, name, fixpoint):
        ZeroaryOperator.__init__(self)
        self.name = name
        self.fixpoint = fixpoint

    def shortStr(self):
        return "%s(%s)" % (self.opname(), self.name)

    def scheme(self):
        return self.fixpoint.scheme()


class Store(UnaryOperator):

    """Store output to a relational table.

    relation_key is a string of the form "program:user:relation".
    """

    def __init__(self, relation_key=None, plan=None):
        UnaryOperator.__init__(self, plan)
        self.relation_key = relation_key

    def num_tuples(self):
        return self.input.num_tuples()

    def shortStr(self):
        return "%s(%s)" % (self.opname(), self.relation_key)

    def __repr__(self):
        return "{op}({rk!r}, {pl!r})".format(op=self.opname(),
                                             rk=self.relation_key,
                                             pl=self.input)

    def copy(self, other):
        self.relation_key = other.relation_key
        UnaryOperator.copy(self, other)


class Dump(UnaryOperator):

    """Echo input to standard out; only useful for standalone raco."""

    def num_tuples(self):
        raise NotImplementedError("{op}.num_tuples".format(op=type(self)))

    def shortStr(self):
        return "%s()" % self.opname()


class EmptyRelation(ZeroaryOperator):

    """Relation with no tuples."""

    def __init__(self, _scheme=None):
        self._scheme = _scheme

    def num_tuples(self):
        return 0

    def shortStr(self):
        return "%s(%s)" % (self.opname(), self._scheme)

    def __repr__(self):
        return "{op}({sch!r})".format(op=self.opname(), sch=self._scheme)

    def copy(self, other):
        """deep copy"""
        self._scheme = other._scheme

    def scheme(self):
        """scheme of the result."""
        return self._scheme


class SingletonRelation(ZeroaryOperator):

    """Relation with a single empty tuple.

    Used for constructing table literals.
    """

    def shortStr(self):
        return "SingletonRelation"

    def num_tuples(self):
        return 1

    def copy(self, other):
        """deep copy"""
        pass

    def scheme(self):
        """scheme of the result."""
        return scheme.Scheme()


class FileScan(ZeroaryOperator):

    """Load table data from a file."""

    def __init__(self, path=None, _scheme=None, options={}):
        self.path = path
        self._scheme = _scheme
        self.options = options
        ZeroaryOperator.__init__(self)

    def __eq__(self, other):
        return (ZeroaryOperator.__eq__(self, other)
                and self.path == other.path
                and self.scheme() == other.scheme()
                and self.options == other.options)

    def __hash__(self):
        return ("%s-%s" % (self.opname(), self.path)).__hash__()

    def shortStr(self):
        return "%s(%s)" % (self.opname(), self.path)

    def __repr__(self):
        return "{op}({path!r}, {sch!r}, {opt!r})".format(
            op=self.opname(),
            path=self.path,
            sch=self._scheme,
            opt=self.options)

    def num_tuples(self):
        raise NotImplementedError("{op}.num_tuples".format(op=type(self)))

    def copy(self, other):
        """deep copy"""
        self.path = other.path
        self._scheme = other._scheme
        self.options = other.options
        ZeroaryOperator.copy(self, other)

    def scheme(self):
        return self._scheme


class Scan(ZeroaryOperator):

    """Logical Scan operator."""

    def __init__(self, relation_key=None, _scheme=None, cardinality=None):
        """Initialize a scan operator.

        relation_key is a string of the form "user:program:relation"
        scheme is the schema of the relation.
        """
        self.relation_key = relation_key
        self._scheme = _scheme
        if cardinality is not None:
            self._cardinality = cardinality
        else:
            self._cardinality = DEFAULT_CARDINALITY
        ZeroaryOperator.__init__(self)

    def __eq__(self, other):
        return (ZeroaryOperator.__eq__(self, other)
                and self.relation_key == other.relation_key
                and self.scheme() == other.scheme())

    def __hash__(self):
        """
        Override since Scan is Zeroary and needs other distinguishing aspects
        to avoid collisions
        """
        return ("%s-%s" % (self.opname(), self.relation_key)).__hash__()

    def shortStr(self):
        return "%s(%s)" % (self.opname(), self.relation_key)

    def num_tuples(self):
        return self._cardinality

    def __repr__(self):
        return "{op}({rk!r}, {sch!r}, {card!r})".format(
            op=self.opname(), rk=self.relation_key, sch=self._scheme,
            card=self._cardinality)

    def copy(self, other):
        """deep copy"""
        self.relation_key = other.relation_key
        self._scheme = other._scheme
        self._cardinality = other._cardinality

        # TODO: need a cleaner and more general way of tracing information
        # through the compilation process for debugging purposes
        if hasattr(other, "originalterm"):
            self.originalterm = other.originalterm
        ZeroaryOperator.copy(self, other)

    def scheme(self):
        """Scheme of the result, which is just the scheme of the relation."""
        return self._scheme


class SampleScan(ZeroaryOperator):

    """Logical Sample Operator"""

    def __init__(self, relation_key, _scheme, sample_size, is_pct,
                 sample_type):
        self.relation_key = relation_key
        self._scheme = _scheme
        self.sample_size = sample_size
        self.is_pct = is_pct
        self.sample_type = sample_type
        ZeroaryOperator.__init__(self)

    def __repr__(self):
        return "{op}({rk!r}, {s!r}, {p!r}, {t!r})".format(op=self.opname(),
                                                          rk=self.relation_key,
                                                          s=self.sample_size,
                                                          p=self.is_pct,
                                                          t=self.sample_type)

    def shortStr(self):
        pct = '%' if self.is_pct else ''
        return "{op}{type}({rel}, {size}{pct})".format(op=self.opname(),
                                                       type=self.sample_type,
                                                       rel=self.relation_key,
                                                       size=self.sample_size,
                                                       pct=pct)

    def num_tuples(self):
        return self.sample_size

    def scheme(self):
        """Scheme of the result, which is just the scheme of the relation."""
        return self._scheme


class StoreTemp(UnaryOperator):

    """Store an input relation to a "temporary" relation.

    Temporary relations exist for the lifetime of a query.
    """

    def __init__(self, name=None, input=None):
        UnaryOperator.__init__(self, input)
        self.name = name

    def num_tuples(self):
        return self.input.num_tuples()

    def shortStr(self):
        return '{op}({name})'.format(op=self.opname(), name=self.name)

    def copy(self, other):
        self.name = other.name
        UnaryOperator.copy(self, other)

    def __eq__(self, other):
        return UnaryOperator.__eq__(self, other) and self.name == other.name

    def __repr__(self):
        return "{op}({name!r}, {inp!r})".format(op=self.opname(),
                                                name=self.name,
                                                inp=self.input)


class AppendTemp(UnaryOperator):

    """Append an input relation to a "temporary" relation.

    Temporary relations exist for the lifetime of a query.
    """

    def __init__(self, name=None, input=None):
        UnaryOperator.__init__(self, input)
        self.name = name

    def num_tuples(self):
        return self.input.num_tuples()

    def shortStr(self):
        return '{op}({name})'.format(op=self.opname(), name=self.name)

    def copy(self, other):
        self.name = other.name
        UnaryOperator.copy(self, other)

    def __eq__(self, other):
        return UnaryOperator.__eq__(self, other) and self.name == other.name

    def __repr__(self):
        return "{op}({name!r}, {inp!r})".format(op=self.opname(),
                                                name=self.name,
                                                inp=self.input)


class ScanTemp(ZeroaryOperator):

    """Read the contents of a temporary relation."""

    def __init__(self, name=None, _scheme=None):
        self.name = name
        self._scheme = _scheme
        ZeroaryOperator.__init__(self)

    def __eq__(self, other):
        return (ZeroaryOperator.__eq__(self, other) and self.name == other.name
                and self._scheme == other._scheme)

    def num_tuples(self):
        raise NotImplementedError("{op}.num_tuples".format(op=type(self)))

    def shortStr(self):
        return "%s(%s,%s)" % (self.opname(), self.name, str(self._scheme))

    def copy(self, other):
        self.name = other.name
        self._scheme = other._scheme
        ZeroaryOperator.copy(self, other)

    def scheme(self):
        return self._scheme

    def __repr__(self):
        return "{op}({name!r}, {sch!r})".format(op=self.opname(),
                                                name=self.name,
                                                sch=self._scheme)


class Sink(UnaryOperator):

    """ Throw the tuples in an relation on the floor."""
    def __init__(self, input=None):
        UnaryOperator.__init__(self, input)

    def num_tuples(self):
        return self.input.num_tuples()

    def shortStr(self):
        return "{op}".format(op=self.opname())

    def __repr__(self):
        return "{op}({pl!r})".format(op=self.opname(), pl=self.input)


class Parallel(NaryOperator):

    """Execute a set of independent plans in parallel."""

    def __init__(self, ops=None):
        NaryOperator.__init__(self, ops)

    def num_tuples(self):
        raise NotImplementedError("{op}.num_tuples".format(op=type(self)))

    def shortStr(self):
        return self.opname()

    def scheme(self):
        """Parallel does not return any tuples."""
        return None


class Sequence(NaryOperator):

    """Execute a sequence of plans in serial order."""

    def __init__(self, ops=None):
        NaryOperator.__init__(self, ops)

    def shortStr(self):
        return self.opname()

    def scheme(self):
        """Sequence does not return any tuples."""
        return None

    def __repr__(self):
        return "{op}({ops!r})".format(op=self.opname(), ops=self.args)

    def num_tuples(self):
        raise NotImplementedError("{op}.num_tuples".format(op=type(self)))


class DoWhile(NaryOperator):

    def __init__(self, ops=None):
        """Repeatedly execute a sequence of plans until a termination
        condition.

        :params ops: A list of operations to execute in serial.  By convention,
        the last operation is the termination condition.  The termination
        condition should map to a single row, single column relation.  The loop
        continues if its value is True.
        """
        if ops is not None:
            assert len(ops) >= 2, "DoWhile should have at least two children"
        NaryOperator.__init__(self, ops)

    def num_tuples(self):
        raise NotImplementedError("{op}.num_tuples".format(op=type(self)))

    def shortStr(self):
        return self.opname()

    def scheme(self):
        """DoWhile does not return any tuples."""
        return None


def inline_operator(dest_op, var, target_op):
    """Convert two operator trees into one by inlining.

    :param dest_op: The Operator that is the inline destination
    :param var: The variable name (String) to replace.
    :param target_op: The operation to replace.
    """
    # Wrap the bool in a list so we pass a pointer that does not change
    # (the list) into the function.
    has_inlined = [False]

    def rewrite_node(node):
        if isinstance(node, ScanTemp) and node.name == var:
            if has_inlined[0]:
                return copy.deepcopy(target_op)
            has_inlined[0] = True
            return target_op
        else:
            return node.apply(rewrite_node)

    return rewrite_node(dest_op)


def convertcondition(condition, left_len, combined_scheme):
    """Convert an equijoin condition to a pair of column lists."""

    if isinstance(condition, expression.AND):
        leftcols1, rightcols1 = convertcondition(condition.left,
                                                 left_len,
                                                 combined_scheme)
        leftcols2, rightcols2 = convertcondition(condition.right,
                                                 left_len,
                                                 combined_scheme)
        return leftcols1 + leftcols2, rightcols1 + rightcols2

    if isinstance(condition, expression.EQ):
        leftpos = condition.left.get_position(combined_scheme)
        rightpos = condition.right.get_position(combined_scheme)
        leftcol = min(leftpos, rightpos)
        rightcol = max(leftpos, rightpos)
        assert rightcol >= left_len
        return [leftcol], [rightcol - left_len]

    raise NotImplementedError("Myria only supports EquiJoins, not %s" % condition)  # noqa
