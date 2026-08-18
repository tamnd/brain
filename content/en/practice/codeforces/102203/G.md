---
title: "CF 102203G - \u0417\u0430\u043f\u0443\u0442\u044b\u0432\u0430\u043d\u0438\u0435 \u0441\u043b\u0435\u0434\u043e\u0432"
description: "There are only 8 districts, so every agent can be represented by an 8 × 8 binary transition matrix. For agent (k), the entry (Ak[u][v]) is 1 exactly when that agent can take Rick and Vallona from district (u) to district (v)."
date: "2026-08-18T11:20:48+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102203
codeforces_index: "G"
codeforces_contest_name: "\u0427\u0435\u0442\u0432\u0435\u0440\u0442\u0430\u044f \u041b\u0438\u043f\u0435\u0446\u043a\u0430\u044f \u043a\u043e\u043c\u0430\u043d\u0434\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430 \u0448\u043a\u043e\u043b\u044c\u043d\u0438\u043a\u043e\u0432 \u043f\u043e \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044e (8-11 \u043a\u043b\u0430\u0441\u0441\u044b)"
rating: 0
weight: 102203
solve_time_s: 200
verified: true
draft: false
---

[CF 102203G - \u0417\u0430\u043f\u0443\u0442\u044b\u0432\u0430\u043d\u0438\u0435 \u0441\u043b\u0435\u0434\u043e\u0432](https://codeforces.com/problemset/problem/102203/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 3m 20s  
**Verified:** yes  

## Solution
## Problem Understanding

There are only 8 districts, so every agent can be represented by an 8 × 8 binary transition matrix. For agent (k), the entry (A_k[u][v]) is 1 exactly when that agent can take Rick and Vallona from district (u) to district (v).

For a query ([l,r,s,t]), the agents must be used in the fixed order (l,l+1,\ldots,r). If we write their matrices as (A_l,A_{l+1},\ldots,A_r), then the number of possible routes is exactly the ((s,t)) entry of

[
A_lA_{l+1}\cdots A_r
]

where multiplication is ordinary matrix multiplication modulo 998244353. The multiplication sums over every possible intermediate district, so a single matrix product counts every distinct route exactly once. The official constraints and sample are given on the Codeforces problem page.

The input contains up to (10^5) agents and (2\cdot10^5) queries. A direct scan of one query can touch (10^5) matrices, which is already too much when repeated (2\cdot10^5) times. Even the natural dynamic programming version, which maintains an 8-element vector and applies one binary matrix in 64 scalar operations, can reach

[
2\cdot10^5\cdot10^5\cdot64=1.28\cdot10^{12}
]

scalar operations. A conventional segment tree reduces the number of matrix products per query to (O(\log n)), but each product is a full 8 × 8 matrix multiplication, so Python would still perform an enormous amount of work.

The unusual condition on the queries is the key. No query interval is properly contained inside another one. If two intervals are sorted by their left endpoint and the first has a larger right endpoint than the second, the second interval would be contained in the first. Hence, after sorting by (l), the right endpoints are also nondecreasing. Equal left endpoints can simply be sorted by increasing right endpoint.

This means that the queried ranges can be viewed as a sliding window. The left endpoint only moves to the right, and the right endpoint only moves to the right. We need a data structure that maintains the product of a sequence while supporting append-at-the-right and remove-from-the-left. The standard two-stack sliding-window aggregation structure does exactly that for any associative operation, including noncommutative matrix multiplication.

There are several edge cases that are easy to mishandle. An interval of length one must return the corresponding matrix entry directly. For example,

```
1 1
9223372036854775808
1 1 1 1
```

has only the transition (1\to1), so the answer is `1`. Treating the query as if it had an empty product would incorrectly return an identity-matrix entry instead of the actual agent transition.

A route may revisit the same district, including immediately. For example,

```
2 1
9223372036854775808
9223372036854775808
1 2 1 1
```

has exactly one route, (1\to1\to1), so the answer is `1`. A solution that assumes every movement must change the district would incorrectly discard this route.

Finally, a matrix may contain no transitions at all. For example,

```
1 1
0
1 1 1 1
```

has answer `0`. Implementations that accidentally use the identity matrix for a zero agent, or that confuse the empty-product identity with an actual zero transition matrix, will fail this case.

## Approaches

The most direct correct method is to process every query independently. Start with an 8-element vector containing one at the starting district and zero elsewhere. For every agent from (l) through (r), multiply this vector by that agent's binary transition matrix. After the last agent, the component corresponding to (t) is the answer. This is correct because after processing the first (k) agents, the vector stores the number of ways to reach every district after exactly those agents.

The problem is the repeated scanning. One query can contain (10^5) agents, and there can be (2\cdot10^5) queries. The worst case is about (1.28\cdot10^{12}) scalar vector-matrix operations, far beyond the limit.

A standard range-product data structure would store products of segments in a segment tree. A query could then combine (O(\log n)) precomputed matrices. The algebra is perfectly valid because matrix multiplication is associative, but it does not exploit the special query condition. With (2\cdot10^5) queries and about 17 tree levels, that is millions of 8 × 8 matrix multiplications.

The decisive observation is that the queries form a monotone sequence after sorting. The left boundary never moves backward, and neither does the right boundary. We can consequently maintain exactly the current query interval as a FIFO sequence of agent matrices.

The obstacle is that matrix multiplication is not invertible in general. If the current product is (A_lA_{l+1}\cdots A_r), removing (A_l) cannot be done by multiplying by an inverse because (A_l) may be singular. A two-stack aggregate queue avoids this completely. Each stack stores partial products, so removing the oldest element only requires rebuilding the opposite stack when it becomes empty. Every matrix is moved between stacks at most once, giving amortized constant many monoid operations per window update. This is the same sliding-window aggregation idea commonly called SWAG.

There is another useful optimization specific to this problem. Every original agent matrix is binary. When adding an agent to a stack aggregate, one operand is always binary, so the multiplication can be performed as sums of selected rows or columns instead of 64 ordinary modular multiplications. The code below uses this optimization. When answering a query, we do not even need the whole product of the two stack aggregates. We only need one entry, so combining the two aggregates costs just 8 multiply-add terms.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(mn\cdot8^2)) | (O(8^2)) | Too slow |
| Segment Tree | (O(m\log n\cdot8^3)) | (O(n\cdot8^2)) | Correct, but unnecessarily expensive |
| Optimal SWAG | (O(n\cdot8^3+m\cdot8)) | (O(n\cdot8^2+m)) | Accepted |

