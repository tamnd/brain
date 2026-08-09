---
title: "CF 102439D - Light show"
description: "There are (n) lightbulbs, so a configuration of the club is a binary vector of length (n). A switch is another binary vector. Pressing a switch means XORing its vector with the current configuration, because every bulb whose corresponding bit is one gets toggled."
date: "2026-08-10T06:49:45+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102439
codeforces_index: "D"
codeforces_contest_name: "2018-2019 9th BSUIR Open Programming Championship. Semifinal"
rating: 0
weight: 102439
solve_time_s: 475
verified: true
draft: false
---

[CF 102439D - Light show](https://codeforces.com/problemset/problem/102439/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 7m 55s  
**Verified:** yes  

## Solution
## Problem Understanding

There are (n) lightbulbs, so a configuration of the club is a binary vector of length (n). A switch is another binary vector. Pressing a switch means XORing its vector with the current configuration, because every bulb whose corresponding bit is one gets toggled.

Each switch is available only on a contiguous interval of days. On every day, Dima may use any subset of the switches available that day, including the empty subset. The question for each day is how many distinct bulb configurations can be produced.

The crucial algebraic observation is that the order of pressing switches does not matter. If the available switches on a particular day are vectors (v_1,v_2,\ldots,v_k), every reachable configuration has the form

[
c_1v_1\oplus c_2v_2\oplus\cdots\oplus c_kv_k,
]

where every (c_i) is either zero or one. Thus the reachable configurations are exactly the linear span of the available vectors over the field GF(2).

If the vectors have rank (r), their span contains exactly (2^r) different vectors. So the original problem is equivalent to computing the rank of the set of active switch vectors for every day.

The bounds force us away from rebuilding a Gaussian basis independently for every day. We can have (d=q=500,000), and even a single pass over all switches for every day would already require (2.5\cdot10^{11}) switch examinations. A quadratic or (O(nq d)) approach is completely impossible.

There is also a useful constraint hidden in the input format. Every switch description contains exactly (n) bits, and the total length of all such strings is at most (500,000). Hence

[
nq\le500,000.
]

This is what makes a Gaussian-basis solution practical. Even though (n) itself can be (500,000), in that case there can only be one switch. Conversely, if there are (500,000) switches, then (n=1).

There are several edge cases that a straightforward implementation can mishandle.

Consider a zero switch:

```
1 1 1
1 1 0
```

The only switch changes nothing. The span therefore has rank zero, so the answer is `1`, not `2`. A careless implementation that counts switches instead of independent vectors would give the wrong result.

Duplicate switches are another trap:

```
2 2 1
1 1 10
1 1 10
```

Both switches are available, but they represent the same vector. The rank is one, so the answer is `2`. Treating every available switch as an independent binary choice would incorrectly produce `4`.

Interval endpoints must also be inclusive. For example:

```
2 2 2
1 2 10
2 2 01
```

On day one only the first vector is available, giving `2` configurations. On day two both independent vectors are available, giving `4`. The correct output is `2 4`. An implementation that interprets the right endpoint as exclusive would lose the second switch on day two.

## Approaches

The direct approach is to process each day independently. For a fixed day, collect every switch whose interval contains that day and insert its vector into a Gaussian basis over GF(2). If the resulting basis has rank (r), output (2^r).

This is correct because Gaussian elimination tells us exactly how many independent directions the available switches provide. However, in the worst case there can be (500,000) days and (500,000) switches. Processing every switch on every day can require (250,000,000,000) switch checks before even considering the cost of elimination.

The structure that saves us is that every switch is active on one interval. Instead of asking which switches are active at a day, we can store a switch on a segment tree covering exactly the days on which that switch is active.

An interval can be represented by (O(\log d)) segment-tree nodes. During a depth-first traversal of the tree, every switch stored at a node is active for every leaf below that node. We can insert all such vectors into one linear basis, recursively visit the children, and then undo the insertions when returning from the node.

Undoing Gaussian elimination sounds difficult because ordinary elimination destroys information. The solution is to use a basis in which every successful insertion creates exactly one new pivot. We remember which pivot was created, and on rollback simply clear that pivot. Because recursive processing rolls back in reverse insertion order, no later vector can depend on a basis entry that has already been removed.

Representing a binary vector as one Python integer makes the implementation especially convenient. Bitwise XOR performs vector addition over GF(2), and `bit_length()` gives the highest set bit, which is the pivot used by the basis.

The segment tree handles the temporal intervals, while the rollback basis handles the linear dependence between switches. These two parts fit together because every recursive node represents a range of days on which all vectors stored at that node are simultaneously available.

The resulting comparison is:

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(ndq)) in the straightforward implementation | (O(nq)) | Too slow |
| Optimal | (O(nq\log d)) worst case | (O(q\log d+n)) | Accepted |

