import collections
import random

from raco.algebra import *
from raco.expression import NamedAttributeRef as AttRef
from raco.expression import UnnamedAttributeRef as AttIndex
from raco.expression import StateVar

from raco.language.myrialang import (
    MyriaShuffleConsumer, MyriaShuffleProducer, MyriaHyperShuffleProducer,
    MyriaBroadcastConsumer, MyriaQueryScan, MyriaSplitConsumer)
from raco.language.myrialang import (MyriaLeftDeepTreeAlgebra,
                                     MyriaHyperCubeAlgebra)
from raco.compile import optimize
from raco import relation_key
from raco.catalog import FakeCatalog

import raco.scheme as scheme
import raco.myrial.myrial_test as myrial_test
from raco import types


class OptimizerTest(myrial_test.MyrialTestCase):

    x_scheme = scheme.Scheme([("a", types.LONG_TYPE), ("b", types.LONG_TYPE), ("c", types.LONG_TYPE)])  # noqa
    y_scheme = scheme.Scheme([("d", types.LONG_TYPE), ("e", types.LONG_TYPE), ("f", types.LONG_TYPE)])  # noqa
    x_key = relation_key.RelationKey.from_string("public:adhoc:X")
    y_key = relation_key.RelationKey.from_string("public:adhoc:Y")

    def setUp(self):
        super(OptimizerTest, self).setUp()

        random.seed(387)  # make results deterministic
        rng = 20
        count = 30
        self.x_data = collections.Counter(
            [(random.randrange(rng), random.randrange(rng),
              random.randrange(rng)) for _ in range(count)])
        self.y_data = collections.Counter(
            [(random.randrange(rng), random.randrange(rng),
              random.randrange(rng)) for _ in range(count)])

        self.db.ingest(OptimizerTest.x_key,
                       self.x_data,
                       OptimizerTest.x_scheme)
        self.db.ingest(OptimizerTest.y_key,
                       self.y_data,
                       OptimizerTest.y_scheme)

        self.expected = collections.Counter(
            [(a, b, c, d, e, f) for (a, b, c) in self.x_data
             for (d, e, f) in self.y_data if a > b and e <= f and c == d])

        self.z_key = relation_key.RelationKey.from_string("public:adhoc:Z")
        self.z_data = collections.Counter([(1, 2), (2, 3), (1, 2), (3, 4)])
        self.z_scheme = scheme.Scheme([('src', types.LONG_TYPE), ('dst', types.LONG_TYPE)])  # noqa
        self.db.ingest('public:adhoc:Z', self.z_data, self.z_scheme)

        self.expected2 = collections.Counter(
            [(s1, d3) for (s1, d1) in self.z_data.elements()
             for (s2, d2) in self.z_data.elements()
             for (s3, d3) in self.z_data.elements() if d1 == s2 and d2 == s3])

    @staticmethod
    def logical_to_physical(lp, **kwargs):
        if kwargs.get('hypercube', False):
            algebra = MyriaHyperCubeAlgebra(FakeCatalog(64))
        else:
            algebra = MyriaLeftDeepTreeAlgebra()
        return optimize(lp, algebra, **kwargs)

    @staticmethod
    def get_count(op, claz):
        """Return the count of operator instances within an operator tree."""

        def count(_op):
            if isinstance(_op, claz):
                yield 1
            else:
                yield 0
        return sum(op.postorder(count))

    @staticmethod
    def get_num_select_conjuncs(op):
        """Get the number of conjunctions within all select operations."""
        def count(_op):
            if isinstance(_op, Select):
                yield len(expression.extract_conjuncs(_op.condition))
            else:
                yield 0
        return sum(op.postorder(count))

    def test_push_selects(self):
        """Test pushing selections into and across cross-products."""
        lp = StoreTemp('OUTPUT',
               Select(expression.LTEQ(AttRef("e"), AttRef("f")),
                 Select(expression.EQ(AttRef("c"), AttRef("d")),
                   Select(expression.GT(AttRef("a"), AttRef("b")),
                      CrossProduct(Scan(self.x_key, self.x_scheme),
                                   Scan(self.y_key, self.y_scheme))))))  # noqa

        self.assertEquals(self.get_count(lp, Select), 3)
        self.assertEquals(self.get_count(lp, CrossProduct), 1)

        pp = self.logical_to_physical(lp)
        self.assertIsInstance(pp.input, MyriaSplitConsumer)
        self.assertIsInstance(pp.input.input.input, Join)
        self.assertEquals(self.get_count(pp, Select), 2)
        self.assertEquals(self.get_count(pp, CrossProduct), 0)

        self.db.evaluate(pp)
        result = self.db.get_temp_table('OUTPUT')
        self.assertEquals(result, self.expected)

    def test_collapse_applies(self):
        """Test pushing applies together."""
        lp = StoreTemp('OUTPUT',
               Apply([(None, AttIndex(1)), ('w', expression.PLUS(AttIndex(0), AttIndex(0)))],       # noqa
                 Apply([(None, AttIndex(1)), (None, AttIndex(0)), (None, AttIndex(1))],             # noqa
                   Apply([('x', AttIndex(0)), ('y', expression.PLUS(AttIndex(1), AttIndex(0)))],    # noqa
                     Apply([(None, AttIndex(0)), (None, AttIndex(1))],
                           Scan(self.x_key, self.x_scheme))))))  # noqa

        self.assertEquals(self.get_count(lp, Apply), 4)

        pp = self.logical_to_physical(lp)
        self.assertIsInstance(pp.input, Apply)
        self.assertEquals(self.get_count(pp, Apply), 1)

        expected = collections.Counter(
            [(b, a + a) for (a, b, c) in
             [(b, a, b) for (a, b) in
              [(a, b + a) for (a, b) in
                [(a, b) for (a, b, c) in self.x_data]]]])  # noqa
        self.db.evaluate(pp)
        result = self.db.get_temp_table('OUTPUT')
        self.assertEquals(result, expected)

    def test_select_count_star(self):
        """Test that we don't generate 0-length applies from a COUNT(*)."""
        lp = StoreTemp('OUTPUT',
                       GroupBy([], [expression.COUNTALL()],
                               Scan(self.x_key, self.x_scheme)))

        self.assertEquals(self.get_count(lp, GroupBy), 1)

        pp = self.logical_to_physical(lp)
        self.assertIsInstance(pp.input.input.input, GroupBy)
        # SplitC.SplitP.GroupBy.CollectP.CollectC.GroupBy.Apply
        apply = pp.input.input.input.input.input.input.input
        self.assertIsInstance(apply, Apply)
        self.assertEquals(self.get_count(pp, Apply), 1)
        self.assertEquals(len(apply.scheme()), 1)

        expected = collections.Counter([(len(self.x_data),)])
        self.db.evaluate(pp)
        result = self.db.get_temp_table('OUTPUT')
        self.assertEquals(result, expected)

    def test_projects_apply_join(self):
        """Test column selection both Apply into ProjectingJoin
        and ProjectingJoin into its input.
        """
        lp = StoreTemp('OUTPUT',
               Apply([(None, AttIndex(1))],
                 ProjectingJoin(expression.EQ(AttIndex(0), AttIndex(3)),
                   Scan(self.x_key, self.x_scheme),
                   Scan(self.x_key, self.x_scheme),
                   [AttIndex(i) for i in xrange(2 * len(self.x_scheme))])))  # noqa

        self.assertIsInstance(lp.input.input, ProjectingJoin)
        self.assertEquals(2 * len(self.x_scheme),
                          len(lp.input.input.scheme()))

        pp = self.logical_to_physical(lp)
        self.assertIsInstance(pp.input, MyriaSplitConsumer)
        proj_join = pp.input.input.input
        self.assertIsInstance(proj_join, ProjectingJoin)
        self.assertEquals(1, len(proj_join.scheme()))
        self.assertEquals(2, len(proj_join.left.scheme()))
        self.assertEquals(1, len(proj_join.right.scheme()))

        expected = collections.Counter(
            [(b,)
             for (a, b, c) in self.x_data
             for (d, e, f) in self.x_data
             if a == d])

        self.db.evaluate(pp)
        result = self.db.get_temp_table('OUTPUT')
        self.assertEquals(result, expected)

    def test_push_selects_apply(self):
        """Test pushing selections through apply."""
        lp = StoreTemp('OUTPUT',
               Select(expression.LTEQ(AttRef("c"), AttRef("a")),
                 Select(expression.LTEQ(AttRef("b"), AttRef("c")),
                   Apply([('b', AttIndex(1)),
                          ('c', AttIndex(2)),
                          ('a', AttIndex(0))],
                         Scan(self.x_key, self.x_scheme)))))  # noqa

        expected = collections.Counter(
            [(b, c, a) for (a, b, c) in self.x_data if c <= a and b <= c])

        self.assertEquals(self.get_count(lp, Select), 2)
        self.assertEquals(self.get_count(lp, Scan), 1)
        self.assertIsInstance(lp.input, Select)

        pp = self.logical_to_physical(lp)
        self.assertIsInstance(pp.input, Apply)
        self.assertEquals(self.get_count(pp, Select), 1)

        self.db.evaluate(pp)
        result = self.db.get_temp_table('OUTPUT')
        self.assertEquals(result, expected)

    def test_push_selects_groupby(self):
        """Test pushing selections through groupby."""
        lp = StoreTemp('OUTPUT',
               Select(expression.LTEQ(AttRef("c"), AttRef("a")),
                 Select(expression.LTEQ(AttRef("b"), AttRef("c")),
                   GroupBy([AttIndex(1), AttIndex(2), AttIndex(0)],
                           [expression.COUNTALL()],
                           Scan(self.x_key, self.x_scheme)))))  # noqa

        expected = collections.Counter(
            [(b, c, a) for (a, b, c) in self.x_data if c <= a and b <= c])
        expected = collections.Counter(k + (v,) for k, v in expected.items())

        self.assertEquals(self.get_count(lp, Select), 2)
        self.assertEquals(self.get_count(lp, Scan), 1)
        self.assertIsInstance(lp.input, Select)

        pp = self.logical_to_physical(lp)
        self.assertIsInstance(pp.input, MyriaSplitConsumer)
        self.assertIsInstance(pp.input.input.input, GroupBy)
        self.assertEquals(self.get_count(pp, Select), 1)

        self.db.evaluate(pp)
        result = self.db.get_temp_table('OUTPUT')
        self.assertEquals(result, expected)

    def test_noop_apply_removed(self):
        lp = StoreTemp('OUTPUT',
               Apply([(None, AttIndex(1))],
                 ProjectingJoin(expression.EQ(AttIndex(0), AttIndex(3)),
                   Scan(self.x_key, self.x_scheme),
                   Scan(self.x_key, self.x_scheme),
                   [AttIndex(i) for i in xrange(2 * len(self.x_scheme))])))  # noqa

        self.assertIsInstance(lp.input, Apply)
        lp_scheme = lp.scheme()

        pp = self.logical_to_physical(lp)
        self.assertNotIsInstance(pp.input, Apply)
        self.assertEquals(lp_scheme, pp.scheme())

    def test_not_noop_apply_not_removed(self):
        lp = StoreTemp('OUTPUT',
               Apply([('hi', AttIndex(1))],
                 ProjectingJoin(expression.EQ(AttIndex(0), AttIndex(3)),
                   Scan(self.x_key, self.x_scheme),
                   Scan(self.x_key, self.x_scheme),
                   [AttIndex(i) for i in xrange(2 * len(self.x_scheme))])))  # noqa

        self.assertIsInstance(lp.input, Apply)
        lp_scheme = lp.scheme()

        pp = self.logical_to_physical(lp)
        self.assertIsInstance(pp.input, Apply)
        self.assertEquals(lp_scheme, pp.scheme())

    def test_extract_join(self):
        """Extract a join condition from the middle of complex select."""
        s = expression.AND(expression.LTEQ(AttRef("e"), AttRef("f")),
                           expression.AND(
                               expression.EQ(AttRef("c"), AttRef("d")),
                               expression.GT(AttRef("a"), AttRef("b"))))

        lp = StoreTemp('OUTPUT', Select(s, CrossProduct(
            Scan(self.x_key, self.x_scheme),
            Scan(self.y_key, self.y_scheme))))

        self.assertEquals(self.get_num_select_conjuncs(lp), 3)

        pp = self.logical_to_physical(lp)

        # non-equijoin conditions should get pushed separately below the join
        self.assertIsInstance(pp.input, MyriaSplitConsumer)
        self.assertIsInstance(pp.input.input.input, Join)
        self.assertEquals(self.get_count(pp, CrossProduct), 0)
        self.assertEquals(self.get_count(pp, Select), 2)

        self.db.evaluate(pp)
        result = self.db.get_temp_table('OUTPUT')
        self.assertEquals(result, self.expected)

    def test_multi_condition_join(self):
        s = expression.AND(expression.EQ(AttRef("c"), AttRef("d")),
                           expression.EQ(AttRef("a"), AttRef("f")))

        lp = StoreTemp('OUTPUT', Select(s, CrossProduct(
            Scan(self.x_key, self.x_scheme),
            Scan(self.y_key, self.y_scheme))))

        self.assertEquals(self.get_num_select_conjuncs(lp), 2)

        pp = self.logical_to_physical(lp)
        self.assertEquals(self.get_count(pp, CrossProduct), 0)
        self.assertEquals(self.get_count(pp, Select), 0)

        expected = collections.Counter(
            [(a, b, c, d, e, f) for (a, b, c) in self.x_data
             for (d, e, f) in self.y_data if a == f and c == d])

        self.db.evaluate(pp)
        result = self.db.get_temp_table('OUTPUT')
        self.assertEquals(result, expected)

    def test_multiway_join_left_deep(self):

        query = """
        T = SCAN(public:adhoc:Z);
        U = [FROM T AS T1, T AS T2, T AS T3
             WHERE T1.dst==T2.src AND T2.dst==T3.src
             EMIT T1.src AS x, T3.dst AS y];
        STORE(U, OUTPUT);
        """

        lp = self.get_logical_plan(query)
        self.assertEquals(self.get_count(lp, CrossProduct), 2)
        self.assertEquals(self.get_count(lp, Join), 0)

        pp = self.logical_to_physical(lp)
        self.assertEquals(self.get_count(pp, CrossProduct), 0)
        self.assertEquals(self.get_count(pp, Join), 2)
        self.assertEquals(self.get_count(pp, MyriaShuffleProducer), 4)
        self.assertEquals(self.get_count(pp, NaryJoin), 0)
        self.assertEquals(self.get_count(pp, MyriaHyperShuffleProducer), 0)

        self.db.evaluate(pp)
        result = self.db.get_table('OUTPUT')
        self.assertEquals(result, self.expected2)

    def test_multiway_join_hyper_cube(self):

        query = """
        T = SCAN(public:adhoc:Z);
        U = [FROM T AS T1, T AS T2, T AS T3
             WHERE T1.dst==T2.src AND T2.dst==T3.src
             EMIT T1.src AS x, T3.dst AS y];
        STORE(U, OUTPUT);
        """

        lp = self.get_logical_plan(query)
        self.assertEquals(self.get_count(lp, CrossProduct), 2)
        self.assertEquals(self.get_count(lp, Join), 0)

        pp = self.logical_to_physical(lp, hypercube=True)
        self.assertEquals(self.get_count(pp, CrossProduct), 0)
        self.assertEquals(self.get_count(pp, Join), 0)
        self.assertEquals(self.get_count(pp, MyriaShuffleProducer), 0)
        self.assertEquals(self.get_count(pp, NaryJoin), 1)
        self.assertEquals(self.get_count(pp, MyriaHyperShuffleProducer), 3)

        self.db.evaluate(pp)
        result = self.db.get_table('OUTPUT')
        self.assertEquals(result, self.expected2)

    def test_hyper_cube_tie_breaking_heuristic(self):
        query = """
        T = SCAN(public:adhoc:Z);
        U = [FROM T AS T1, T AS T2, T AS T3, T AS T4
             WHERE T1.dst=T2.src AND T2.dst=T3.src AND
                   T3.dst=T4.src AND T4.dst=T1.src
             EMIT T1.src AS x, T3.dst AS y];
        STORE(U, OUTPUT);
        """
        lp = self.get_logical_plan(query)
        pp = self.logical_to_physical(lp, hypercube=True)

        def get_max_dim_size(_op):
            if isinstance(_op, MyriaHyperShuffleProducer):
                yield max(_op.hyper_cube_dimensions)

        # the max hypercube dim size will be 8, e.g (1, 8, 1, 8) without
        # tie breaking heuristic, now it is (2, 4, 2, 4)
        self.assertTrue(max(pp.postorder(get_max_dim_size)) <= 4)

    def test_naryjoin_merge(self):
        query = """
        T1 = scan(public:adhoc:Z);
        T2 = [from T1 emit count(dst) as dst, src];
        T3 = scan(public:adhoc:Z);
        twohop = [from T1, T2, T3
                  where T1.dst = T2.src and T2.dst = T3.src
                  emit *];
        store(twohop, anothertwohop);
        """
        statements = self.parser.parse(query)
        self.processor.evaluate(statements)
        lp = self.processor.get_logical_plan()
        pp = self.logical_to_physical(lp, hypercube=True)
        self.assertEquals(self.get_count(pp, NaryJoin), 0)

    def test_right_deep_join(self):
        """Test pushing a selection into a right-deep join tree.

        Myrial doesn't emit these, so we need to cook up a plan by hand."""

        s = expression.AND(expression.EQ(AttIndex(1), AttIndex(2)),
                           expression.EQ(AttIndex(3), AttIndex(4)))

        lp = Apply([('x', AttIndex(0)), ('y', AttIndex(5))],
                   Select(s,
                          CrossProduct(Scan(self.z_key, self.z_scheme),
                                       CrossProduct(
                                           Scan(self.z_key, self.z_scheme),
                                           Scan(self.z_key, self.z_scheme)))))
        lp = StoreTemp('OUTPUT', lp)

        self.assertEquals(self.get_count(lp, CrossProduct), 2)

        pp = self.logical_to_physical(lp)
        self.assertEquals(self.get_count(pp, CrossProduct), 0)

        self.db.evaluate(pp)

        result = self.db.get_temp_table('OUTPUT')
        self.assertEquals(result, self.expected2)

    def test_explicit_shuffle(self):
        """Test of a user-directed partition operation."""

        query = """
        T = SCAN(public:adhoc:X);
        STORE(T, OUTPUT, [$2, b]);
        """
        statements = self.parser.parse(query)
        self.processor.evaluate(statements)
        lp = self.processor.get_logical_plan()

        self.assertEquals(self.get_count(lp, Shuffle), 1)

        for op in lp.walk():
            if isinstance(op, Shuffle):
                self.assertEquals(op.columnlist, [AttIndex(2), AttIndex(1)])

    def test_shuffle_before_distinct(self):
        query = """
        T = DISTINCT(SCAN(public:adhoc:Z));
        STORE(T, OUTPUT);
        """

        pp = self.get_physical_plan(query)
        self.assertEquals(self.get_count(pp, Distinct), 2)  # distributed
        first = True
        for op in pp.walk():
            if isinstance(op, Distinct):
                self.assertIsInstance(op.input, MyriaShuffleConsumer)
                self.assertIsInstance(op.input.input, MyriaShuffleProducer)
                break

    def test_shuffle_before_difference(self):
        query = """
        T = DIFF(SCAN(public:adhoc:Z), SCAN(public:adhoc:Z));
        STORE(T, OUTPUT);
        """

        pp = self.get_physical_plan(query)
        self.assertEquals(self.get_count(pp, Difference), 1)
        for op in pp.walk():
            if isinstance(op, Difference):
                self.assertIsInstance(op.left, MyriaShuffleConsumer)
                self.assertIsInstance(op.left.input, MyriaShuffleProducer)
                self.assertIsInstance(op.right, MyriaShuffleConsumer)
                self.assertIsInstance(op.right.input, MyriaShuffleProducer)

    def test_bug_240_broken_remove_unused_columns_rule(self):
        query = """
        particles = empty(nowGroup:int, timestep:int, grp:int);

        haloTable1 = [from particles as P
                      emit P.nowGroup,
                           (P.timestep+P.grp) as halo,
                           count(*) as totalParticleCount];

        haloTable2 = [from haloTable1 as H, particles as P
                      where H.nowGroup = P.nowGroup
                      emit *];
        store(haloTable2, OutputTemp);
        """

        # This is it -- just test that we can get the physical plan and
        # compile to JSON. See https://github.com/uwescience/raco/issues/240
        pp = self.execute_query(query, output='OutputTemp')

    def test_broadcast_cardinality_right(self):
        # x and y have the same cardinality, z is smaller
        query = """
        x = scan({x});
        y = scan({y});
        z = scan({z});
        out = [from x, z emit *];
        store(out, OUTPUT);
        """.format(x=self.x_key, y=self.y_key, z=self.z_key)

        pp = self.get_physical_plan(query)
        counter = 0
        for op in pp.walk():
            if isinstance(op, CrossProduct):
                counter += 1
                self.assertIsInstance(op.right, MyriaBroadcastConsumer)
        self.assertEquals(counter, 1)

    def test_broadcast_cardinality_left(self):
        # x and y have the same cardinality, z is smaller
        query = """
        x = scan({x});
        y = scan({y});
        z = scan({z});
        out = [from z, y emit *];
        store(out, OUTPUT);
        """.format(x=self.x_key, y=self.y_key, z=self.z_key)

        pp = self.get_physical_plan(query)
        counter = 0
        for op in pp.walk():
            if isinstance(op, CrossProduct):
                counter += 1
                self.assertIsInstance(op.left, MyriaBroadcastConsumer)
        self.assertEquals(counter, 1)

    def test_broadcast_cardinality_with_agg(self):
        # x and y have the same cardinality, z is smaller
        query = """
        x = scan({x});
        y = countall(scan({y}));
        z = scan({z});
        out = [from y, z emit *];
        store(out, OUTPUT);
        """.format(x=self.x_key, y=self.y_key, z=self.z_key)

        pp = self.get_physical_plan(query)
        counter = 0
        for op in pp.walk():
            if isinstance(op, CrossProduct):
                counter += 1
                self.assertIsInstance(op.left, MyriaBroadcastConsumer)
        self.assertEquals(counter, 1)

    def test_relation_cardinality(self):
        query = """
        x = scan({x});
        out = [from x as x1, x as x2 emit *];
        store(out, OUTPUT);
        """.format(x=self.x_key)
        lp = self.get_logical_plan(query)
        self.assertIsInstance(lp, Sequence)
        self.assertEquals(1, len(lp.children()))
        self.assertEquals(sum(self.x_data.values()) ** 2,
                          lp.children()[0].num_tuples())

    def test_relation_physical_cardinality(self):
        query = """
        x = scan({x});
        out = [from x as x1, x as x2 emit *];
        store(out, OUTPUT);
        """.format(x=self.x_key)

        pp = self.get_physical_plan(query)
        self.assertEquals(sum(self.x_data.values()) ** 2,
                          pp.num_tuples())

    def test_catalog_cardinality(self):
        self.assertEquals(sum(self.x_data.values()),
                          self.db.num_tuples(self.x_key))
        self.assertEquals(sum(self.y_data.values()),
                          self.db.num_tuples(self.y_key))
        self.assertEquals(sum(self.z_data.values()),
                          self.db.num_tuples(self.z_key))

    def test_groupby_to_distinct(self):
        query = """
        x = scan({x});
        y = select $0, count(*) from x;
        z = select $0 from y;
        store(z, OUTPUT);
        """.format(x=self.x_key)

        lp = self.get_logical_plan(query)
        self.assertEquals(self.get_count(lp, GroupBy), 1)
        self.assertEquals(self.get_count(lp, Distinct), 0)

        pp = self.logical_to_physical(copy.deepcopy(lp))
        self.assertEquals(self.get_count(pp, GroupBy), 0)
        self.assertEquals(self.get_count(pp, Distinct), 2)  # distributed

        self.assertEquals(self.db.evaluate(lp), self.db.evaluate(pp))

    def test_groupby_to_lesser_groupby(self):
        query = """
        x = scan({x});
        y = select $0, count(*), sum($1) from x;
        z = select $0, $2 from y;
        store(z, OUTPUT);
        """.format(x=self.x_key)

        lp = self.get_logical_plan(query)
        self.assertEquals(self.get_count(lp, GroupBy), 1)
        for op in lp.walk():
            if isinstance(op, GroupBy):
                self.assertEquals(len(op.grouping_list), 1)
                self.assertEquals(len(op.aggregate_list), 2)

        pp = self.logical_to_physical(copy.deepcopy(lp))
        self.assertEquals(self.get_count(pp, GroupBy), 2)  # distributed
        for op in pp.walk():
            if isinstance(op, GroupBy):
                self.assertEquals(len(op.grouping_list), 1)
                self.assertEquals(len(op.aggregate_list), 1)

        self.assertEquals(self.db.evaluate(lp), self.db.evaluate(pp))

    def __run_uda_test(self, uda_state=None):
        scan = Scan(self.x_key, self.x_scheme)

        init_ex = expression.NumericLiteral(0)
        update_ex = expression.PLUS(expression.NamedStateAttributeRef("value"),
                                    AttIndex(1))
        emit_ex = expression.UdaAggregateExpression(
            expression.NamedStateAttributeRef("value"), uda_state)
        statemods = [StateVar("value", init_ex, update_ex)]

        log_gb = GroupBy([AttIndex(0)], [emit_ex], scan, statemods)

        lp = StoreTemp('OUTPUT', log_gb)
        pp = self.logical_to_physical(copy.deepcopy(lp))

        self.db.evaluate(lp)
        log_result = self.db.get_temp_table('OUTPUT')

        self.db.delete_temp_table('OUTPUT')
        self.db.evaluate(pp)
        phys_result = self.db.get_temp_table('OUTPUT')

        self.assertEquals(log_result, phys_result)
        self.assertEquals(len(log_result), 15)

        self.assertEquals(self.get_count(pp, MyriaShuffleProducer), 1)
        self.assertEquals(self.get_count(pp, MyriaShuffleConsumer), 1)

        return pp

    def test_non_decomposable_uda(self):
        """Test that optimization preserves the value of a non-decomposable UDA
        """
        pp = self.__run_uda_test()

        for op in pp.walk():
            if isinstance(op, MyriaShuffleProducer):
                self.assertEquals(op.hash_columns, [AttIndex(0)])
                self.assertEquals(self.get_count(op, GroupBy), 0)

    def test_decomposable_uda(self):
        """Test that optimization preserves the value of decomposable UDAs"""
        lemits = [expression.UdaAggregateExpression(
                  expression.NamedStateAttributeRef("value"))]
        remits = copy.deepcopy(lemits)

        init_ex = expression.NumericLiteral(0)
        update_ex = expression.PLUS(expression.NamedStateAttributeRef("value"),
                                    AttIndex(1))
        lstatemods = [StateVar("value", init_ex, update_ex)]
        rstatemods = copy.deepcopy(lstatemods)

        uda_state = expression.DecomposableAggregateState(
            lemits, lstatemods, remits, rstatemods)
        pp = self.__run_uda_test(uda_state)

        self.assertEquals(self.get_count(pp, GroupBy), 2)

        for op in pp.walk():
            if isinstance(op, MyriaShuffleProducer):
                self.assertEquals(op.hash_columns, [AttIndex(0)])
                self.assertEquals(self.get_count(op, GroupBy), 1)

    def test_successful_append(self):
        """Insert an append if storing a relation into itself with a
        UnionAll."""
        query = """
        x = scan({x});
        y = select $0 from x;
        y2 = select $1 from x;
        y = y+y2;
        store(y, OUTPUT);
        """.format(x=self.x_key)

        lp = self.get_logical_plan(query, apply_chaining=False)
        self.assertEquals(self.get_count(lp, ScanTemp), 5)
        self.assertEquals(self.get_count(lp, StoreTemp), 4)
        self.assertEquals(self.get_count(lp, AppendTemp), 0)
        self.assertEquals(self.get_count(lp, Store), 1)
        self.assertEquals(self.get_count(lp, Scan), 1)

        pp = self.logical_to_physical(copy.deepcopy(lp))
        self.assertEquals(self.get_count(pp, ScanTemp), 4)
        self.assertEquals(self.get_count(pp, StoreTemp), 3)
        self.assertEquals(self.get_count(pp, AppendTemp), 1)
        self.assertEquals(self.get_count(pp, Store), 1)
        self.assertEquals(self.get_count(pp, Scan), 1)

        self.assertEquals(self.db.evaluate(lp), self.db.evaluate(pp))

    def test_failed_append(self):
        """Do not insert an append when the tuples to be appended
        depend on the relation itself."""

        # NB test in both the left and right directions
        # left: y = y + y2
        # right: y = y2 + y
        query = """
        x = scan({x});
        y = select $0, $1 from x;
        t = empty(a:int);
        y2 = select $1, $1 from y;
        y = y+y2;
        t = empty(a:int);
        y3 = select $1, $1 from y;
        y = y3+y;
        s = empty(a:int);
        store(y, OUTPUT);
        """.format(x=self.x_key)

        lp = self.get_logical_plan(query, dead_code_elimination=False)
        self.assertEquals(self.get_count(lp, AppendTemp), 0)

        # No AppendTemp
        pp = self.logical_to_physical(copy.deepcopy(lp))
        self.assertEquals(self.get_count(pp, AppendTemp), 0)

        self.assertEquals(self.db.evaluate(lp), self.db.evaluate(pp))

    def test_push_work_into_sql(self):
        """Test generation of MyriaQueryScan operator for query with
        projects"""
        query = """
        r3 = scan({x});
        intermediate = select a, c from r3;
        store(intermediate, OUTPUT);
        """.format(x=self.x_key)

        pp = self.get_physical_plan(query, push_sql=True)
        self.assertEquals(self.get_count(pp, Operator), 2)
        self.assertTrue(isinstance(pp.input, MyriaQueryScan))

        expected = collections.Counter([(a, c) for (a, b, c) in self.x_data])

        self.db.evaluate(pp)
        result = self.db.get_table('OUTPUT')
        self.assertEquals(result, expected)

    def test_push_work_into_sql_2(self):
        """Test generation of MyriaQueryScan operator for query with projects
        and a filter"""
        query = """
        r3 = scan({x});
        intermediate = select a, c from r3 where b < 5;
        store(intermediate, OUTPUT);
        """.format(x=self.x_key)

        pp = self.get_physical_plan(query, push_sql=True)
        self.assertEquals(self.get_count(pp, Operator), 2)
        self.assertTrue(isinstance(pp.input, MyriaQueryScan))

        expected = collections.Counter([(a, c)
                                        for (a, b, c) in self.x_data
                                        if b < 5])

        self.db.evaluate(pp)
        result = self.db.get_table('OUTPUT')
        self.assertEquals(result, expected)

    def test_no_push_when_shuffle(self):
        """When data is not co-partitioned, the join should not be pushed."""
        query = """
        r3 = scan({x});
        s3 = scan({y});
        intermediate = select r3.a, s3.f from r3, s3 where r3.b=s3.e;
        store(intermediate, OUTPUT);
        """.format(x=self.x_key, y=self.y_key)

        pp = self.get_physical_plan(query, push_sql=True)
        # Join is not pushed
        self.assertEquals(self.get_count(pp, Join), 1)
        # The projections are pushed into the QueryScan
        self.assertEquals(self.get_count(pp, MyriaQueryScan), 2)
        # We should not need any Apply since there is no rename and no other
        # project.
        self.assertEquals(self.get_count(pp, Apply), 0)

        expected = collections.Counter([(a, f)
                                        for (a, b, c) in self.x_data
                                        for (d, e, f) in self.y_data
                                        if b == e])

        self.db.evaluate(pp)
        result = self.db.get_table('OUTPUT')
        self.assertEquals(result, expected)

    def test_no_push_when_random(self):
        """Selection with RANDOM() doesn't push through joins"""
        query = """
        r = scan({x});
        s = scan({y});
        t = [from r,s where random()*10 > .3 emit *];
        store(t, OUTPUT);
        """.format(x=self.x_key, y=self.y_key)

        lp = self.get_logical_plan(query)
        self.assertEquals(self.get_count(lp, Select), 1)
        self.assertEquals(self.get_count(lp, CrossProduct), 1)

        pp = self.logical_to_physical(lp)
        self.assertEquals(self.get_count(pp, Select), 1)
        self.assertEquals(self.get_count(pp, CrossProduct), 1)
        # The selection should happen after the cross product
        for op in pp.walk():
            if isinstance(op, Select):
                self.assertIsInstance(op.input, MyriaSplitConsumer)
                self.assertIsInstance(op.input.input.input, CrossProduct)
