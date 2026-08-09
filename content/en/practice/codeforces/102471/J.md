---
title: "CF 102471J - Permutation"
description: "We have a permutation of the numbers from 1 to n, and an integer c. An operation looks at exactly c+1 consecutive positions. If the smallest value in that interval is at one endpoint, that endpoint is kept fixed and the other c values may be rearranged arbitrarily."
date: "2026-08-09T18:42:43+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102471
codeforces_index: "J"
codeforces_contest_name: "2019 ICPC Asia-East Continent Final"
rating: 0
weight: 102471
solve_time_s: 450
verified: true
draft: false
---

[CF 102471J - Permutation](https://codeforces.com/problemset/problem/102471/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 7m 30s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a permutation of the numbers from `1` to `n`, and an integer `c`. An operation looks at exactly `c+1` consecutive positions. If the smallest value in that interval is at one endpoint, that endpoint is kept fixed and the other `c` values may be rearranged arbitrarily.

The task is not to find one reachable permutation. We need the total number of distinct permutations that can be reached after applying such operations any number of times, with the answer taken modulo `998244353`. The official statement uses the same two endpoint cases, one with the minimum at the left endpoint and one with the minimum at the right endpoint.

The decisive role is played by the position of `1`. Since `1` is globally smallest, it can never be moved by an operation. Any operation containing `1` must have `1` as its endpoint. Consequently, operations using `1` can only rearrange the `c` positions immediately to its left or the `c` positions immediately to its right.

Let there be `L` elements to the left of `1` and `R` elements to its right. Operations on the two sides never have to interact, so the total number of reachable permutations is the product of the number obtainable from the left side and the number obtainable from the right side.

The constraints make an exponential or factorial algorithm impossible. Although the statement allows `n` up to `500000`, the sum of `n` over all test cases is also at most `500000`. This means the intended solution should be essentially linear in the total input size. Even `O(n log n)` is unnecessary here, while anything involving the `n!` possible permutations is immediately impossible.

There are several easy boundary cases that a careless implementation can mishandle. For example, consider

```
1
2 2
1 2
```

There is no interval of length `3`, so no operation is possible. The answer is `1`. A solution that treats the `c` positions beside `1` as freely permutable even when fewer than `c` positions exist would incorrectly return `2`.

Another important case is

```
1
3 2
2 1 3
```

The value `1` is in the middle, so there is only one element on either side. Neither side contains the required `c=2` elements. Again the answer is `1`. The fact that `1` has nearby elements is not enough, the whole group of `c` movable elements must exist.

On the other hand,

```
1
3 2
1 2 3
```

has two elements to the right of `1`. The entire pair can be permuted, so the answer is `2`. This is the smallest example where an operation actually exists.

The input is guaranteed to be a permutation, so an "all equal values" test is not a valid test for this problem. Such an input would violate the definition of a permutation. The implementation should rely on distinct values and should not attempt to support duplicates as a special case.

## Approaches

A direct approach is to perform a breadth-first search over reachable permutations. For every current permutation, inspect every interval of length `c+1`. Whenever the minimum is at an endpoint, generate every permutation of the other `c` elements and insert the resulting arrays into a visited set.

This is correct because every legal operation is explicitly enumerated, and BFS continues until there is no unseen permutation. The problem is the size of the state space. There can be `n!` different permutations, and even checking all intervals for every state already costs `O(n · n!)`. If every possible rearrangement inside an operation is explicitly generated, the transition work contains another factor of up to `c!`. With `n` reaching `500000`, this is not remotely feasible.

The structure around `1` gives a much smaller description. Since `1` never moves, consider only one side of it. Suppose this side contains `m` elements, ordered from the position closest to `1` toward the outside.

The first `c` positions can be permuted whenever they exist. Among these `c` positions, one element is distinguished: the smallest one. It can move inside those `c` positions, but it cannot escape them. When another complete group of `c` positions becomes available, the same reasoning creates another distinguished element whose position is restricted to the first `2c` positions of the side. Continuing outward creates one restricted element for every complete group of `c` positions.

Thus, if

[
k=\left\lfloor\frac{m}{c}\right\rfloor,
]

there are exactly `k` nested restrictions. The `j`-th restricted element must occupy one of the first `jc` positions. When we count these restricted elements from the smallest allowed prefix to the largest, `j-1` positions have already been occupied by earlier restricted elements. Hence the `j`-th element has

[
jc-(j-1)=j(c-1)+1
]

choices.

After all `k` restricted elements have been placed, the other `m-k` elements have no remaining restriction and can be arranged arbitrarily. Their contribution is `(m-k)!`.

So the contribution of a side containing `m` elements is

[
F(m,c)=
(m-k)!\prod_{j=1}^{k}\left(jc-j+1\right),
\qquad
k=\left\lfloor\frac{m}{c}\right\rfloor.
]

If `m<c`, then `k=0`, giving `F(m,c)=m!`. However, this expression would be wrong for the actual operation rules because no operation exists when fewer than `c` elements are present. In that case the correct contribution is `1`. Therefore we use

[
F(m,c)=
\begin{cases}
1,&m<c,\
(m-k)!\displaystyle\prod_{j=1}^{k}(jc-j+1),&m\ge c.
\end{cases}
]

The final answer is simply

[
F(L,c)\cdot F(R,c).
]

The brute force works because it explicitly explores the same reachable state space that the combinatorial argument describes. The observation about `1` lets us replace that enormous state space by two independent sides and a small number of nested position restrictions. This is the same structural observation highlighted in the published solution discussion.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `O(n · n! · c!)` in the explicit transition version | `O(n!)` | Too slow |
| Optimal | `O(n)` per test case | `O(n)` | Accepted |

## Algorithm Walkthrough

1. Find the position of `1`. If it is at zero-based position `pos`, then there are `L=pos` elements on its left and `R=n-1-pos` elements on its right. Since `1` can never move, these two sides can be counted independently.
2. Precompute factorials modulo `998244353` up to the largest `n`. The final side formula contains `(m-k)!`, so factorial values are needed for constant-time access.
3. Define the contribution of a side of length `m`. If `m<c`, return `1`, because there are not enough elements to form an operation containing `1` and `c` movable elements.
4. Otherwise set `k=m//c`. There are `k` nested restricted elements, because every complete group of `c` positions creates one more prefix in which a distinguished element is allowed to move.
5. Start the side contribution with `(m-k)!`. These are the elements that remain completely unrestricted after all restricted elements have been accounted for.
6. For every `j` from `1` through `k`, multiply by `jc-j+1`. The `j`-th restricted element has `jc` possible positions in its allowed prefix, but `j-1` of those positions are already occupied by previously processed restricted elements.
7. Compute the contribution independently for the left and right sides and multiply them modulo `998244353`. The two sides do not compete for positions because `1` separates them permanently.

### Why it works

The invariant is that after exposing `j` complete groups of `c` positions on one side, exactly `j` distinguished elements have restricted locations, and the `j`-th one is allowed anywhere inside the first `jc` positions. Earlier distinguished elements remain inside those prefixes, while every other element in the exposed region can be rearranged freely.

Because these allowed prefixes are nested, the restricted elements can be placed one after another. At stage `j`, exactly `j-1` positions inside the first `jc` positions are already occupied by earlier restricted elements, leaving `jc-j+1` choices. Once all `k` restricted elements are placed, every other element is unrestricted, giving `(m-k)!` arrangements.

Every reachable arrangement satisfies these restrictions because an operation keeps the minimum endpoint fixed. Conversely, the operations can realize every arrangement satisfying the nested restrictions by successively exposing the next group of `c` positions and permuting all currently free positions. Thus the formula counts every reachable permutation exactly once.

## Python Solution

```python
import sys

input = sys.stdin.readline

MOD = 998244353

def side_ways(m, c, fact):
    if m < c:
        return 1

    k = m // c
    ans = fact[m - k]

    for j in range(1, k + 1):
        ans = ans * (j * c - j + 1) % MOD

    return ans

def solve():
    t = int(input())

    tests = []
    max_n = 0

    for _ in range(t):
        n, c = map(int, input().split())
        p = list(map(int, input().split()))
        tests.append((n, c, p))
        max_n = max(max_n, n)

    fact = [1] * (max_n + 1)
    for i in range(1, max_n + 1):
        fact[i] = fact[i - 1] * i % MOD

    out = []

    for n, c, p in tests:
        pos = p.index(1)

        left = pos
        right = n - 1 - pos

        ans_left = side_ways(left, c, fact)
        ans_right = side_ways(right, c, fact)

        ans = ans_left * ans_right % MOD
        out.append(str(ans))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The factorial precomputation is done once for all test cases. This matters because there can be up to `100000` test cases, although their total length is only `500000`.

The position of `1` is found with `p.index(1)`. With zero-based indexing, that position is exactly the number of elements on its left, while `n-1-pos` is the number on its right.

The `m<c` check is essential. The formula with `k=0` would give `m!`, but when fewer than `c` elements exist, there is no legal interval involving `1`, so the side is completely unchanged and contributes exactly `1`.

For `m>=c`, `k=m//c` counts complete groups of `c` positions. The loop multiplies the `k` factors `jc-j+1`. Its total number of iterations over both sides is `O(n/c)` for a test case, which is at most `O(n)`.

Python integers do not overflow, but every multiplication is reduced modulo `998244353`. The factorial array also stores values modulo the same modulus.

The input is read using `sys.stdin.readline`, as required for the large total input size.

## Worked Examples

### Sample 1

The first test case is

```
5 3
3 4 2 1 5
```

The value `1` is at position `4` in one-based indexing. Thus there are `3` elements on its left and `1` on its right.

For the left side, `m=3` and `c=3`, so `k=1`.

| Side | `m` | `c` | `k` | Factorial part | Restricted factors | Contribution |
| --- | --- | --- | --- | --- | --- | --- |
| Left | 3 | 3 | 1 | `2! = 2` | `3-1+1 = 3` | `6` |
| Right | 1 | 3 | 0 | not used | none | `1` |

The final answer is `6*1=6`.

The left side consists of exactly `c` elements, so the operation around `1` can arbitrarily permute those three elements. There are `3!=6` possibilities.

### Sample 2

The second test case is

```
5 4
4 2 1 3 5
```

Here `1` is in position `3`. Both sides contain exactly two elements, but `c=4`.

| Side | `m` | `c` | `m<c` | Contribution |
| --- | --- | --- | --- | --- |
| Left | 2 | 4 | yes | `1` |
| Right | 2 | 4 | yes | `1` |

No interval of length `5` containing `1` exists, so no operation can involve `1`. The other possible length `5` interval is the entire array, whose minimum is `1` in the middle, so it is invalid as well. The answer is `1`.

These two samples demonstrate both sides of the main boundary: having exactly `c` elements gives freedom, while having fewer than `c` gives none.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(n)` per test case, `O(sum n)` overall | Finding `1` is linear, and the side loops together use at most linear work |
| Space | `O(n)` | The permutation and factorial array use linear memory |

The total `n` over all test cases is at most `500000`, so the factorial precomputation and all per-test-case work together are `O(500000)`. The memory usage is also linear and comfortably fits the `256 MB` limit. The official problem specifies the same `500000` aggregate bound and `998244353` modulus.

## Test Cases

```python
import sys
import io

MOD = 998244353

def reference(inp: str) -> str:
    data = inp.split()
    it = iter(data)

    t = int(next(it))
    tests = []
    max_n = 0

    for _ in range(t):
        n = int(next(it))
        c = int(next(it))
        p = [int(next(it)) for _ in range(n)]
        tests.append((n, c, p))
        max_n = max(max_n, n)

    fact = [1] * (max_n + 1)
    for i in range(1, max_n + 1):
        fact[i] = fact[i - 1] * i % MOD

    def side(m, c):
        if m < c:
            return 1

        k = m // c
        ans = fact[m - k]

        for j in range(1, k + 1):
            ans = ans * (j * c - j + 1) % MOD

        return ans

    ans = []

    for n, c, p in tests:
        pos = p.index(1)
        left = pos
        right = n - pos - 1

        ans.append(str(side(left, c) * side(right, c) % MOD))

    return "\n".join(ans) + "\n"

# Provided samples.
sample = """\
5
5 3
3 4 2 1 5
5 4
4 2 1 3 5
5 2
4 5 3 1 2
5 3
4 3 2 1 5
5 2
2 3 1 5 4
"""

assert reference(sample) == "6\n1\n4\n6\n4\n", "provided samples"

# Minimum-size case. No interval of length c+1 exists.
assert reference("""\
1
2 2
1 2
""") == "1\n", "minimum n"

# 1 in the middle, so neither side contains c elements.
assert reference("""\
1
3 2
2 1 3
""") == "1\n", "insufficient elements on both sides"

# Exactly c elements on one side can be permuted.
assert reference("""\
1
3 2
1 2 3
""") == "2\n", "exactly one active side"

# Both sides contain exactly c elements.
assert reference("""\
1
5 2
2 3 1 5 4
""") == "4\n", "two independent sides"

# Four elements on one side with c = 2.
# The side contribution is:
# (4 - 2)! * 2 * 3 = 12.
assert reference("""\
1
5 2
1 2 3 4 5
""") == "12\n", "multiple nested restrictions"

# Maximum-size n with c = n.
# No side can contain c elements, so the answer is 1.
n = 500000
p = list(range(1, n + 1))
large_input = "1\n{} {}\n{}\n".format(n, n, " ".join(map(str, p)))
assert reference(large_input) == "1\n", "maximum-size boundary"

# Duplicate values are deliberately not tested:
# [1, 1, 2] is not a valid permutation for this problem.
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 2 / 1 2` | `1` | Minimum size and absence of any legal interval |
| `3 2 / 2 1 3` | `1` | `1` in the middle with both sides too short |
| `3 2 / 1 2 3` | `2` | Exactly `c` elements on one side |
| `5 2 / 2 3 1 5 4` | `4` | Two independent active sides |
| `5 2 / 1 2 3 4 5` | `12` | More than one nested restriction |
| `500000 500000 / 1 2 ... 500000` | `1` | Maximum `n` and the `c=n` boundary |

The requested all-equal test cannot be included because the input is guaranteed to be a permutation, so repeated values would make the test invalid rather than exercise an edge case of the algorithm.

## Edge Cases

When a side contains fewer than `c` elements, no operation involving `1` can use that side. For example,

```
1
2 2
1 2
```

has one element on the right, which is fewer than `c=2`. The side contribution is `1`, and there is no other valid interval. The algorithm enters the `m<c` branch and returns `1`.

When `1` is strictly inside the permutation and both sides are shorter than `c`, neither side can participate. For

```
1
3 2
2 1 3
```

both sides have length `1`. The algorithm computes `F(1,2)=1` twice, producing `1`.

When a side has exactly `c` elements, those elements can be arbitrarily permuted. For

```
1
3 2
1 2 3
```

the right side has length `2`. Here `k=1`, so the contribution is

[
(2-1)!\cdot(2-1+1)=1\cdot2=2.
]

The left side contributes `1`, giving the final answer `2`.

When a side is longer than `c`, additional nested restrictions appear. For `m=4,c=2`, we have `k=2`. The contribution is

[
(4-2)!\cdot2\cdot3
=2\cdot2\cdot3
=12.
]

The first restricted element has `2` possible positions, while the second has `4-1=3` choices after the first restricted element has been placed. The remaining two elements are unrestricted and contribute `2!`.

When `c=n`, neither side can contain `c` elements because their combined size is only `n-1`. Thus every test case with `c=n` has answer `1`. The maximum-size test with `n=c=500000` exercises exactly this boundary and is handled by the `m<c` branch on both sides.
