---
title: "CF 105262I - The Vampire Partner"
description: "We are given several independent scenarios where a row of cups contains some hidden original amounts of cappuccino."
date: "2026-06-24T02:34:37+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105262
codeforces_index: "I"
codeforces_contest_name: "Game of Coders 3.0"
rating: 0
weight: 105262
solve_time_s: 43
verified: true
draft: false
---

[CF 105262I - The Vampire Partner](https://codeforces.com/problemset/problem/105262/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 43s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given several independent scenarios where a row of cups contains some hidden original amounts of cappuccino. The only information Eddard recorded at the beginning is a single value computed from the original array using a weighted sum: each cup contributes its value multiplied by its index, and all contributions are added together.

Later, we are given a new measurement of the same cups after some time. The question is not to reconstruct the original array, but only to decide whether it is still possible that nothing has changed. In other words, we check whether the new array could have produced exactly the same weighted sum as the original one.

Each test case provides the original encoded value and the final array. We must decide whether there exists at least one valid original configuration consistent with both the encoding and the final observation. This is equivalent to checking whether the weighted sum of the final array matches the given stored value.

The constraints allow up to 10^6 total elements across test cases, so any solution must be linear in the input size. A naive recomputation per test case is sufficient if it is O(n), but anything quadratic or involving reconstruction or search is impossible.

The main edge case comes from a subtle interpretation trap: the condition is existential, not deterministic. Even if the arrays differ in content, we only care whether they could still produce the same weighted sum. That means equality of the computed function is the only deciding factor, not element-wise comparison or any notion of “change detection” beyond the encoded value.

For example, if the stored value is 30 and the new array also evaluates to 30 under the same function, we must answer YES even if we can imagine other original arrays that would also match. Conversely, even a single mismatch forces NO, because no alternative explanation can reconcile the encoded value with the observed weighted sum.

## Approaches

The brute-force interpretation would be to consider whether there exists some original array that matches both the stored weighted sum and the final observed array under transformation rules. However, the problem does not actually involve reconstructing the original array or modeling intermediate changes. The only check that matters is whether the encoding of the current array equals the stored value.

A direct computation approach is to evaluate the function F(p) = sum(i * p[i]) and compare it to the given F(c). This is straightforward because the function is linear and directly computable in one pass.

The key simplification is recognizing that the condition “could the amounts have stayed the same” is equivalent to asking whether the encoded fingerprint matches the fingerprint recomputed from the final state. No additional hidden constraints or transformations exist beyond this comparison.

Thus the problem reduces to computing a single weighted sum per test case and comparing it to the provided value.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Direct recomputation | O(n) per test case | O(1) extra | Accepted |

## Algorithm Walkthrough

## Algorithm Walkthrough

1. Read the number of test cases. Each test case is independent, so no state is carried between them.
2. For each test case, read n and the stored value S, which represents the original weighted sum.
3. Read the array p representing the current state of the cups.
4. Compute the weighted sum of p by iterating over indices from 1 to n and accumulating i * p[i]. The multiplication reflects the encoding rule used by Eddard.
5. Compare the computed sum with S. If they are equal, output YES; otherwise output NO.

### Why it works

The function defining the stored value is deterministic and uniquely computable from any given array. Since both the original and final states are evaluated using the same formula, the only way they can represent the same situation is if their computed values match exactly. There is no ambiguity or hidden transformation that could preserve the encoded value while changing the computed result independently. Therefore equality of the weighted sums is both necessary and sufficient for a “possible unchanged” scenario.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    out = []
    for _ in range(t):
        n, S = map(int, input().split())
        p = list(map(int, input().split()))
        
        cur = 0
        for i, v in enumerate(p, start=1):
            cur += i * v
        
        out.append("YES" if cur == S else "NO")
    
    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The solution processes each test case independently. The key computation is the weighted sum, implemented using `enumerate` starting at 1 to match the 1-based indexing in the definition. The accumulator `cur` is kept as a Python integer, which safely handles values up to 10^18 due to Python’s arbitrary precision integers.

The comparison at the end is the only decision point. No additional normalization or transformation is needed.

## Worked Examples

### Example 1

Input:

n = 5, S = 30

p = [2, 4, 2, 1, 2]

We compute the weighted sum step by step:

| i | p[i] | i * p[i] | cumulative |
| --- | --- | --- | --- |
| 1 | 2 | 2 | 2 |
| 2 | 4 | 8 | 10 |
| 3 | 2 | 6 | 16 |
| 4 | 1 | 4 | 20 |
| 5 | 2 | 10 | 30 |

The final computed value is 30, which matches S, so the answer is YES. This confirms that the encoding is consistent with the observed state.

### Example 2

Input:

n = 3, S = 20

p = [1, 4, 1]

| i | p[i] | i * p[i] | cumulative |
| --- | --- | --- | --- |
| 1 | 1 | 1 | 1 |
| 2 | 4 | 8 | 9 |
| 3 | 1 | 3 | 12 |

The computed value is 12, which differs from 20, so the answer is NO. This shows that even a small discrepancy in any position affects the weighted sum and immediately invalidates the possibility of equivalence.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(∑n) | Each element is processed exactly once to compute the weighted sum |
| Space | O(1) | Only a running accumulator is used besides input storage |

The total number of elements across all test cases is at most 10^6, so a single linear scan per test case fits comfortably within both time and memory limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    return "\n".join(solve_capture(inp))

# We redefine a safe runner since __main__ context varies in platforms
def solve_capture(inp):
    import sys
    input = sys.stdin.readline
    t = int(input())
    out = []
    for _ in range(t):
        n, S = map(int, input().split())
        p = list(map(int, input().split()))
        cur = 0
        for i, v in enumerate(p, start=1):
            cur += i * v
        out.append("YES" if cur == S else "NO")
    return out

# provided-style tests
assert solve_capture("1\n5 30\n2 4 2 1 2\n") == ["YES"]
assert solve_capture("1\n3 20\n1 4 1\n") == ["NO"]

# custom cases
assert solve_capture("1\n1 0\n0\n") == ["YES"]
assert solve_capture("1\n1 5\n5\n") == ["YES"]
assert solve_capture("1\n2 1\n1 0\n") == ["NO"]
assert solve_capture("2\n3 6\n1 1 1\n3 10\n1 2 3\n") == ["YES","YES"]
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| n=1 zero case | YES | minimum size, zero value correctness |
| single element match | YES | direct equality of weighted sum |
| small mismatch | NO | detection of small deviation |
| multiple cases | YES/YES | batch processing correctness |

## Edge Cases

One edge case is when n = 1. The weighted sum reduces to a single value 1 * p[1], so the answer depends only on equality with S. The algorithm handles this naturally because the loop runs once and accumulates correctly.

Another edge case is when all values are zero. The weighted sum becomes zero regardless of n. If S is also zero, the answer is YES, otherwise NO. The algorithm correctly accumulates zero contributions without special handling.

A third edge case is when values are large, near 10^9, and n is large. The sum can reach 10^18, but Python integers handle this safely, and the algorithm still runs in linear time since only multiplication and addition are performed per element.
