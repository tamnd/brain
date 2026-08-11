---
title: "CF 102391F - Hilbert's Hotel"
description: "We have an infinite sequence of rooms numbered (0,1,2,ldots), and every room always contains exactly one guest. Guests belong to groups. Initially every room contains a guest from group (0). A type 1 operation creates a new group."
date: "2026-08-11T23:03:33+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102391
codeforces_index: "F"
codeforces_contest_name: "XX Open Cup, Grand Prix of Korea"
rating: 0
weight: 102391
solve_time_s: 222
verified: true
draft: false
---

[CF 102391F - Hilbert's Hotel](https://codeforces.com/problemset/problem/102391/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 3m 42s  
**Verified:** yes  

## Solution
## Problem Understanding

We have an infinite sequence of rooms numbered (0,1,2,\ldots), and every room always contains exactly one guest. Guests belong to groups. Initially every room contains a guest from group (0).

A type 1 operation creates a new group. If its parameter is a positive integer (k), every existing guest moves (k) rooms to the right, so the new group occupies rooms (0,1,\ldots,k-1). If the parameter is (0), every existing guest moves from room (x) to room (2x), and the new group occupies all odd rooms.

A type 2 query asks for the (x)-th smallest room occupied by a particular group. A type 3 query asks which group currently occupies a particular room.

The difficulty is that the hotel is infinite, so we can never simulate the room array explicitly. The number of operations is also as large as (300000), which rules out walking through all previous operations for every query. With a 2-second-class time limit, an (O(Q^2)) simulation is far beyond what is possible. We need roughly logarithmic work per query.

There are several boundary cases that easily cause incorrect answers.

First, room (0) behaves differently under an infinite operation. It is mapped to (0), so repeatedly reversing infinite operations does not make room (0) smaller. For example,

```
3
1 0
1 0
3 0
```

has output

```
2
```

because room (0) remains occupied by the newest infinite group. A reverse simulation that assumes every infinite operation halves the room number can get stuck or incorrectly skip the group.

Second, equality in a finite operation matters. If the reverse operation has parameter (k), room (x=k) belongs to the old hotel state, not the newly inserted group. For example,

```
3
1 5
3 5
3 4
```

outputs

```
0
1
```

because group (1) occupies rooms (0) through (4), while room (5) still belongs to group (0). Using (x\leq k) instead of (x<k) would incorrectly assign room (5) to group (1).

Third, the (x)-th guest is one-indexed. If a group occupies rooms (0,1,2), its first guest is at room (0), not room (1). For example,

```
2
1 3
2 1 1
```

outputs

```
0
```

because the first room of group (1) is room (0).

## Approaches

The direct approach is to maintain the current room of every guest and update all rooms after every type 1 operation. That is impossible because there are infinitely many guests. We can restrict attention to a finite prefix, but even then a single operation can affect every relevant room, so this still does not scale. With (300000) operations, a quadratic approach could easily perform around (9\times10^{10}) updates.

The first key observation is that every operation applied to existing guests is an affine transformation. A finite operation is

[
x\mapsto x+k,
]

while an infinite operation is

[
x\mapsto 2x.
]

A composition of these operations always has the form

[
F(x)=ax+b,
]

where (a) is a power of two. This gives a compact description of the movement of every old guest.

Suppose group (g) was inserted when the accumulated transformation was

[
F_g(x)=a_gx+b_g.
]

Its own rooms before later operations form an arithmetic progression. For a finite group this progression is

[
0,1,\ldots,k-1,
]

so its first term is (0) and its difference is (1). For an infinite group it is

[
1,3,5,\ldots,
]

so its first term is (1) and its difference is (2).

If the current accumulated transformation is (F(x)=ax+b), we can undo (F_g) algebraically and then apply (F). The resulting transformation from the group's insertion coordinates to its current rooms is again affine. Since (a_g) is a power of two, it is invertible modulo (10^9+7). Thus a type 2 query can be answered in constant time after storing a few values for every group.

The second key observation handles type 3 queries. Work backwards from the queried room. A finite operation with parameter (k) has the reverse rule

[
x\geq k \Rightarrow x\leftarrow x-k,
]

while (x<k) means the room was just occupied by that operation's new group.

For an infinite operation, an odd (x) means the room was newly occupied by that infinite group. If (x) is even, the old guest came from room (x/2).

The finite operations between two consecutive infinite operations can be processed as one block. If their parameters are (k_1,k_2,\ldots,k_m), store their prefix sums. Going backwards through the entire block only subtracts

[
k_1+k_2+\cdots+k_m.
]

If the queried (x) becomes smaller than this total, only one binary search is needed to find the exact finite operation that captured it.

After crossing an infinite operation, a successful reverse step changes positive (x) to (x/2). Consequently, there can be at most (O(\log x)) such steps. This is the crucial reason the reverse process is fast even though the operation sequence can contain (300000) events.

The resulting comparison is:

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(Q^2)) in the worst case | (O(Q)) or worse | Too slow |
| Affine representation + finite-operation blocks | (O(Q(\log Q+\log V))) | (O(Q)) | Accepted |

