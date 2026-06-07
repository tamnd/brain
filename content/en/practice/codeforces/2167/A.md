---
title: "CF 2167A - Square?"
description: "We are given four stick lengths per test case, and we want to know whether these four sticks can be arranged to form the boundary of a square."
date: "2026-06-07T23:24:13+07:00"
tags: ["codeforces", "competitive-programming", "math", "sortings"]
categories: ["algorithms"]
codeforces_contest: 2167
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 1062 (Div. 4)"
rating: 800
weight: 2167
solve_time_s: 68
verified: true
draft: false
---

[CF 2167A - Square?](https://codeforces.com/problemset/problem/2167/A)

**Rating:** 800  
**Tags:** math, sortings  
**Solve time:** 1m 8s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given four stick lengths per test case, and we want to know whether these four sticks can be arranged to form the boundary of a square. Each stick must be used as a whole segment, and we are not allowed to cut or deform them, so the only freedom we have is how to assign each stick to one side of the square.

A square has four sides of identical length. Since we are not combining sticks, each side must correspond to exactly one stick, which means the four given lengths must collectively represent the four equal sides of the square.

This immediately reduces the task to checking whether all four numbers can be made equal after rearrangement is not even needed, since order does not matter.

The constraints are small per test case, with each length between 1 and 10, but the number of test cases can be as large as 10^4. This pushes us toward an O(1) or O(log n) per test solution, since even a linear scan per test is trivial but anything involving combinatorial checking would be unnecessary.

A subtle failure case appears when someone tries to be overly flexible, for example by attempting to “pair” sticks or combine them mentally. For instance, with input `1 2 1 2`, one might think pairing equal values helps form opposite sides of a square. But this is invalid because each side must be exactly one stick, so unequal values cannot form a square even if they appear in balanced pairs.

Another misleading case is `1 1 5 5`. It might resemble a rectangle intuition, but a square requires all four sides equal, so this is still impossible.

## Approaches

A brute-force interpretation would be to try assigning each stick to one of four sides and check whether a valid square can be formed. However, since all four sides of a square must be equal, any assignment that uses all four sticks immediately forces a single condition: all chosen side lengths must match exactly.

A more general brute-force idea would be to permute assignments of sticks to sides, but there are only four sticks, so this is at most 4! = 24 arrangements. For each arrangement, we check whether all sides are equal. This is already constant work per test case, so even the naive approach is effectively sufficient.

The key simplification is recognizing that permutations are irrelevant. Since all four sides must be identical, the only property that matters is whether all four values are equal. Sorting is optional, but even without sorting, we just check equality across all elements.

This reduces the problem to a single comparison: the maximum equals the minimum, or equivalently all values are identical.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force permutations | O(1) per test (24 checks) | O(1) | Accepted |
| Direct equality check | O(1) per test | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the four stick lengths for a test case. We treat them as a small multiset where order is irrelevant.
2. Check whether all four values are equal. This can be done by comparing each value to the first one.
3. If every comparison succeeds, output "YES" because all sticks can serve as equal sides of a square.
4. Otherwise output "NO" because at least one side length differs, making a square impossible without cutting or modifying sticks.

### Why it works

A square boundary consists of exactly four equal-length edges. Since each input stick must be used as a single edge, the only valid configuration is that all four input values are identical. No rearrangement or grouping can change this constraint, because merging sticks is not allowed. Therefore, equality across all four values is both necessary and sufficient.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    a, b, c, d = map(int, input().split())
    if a == b == c == d:
        print("YES")
    else:
        print("NO")
```

The solution reads each test case independently and performs a constant-time comparison chain. The chained equality check `a == b == c == d` directly enforces the condition that all four sides match, avoiding any sorting or extra data structures.

No special ordering or preprocessing is needed because the problem does not depend on arrangement, only on equality.

## Worked Examples

We trace two inputs: one positive and one negative case.

### Example 1: `1 1 1 1`

| Step | a | b | c | d | Check result |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 1 | 1 | 1 | all equal |

All comparisons succeed, so the algorithm outputs YES. This confirms the condition where a square exists trivially with all sides identical.

### Example 2: `1 2 1 2`

| Step | a | b | c | d | Check result |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 2 | 1 | 2 | mismatch at first comparison |

The first inequality already fails since `a != b`, so the condition is false and the output is NO. This demonstrates that even balanced frequency distributions do not matter unless all values match exactly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t) | Each test case requires a constant number of comparisons between four integers |
| Space | O(1) | Only four integers are stored per test case |

The solution scales linearly with the number of test cases, which is optimal given up to 10^4 inputs. Each operation is constant-time, so the full program easily fits within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    t = int(input())
    out = []
    for _ in range(t):
        a, b, c, d = map(int, input().split())
        out.append("YES" if a == b == c == d else "NO")
    return "\n".join(out)

# provided samples
assert run("""7
1 2 3 4
1 1 1 1
2 2 2 2
1 2 1 2
1 1 5 5
5 5 5 5
4 10 5 9
""") == """NO
YES
YES
NO
NO
YES
NO"""

# custom cases
assert run("1\n1 1 1 1\n") == "YES"
assert run("1\n1 1 1 2\n") == "NO"
assert run("1\n10 10 10 10\n") == "YES"
assert run("1\n2 3 2 3\n") == "NO"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 1 1` | YES | minimum valid square |
| `1 1 1 2` | NO | single mismatch breaks validity |
| `10 10 10 10` | YES | max-value uniform case |
| `2 3 2 3` | NO | balanced but unequal set fails |

## Edge Cases

One subtle case is when three sticks are equal and one differs, such as `5 5 5 4`. The algorithm compares sequentially: `a == b == c == d` fails at `c == d`, so it correctly outputs NO. This confirms that partial uniformity is insufficient.

Another case is alternating values like `2 3 2 3`. Even though the multiset is balanced, the equality chain fails immediately at `a == b`, producing NO. This shows that frequency balance does not matter; structural equality is required.

A maximum-uniform case like `10 10 10 10` passes all comparisons cleanly, confirming that boundary values behave identically to small ones.
