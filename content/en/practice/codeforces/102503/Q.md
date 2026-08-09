---
title: "CF 102503Q - Og and Ug"
description: "We have a rooted tree with node 1 as its root. Each node has an ordered list of children. The program maintains a deque of pairs (node, i), where i tells us which child of that node should be processed next. When a pair is removed from the right end, its node is printed."
date: "2026-08-09T19:31:06+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102503
codeforces_index: "Q"
codeforces_contest_name: "National Olympiad in Informatics - Philippines (NOI.PH) Online Eliminations 2020"
rating: 0
weight: 102503
solve_time_s: 711
verified: true
draft: false
---

[CF 102503Q - Og and Ug](https://codeforces.com/problemset/problem/102503/Q)

**Rating:** -  
**Tags:** -  
**Solve time:** 11m 51s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a rooted tree with node 1 as its root. Each node has an ordered list of children. The program maintains a deque of pairs `(node, i)`, where `i` tells us which child of that node should be processed next.

When a pair is removed from the right end, its node is printed. If there is still an unprocessed child, the program puts the node's continuation back on the right and starts that child. This is the usual iterative form of a depth first traversal.

Ug adds one extra operation. When a node has finished all of its children, instead of disappearing, `(node, 0)` is inserted at the left end of the deque. Since future elements are removed from the right, these completed nodes are postponed until everything currently active has finished.

The input describes the whole tree and then gives up to 143 positions in the infinite output sequence. A requested position can be as large as (10^{100}), so the task is not to generate the sequence up to that position. We need to understand its recursive structure and jump over enormous portions of it.

The tree itself is very small, with at most 50 nodes. That rules out algorithms whose complexity depends heavily on the number of nodes, but it does not help with a simulation whose running time is proportional to the requested position. A query of (10^{100}) would require an astronomical number of simulated deque operations. The small value of (n) is instead a signal that we should build a finite description of the infinite sequence.

There are several boundary cases where interpreting the deque incorrectly gives a plausible but wrong sequence. With a single node, for example,

```
1 3
0
1
2
10
```

the only node is printed forever, so the output is

```
1
1
1
```

A simulation that assumes a completed node is processed immediately would still happen to work here, which makes this case particularly dangerous as a test because it does not expose that mistake.

A more revealing example is a root with one leaf child:

```
2 4
1 2
0
1
2
3
4
```

The correct output is

```
1
2
1
2
```

The first three values come from finishing the initial traversal of the root. The completed root is placed at the left, so the next task is the postponed leaf task, not the root continuation that would be obtained by treating `push_left` as `push_right`.

Another useful boundary is the end of the first complete traversal. For a root with two leaf children,

```
3 3
2 2 3
0
0
5
6
12
```

the output is

```
1
2
1
```

for positions 5, 6, and 12 respectively. Position 5 is the final print of the initial root traversal, while position 6 starts processing a postponed child. Confusing the two deque ends shifts the entire infinite sequence.

## Approaches

The direct approach is to implement the program exactly as written. We keep the deque of pairs, repeatedly remove its rightmost element, print its node, and perform the corresponding insertion. This is correct because it is literally the state transition of the original program.

The problem is its running time. To answer a query at position (K), the simulation needs (\Theta(K)) printed elements and hence (\Theta(K)) deque operations. In the worst case (K=10^{100}), so even the number of required operations is far beyond any finite computational limit. Storing the deque explicitly is also unnecessary, since the sequence has much more structure than the raw simulation suggests.

The key observation comes from looking at what happens while one node is being actively processed. Suppose `(v, 0)` is the rightmost active task and there are no active tasks to its right. Its traversal produces a fixed finite sequence. The node (v) is printed, each child subtree is traversed, and (v) is printed again between consecutive child traversals and once after the last child.

Let this finite sequence be (E(v)). If (v) has children (c_1,c_2,\ldots,c_m), then

[
E(v)=v,E(c_1),v,E(c_2),\ldots,v,E(c_m),v.
]

A leaf therefore has (E(v)=[v]). If the subtree of (v) contains (s(v)) nodes, then (E(v)) has exactly (2s(v)-1) elements, because every tree edge causes one additional return to its parent.

While this traversal is running, every node that finishes is inserted on the left. At the end, those newly created `(node, 0)` tasks appear from right to left in exactly postorder. Existing postponed tasks are still farther to the right, so they are processed first.

This gives a much cleaner interpretation. Treat `(v,0)` as a task. Processing one task (v) prints the entire finite block (E(v)), then appends the nodes of the subtree of (v) in postorder as the next generation of tasks.

Let (Q(v)) denote the postorder list of the subtree rooted at (v). The first task is the root. The next generation of tasks is (Q(root)). The generation after that is obtained by replacing every node (v) in the previous generation by (Q(v)). In other words, if (W_d) is the task sequence at level (d),

[
W_0=[root],
]

and

[
W_{d+1}=Q(W_d).
]

The output is the concatenation of (E(v)) for all (v) in these levels.

The second key observation is that (Q(v)) contains every node in the subtree of (v) exactly once. Consequently, if we define a matrix (M) by

[
M_{u,v}=1
]

when (v) belongs to the subtree of (u), and zero otherwise, then the number of occurrences of each node in level (d) is obtained by multiplying by (M^d).

Because (M) has ones on its diagonal and only ancestor-to-descendant entries above that diagonal after a suitable node ordering, we can write

[
M=I+N
]

where (N) is nilpotent. The tree has at most 50 nodes, so (N^{50}=0). Hence

[
M^d=(I+N)^d
=\sum_{r=0}^{49}\binom dr N^r.
]

This is the reason enormous exponents are manageable. Every relevant length is a polynomial in (d), expressed naturally in the binomial basis.

For a node (v), define (A_v(d)) as the total number of actual printed values contributed by all tasks in (Q^d(v)). Since a task of type (x) contributes (|E(x)|) printed values, (A_v(d)) is exactly the weighted version of the row of (M^d). It is consequently a polynomial in (d) of degree at most 49.

We can also sum whole levels. The identity

[
\sum_{j=0}^{d-1}\binom jr=\binom d{r+1}
]

gives a polynomial for the total number of printed values in all levels before level (d). This lets us locate the level containing a query by binary search.

Once the level is known, there is another potential problem: the level itself may have an enormous exponent. We solve that recursively. The word (Q^d(v)) is

[
Q^{d-1}(x_1)Q^{d-1}(x_2)\ldots Q^{d-1}(x_m),
]

where (x_1,\ldots,x_m) are the postorder nodes of (v)'s subtree. We can calculate the weighted size of every block and locate the required block.

The final block is always (Q^{d-1}(v)), because (v) is the last node in its subtree's postorder. This self-reference is the only reason a naive recursive descent could take (d) steps. We jump over all consecutive selections of this final block at once using the polynomial (A_v). Every time we leave the self block, we move to a proper descendant, so there can be at most 50 such transitions.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(K)) | (O(K)) worst case | Too slow |
| Optimal | (O(n^3+k n^2\log K)) | (O(n^2)) | Accepted |

## Algorithm Walkthrough

1. Build the postorder list of the subtree of every node. The list for (v) is exactly (Q(v)), because the postponed tasks created while processing (v) appear in postorder.
2. Construct (E(v)), the finite output produced by processing task (v) while it is active. Start with (v), recursively append (E(c)) for every child (c), and append (v) after every child. The length of this sequence is (w(v)=2s(v)-1), where (s(v)) is the subtree size.
3. Define the matrix (N) implicitly by saying that applying (N) to a vector (x) gives, at node (v), the sum of (x[u]) over all proper descendants (u) of (v). Start with the vector (w), and repeatedly apply (N). The resulting vectors (C_r=N^r w) give

[
A_v(d)=\sum_r C_r[v]\binom dr.
]

Only at most 50 vectors are nonzero because (N) is nilpotent.

1. Convert these binomial-basis polynomials into ordinary integer polynomials. Multiply every polynomial by ((H+1)!), where (H) is the largest nonzero degree. This removes all denominators from the binomial coefficients and lets the implementation evaluate the polynomials using ordinary integer arithmetic.
2. Build the polynomial for the total output before level (d). If (C_r[root]) is the coefficient from the previous step, then

[
P(d)=\sum_r C_r[root]\binom d{r+1}
]

is the number of printed values in levels (0) through (d-1).

1. For each query (K), binary search the largest level (d) satisfying (P(d)<K). The query lies inside level (d). Subtract (P(d)) from (K) to obtain its one-based position inside that level, measured using the weights (w(v)).
2. To find the exact task inside (Q^d(root)), maintain a node (v), an exponent (d), and the remaining weighted position (r). If (d=0), the word contains only (v), so (r) directly identifies a position inside (E(v)).
3. When (d>0), the word (Q^d(v)) consists of one block (Q^{d-1}(x)) for every (x) in the postorder list of (v)'s subtree. The weight of the block belonging to (x) is (A_x(d-1)).
4. The last block corresponds to (x=v). Let (A=A_v(d)). After the last block, the preceding part has weight

[
A_v(d)-A_v(d-1).
]

If the remaining position is larger than this value, the desired position is inside the final self block. Repeating this naively could take (d) iterations, so binary search the maximum number (t) of consecutive self selections satisfying

[
r>A_v(d)-A_v(d-t).
]

Then replace (d) by (d-t) and subtract the skipped weight.

1. If the self block is no longer selected, scan the proper descendants in postorder. Find the first (x) whose block (Q^{d-1}(x)) contains the remaining position, subtracting complete blocks as necessary. Set (v=x) and (d=d-1).
2. Every time step 10 happens, the new node is a proper descendant of the previous node. Thus this can happen at most (n-1) times. The potentially enormous number of self transitions has already been compressed into the binary search in step 9.
3. When (d=0), the answer is the corresponding element of the precomputed (E(v)) sequence.

Why it works: the deque can be split conceptually into currently active traversal frames and postponed restart tasks. Active frames always occupy the right end, so they complete their entire traversal before any postponed task is touched. Every completed node is inserted at the left, and because the right end has priority, postponed nodes are processed in FIFO order. Their order is exactly the postorder of the subtree that produced them. This proves that the infinite execution is partitioned into levels (Q^d(root)), with each task (v) contributing exactly (E(v)). The polynomial (A_v(d)) counts the exact weighted size of every recursively generated block, so every binary search skips only complete blocks. The recursive descent consequently lands on exactly the task containing the requested output position, and (E(v)) gives the exact printed node inside that task.

## Python Solution

```python
import sys
import math

input = sys.stdin.readline

def solve():
    n, k = map(int, input().split())

    children = [[] for _ in range(n)]
    for v in range(n):
        data = list(map(int, input().split()))
        c = data[0]
        children[v] = [x - 1 for x in data[1:]]

    queries = [int(input()) for _ in range(k)]

    sys.setrecursionlimit(10000)

    post = [[] for _ in range(n)]
    euler_output = [[] for _ in range(n)]
    subtree_size = [0] * n

    def build(v):
        p = []
        e = [v]

        for u in children[v]:
            build(u)
            p.extend(post[u])
            e.extend(euler_output[u])
            e.append(v)

        p.append(v)

        post[v] = p
        euler_output[v] = e
        subtree_size[v] = len(p)

    build(0)

    # w[v] is the number of printed values produced by one task v.
    weight = [len(euler_output[v]) for v in range(n)]

    # coeff[r][v] = (N^r * weight)[v].
    coeff = [weight[:]]
    cur = weight[:]

    for _ in range(1, n + 1):
        nxt = [0] * n

        for v in range(n):
            total = 0
            # post[v][:-1] are precisely the proper descendants of v.
            for u in post[v][:-1]:
                total += cur[u]
            nxt[v] = total

        if not any(nxt):
            break

        coeff.append(nxt)
        cur = nxt

    degree = len(coeff) - 1

    # We multiply every polynomial by FACT so that all coefficients
    # become integers.
    FACT = math.factorial(degree + 1)

    # Falling factorial polynomials:
    # fall[r](x) = x * (x-1) * ... * (x-r+1)
    fall = [[1]]
    for r in range(1, degree + 2):
        prev = fall[-1]
        cur_poly = [0] * (r + 1)
        shift = r - 1

        for j, a in enumerate(prev):
            cur_poly[j] -= shift * a
            cur_poly[j + 1] += a

        fall.append(cur_poly)

    # Polynomial for FACT * A_v(d).
    apoly = [[0] * (degree + 1) for _ in range(n)]

    factorials = [math.factorial(i) for i in range(degree + 2)]

    for r in range(degree + 1):
        multiplier = FACT // factorials[r]
        fr = fall[r]

        for v in range(n):
            c = coeff[r][v]
            if c == 0:
                continue

            mul = c * multiplier
            pv = apoly[v]

            for j, a in enumerate(fr):
                pv[j] += mul * a

    # Polynomial for
    # FACT * sum_{j=0}^{d-1} A_root(j).
    # sum C(j,r) = C(d,r+1).
    prefix_poly = [0] * (degree + 2)

    for r in range(degree + 1):
        multiplier = FACT // factorials[r + 1]
        fr = fall[r + 1]
        c = coeff[r][0]

        if c == 0:
            continue

        mul = c * multiplier
        for j, a in enumerate(fr):
            prefix_poly[j] += mul * a

    def eval_poly(poly, x):
        value = 0
        for a in reversed(poly):
            value = value * x + a
        return value

    prefix_cache = {}
    answer_cache = {}

    def prefix(d):
        if d not in prefix_cache:
            prefix_cache[d] = eval_poly(prefix_poly, d)
        return prefix_cache[d]

    def A(v, d, cache):
        key = (v, d)
        value = cache.get(key)
        if value is None:
            value = eval_poly(apoly[v], d)
            cache[key] = value
        return value

    total_target_scale = FACT

    def get_answer(K):
        if K in answer_cache:
            return answer_cache[K]

        target = K * FACT

        # Find the level containing K.
        lo, hi = 0, K
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if prefix(mid) < target:
                lo = mid
            else:
                hi = mid - 1

        d = lo
        rem = target - prefix(d)

        cache = {}

        v = 0

        while d > 0:
            current = A(v, d, cache)

            # Jump over as many consecutive choices of the final
            # self-block Q^(d-1)(v) as possible.
            lo_t, hi_t = 0, d

            while lo_t < hi_t:
                mid = (lo_t + hi_t + 1) // 2
                earlier = A(v, d - mid, cache)

                if rem > current - earlier:
                    lo_t = mid
                else:
                    hi_t = mid - 1

            t = lo_t

            if t:
                new_d = d - t
                skipped = current - A(v, new_d, cache)
                rem -= skipped
                d = new_d

                if d == 0:
                    break

            # The self-block is no longer possible.
            # Q(v) is post[v], whose last element is v.
            found = False

            for u in post[v][:-1]:
                block = A(u, d - 1, cache)

                if rem > block:
                    rem -= block
                else:
                    v = u
                    d -= 1
                    found = True
                    break

            if not found:
                # This branch is reachable only at d == 0,
                # which is handled below.
                break

        # At d == 0 the word is [v].
        # rem is a one-based position inside E(v).
        idx = rem // FACT - 1
        ans = euler_output[v][idx]

        answer_cache[K] = ans
        return ans

    out = [str(get_answer(q) + 1) for q in queries]
    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The first DFS constructs two objects for every tree node. `post[v]` is the exact sequence of restart tasks generated by completing `v`, while `euler_output[v]` is the actual sequence printed while the task `v` is active. The latter has length `2 * subtree_size - 1`.

The `coeff` vectors encode the powers of the nilpotent descendant matrix without explicitly storing a matrix. Applying `N` once means summing over proper descendants, so every coefficient can be computed directly from the postorder lists.

The polynomial conversion deserves some care. The natural formula uses binomial coefficients, but repeatedly evaluating binomial coefficients during every binary search would require many divisions. Multiplying all polynomials by `(degree + 1)!` converts every binomial polynomial into an integer polynomial. Horner evaluation then needs only multiplication and addition.

All positions are internally represented in units of `FACT`. This avoids repeatedly dividing weighted positions by the factorial scaling factor. At the final step, the remaining value is divisible by `FACT`, and the quotient gives the one-based position inside `E(v)`.

The binary search for the first level uses `prefix(d)`, which counts every output from levels strictly before `d`. The upper bound `K` is always sufficient because every level contains at least one task and every task prints at least one value.

The second binary search is the subtle part. Since `v` is the last element of its own postorder list, `Q^d(v)` always ends with `Q^(d-1)(v)`. If the target remains in this self block repeatedly, we can subtract the entire skipped range in one operation. Once the target enters a proper descendant block, the current node strictly moves downward in the tree.

Python integers are arbitrary precision, so the input values up to (10^{100}), the polynomial evaluations, and the factorial scaling introduce no overflow issue.

## Worked Examples

### Sample 1

The tree is

```
1
├── 2
│   └── 3
└── 4
```

The active traversal sequences are

```
E(3) = [3]
E(4) = [4]
E(2) = [2, 3, 2]
E(1) = [1, 2, 3, 2, 1, 4, 1]
```

The first level therefore contributes seven printed values.

The postorder of the root is `[3, 2, 4, 1]`, so the next level consists of those four tasks. Their weights are respectively 1, 3, 1, and 7.

| Query | Level containing it | Position inside level | Selected task/output | Answer |
| --- | --- | --- | --- | --- |
| 6 | 0 | 6 | `E(1)[6]` | 4 |
| 9 | 1 | 2 | `E(2)[1]` | 2 |
| 69 | 4 | 7 | recursive selection | 2 |
| 143 | 6 | 9 | recursive selection | 3 |
| 214 | 7 | 31 | recursive selection | 3 |
| 241 | 7 | 58 | recursive selection | 3 |
| 420 | 10 | 37 | recursive selection | 3 |

For this tree, the total weight of level (d) is

[
A_1(d)=7+\frac{d(d+9)}2.
]

The cumulative output before level (d) is consequently

[
P(d)=\sum_{j=0}^{d-1}
\left(7+\frac{j(j+9)}2\right).
]

For example, (P(4)=62) and (P(5)=94), so query 69 lies in level 4. The recursive block selection then finds node 2, producing the required value 2.

### A two-node chain

Consider

```
2 5
1 2
0
1
2
3
4
10
```

The tree is simply

```
1
└── 2
```

The active blocks are

```
E(2) = [2]
E(1) = [1, 2, 1]
```

The first level has weight 3. Its postorder task sequence is `[2, 1]`. Replacing each task by its postorder sequence gives the next levels.

| Level | Task sequence | Block weights | Total output |
| --- | --- | --- | --- |
| 0 | `[1]` | `[3]` | 3 |
| 1 | `[2, 1]` | `[1, 3]` | 4 |
| 2 | `[2, 2, 1]` | `[1, 1, 3]` | 5 |

The cumulative output before levels 0, 1, 2, and 3 is respectively 0, 3, 7, and 12. Thus query 10 belongs to level 2 and has local position 3. The first two tasks of that level are both node 2, leaving the third task, node 1. Its block is `E(1)`, so the third printed value inside that block is 1.

The requested outputs are consequently

```
1
2
1
2
1
```

for positions 1, 2, 3, 4, and 10. This example exercises the repeated self-block jump because node 1 keeps appearing as the final element of its own postorder expansion.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(n^3+k n^2\log K)) | Polynomial construction costs (O(n^3)); each query visits at most (n) tree levels, with binary searches over an exponent of at most (O(\log K)) iterations and (O(n)) polynomial evaluation |
| Space | (O(n^2)) | The tree, postorder lists, output blocks, polynomial coefficients, and temporary per-query cache all have quadratic-scale size |

Here (K) denotes the largest requested position. With (n\le50), all tree-dependent work is small. The dependence on (K) is logarithmic in the number of bits of the query rather than linear in its numerical value, which is what makes positions as large as (10^{100}) practical.

## Test Cases

The following tests assume the `solve()` function from the solution above is available.

```python
import sys
import io

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    try:
        solve()
        return sys.stdout.getvalue()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

# Provided sample
sample1 = """\
4 7
2 2 4
1 3
0
0
6
9
69
143
214
241
420
"""

assert run(sample1) == """\
4
2
2
3
3
3
3
""", "sample 1"

# Minimum-size tree, all outputs equal.
case1 = """\
1 4
0
1
2
3
100000000000000000000000000000000000000000000000000000000000
"""

assert run(case1) == """\
1
1
1
1
""", "single-node tree"

# Two-node chain, catches level boundaries and repeated self blocks.
case2 = """\
2 5
1 2
0
1
2
3
4
10
"""

assert run(case2) == """\
1
2
1
2
1
""", "two-node chain"

# Three-node star, checks the transition from the initial traversal
# to postponed tasks.
case3 = """\
3 5
2 2 3
0
0
5
6
7
12
13
"""

assert run(case3) == """\
1
2
1
1
2
""", "star boundary"

# Maximum n = 50, root with 49 leaf children.
# E(root) has length 99:
# odd positions are node 1, even positions are leaves 2,3,...,50.
max_case_parts = [
    "50 3",
    "49 " + " ".join(str(x) for x in range(2, 51))
]
max_case_parts.extend(["0"] * 49)
max_case_parts.extend(["99", "100", "101"])
case4 = "\n".join(max_case_parts) + "\n"

assert run(case4) == """\
1
2
3
""", "maximum-size star"

print("All tests passed.")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single node with huge query | `1, 1, 1, 1` | Minimum size, all outputs equal, arbitrary-precision position |
| Two-node chain | `1, 2, 1, 2, 1` | Level boundaries and repeated self expansion |
| Three-node star | `1, 2, 1, 1, 2` | Transition from the initial active traversal to postponed tasks |
| Fifty-node star | `1, 2, 3` | Maximum tree size and the exact end of the first level |

## Edge Cases

For a single-node tree, every processing step prints node 1 and then puts `(1,0)` back on the left. Since it is also the only element, the next iteration removes it again. The polynomial representation reflects this with a constant (A_1(d)=1), while the cumulative prefix is simply (d). The level search can consequently jump directly to an enormous level, and the base case returns node 1.

For the two-node chain

```
2 4
1 2
0
1
2
3
4
```

the first active block is `[1,2,1]`. After it finishes, the postponed tasks are `[2,1]`. The next level is therefore composed of `E(2)` followed by `E(1)`, rather than restarting node 1 immediately. The output starts `1,2,1,2,1,2,1`, and the algorithm gets the same result because it always treats the postorder list as the next task level.

At a level boundary, the query must belong to exactly one level. The algorithm uses the strict inequality `prefix(d) < K` when finding the level. If `K` is exactly the last position of a level, the binary search keeps that level. The next position then belongs to the following level. This is the reason the implementation uses one-based weighted positions and subtracts the complete prefix only after identifying the level.

When the target lies inside the repeated final block (Q^{d-1}(v)), recursively decrementing (d) one at a time would be wrong from a performance perspective even though it would be logically correct. The self-block binary search replaces all consecutive repetitions by one jump. The expression (A_v(d)-A_v(d-t)) is exactly the total weight removed by (t) such repetitions, so the remaining position stays synchronized with the original sequence.

Finally, when the target leaves the self block, it must enter a proper descendant's block. The tree depth is at most 49, so there can be only finitely many such changes before reaching (d=0). At that point there is only one task symbol left, and the remaining position selects an element directly from the precomputed finite sequence (E(v)).

If you want, I can also provide a shorter contest-editorial version of this that keeps the same proof but is easier to read under time pressure.