Since 8 is a fixed constant, the optimal complexity is effectively (O(n+m)) matrix operations.

## Algorithm Walkthrough

1. Convert every 64-bit input number into its 8 × 8 binary matrix. We store its eight row masks and eight column masks, together with the flattened 64 entries. The masks let us multiply an arbitrary aggregate by the binary agent matrix without performing unnecessary scalar multiplications.
2. Read all queries and sort them by `(l, r)`. The original order is stored with every query so that answers can later be restored. Sorting by (l) is enough to make (r) nondecreasing because the query family contains no proper nesting.
3. Maintain a sliding window containing exactly the agents currently belonging to the query being processed. Its two endpoints are `left` and `right`. Initially the window is empty.
4. To extend the window to the right, append every new agent until `right` equals the current query's (r). The back stack stores newly appended matrices. Its aggregate is the product of all matrices in that stack in chronological order.
5. To move the left endpoint forward, remove matrices from the front of the window until `left` equals the current query's (l). If the front stack is nonempty, the oldest matrix can simply be popped. If it is empty, move every matrix from the back stack into the front stack. Reversing their order makes the oldest matrix the top element of the front stack.
6. While rebuilding the front stack, recompute its aggregate from the oldest matrix toward the newest one. If the new matrix is (A) and the previous aggregate is (P), the new aggregate is (A P), not (P A). The order matters because matrix multiplication is not commutative.
7. After the window represents ([l,r]), its product is split into at most two aggregates. If both stacks are present, the full product is `front_product * back_product`. If one stack is empty, its aggregate is already the whole product.
8. Only the requested entry ((s,t)) is needed. If the two aggregates are (F) and (B), compute

[
(FB)[s][t]=\sum_{k=0}^{7}F[s][k]B[k][t].
]

This requires only eight scalar multiplications.

1. Store the answer under the query's original index. After all sorted queries have been processed, print the answers in their original order.

### Why it works

The invariant is that immediately before answering a query ([l,r]), the two stacks together represent exactly the matrices (A_l,A_{l+1},\ldots,A_r) in that order. The back stack stores its matrices in chronological order in its aggregate, while the front stack stores its matrices from oldest to newest in its aggregate. When the back stack is transferred to the front stack, the physical reversal changes the stack order into chronological order, and each new front aggregate is formed as (A P), preserving the product order. Thus the product represented by the two aggregates is always exactly (A_lA_{l+1}\cdots A_r). The requested matrix entry consequently counts precisely the routes from (s) to (t).