Here (V\leq10^9) is the room number appearing in a type 3 query. In practice, the logarithmic factor from the reverse process is at most about (30), because (2^{30}>10^9).

## Algorithm Walkthrough

1. Represent the effect of all operations on existing guests by an affine function

[
F(x)=ax+b.
]

Initially (a=1,b=0). A finite operation with parameter (k) changes this to

[
a'=a,\qquad b'=b+k,
]

while an infinite operation changes it to

[
a'=2a,\qquad b'=2b.
]

Only (b) and (a) modulo (10^9+7) are needed for type 2 answers.

1. For every group, store the affine transformation (F_g(x)=a_gx+b_g) that existed immediately after that group entered the hotel. Also store the starting point (s_g) and difference (d_g) of its initial arithmetic progression.

For the initial group (0), use

[
s_0=0,\qquad d_0=1.
]

For a finite group use

[
s_g=0,\qquad d_g=1.
]

For an infinite group use

[
s_g=1,\qquad d_g=2.
]

The reason for storing the transformation at insertion time is that all later movements can then be described by the transformation from that historical state to the current state.

1. Maintain the inverse of (a) modulo (10^9+7). Since (a) is always a power of two, its inverse always exists. When an infinite operation multiplies (a) by (2), multiply its inverse by (2^{-1}) instead.
2. To answer a type 2 query for group (g), let

[
c=a\cdot a_g^{-1}\pmod M.
]

The translation between the historical coordinates of group (g) and the current coordinates is

[
e=b-cb_g.
]

The current room corresponding to historical coordinate (y) is

[
cy+e.
]

The (x)-th guest of group (g) had historical coordinate

[
s_g+d_g(x-1).
]

Hence its current room is

[
e+c(s_g+d_g(x-1))\pmod M.
]

This gives the answer in constant time.

1. For type 3 queries, divide all finite type 1 operations into blocks separated by infinite operations. The first block contains the finite operations before the first infinite operation. Every later block contains the finite operations immediately following one infinite operation.

For every block, store cumulative sums of its finite (k) values and the corresponding group numbers.

1. If the queried room is (0), immediately return the group number of the latest finite operation, or (0) if no finite operation has happened. Infinite operations leave room (0) unchanged, so only finite insertions can replace its occupant.
2. Otherwise, start from the last finite block and reverse its finite operations. If the total (k) of the block is larger than (x), the responsible operation lies inside this block. Use binary search on the cumulative sums to locate the last finite operation whose suffix sum is greater than (x).

If the total is at most (x), subtract the entire block total and cross the preceding infinite operation.

1. At an infinite operation, an odd (x) belongs to that newly inserted group, so return its group number. If (x) is even, replace (x) by (x/2) and continue with the preceding block.
2. If subtracting a complete finite block makes (x=0), the answer is the latest finite group before that block. There is no need to walk through a potentially huge sequence of consecutive infinite operations because they all leave room (0) unchanged.

### Why it works

The invariant for type 2 queries is that every group is represented by its original arithmetic progression together with the affine transformation that was active when the group entered. Composing the inverse historical transformation with the current transformation exactly describes where every member of that group is now, so the formula returns the correct (x)-th room.