The bound (nq\le500,000) makes the optimal time roughly (O(500,000\log 500,000)), with the actual constant depending on how many Gaussian-basis reductions are needed.

## Algorithm Walkthrough

1. Read every switch and convert its binary string into an integer. Bit (i) represents whether bulb (i) is toggled. The integer representation lets us perform vector addition using ordinary XOR.
2. Build an implicit segment tree over the days from (1) through (d). For a switch available on ([l,r]), decompose that interval into the canonical segment-tree nodes whose ranges together equal exactly ([l,r]). Store the switch vector in every such node.
3. Maintain a linear basis indexed by the highest set bit of each basis vector. To insert a vector (x), repeatedly look at its highest set bit. If the corresponding pivot already exists, XOR the existing basis vector from (x). If the pivot is empty, put (x) there and increase the rank by one.
4. Whenever an insertion creates a new pivot, record that pivot in a rollback stack. If the vector reduces to zero, it was linearly dependent on the current basis, so nothing needs to be recorded.
5. Traverse the segment tree recursively. At a node, remember the current rollback-stack size, then insert every vector stored at that node. All of these vectors are active throughout the whole node range, so they belong in the basis for every descendant day.
6. If the node is a leaf representing day (i), the current basis contains exactly the independent switches available on that day. If its rank is (r), write (2^r\bmod(10^9+7)) as the answer for day (i).
7. For an internal node, recursively process both children. The basis is shared between the two children, but each child receives exactly the vectors that are active throughout its range plus the vectors inherited from its ancestors.
8. After processing a node, repeatedly pop the rollback stack until it reaches the saved checkpoint. For every removed pivot, clear that basis entry and decrease the rank. This restores the basis to exactly the state it had when entering the node.

### Why it works

At every segment-tree node, the invariant is that the linear basis contains precisely the switches whose intervals completely cover the path from the root to that node. When a leaf is reached, that path corresponds to one day, so the basis contains exactly all switches active on that day. Gaussian elimination preserves the span while removing dependent vectors, meaning its rank is exactly the dimension of the reachable configuration space. A vector space of dimension (r) over GF(2) contains exactly (2^r) vectors, so the value produced at every leaf is exactly the number of reachable light configurations.

Rollback is correct because insertions are undone in reverse order. A successful insertion occupies a previously empty pivot, and every insertion made after it is later removed first. Clearing the recorded pivot thus restores the previous basis without affecting older basis vectors.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 1_000_000_007

def solve():
    n, q, d = map(int, input().split())

    # Use a power-of-two segment tree.
    size = 1
    while size < d:
        size <<= 1

    # events[v] contains vector integers assigned to segment-tree node v.
    # None avoids creating millions of empty Python lists.
    events = [None] * (2 * size)

    for _ in range(q):
        l, r, s = input().split()
        l = int(l) - 1
        r = int(r)

        # One object is shared by all segment-tree copies of this switch.
        vec = int(s, 2)

        l += size
        r += size

        while l < r:
            if l & 1:
                if events[l] is None:
                    events[l] = [vec]
                else:
                    events[l].append(vec)
                l += 1

            if r & 1:
                r -= 1
                if events[r] is None:
                    events[r] = [vec]
                else:
                    events[r].append(vec)

            l >>= 1
            r >>= 1

    # basis[p] is the vector whose highest set bit is p.
    basis = [0] * n
    changes = []
    rank = 0

    pow2 = [1] * (n + 1)
    for i in range(1, n + 1):
        pow2[i] = (pow2[i - 1] * 2) % MOD

    ans = [0] * d

    def add_vector(x):
        nonlocal rank

        while x:
            p = x.bit_length() - 1
            b = basis[p]

            if b:
                x ^= b
            else:
                basis[p] = x
                changes.append(p)
                rank += 1
                return

    def rollback(checkpoint):
        nonlocal rank

        while len(changes) > checkpoint:
            p = changes.pop()
            basis[p] = 0
            rank -= 1

    sys.setrecursionlimit(1_000_000)

    def dfs(v, left, right):
        checkpoint = len(changes)

        ev = events[v]
        if ev is not None:
            for x in ev:
                add_vector(x)

        if right - left == 1:
            if left < d:
                ans[left] = pow2[rank]
        else:
            mid = (left + right) >> 1
            dfs(v << 1, left, mid)
            dfs(v << 1 | 1, mid, right)

        rollback(checkpoint)

    dfs(1, 0, size)

    sys.stdout.write(" ".join(map(str, ans)))

