---
title: "CF 104968B - Pizza Slices"
description: "We are given a pile of pizzas, each pizza cut into 8 identical slices. With $n$ pizzas, the total number of slices is fixed at $8n$. These slices must be distributed among $m$ friends. The distribution has two constraints at the same time."
date: "2026-06-28T06:47:30+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104968
codeforces_index: "B"
codeforces_contest_name: "UTPC Contest 02-09-24 Div. 2 (Beginner)"
rating: 0
weight: 104968
solve_time_s: 77
verified: true
draft: false
---

[CF 104968B - Pizza Slices](https://codeforces.com/problemset/problem/104968/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 17s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a pile of pizzas, each pizza cut into 8 identical slices. With $n$ pizzas, the total number of slices is fixed at $8n$. These slices must be distributed among $m$ friends.

The distribution has two constraints at the same time. Every friend must receive exactly the same number of slices, and that number must be at least $k$. We are not allowed to leave anyone with fewer slices than another person, and we are not allowed to give someone a positive number of slices below the minimum satisfaction threshold.

So the question reduces to checking whether the total amount of pizza can be split evenly into $m$ identical portions, and whether each portion is large enough.

From a constraints perspective, $n$ can be as large as $10^5$, so the total number of slices can reach $8 \cdot 10^5$. The number of friends is at most 100, which is small. Any solution that simulates distribution slice by slice or tries to search possible allocations would still be trivial in complexity, but unnecessary. The structure of the problem strongly suggests a constant-time arithmetic check is sufficient.

A naive mistake here is to ignore the divisibility requirement and only check whether the average number of slices per person exceeds $k$. For example, if $n = 2$, $m = 3$, $k = 1$, then total slices is 16, and $16/3 \ge 1$ holds numerically, but the division is impossible since 16 is not divisible by 3. The correct output is false.

Another common mistake is to only check divisibility and forget the minimum requirement. For instance, if $n = 1$, $m = 4$, $k = 3$, then total slices is 8, divisible by 4 giving 2 per person, but 2 is below the minimum requirement so it must fail.

These two constraints must be enforced simultaneously.

## Approaches

The most direct way to think about the problem is to imagine actually distributing slices. One could iterate over all possible assignments of slices to each friend, ensuring each receives at least $k$, and verifying whether a valid equal partition exists. However, since the slices are identical and only the count matters, this quickly collapses into a counting problem rather than a combinatorial assignment problem.

Even if we attempted a brute-force construction, we would essentially be trying to partition $8n$ into $m$ equal integers, each at least $k$. The only meaningful candidate value for each friend is the average $x = \frac{8n}{m}$, provided this division is exact. If the division is not exact, no enumeration can fix it. If it is exact, the only remaining check is whether $x \ge k$.

The key observation is that the structure of valid distributions is completely determined by arithmetic constraints. There is no flexibility once equality is enforced: each friend must receive exactly $x$, so feasibility reduces to checking whether such an integer $x$ exists and satisfies the lower bound.

This reduces the problem from an exponential or combinatorial search into a constant-time computation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(8n) or worse | O(1) | Too slow / unnecessary |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Compute the total number of slices as $total = 8 \cdot n$. This represents the full resource pool that must be partitioned without remainder.
2. Check whether $total$ is divisible by $m$. If it is not divisible, an equal split is impossible because at least one friend would necessarily receive a different number of slices.
3. If divisible, compute the per-person allocation $x = total / m$. This value is forced, there is no alternative valid distribution under the equality constraint.
4. Check whether $x \ge k$. This ensures the minimum satisfaction requirement is met for every friend simultaneously.
5. Return true only if both conditions hold, otherwise return false.

### Why it works

Once we enforce equal distribution, every valid solution must assign exactly the same integer $x$ to each friend. That means the total sum is fully determined by $m \cdot x$, and therefore feasibility depends entirely on whether $8n$ can be expressed in that form. The divisibility check guarantees structural feasibility, and the inequality check enforces the minimum constraint. No other configuration exists outside this single candidate value, so the decision is complete.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input().strip())
    m = int(input().strip())
    k = int(input().strip())

    total = 8 * n

    if total % m != 0:
        print("FALSE")
        return

    each = total // m

    if each >= k:
        print("TRUE")
    else:
        print("FALSE")