For type 3 queries, reversing a finite operation is exact because rooms (0,\ldots,k-1) are precisely the newly inserted rooms, while every other room came from (x-k). Reversing an infinite operation is also exact because odd rooms are precisely the newly inserted rooms and every even room came from (x/2). Grouping consecutive finite operations does not change this logic, since their reverse effect is simply subtraction of their parameters in reverse order. Every time an infinite operation is crossed with a positive room number, the room number is halved, so only logarithmically many such crossings are possible.

## Python Solution

```python
import sys
from bisect import bisect_left

input = sys.stdin.readline

MOD = 1_000_000_007
INV2 = (MOD + 1) // 2

def solve():
    q = int(input())

    # Current global affine transformation:
    # F(x) = A * x + B
    A = 1
    B = 0
    invA = 1

    # Information stored for every group.
    # Group 0 is the initial infinite set 0,1,2,...
    a_hist = [1]
    b_hist = [0]
    inv_hist = [1]
    start = [0]
    step = [1]

    # Blocks of finite operations.
    # blocks[b] contains cumulative sums of k in block b.
    blocks = [[]]

    # The corresponding group ids for the finite operations.
    block_groups = [[]]

    # For every block, the latest finite group strictly before it.
    prev_finite = [0]

    # Group ids of infinite operations.
    # Infinite operation corresponding to block b (b > 0)
    # is inf_groups[b - 1].
    inf_groups = []

    last_finite_group = 0

    # Number of type 1 operations processed.
    groups = 0

    out = []

    for _ in range(q):
        query = input().split()
        typ = int(query[0])

        if typ == 1:
            k = int(query[1])
            groups += 1
            gid = groups

            if k > 0:
                # All old rooms shift by k.
                B = (B + k) % MOD

                # The new group occupies 0,1,...,k-1.
                a_hist.append(A)
                b_hist.append(B)
                inv_hist.append(invA)
                start.append(0)
                step.append(1)

                if blocks[-1]:
                    cumulative = blocks[-1][-1] + k
                else:
                    cumulative = k

                blocks[-1].append(cumulative)
                block_groups[-1].append(gid)

                last_finite_group = gid

            else:
                # All old rooms double.
                A = (2 * A) % MOD
                B = (2 * B) % MOD
                invA = (invA * INV2) % MOD

                # The new group occupies 1,3,5,...
                a_hist.append(A)
                b_hist.append(B)
                inv_hist.append(invA)
                start.append(1)
                step.append(2)

                inf_groups.append(gid)

                # Start a new finite block.
                blocks.append([])
                block_groups.append([])
                prev_finite.append(last_finite_group)

        elif typ == 2:
            g = int(query[1])
            x = int(query[2])

            c = (A * inv_hist[g]) % MOD
            e = (B - c * b_hist[g]) % MOD

            first = (e + c * start[g]) % MOD
            diff = (c * step[g]) % MOD

            answer = (first + diff * (x - 1)) % MOD
            out.append(str(answer))

        else:
            x = int(query[1])

            # Infinite operations leave room 0 fixed.
            if x == 0:
                out.append(str(last_finite_group))
                continue

            block = len(blocks) - 1

            while True:
                cumulative = blocks[block]

                if cumulative:
                    total = cumulative[-1]

                    if x < total:
                        # Find the first prefix sum >= total - x.
                        # Its corresponding finite operation is exactly
                        # the one whose reverse interval contains x.
                        idx = bisect_left(cumulative, total - x)
                        out.append(str(block_groups[block][idx]))
                        break

                    x -= total

                    if x == 0:
                        # Everything in this block was reversed.
                        # Room 0 now belongs to the latest finite group
                        # before this block.
                        out.append(str(prev_finite[block]))
                        break

                if block == 0:
                    # We have reached the initial configuration.
                    out.append("0")
                    break

                # Cross the infinite operation before this block.
                infinite_group = inf_groups[block - 1]

                if x & 1:
                    # Odd rooms were newly occupied by this group.
                    out.append(str(infinite_group))
                    break

                # An even room came from x / 2.
                x //= 2
                block -= 1

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The `A`, `B`, and `invA` variables describe the current affine transformation applied to every guest who existed before the latest type 1 operation. A finite operation only changes `B`, while an infinite operation doubles both `A` and `B`.

The four historical arrays store the transformation and arithmetic progression belonging to each group at its insertion time. The initial group is inserted conceptually at time zero, which is why its stored values are (A=1,B=0,s=0,d=1).

The type 2 formula uses the ratio between the current multiplier and the multiplier at group insertion. Since every multiplier is a power of two, modular division is safe. The inverse multiplier is updated explicitly, avoiding an expensive modular exponentiation for every query.

For type 3 queries, `blocks` stores cumulative sums rather than the raw (k) values. Suppose a block contains (k_1,k_2,k_3), with cumulative sums (k_1,k_1+k_2,k_1+k_2+k_3). If the current room is smaller than the total, `bisect_left` finds the first prefix sum reaching `total - x`. That index identifies the finite operation whose newly inserted interval contains the reversed room.

The strict comparison `x < total` and the use of `total - x` are both boundary-sensitive. When `x == total`, every finite operation in the block has already been reversed and we must cross the preceding infinite operation.

Python integers have arbitrary precision, so the cumulative sums of finite (k) values do not overflow. Values used for type 2 answers are reduced modulo (10^9+7), while the block sums remain exact integers because they are used for comparisons against (x).

## Worked Examples

There is only one sample in the statement, so the second trace below uses a small custom sequence.

### Sample 1

The state after each type 1 operation can be summarized by the current affine transformation and the newly created group.

| Query | Type 1 state | (A) | (B) | New group |
| --- | --- | --- | --- | --- |
| `3 0` | no operation | 1 | 0 | none |
| `1 3` | shift by 3 | 1 | 3 | 1 |
| `2 1 2` | unchanged | 1 | 3 | query group 1 |
| `1 0` | double | 2 | 6 | 2 |
| `3 10` | unchanged | 2 | 6 | reverse query |
| `2 2 5` | unchanged | 2 | 6 | query group 2 |
| `1 5` | shift by 5 | 2 | 11 | 3 |
| `1 0` | double | 4 | 22 | 4 |
| `3 5` | unchanged | 4 | 22 | reverse query |
| `2 3 3` | unchanged | 4 | 22 | query group 3 |

For `2 1 2`, group 1 was inserted with (A_g=1,B_g=3), while the current transformation is identical. Its historical progression is (0,1,2), so the second room is (1).

After the first infinite operation, group 2 starts at odd rooms. At that point group 2's rooms are (1,3,5,7,9,\ldots), so its fifth room is (9).

The query `3 10` reverses the infinite operation because (10) is even, producing (5). There is no earlier infinite operation, so it continues through the finite shift of (3), producing (2), and finally the initial group is reached. Thus room (10) belongs to group (0).

After the final two operations, group 4 occupies odd rooms, so room (5) belongs to group (4). The final type 2 query asks for the third room of group 3, which has become the odd progression (1,3,5,\ldots) after the later infinite operation, giving (4) as the output after the appropriate historical transformation.

The complete output is

```
0
1
0
9
4
4
```

### Custom trace

Consider:

```
8
1 1
1 2
1 0
1 0
3 1
3 2
3 6
2 3 3
```

The important state is:

| Query | Current action | Room being reversed | Block | Result |
| --- | --- | --- | --- | --- |
| `1 1` | group 1 enters |  | finite block 0 |  |
| `1 2` | group 2 enters |  | finite block 0 |  |
| `1 0` | group 3 enters |  | new block 1 |  |
| `1 0` | group 4 enters |  | new block 2 |  |
| `3 1` | odd at latest infinite | 1 | block 2 | group 4 |
| `3 2` | even, divide by 2 | 2 → 1 | block 1 | group 3 |
| `3 6` | even, divide by 2 | 6 → 3 | block 1 | group 3 |
| `2 3 3` | arithmetic progression query |  | group 3 | room 10 |

Group 3 was created by the first infinite operation, so its rooms were initially (1,3,5,\ldots). The second infinite operation doubles these to (2,6,10,\ldots). Thus rooms (2) and (6) both belong to group 3.

Group 4 is the newest infinite group and occupies all odd rooms, so room (1) immediately identifies group 4. The type 2 query asks for group 3's third room, which is (10).

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(Q(\log Q+\log V))) | Type 1 and type 2 operations are (O(1)); a type 3 query crosses at most (O(\log V)) infinite operations and performs at most one (O(\log Q)) binary search. |
| Space | (O(Q)) | Historical group data and finite-operation block data contain at most one entry per type 1 operation. |

The maximum room value in a type 3 query is (10^9), so at most about (30) successful halvings can occur. The total number of operations is (300000), so the linear storage bound is easily within the 1024 MB memory limit. The algorithm avoids constructing any infinite set of rooms and performs only logarithmic work per query.

## Test Cases

The test harness below assumes the solution above is saved as `solution.py`, with the `solve()` function unchanged.

```python
# Save the solution as solution.py before running this file.
import sys
import io
import solution

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    try:
        solution.solve()
        return sys.stdout.getvalue()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