if __name__ == "__main__":
    solve()
```

The input conversion `int(s, 2)` is the central representation trick. The leftmost character becomes a high bit, but the exact orientation does not matter because XOR and linear dependence are unaffected by consistently renaming coordinates.

The interval conversion uses the half-open range `[l, r)`. The input interval `[l,r]` is first changed to zero-based coordinates by subtracting one from `l`, while the right endpoint remains unchanged. Thus a switch active on input days `1..3` becomes the half-open range `[0,3)`. This is a convenient way to avoid endpoint mistakes in the iterative segment-tree decomposition.

The `events` array has size `2 * size`, where `size` is the smallest power of two at least `d`. Empty nodes are represented by `None`. This matters in Python because creating several million empty lists would consume substantially more memory than necessary.

The basis stores one vector for each possible pivot bit. When a vector has highest bit `p`, an existing `basis[p]` can eliminate that bit. Eventually either the vector becomes zero, proving dependence, or it reaches an unused pivot and becomes a new independent basis vector.

The rollback stack contains only pivot indices, not copies of the whole basis. Suppose an insertion creates pivot `p`. At that moment `basis[p]` was zero. Every later insertion is undone before this insertion, so clearing `basis[p]` restores the exact earlier state.

The answer is precomputed as `pow2[r]`. The rank never exceeds `n`, so only `n+1` powers are necessary. Python integers do not overflow, but reducing the powers modulo (10^9+7) keeps the stored answers small.

The traversal uses the complete power-of-two tree even when `d` is not itself a power of two. Leaves with indices at least `d` are ignored. The interval decomposition only inserts real days, so these artificial leaves never affect a valid answer.

## Worked Examples

### Sample 1

The input is:

```
3 3 3
1 3 011
3 3 101
3 3 001
```

The vectors are `011`, `101`, and `001`.

| Day | Active vectors | Independent pivots | Rank | Answer |
| --- | --- | --- | --- | --- |
| 1 | `011` | `011` | 1 | 2 |
| 2 | `011` | `011` | 1 | 2 |
| 3 | `011`, `101`, `001` | three independent vectors | 3 | 8 |

On days one and two, only one nonzero direction is available, so there are two reachable configurations: using the switch or not using it.

On day three, the three vectors are independent. In particular, none of them can be produced as an XOR of the other two, so the span has dimension three and contains all (2^3=8) possible bulb configurations.

### Sample 2

The input is:

```
4 3 4
2 4 1010
2 4 0101
3 4 1101
```

The first two switches become available on day two, while the third starts on day three.

| Day | Active vectors | Rank | Answer |
| --- | --- | --- | --- |
| 1 | none | 0 | 1 |
| 2 | `1010`, `0101` | 2 | 4 |
| 3 | `1010`, `0101`, `1101` | 3 | 8 |
| 4 | `1010`, `0101`, `1101` | 3 | 8 |

Day one has no switches, but Dima may use the empty subset, so the all-off configuration is reachable. That gives (2^0=1).

On day two, the two vectors are independent. On day three, the third vector adds another independent direction, increasing the rank from two to three. The same three switches remain available on day four, so the answer stays eight.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(nq\log d)) worst case | Each switch is stored in (O(\log d)) segment-tree nodes, and each basis insertion performs at most (O(n)) pivot eliminations |
| Space | (O(q\log d+n+d)) | Segment-tree interval copies, the basis, rollback stack, answers, and tree metadata |

The special constraint that the total length of all switch strings is at most (500,000) gives (nq\le500,000). Consequently the worst-case elimination work is bounded by roughly (500,000\log 500,000), rather than (nq d). The rollback basis contains at most (n) vectors at any moment, and recursion depth is only (O(\log d)).

The original contest solution was designed for the (2)-second, (256)-MB limits, and accepted C++ implementations use the same essential combination of interval decomposition and linear-basis maintenance.

## Test Cases

The following test harness assumes the solution above is saved as `solution.py` with its `solve()` function exposed. The maximum-size cases are generated rather than written out literally, which keeps the test file usable.

```python
# test_solution.py
import io
import sys