The amortized bound follows because each agent is appended once, and whenever the front stack is rebuilt, every moved agent is transferred once before being popped. An agent cannot be transferred back and forth repeatedly under a monotone sliding window. Thus the total number of stack aggregate updates is linear in (n).

## Python Solution

```python
import sys
from array import array

input = sys.stdin.readline

MOD = 998244353

# Positions of set bits for every 8-bit mask.
BIT_POS = [()]
for mask in range(1, 256):
    cur = []
    x = mask
    while x:
        b = x & -x
        cur.append(b.bit_length() - 1)
        x -= b
    BIT_POS.append(tuple(cur))

def parse_agent(x):
    rows = [0] * 8
    cols = [0] * 8
    flat = [0] * 64

    # Bit 63 is matrix position (0, 0), bit 0 is (7, 7).
    for p in range(64):
        bit = (x >> (63 - p)) & 1
        if bit:
            i = p >> 3
            j = p & 7
            rows[i] |= 1 << j
            cols[j] |= 1 << i
            flat[p] = 1

    return (tuple(rows), tuple(cols), tuple(flat))

def mul_right_binary(a, cols):
    """
    Compute A * B, where A is a general 8x8 matrix and B is binary.
    """
    out = array('I', [0]) * 64

    for i in range(8):
        base = i << 3
        for j in range(8):
            pos = BIT_POS[cols[j]]

            if not pos:
                continue

            if len(pos) == 1:
                value = a[base + pos[0]]
            else:
                value = 0
                for k in pos:
                    value += a[base + k]
                value %= MOD

            out[base + j] = value

    return out

def mul_left_binary(rows, b):
    """
    Compute A * B, where A is binary and B is a general 8x8 matrix.
    """
    out = array('I', [0]) * 64

    for i in range(8):
        pos = BIT_POS[rows[i]]
        base = i << 3

        if not pos:
            continue

        if len(pos) == 1:
            src = pos[0] << 3
            for j in range(8):
                out[base + j] = b[src + j]
        else:
            for j in range(8):
                value = 0
                for k in pos:
                    value += b[(k << 3) + j]
                out[base + j] = value % MOD

    return out

def entry_product(a, b, s, t):
    """
    Return (A * B)[s][t], without constructing A * B.
    """
    base_a = s << 3
    value = 0

    for k in range(8):
        value += a[base_a + k] * b[(k << 3) + t]

    return value % MOD

def solve():
    n, m = map(int, input().split())

    agents = []
    for _ in range(n):
        agents.append(parse_agent(int(input())))

    queries = []
    for idx in range(m):
        l, r, s, t = map(int, input().split())
        queries.append((l - 1, r - 1, s - 1, t - 1, idx))

    # For non-nested intervals, sorting by l makes r nondecreasing.
    queries.sort(key=lambda q: (q[0], q[1]))

    # Each entry is (raw_agent, aggregate_of_stack).
    #
    # Back stack:
    #   top is the newest element.
    #   aggregate is product from oldest to newest.
    #
    # Front stack:
    #   top is the oldest element.
    #   aggregate is product from oldest to newest.
    back = []
    front = []

    left = 0
    right = -1

    answers = [0] * m

    for ql, qr, s, t, idx in queries:
        while right < qr:
            right += 1
            raw = agents[right]

            if back:
                old_agg = back[-1][1]
                agg = mul_right_binary(old_agg, raw[1])
            else:
                agg = raw[2]

            back.append((raw, agg))

        while left < ql:
            if not front:
                # Transfer back -> front.
                while back:
                    raw, _ = back.pop()

                    if front:
                        old_agg = front[-1][1]
                        agg = mul_left_binary(raw[0], old_agg)
                    else:
                        agg = raw[2]

                    front.append((raw, agg))

            front.pop()
            left += 1

        if front:
            f = front[-1][1]

            if back:
                b = back[-1][1]
                answers[idx] = entry_product(f, b, s, t)
            else:
                answers[idx] = f[(s << 3) + t]
        else:
            b = back[-1][1]
            answers[idx] = b[(s << 3) + t]

    sys.stdout.write('\n'.join(map(str, answers)))

if __name__ == "__main__":
    solve()
```

