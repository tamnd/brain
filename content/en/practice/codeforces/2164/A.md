---
title: "CF 2164A - Sequence Game"
description: "We are given a sequence of numbers, and we repeatedly compress it until only one value remains. Each operation takes two adjacent elements, removes them, and replaces them with any integer lying between the two original values, inclusive."
date: "2026-06-07T23:36:29+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "sortings"]
categories: ["algorithms"]
codeforces_contest: 2164
codeforces_index: "A"
codeforces_contest_name: "Codeforces Global Round 30 (Div. 1 + Div. 2)"
rating: 800
weight: 2164
solve_time_s: 74
verified: true
draft: false
---

[CF 2164A - Sequence Game](https://codeforces.com/problemset/problem/2164/A)

**Rating:** 800  
**Tags:** brute force, sortings  
**Solve time:** 1m 14s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of numbers, and we repeatedly compress it until only one value remains. Each operation takes two adjacent elements, removes them, and replaces them with any integer lying between the two original values, inclusive. The key freedom is that we are not forced to pick an average or a fixed rule, but we can choose any value inside the interval formed by the pair.

After exactly $n-1$ such merges, the array becomes a single number. The question is whether there exists some sequence of merges and choices of intermediate values such that the final remaining number is exactly $x$.

The constraints are small: each test has at most 100 elements and up to 500 test cases. This immediately suggests that even quadratic or cubic reasoning per test is acceptable, but anything exponential over all merge sequences is not. A naive simulation that tries all possible merge orders and all possible values is impossible because each merge introduces a continuous range of possibilities, and the number of merge trees is already exponential in $n$.

A subtle edge case appears when all values are equal or when $x$ lies outside the range of the array. For instance, if all elements are $[3,3,3]$, the final value must always be 3, so any $x \neq 3$ is impossible. Similarly, if we start with $[1, 5]$, we can always choose any final value in $[1,5]$, so any $x$ outside this interval is immediately impossible. The interesting part is whether every value inside the global range is always achievable.

A naive mistake would be to assume that because we can pick any value between two numbers, we can “steer” the final result arbitrarily. That intuition fails if we think in terms of constraints propagation rather than local freedom.

## Approaches

A brute-force idea would try to simulate all possible merge sequences. At each step, we pick an adjacent pair and replace it with every integer in its range. This creates a branching factor of both positions and values. Even ignoring values, there are Catalan-number-many merge structures, and with value choices, the state space becomes infinite. Even discretizing values does not help, because the combinations explode beyond feasibility.

The key insight is that we do not actually care about the order of merges. Every operation only ever merges two contiguous segments into a segment whose achievable values form an interval. This suggests that each segment $[l, r]$ can be represented by a continuous range $[min(l,r), max(l,r)]$, and merging two segments simply unifies their possible ranges into the full interval between all elements in that segment.

So the problem collapses into a much simpler invariant: after any sequence of operations, the final value can be any integer between the global minimum and global maximum of the original array. This is because we can always propagate extremes inward using merges, and at each step we can choose intermediate values freely to avoid introducing new constraints.

Thus the final answer is simply whether $x$ lies within $[\min(a), \max(a)]$.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| Optimal | O(n) per test | O(1) | Accepted |

## Algorithm Walkthrough

We reduce each test case to a range query over the array.

1. Compute the minimum value in the sequence. This represents the lowest value that can ever be preserved through merges, since no operation can produce something outside the convex hull of its inputs.
2. Compute the maximum value in the sequence. This is the symmetric upper bound for the same reason.
3. Check whether $x$ lies between these two values, inclusive.
4. If it does, output "YES", otherwise output "NO".

The only non-obvious part is why the entire interval is achievable. The merging rule allows us to pick any value between two adjacent segments. By repeatedly merging and choosing values that gradually move toward $x$, we can always construct a path that does not “skip over” any integer in the range.

### Why it works

Each merge replaces two adjacent segments with a single segment whose achievable values form a connected interval covering both inputs. Since intervals are closed under this merging operation, the final segment must also be an interval. The initial segments are single points, so the final interval is exactly the convex hull of all initial values, which is $[\min(a), \max(a)]$. Therefore, any $x$ inside this interval is reachable.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        x = int(input())

        mn = min(a)
        mx = max(a)

        if mn <= x <= mx:
            print("YES")
        else:
            print("NO")

if __name__ == "__main__":
    solve()
```

The code directly computes the minimum and maximum of each array and checks whether $x$ lies in that interval. The implementation is intentionally minimal because the structure of the problem eliminates any need for simulation.

A common mistake here would be to attempt greedy merging or simulate operations, but that is unnecessary. Another potential pitfall is forgetting that intermediate values can be any integer in the range, which is what makes the reachable set continuous rather than discrete.

## Worked Examples

### Example 1

Input:

$$[2, 7, 5],\ x = 4$$

We compute the range:

| Step | Array | min | max | x in range? |
| --- | --- | --- | --- | --- |
| init | [2,7,5] | 2 | 7 | yes |

Since 4 lies between 2 and 7, the answer is YES.

This demonstrates that even though 4 is not present in the array, intermediate merges allow constructing it.

### Example 2

Input:

$$[-1, 3, 7, -9, -2],\ x = 8$$

| Step | Array | min | max | x in range? |
| --- | --- | --- | --- | --- |
| init | [-1,3,7,-9,-2] | -9 | 7 | no |

Here the maximum possible final value cannot exceed 7, so 8 is unreachable regardless of merge choices. This confirms that the range boundary is tight.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test | We compute min and max over the array once |
| Space | O(1) | Only a few variables are stored |

The constraints allow up to 500 test cases with arrays of size 100, so this linear scan is easily fast enough. The solution runs in microseconds per test in practice.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from sys import stdout
    out = []

    input = sys.stdin.readline
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        x = int(input())
        mn, mx = min(a), max(a)
        out.append("YES" if mn <= x <= mx else "NO")

    return "\n".join(out)

# provided samples
assert run("""3
3
2 7 5
4
5
-1 3 7 -9 -2
8
6
1 -1 -4 5 1 -4
-2
""") == """YES
NO
YES"""

# custom cases
assert run("""1
1
5
5
""") == "YES"

assert run("""1
1
5
6
""") == "NO"

assert run("""1
4
1 2 3 4
10
""") == "NO"

assert run("""1
4
1 2 3 4
1
""") == "YES"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single equal element | YES | base case correctness |
| single mismatch | NO | single-element boundary |
| out of range large x | NO | upper bound handling |
| x equals min | YES | inclusive boundary correctness |

## Edge Cases

One edge case is when the array has a single element. For input $[5]$, the only possible final value is 5 because no operations exist. The algorithm computes $mn = mx = 5$, so only $x = 5$ returns YES, which matches the process exactly.

Another edge case is when all values are identical, such as $[3,3,3,3]$. Every merge preserves the value 3 regardless of choices, so the final result is fixed. The computed range is $[3,3]$, which correctly restricts the answer.

A more subtle case is when $x$ lies strictly between two distant values, such as $[1, 100]$ with $x = 50$. Even though no intermediate values exist initially, a direct merge of the two elements allows choosing any integer in that interval, making 50 achievable. The range check captures this immediately without needing to simulate intermediate states.
