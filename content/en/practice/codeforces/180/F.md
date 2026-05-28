---
title: "CF 180F - Mathematical Analysis Rocks!"
description: "Every student points to exactly one best friend, and every student is pointed to by exactly one other student. That means the friendship relation forms a permutation p. On day 1, notebook i stays with student i. On every following day, notebooks move according to p."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 180
codeforces_index: "F"
codeforces_contest_name: "Codeforces Round 116 (Div. 2, ACM-ICPC Rules)"
rating: 1200
weight: 180
solve_time_s: 88
verified: true
draft: false
---

[CF 180F - Mathematical Analysis Rocks!](https://codeforces.com/problemset/problem/180/F)

**Rating:** 1200  
**Tags:** constructive algorithms, implementation, math  
**Solve time:** 1m 28s  
**Verified:** yes  

## Solution
## Problem Understanding

Every student points to exactly one best friend, and every student is pointed to by exactly one other student. That means the friendship relation forms a permutation `p`.

On day 1, notebook `i` stays with student `i`.

On every following day, notebooks move according to `p`. After one transfer, notebook `i` goes to `p[i]`. After two transfers, it goes to `p[p[i]]`. In general, after `k` transfers, it goes to `p^k[i]`, the permutation applied `k` times.

The input gives two permutations:

`a[i]` is the owner of notebook `i` on the third day.

`b[i]` is the owner of notebook `i` on the fourth day.

Since day 1 is the starting position, the third day corresponds to applying `p` twice:

```
a[i] = p²[i]
```

The fourth day corresponds to applying `p` three times:

```
b[i] = p³[i]
```

We must reconstruct the original permutation `p`.

The constraint `n ≤ 100000` immediately rules out anything quadratic. A solution that tries all possible permutations is impossible. Even checking all pairs repeatedly would already be too slow. We need something close to linear time.

The tricky part is recognizing what the arrays actually represent. A careless implementation may treat `a[i]` as `p[i]` itself, but it is already the result after multiple applications of the permutation.

Another subtle case appears with fixed points. Consider:

```
n = 1
a = [1]
b = [1]
```

The only valid permutation is:

```
p = [1]
```

If the solution assumes every cycle has length at least two, it breaks immediately.

Another easy mistake is mixing up composition order. Suppose:

```
n = 4
a = [2 1 4 3]
b = [3 4 2 1]
```

A wrong derivation might compute `p[i] = a[b[i]]` instead of using the inverse relation correctly. Since permutation composition is directional, reversing the order silently produces the wrong permutation.

A final edge case involves longer cycles. For example:

```
n = 5
a = [3 4 5 1 2]
b = [4 5 1 2 3]
```

Here the answer is:

```
p = [2 3 4 5 1]
```

A solution that tries to infer the cycle structure locally instead of using the algebraic relation may fail because all positions participate in the same cycle.

## Approaches

A brute-force solution would try every possible permutation `p`, compute `p²` and `p³`, and compare them with `a` and `b`.

This works conceptually because the definitions match the process exactly. For a candidate permutation, we can simulate notebook movements and verify whether the resulting permutations equal the given arrays.

The problem is the number of permutations. There are `n!` possibilities. Even for `n = 10`, that is already more than three million permutations. For `n = 100000`, brute force is completely impossible.

The key observation comes from writing the given relations algebraically:

```
a = p²
b = p³
```

Since `b = p · a`, we can isolate `p`:

```
p = b · a⁻¹
```

This is the entire problem.

Because `a` is a permutation, it has an inverse permutation `a⁻¹`. Once we compute that inverse, every value of `p` becomes directly determined.

Suppose:

```
a[x] = y
```

Then:

```
p[y] = b[x]
```

Why? Because:

```
b[x] = p(a[x]) = p(y)
```

So if we iterate through all positions `x`, we can directly fill the permutation `p`.

This transforms the problem from impossible brute force into a simple linear-time reconstruction.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n! · n) | O(n) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read `n`, array `a`, and array `b`.
2. Create an array `p` of size `n`.
3. Iterate through every index `i` from `0` to `n-1`.
4. Let:

```
y = a[i]
```

Since `a[i] = p²[i]`, notebook `i` reaches student `y` on day 3.
5. On day 4, the same notebook reaches:

```
b[i] = p[y]
```

This directly tells us:

```
p[y] = b[i]
```
6. Store:

```
p[a[i]] = b[i]
```
7. Output the constructed permutation.

### Why it works

The algorithm relies on the identity:

```
b = p ∘ a
```

For every notebook `i`:

```
a[i] = p²[i]
b[i] = p³[i]
```

Applying one more transition to `a[i]` produces `b[i]`:

```
p(a[i]) = b[i]
```

Since `a` is a permutation, every value from `1` to `n` appears exactly once in `a`. That means every position in `p` is assigned exactly once, so the reconstruction is complete and unambiguous.