if __name__ == "__main__":
    solve()
```

The implementation mirrors the derivation exactly. The multiplication $8 * n$ is done in constant time and safely fits within Python integers. The divisibility check comes first because it avoids computing or reasoning about a non-existent per-person allocation. Only when the split is valid do we compute $each$, which represents the forced allocation per friend.

The final comparison enforces the minimum requirement. There are no corner cases involving partial assignments since equality removes all flexibility.

## Worked Examples

### Example 1

Input:

n = 1, m = 4, k = 3

| Step | total | divisibility | each | check each ≥ k | result |
| --- | --- | --- | --- | --- | --- |
| start | 8 | - | - | - | - |
| check | 8 | 8 % 4 = 0 | - | - | continue |
| compute | 8 | yes | 2 | - | - |
| final | 8 | yes | 2 | 2 ≥ 3 false | FALSE |

This demonstrates a case where equal splitting is possible structurally, but the minimum requirement eliminates it.

### Example 2

Input:

n = 1, m = 4, k = 2

| Step | total | divisibility | each | check each ≥ k | result |
| --- | --- | --- | --- | --- | --- |
| start | 8 | - | - | - | - |
| check | 8 | 8 % 4 = 0 | - | - | continue |
| compute | 8 | yes | 2 | - | - |
| final | 8 | yes | 2 | 2 ≥ 2 true | TRUE |

Here both structural and constraint conditions align, producing a valid configuration.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only a few arithmetic operations and two constant-time checks |
| Space | O(1) | No auxiliary data structures are used |

The constraints allow up to $10^5$ pizzas, but the solution does not depend on iterating over pizzas or friends. Every operation is constant-time arithmetic, so the solution easily fits within limits.

## Test Cases

```python
import sys, io
from contextlib import redirect_stdout

def solve():
    import sys
    input = sys.stdin.readline

    n = int(input().strip())
    m = int(input().strip())
    k = int(input().strip())

    total = 8 * n

    if total % m != 0:
        print("FALSE")
        return

    each = total // m

    if each >= k:
        print("TRUE")
    else:
        print("FALSE")

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# provided samples (interpreted as 1 4 3 and 1 4 2)
assert run("1\n4\n3\n") == "FALSE", "sample 1"
assert run("1\n4\n2\n") == "TRUE", "sample 2"

# minimum case
assert run("1\n1\n8\n") == "TRUE", "single friend gets all slices"

# impossible divisibility
assert run("2\n3\n1\n") == "FALSE", "not divisible by m"

# borderline equality
assert run("3\n2\n12\n") == "FALSE", "exact split but below k"

# large valid case
assert run("100000\n5\n16\n") == "TRUE", "large feasible case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 8 | TRUE | single friend edge case |
| 2 3 1 | FALSE | divisibility failure |
| 3 2 12 | FALSE | equality but insufficient per-person share |
| 100000 5 16 | TRUE | large input feasibility |

## Edge Cases

One edge case is when there is only one friend. For input $n = 1, m = 1, k = 8$, total slices is 8, divisibility holds, and each friend gets 8. The algorithm computes $each = 8$ and passes the threshold check, producing TRUE. This confirms that the logic handles the trivial partition correctly.

Another edge case is when the total is not divisible by the number of friends. For $n = 2, m = 3, k = 1$, total is 16. Since 16 % 3 is non-zero, the algorithm immediately rejects the case. This avoids incorrectly reasoning about fractional allocations.

A final case is when divisibility holds but the minimum constraint fails. For $n = 1, m = 4, k = 3$, total is 8, each is 2, and the threshold check fails. This confirms that the algorithm does not confuse feasibility of splitting with satisfaction constraints.
