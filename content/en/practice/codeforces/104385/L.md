---
title: "CF 104385L - Zhang Fei Threading Needles - Thick with Fine"
description: "We are given a single integer $N$, representing the number of soldiers in Cao Cao’s army positioned in front of Changban Bridge. The story describes Zhang Fei’s roar causing panic and making soldiers flee."
date: "2026-07-01T02:55:19+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104385
codeforces_index: "L"
codeforces_contest_name: "2023 (ICPC) Jiangxi Provincial Contest -- Official Contest"
rating: 0
weight: 104385
solve_time_s: 37
verified: true
draft: false
---

[CF 104385L - Zhang Fei Threading Needles - Thick with Fine](https://codeforces.com/problemset/problem/104385/L)

**Rating:** -  
**Tags:** -  
**Solve time:** 37s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a single integer $N$, representing the number of soldiers in Cao Cao’s army positioned in front of Changban Bridge. The story describes Zhang Fei’s roar causing panic and making soldiers flee. However, there is a specific exception: General Xia Houjie is affected differently and is explicitly stated to not be included in the count of those who were “scared away”.

So the task reduces to determining how many soldiers actually flee after excluding the one person who does not count as part of the scared-away group.

Although the narrative is heavily stylized, the underlying structure is purely arithmetic. The input size goes up to $10^6$, which immediately rules out anything involving simulation over individual soldiers with complex behavior, but here even that is unnecessary since we are not tracking interactions or sequences. A constant-time computation is sufficient.

A subtle edge case appears when $N = 1$. In that situation, if the only person present is the one excluded from the count, the number of scared-away soldiers becomes zero. Any naive subtraction must handle this cleanly without producing negative values.

## Approaches

A brute-force interpretation would explicitly simulate each soldier, mark whether they flee due to the roar, and then adjust the count by excluding Xia Houjie. This would conceptually involve iterating over all $N$ entities and maintaining a status flag per soldier. While this is already linear and would pass easily for $N \le 10^6$, it is unnecessary because no individual state transitions actually depend on position or interactions.

The key observation is that the story defines a single exceptional individual who should not be included in the final count. That means the answer is simply the total number of soldiers minus one excluded person. No further structure, ordering, or conditions affect the result.

Thus the problem collapses into a constant-time arithmetic computation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(N) | O(1) | Accepted but unnecessary |
| Optimal Arithmetic | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the integer $N$, which represents the total number of soldiers in front of the bridge. This is the full population before any exclusions are applied.
2. Identify that exactly one individual is not included in the final “scared away” count. The statement explicitly defines this exception, so we do not count that person in the result.
3. Compute the result as $N - 1$. This directly removes the excluded individual from the total.
4. If $N = 1$, the same formula still applies and naturally yields 0, which correctly represents that no soldiers are counted as scared away.

### Why it works

The key invariant is that all soldiers except one contribute to the final count of those who flee. Since the problem guarantees exactly one exclusion and no other filtering conditions, the final answer is always the total size minus that single excluded entity. There is no dependency between soldiers, no conditional behavior, and no dynamic change in the population, so the subtraction remains valid for all inputs.

## Python Solution

```python
import sys
input = sys.stdin.readline

def main():
    n = int(input().strip())
    print(max(0, n - 1))

if __name__ == "__main__":
    main()
```

The implementation is intentionally minimal. The subtraction $n - 1$ encodes the exclusion described in the statement. The `max(0, ...)` guard ensures correctness when $n = 1$, preventing any negative output in degenerate cases.

The solution uses constant time input processing and avoids storing anything beyond the single integer.

## Worked Examples

### Example 1

Input:

```
5
```

We start with $n = 5$.

| Step | Value of n | Computation | Result |
| --- | --- | --- | --- |
| Initial | 5 | - | - |
| Apply rule | 5 | 5 - 1 | 4 |

Output:

```
4
```

This confirms that one individual is excluded from the final count.

### Example 2

Input:

```
1
```

| Step | Value of n | Computation | Result |
| --- | --- | --- | --- |
| Initial | 1 | - | - |
| Apply rule | 1 | 1 - 1 | 0 |

Output:

```
0
```

This case shows the boundary condition where the only soldier is the excluded one, resulting in zero counted fugitives.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only a single arithmetic operation is performed regardless of input size |
| Space | O(1) | No additional data structures are used |

The constraints allow up to one million soldiers, but the computation does not depend on iterating over them. The solution comfortably fits within both time and memory limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline
    n = int(input().strip())
    return str(max(0, n - 1))

# provided sample-like cases
assert run("5\n") == "4"
assert run("1\n") == "0"

# custom cases
assert run("2\n") == "1", "minimum non-trivial case"
assert run("1000000\n") == "999999", "maximum boundary case"
assert run("3\n") == "2", "small mid-range sanity check"
assert run("10\n") == "9", "typical linear check"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2 | 1 | smallest case where subtraction is non-zero |
| 1 | 0 | boundary exclusion case |
| 1000000 | 999999 | maximum constraint behavior |
| 3 | 2 | general correctness |

## Edge Cases

### Case $N = 1$

Input:

```
1
```

The algorithm computes $1 - 1 = 0$. This matches the interpretation that the only individual is the excluded one, leaving no counted soldiers.

### Case $N = 2$

Input:

```
2
```

Execution proceeds as $2 - 1 = 1$. One soldier remains after excluding the special individual. There are no hidden conditions that alter this outcome, so the computation is stable.

### Large Input Case

Input:

```
1000000
```

The subtraction yields $999999$ directly. Since the operation is constant time, there is no risk of performance degradation or overflow in Python’s integer arithmetic.