The statement guarantees the solution is unique, and this formula constructs exactly that unique permutation.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))

    p = [0] * n

    for i in range(n):
        p[a[i] - 1] = b[i]

    print(*p)

solve()
```

The implementation follows the mathematical derivation directly.

The array `a` uses 1-based student numbering, while Python lists use 0-based indexing. The assignment:

```
p[a[i] - 1] = b[i]
```

implements:

```
p[a[i]] = b[i]
```

with the required index shift.

A common mistake is trying to store:

```
p[i] = ...
```

instead of indexing by `a[i]`. The relation comes from where the notebook is on the third day, not from the notebook's original owner.

Another subtle point is that `b[i]` should not be decremented. It is stored as the permutation value itself, not as an array index.

The algorithm never explicitly computes an inverse permutation because the inverse relationship is already encoded by iterating through positions of `a`.

## Worked Examples

### Example 1

Input:

```
4
2 1 4 3
3 4 2 1
```

Trace:

| i | a[i] | b[i] | Assignment | p after step |
| --- | --- | --- | --- | --- |
| 0 | 2 | 3 | p[2] = 3 | [0,3,0,0] |
| 1 | 1 | 4 | p[1] = 4 | [4,3,0,0] |
| 2 | 4 | 2 | p[4] = 2 | [4,3,0,2] |
| 3 | 3 | 1 | p[3] = 1 | [4,3,1,2] |

Final answer:

```
4 3 1 2
```

This example shows that every value of `a` becomes a position inside `p`. Since `a` is a permutation, each slot is filled exactly once.

### Example 2

Input:

```
5
3 4 5 1 2
4 5 1 2 3
```

Trace:

| i | a[i] | b[i] | Assignment | p after step |
| --- | --- | --- | --- | --- |
| 0 | 3 | 4 | p[3] = 4 | [0,0,4,0,0] |
| 1 | 4 | 5 | p[4] = 5 | [0,0,4,5,0] |
| 2 | 5 | 1 | p[5] = 1 | [0,0,4,5,1] |
| 3 | 1 | 2 | p[1] = 2 | [2,0,4,5,1] |
| 4 | 2 | 3 | p[2] = 3 | [2,3,4,5,1] |

Final answer:

```
2 3 4 5 1
```

This example demonstrates a single large cycle. The algorithm works uniformly regardless of cycle structure.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | One pass through the arrays |
| Space | O(n) | Storage for the answer permutation |

With `n ≤ 100000`, linear complexity easily fits within the limits. The solution performs only a few simple assignments per element and uses modest memory.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline

    n = int(input())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))

    p = [0] * n

    for i in range(n):
        p[a[i] - 1] = b[i]

    print(*p)

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()

    backup_stdout = sys.stdout
    sys.stdout = out

    solve()

    sys.stdout = backup_stdout

    return out.getvalue()

# provided sample
assert run(
    "4\n2 1 4 3\n3 4 2 1\n"
) == "4 3 1 2\n", "sample 1"

# minimum size
assert run(
    "1\n1\n1\n"
) == "1\n", "single fixed point"

# single large cycle
assert run(
    "5\n3 4 5 1 2\n4 5 1 2 3\n"
) == "2 3 4 5 1\n", "single cycle"

# identity permutation
assert run(
    "3\n1 2 3\n1 2 3\n"
) == "1 2 3\n", "all fixed points"

# two disjoint swaps
assert run(
    "4\n1 2 3 4\n2 1 4 3\n"
) == "2 1 4 3\n", "multiple 2-cycles"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `n = 1` | `1` | Smallest valid input |
| Identity permutations | Identity answer | Fixed-point handling |
| One long cycle | Rotating permutation | Correct cycle reconstruction |
| Two swaps | Pairwise cycles | Multiple independent cycles |

## Edge Cases

Consider the smallest possible input:

```
1
1
1
```

The algorithm performs one iteration:

| i | a[i] | b[i] | Assignment |
| --- | --- | --- | --- |
| 0 | 1 | 1 | p[1] = 1 |

Result:

```
1
```

This confirms the solution correctly handles fixed points and does not assume cycle length greater than one.

Now consider the identity permutation:

```
3
1 2 3
1 2 3
```

Every notebook stays with its owner forever. The assignments become:

```
p[1] = 1
p[2] = 2
p[3] = 3
```

The algorithm reconstructs the identity permutation exactly.

Finally, consider a longer cycle:

```
5
3 4 5 1 2
4 5 1 2 3
```

The important detail here is that `a` itself is not the answer. A careless implementation may mistakenly output `a` directly because it resembles a shifted cycle. The trace shows that the correct reconstruction uses:

```
p[a[i]] = b[i]
```

which yields:

```
2 3 4 5 1
```

and not:

```
3 4 5 1 2
```
