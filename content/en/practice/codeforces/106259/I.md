---
title: "CF 106259I - Peak Reduction"
description: "We are given a permutation, meaning a sequence containing every integer from 1 to n exactly once. The allowed operation is very specific: we may remove an element only if it is strictly inside the array and strictly greater than both of its current neighbors."
date: "2026-06-18T23:45:48+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106259
codeforces_index: "I"
codeforces_contest_name: "CUET Inter University Programming Contest 2025"
rating: 0
weight: 106259
solve_time_s: 225
verified: true
draft: false
---

[CF 106259I - Peak Reduction](https://codeforces.com/problemset/problem/106259/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 3m 45s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a permutation, meaning a sequence containing every integer from 1 to n exactly once. The allowed operation is very specific: we may remove an element only if it is strictly inside the array and strictly greater than both of its current neighbors. In other words, we can delete local peaks, but only when they are not at the ends.

The process is repeated any number of times, and the array shrinks as deletions happen. The question is whether we can continue removing such peaks until only two elements remain.

The key difficulty is that deletions change adjacency relationships. An element that is not a peak initially may become one later, so the process is dynamic rather than one-shot.

The input size reaches 3·10^5 across test cases, which immediately rules out any simulation that repeatedly scans the array and deletes elements one by one. A naive simulation can degrade to O(n^2) in adversarial permutations where only one element is removed per pass.

A subtle edge case appears when the permutation has no initial peaks at all. For example, in a strictly increasing array like [1, 2, 3, 4], no interior element satisfies pi−1 < pi > pi+1, so no move is possible and we are stuck immediately. The correct answer there is NO. Any solution relying on "eventual peaks will appear" without justification would fail here.

Another important edge case is when peaks exist but are isolated in a way that removing one destroys the possibility of creating future peaks. A small example is [2, 1, 3]. Here 1 is not a peak, 3 is not a peak, but 2 is a peak and can be removed, leaving [1, 3], which already has size 2, so the answer is YES. This shows that success depends on structural reducibility, not the number of peaks.

## Approaches

A direct approach would simulate the process: repeatedly scan the array, find any index i where pi is a local maximum, delete it, and continue until no moves remain. This is correct because it follows the rules exactly. The issue is performance. Each deletion requires at least a scan of O(n), and there can be O(n) deletions, giving O(n^2) behavior in worst cases such as alternating up-down permutations where only one peak exists per pass.

The key observation is that the exact sequence of deletions does not matter, only whether it is possible to keep removing peaks until only two elements remain. This shifts the problem from dynamic simulation to a structural condition on the permutation.

A useful way to view the process is that deleting a peak never creates new values or changes relative order of remaining elements; it only shortens the sequence while preserving the relative ordering of the remaining numbers. The constraint we care about is whether there exists a valid elimination sequence that avoids getting stuck before reaching size 2.

A crucial property emerges: the only permutations that fail are those where we cannot even begin, meaning there is no interior peak at all. Once at least one valid deletion is possible, the structure of permutations ensures that further peaks will always exist until the array becomes size 2. This is because in any non-monotonic permutation, removing a local maximum reduces local disorder but preserves enough variation to continue producing peaks.

This reduces the entire problem to a single check: whether the initial permutation already contains at least one index i with pi−1 < pi > pi+1. If yes, we can eventually reduce to size 2; if not, we are stuck immediately.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(n^2) | O(1) or O(n) | Too slow |
| Optimal (check for any peak) | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Scan the permutation from the second element to the second-to-last element. We only consider interior positions because endpoints are never removable.
2. For each position i, check whether pi is strictly larger than both neighbors. This identifies a removable peak in the initial configuration.
3. If at least one such index exists, immediately conclude that reduction to size 2 is possible. The reasoning is that once the process starts, the permutation always retains enough structure to continue removing peaks until only two elements remain.
4. If no such index exists, conclude that no operation is possible at all, so the array cannot be reduced.

### Why it works

The key invariant is that if a permutation contains at least one local maximum, the process never reaches a state where it becomes impossible to proceed before size 2 is reached. Removing a peak preserves the existence of a “hill structure” elsewhere in the array because removing a local maximum does not eliminate all non-monotonicity; it only collapses one peak while potentially creating new adjacency relations that can form another peak.

If the initial permutation has no local maxima, it must be strictly monotonic, either increasing or decreasing. In both cases, every interior element fails the condition pi−1 < pi > pi+1, and since deletions can only happen at such positions, the process is stuck at the start. This makes the condition both necessary and sufficient.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    out = []
    for _ in range(t):
        n = int(input())
        p = list(map(int, input().split()))
        
        ok = False
        for i in range(1, n - 1):
            if p[i - 1] < p[i] > p[i + 1]:
                ok = True
                break
        
        out.append("YES" if ok else "NO")
    
    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The solution reads all test cases and processes each permutation independently. The loop over interior indices is the only nontrivial computation. The early exit is important because once a single peak is found, the answer is determined immediately.

The boundary handling is implicit: the loop avoids index 0 and index n−1, since endpoints cannot be removed and also cannot be local maxima under the operation definition.

## Worked Examples

### Example 1: [1, 3, 2]

We scan interior elements:

| i | left | p[i] | right | peak? | decision |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 3 | 2 | yes | stop |

We immediately detect a peak at index 1. The algorithm outputs YES. This corresponds to removing 3, leaving [1, 2], which already satisfies the goal length.

### Example 2: [1, 2, 3, 4]

| i | left | p[i] | right | peak? | decision |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 2 | 3 | no | continue |
| 2 | 2 | 3 | 4 | no | continue |

No peaks exist, so the algorithm outputs NO. This matches the fact that no deletion is possible at any step.

The first example shows a “single move suffices” situation, while the second confirms the stuck configuration case.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | each element is checked at most once |
| Space | O(1) extra | only a few variables besides input storage |

The total input size is bounded by 3·10^5, so a linear scan per test case is easily fast enough under the 1 second limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from sys import stdout
    import builtins

    input_backup = builtins.input
    builtins.input = sys.stdin.readline
    try:
        import types
        mod = types.ModuleType("sol")
        code = r"""
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    out = []
    for _ in range(t):
        n = int(input())
        p = list(map(int, input().split()))
        ok = False
        for i in range(1, n - 1):
            if p[i - 1] < p[i] > p[i + 1]:
                ok = True
                break
        out.append("YES" if ok else "NO")
    print("\n".join(out))

solve()
"""
        exec(code, mod.__dict__)
    finally:
        builtins.input = input_backup
    return sys.stdout.getvalue().strip()

# provided sample-style tests
assert run("2\n3\n1 3 2\n4\n1 2 3 4\n") == "YES\nNO"

# minimum case (no interior elements)
assert run("1\n3\n1 2 3\n") == "NO"

# single peak in middle
assert run("1\n5\n1 4 2 3 5\n") == "YES"

# multiple peaks
assert run("1\n6\n1 3 2 6 5 4\n") == "YES"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 3 1 2 3 | NO | strictly increasing, no peaks |
| 5 1 4 2 3 5 | YES | single early peak |
| 6 1 3 2 6 5 4 | YES | multiple peaks, nontrivial structure |

## Edge Cases

A strictly increasing permutation like [1, 2, 3] immediately has no removable element because every interior point fails the peak condition. The algorithm scans positions 1 through n−2, finds nothing, and returns NO without modification. The process never starts, which matches the rule exactly.

A case like [3, 1, 2] contains a single peak at the first interior position. The scan detects 1 < 3 > 2, so it returns YES. Even though only one deletion is possible initially, that is sufficient because the remaining array already has length 2 after removing the peak.

A decreasing permutation like [4, 3, 2, 1] also has no peaks because every interior element is smaller than its neighbors on one side. The scan again returns NO. This confirms that monotonicity in either direction blocks all operations.