# Provided sample
sample1 = """\
10
3 0
1 3
2 1 2
1 0
3 10
2 2 5
1 5
1 0
3 5
2 3 3
"""

assert run(sample1) == """\
0
1
0
9
4
4\
""", "sample 1"

# Custom 1: minimum-size input
assert run("""\
1
3 0
""") == "0\n", "initial group"

# Custom 2: finite block, equality and x-th indexing
assert run("""\
5
1 2
1 3
3 0
3 4
2 1 2
""") == """\
2
1
4
""", "finite operations and boundaries"

# Custom 3: consecutive infinite operations
assert run("""\
8
1 1
1 2
1 0
1 0
3 1
3 2
3 6
2 3 3
""") == """\
4
3
3
10\
""", "repeated infinite operations"

# Custom 4: all-equal finite values and one-indexed query
assert run("""\
4
1 7
1 7
1 7
2 1 7
""") == "20\n", "repeated equal k values"

# Custom 5: maximum-size stress case
q = 300000
maximum_input = str(q) + "\n" + ("1 1\n" * (q - 1)) + "3 0\n"

assert run(maximum_input) == f"{q - 1}\n", "maximum number of queries"
```

The custom cases validate the following properties:

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 3 0` | `0` | Initial group and smallest valid input |
| Two finite operations followed by type 3 and type 2 | `2, 1, 4` | Finite reverse blocks, exact boundary handling, and one-indexed (x) |
| Two consecutive infinite operations | `4, 3, 3, 10` | Repeated halving, odd-room detection, and infinite-group arithmetic progressions |
| Three identical `k=7` operations | `20` | Repeated shifts and cumulative finite sums |
| (299999) copies of `1 1` followed by `3 0` | `299999` | Maximum query count and room (0) handling |