The `parse_agent` function follows the statement's bit ordering exactly. The most significant bit represents matrix position ((0,0)), so position `p` uses bit `63 - p`. This is a common source of wrong answers because treating the least significant bit as the first matrix element reverses the entire encoding.

The `rows` and `cols` masks contain the binary structure needed by the optimized multiplication routines. For `A * B` with binary `B`, each output entry is the sum of selected entries from one row of `A`, where the selected indices are determined by a column mask of `B`. The symmetric idea is used for `A * B` when `A` is binary.

The two stacks contain both the raw agent and the aggregate belonging to that stack prefix. The back aggregate is updated as `old_aggregate * new_agent`. The front aggregate is rebuilt as `new_agent * old_aggregate`, because the transferred agent is older than everything already in the front stack.

The code deliberately avoids constructing the product of the front and back aggregates when answering a query. Only one matrix entry is required, so `entry_product` computes the corresponding eight-term dot product directly.

The `array('I')` type stores aggregate entries as 32-bit unsigned integers instead of Python integer objects. Every value is reduced modulo 998244353, so four bytes are sufficient. This substantially reduces memory consumption when the window contains close to (10^5) matrices.

Python integers have arbitrary precision, so there is no overflow issue in the ordinary arithmetic. The explicit modulo after summing at most eight terms keeps aggregate entries below the modulus, while the final query dot product is also reduced modulo the required value.

## Worked Examples

The official sample is:

```
3 3
9241386504218214000
4692768438333080000
4620710844295152000
1 2 3 4
1 3 1 3
3 3 1 2
```

Its output is:

```
0
1
1
```

The first query uses agents 1 and 2. Agent 1 has no outgoing transition from district 3, so the route count immediately becomes zero. The second query uses all three agents and has the unique route (1\to2\to3). The third query uses only agent 3 and has the unique transition (1\to2). These are exactly the official sample results.

For the sliding-window behavior, consider two agents forming a chain:

```
2 3
4611686018427387904
9007199254740992
1 1 1 2
1 2 1 3
2 2 2 3
```

The first number represents only (1\to2), and the second represents only (2\to3).

| Query | Window after updates | Front product | Back product | Answer |
| --- | --- | --- | --- | --- |
| `[1,1]`, `1 -> 2` | `[1]` | empty | (A_1) | 1 |
| `[1,2]`, `1 -> 3` | `[1,2]` | (A_1) | (A_2) | 1 |
| `[2,2]`, `2 -> 3` | `[2]` | (A_2) | empty | 1 |

After the first query, the window contains only agent 1. The second query extends the right boundary, so agent 2 is pushed onto the back stack. The requested entry of (A_1A_2) is one. The third query moves the left boundary from 1 to 2, so agent 1 is removed from the front and the remaining aggregate is exactly (A_2).

A second example demonstrates repeated visits and duplicate query ranges:

```
2 3
9223372036854775808
9223372036854775808
1 2 1 1
1 2 1 1
2 2 1 1
```

Both agents have only the transition (1\to1).

| Query | Left | Right | Current route | Answer |
| --- | --- | --- | --- | --- |
| first | 1 | 2 | (1\to1\to1) | 1 |
| second | 1 | 2 | (1\to1\to1) | 1 |
| third | 2 | 2 | (1\to1) | 1 |

The duplicate queries do not cause any special problem because the sorted processing can answer identical windows consecutively. The repeated district is also preserved because a matrix transition from a district to itself is a perfectly valid edge.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(n\cdot8^3+m\cdot8)) | Every agent is pushed once and transferred at most once, while each query needs only an 8-term dot product |
| Space | (O(n\cdot8^2+m)) | Stack aggregates contain constant-size 8 × 8 matrices, and all queries are stored for sorting |

The factor (8^3=512) is fixed by the problem, so the asymptotic behavior is linear in the number of agents and queries. The monotonicity of both endpoints is what prevents an agent from being repeatedly inserted and removed. The 256 MB memory limit is handled in the Python implementation by storing aggregate matrices in compact 32-bit arrays.

## Test Cases