from solution import solve

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    try:
        solve()
        return sys.stdout.getvalue().strip()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

# Provided sample 1
assert run(
    """3 3 3
1 3 011
3 3 101
3 3 001
"""
) == "2 2 8"

# Provided sample 2
assert run(
    """4 3 4
2 4 1010
2 4 0101
3 4 1101
"""
) == "1 4 8 8"

# Provided sample 3
assert run(
    """5 2 2
1 2 01101
1 1 10101
"""
) == "4 2"

# Minimum-size case.
assert run(
    """1 1 1
1 1 0
"""
) == "1"

# Duplicate vectors: rank is one, not two.
assert run(
    """2 2 1
1 1 10
1 1 10
"""
) == "2"

# Endpoint test: the second switch exists only on day 2.
assert run(
    """2 2 2
1 2 10
2 2 01
"""
) == "2 4"

# Zero vector plus a nonzero vector.
assert run(
    """2 3 3
1 3 00
2 3 10
3 3 01
"""
) == "1 2 4"

# Maximum q and d with n = 1.
# Every switch is the same vector, so the rank is always one.
q = 500_000
d = 500_000

maximum_input = (
    f"1 {q} {d}\n"
    + ("1 " + str(d) + " 1\n") * q
)

maximum_expected = " ".join(["2"] * d)

assert run(maximum_input) == maximum_expected

# Maximum n with q = 1.
# The single vector is active for every day, so every answer is 2.
n = 500_000
d = 5
large_vector = "1" * n

large_input = f"{n} 1 {d}\n1 {d} {large_vector}\n"

assert run(large_input) == "2 2 2 2 2"

print("all tests passed")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 1 / 1 1 0` | `1` | Minimum size and zero vector |
| Two identical `10` vectors | `2` | Dependent duplicate switches |
| `10` on days 1 to 2 and `01` on day 2 | `2 4` | Inclusive interval endpoints |
| `00`, `10`, `01` with staggered intervals | `1 2 4` | Zero vectors and increasing rank |
| (n=1,q=d=500000) | 500000 copies of `2` | Maximum number of switches and days |
| (n=500000,q=1) | five copies of `2` | Maximum vector length and total-string constraint |

## Edge Cases

A zero vector is handled naturally by the basis. For

```
1 1 1
1 1 0
```

the integer representation is zero, so `add_vector(0)` immediately returns without creating a pivot. The rank remains zero and the leaf receives `2^0 = 1`. The switch exists, but pressing it cannot change the light configuration.

Duplicate vectors are also handled by Gaussian elimination rather than by counting switches. For

```
2 2 1
1 1 10
1 1 10
```

the first `10` creates one pivot. The second `10` is XORed with the existing basis vector and becomes zero. Only one pivot remains, so the answer is `2`.

The inclusive right endpoint is handled by converting `[l,r]` into a zero-based half-open range `[l-1,r)`. For

```
2 2 2
1 2 10
2 2 01
```

the first switch occupies both leaves, while the second occupies only the second leaf. The first leaf therefore has rank one and produces `2`, while the second leaf has two independent vectors and produces `4`.

A day with no available switches is also valid. The empty subset of switches always exists, so the all-off configuration is reachable even when the active set is empty. The basis then has rank zero and the answer is exactly one.

Finally, vectors can be much longer than a machine word. Python's arbitrary-precision integers are useful here because a vector of (500,000) bits is represented directly, and XOR operates on all machine words internally. The input guarantee prevents this large-vector case from coinciding with a large number of switches, since (nq\le500,000).