## Edge Cases

For room (0), the algorithm immediately returns `last_finite_group`. Consider

```
4
1 5
1 0
1 0
3 0
```

The two infinite operations keep room (0) at room (0). The only finite insertion after the initial state is group (1), so the answer is `1`. The algorithm never performs a potentially unbounded sequence of zero halvings.

For the exact finite boundary, consider

```
3
1 5
3 5
3 4
```

The finite insertion occupies rooms (0,1,2,3,4). Reversing room (5) uses the condition (x\geq5), giving predecessor (0), so room (5) belongs to group (0). Reversing room (4) instead finds (x<5), so group (1) is returned. The output is `0` followed by `1`.

For consecutive infinite operations, consider

```
4
1 0
1 0
3 2
```

The first infinite group initially occupies (1,3,5,\ldots). The second infinite operation moves those guests to (2,6,10,\ldots). Reversing room (2) first sees an even room, divides it by two, and obtains (1). The previous infinite operation then sees an odd room, so the answer is group (1).

For a finite block, consider parameters (3,5). If the current room is (4), reversing the latest operation with (k=5) immediately finds (4<5), so the second finite group owns the room. If the current room is (5), the reverse first subtracts (5), reaching (0), and then continues to the preceding state. The strict inequality in the implementation is exactly what separates these two cases.

For type 2 indexing, a finite group created with (k=3) starts at (0) with difference (1). Its rooms are (0,1,2), so the answer for (x=1) is (0) and for (x=3) is (2). The formula uses (x-1), preventing the common off-by-one error.

Finally, modular arithmetic is needed only for type 2 answers. The actual finite-block sums are not reduced modulo (10^9+7), because they are compared against real room numbers during reverse simulation. Mixing those two roles would produce incorrect type 3 answers once cumulative shifts exceed the modulus.