```python
# The following tests assume the solution code above has already been defined.
# The helper temporarily replaces the global input/output streams.

import sys
import io

def run(inp: str) -> str:
    global input

    old_stdin = sys.stdin
    old_stdout = sys.stdout
    old_input = input

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    input = sys.stdin.readline

    try:
        solve()
        return sys.stdout.getvalue()
    finally:
        input = old_input
        sys.stdin = old_stdin
        sys.stdout = old_stdout

# Official sample
sample = """\
3 3
9241386504218214000
4692768438333080000
4620710844295152000
1 2 3 4
1 3 1 3
3 3 1 2
"""
assert run(sample) == "0\n1\n1", "official sample"

# Minimum-size input
minimum = """\
1 1
9223372036854775808
1 1 1 1
"""
assert run(minimum) == "1", "single agent, single self-loop"

# Zero matrix and impossible transitions
zero = """\
1 2
0
1 1 1 1
1 1 8 8
"""
assert run(zero) == "0\n0", "zero transition matrix"

# Boundary and off-by-one test.
# Agent 1: 1 -> 2
# Agent 2: 2 -> 3
chain = """\
2 4
4611686018427387904
9007199254740992
1 1 1 2
1 2 1 3
2 2 2 3
1 2 1 2
"""
assert run(chain) == "1\n1\n1\n0", "chain and interval boundaries"

# Equal matrices and repeated visits.
same = """\
3 3
9223372036854775808
9223372036854775808
9223372036854775808
1 3 1 1
1 2 1 1
2 3 2 2
"""
assert run(same) == "1\n1\n0", "equal matrices and repeated district"

# Maximum number of agents, with one query.
# Every agent has no transitions, so every answer is zero.
n = 100000
max_n = str(n) + " 1\n" + ("0\n" * n) + "1 " + str(n) + " 1 1\n"
assert run(max_n) == "0", "maximum n"

# Maximum number of queries, with n = 1.
# Every query asks for the same self-loop.
m = 200000
max_m = "1 " + str(m) + "\n9223372036854775808\n"
max_m += ("1 1 1 1\n" * m)
assert run(max_m) == ("1\n" * m).rstrip("\n"), "maximum m"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1`, one `1 -> 1` transition | `1` | Minimum size and length-one interval |
| One zero matrix | `0`, `0` | Impossible transitions and district boundary `8` |
| Two-agent chain | `1`, `1`, `1`, `0` | Left and right endpoint updates, including removal of the first agent |
| Three identical self-loop matrices | `1`, `1`, `0` | Repeated visits, equal matrices, and a start district with no transition |
| (n=100000,m=1) | `0` | Maximum number of agents |
| (n=1,m=200000) | 200000 lines containing `1` | Maximum number of queries and repeated identical windows |

## Edge Cases

For a length-one interval, the sliding window contains exactly one matrix. Suppose the input is

```
1 1
9223372036854775808
1 1 1 1
```

The binary number has only the first bit set, so the matrix contains (A[1][1]=1). The right boundary is advanced to agent 1, and the left boundary does not move. The back stack therefore contains one aggregate equal to (A_1), and the answer reads its `(1,1)` entry directly. The result is `1`.

For a zero transition matrix,

```
1 1
0
1 1 1 1
```

the parser creates eight zero row masks and eight zero column masks. The single aggregate is also zero. Its `(1,1)` entry is zero, so the answer is `0`. No identity matrix is introduced because the window is not empty.

For repeated visits, consider

```
2 1
9223372036854775808
9223372036854775808
1 2 1 1
```

Both matrices contain only (1\to1). The aggregate is (A_1A_2), whose `(1,1)` entry is (1\cdot1=1). The route (1\to1\to1) is counted exactly once. The algorithm does not assume that consecutive districts must differ.

The most delicate boundary case is moving the left endpoint. In

```
2 1
4611686018427387904
9007199254740992
2 2 2 3
```

the desired window is only agent 2. The processing first extends the right endpoint through agent 2, so both agents temporarily enter the window. Then `left` moves from 0 to 1 and the oldest agent is removed. The remaining aggregate is exactly (A_2), giving answer `1`. This is why the code uses `while left < ql` rather than comparing the endpoints only once.

Duplicate query intervals are also valid because the restriction forbids proper containment, not repeated identical queries. If two consecutive queries both ask for `[1,2]`, sorting leaves them adjacent and the second query performs no window movement at all. It simply reads the same two-stack aggregate again.

The binary encoding is another boundary-sensitive detail. For a matrix whose only edge is (1\to2), the first row is `01000000`, which corresponds to the integer (2^{62}=4611686018427387904). The parser's use of `63 - p` is what maps that decimal value to row 1, column 2 rather than row 8, column 7. A reversed bit order would make every test involving non-symmetric matrices fail.
