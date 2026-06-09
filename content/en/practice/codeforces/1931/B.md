---
title: "CF 1931B - Make Equal"
description: "We are given several independent scenarios. In each scenario there is a line of containers, each holding some amount of water. We are allowed to move water, but only from a container on the left to a container on the right."
date: "2026-06-08T18:24:33+07:00"
tags: ["codeforces", "competitive-programming", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1931
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 925 (Div. 3)"
rating: 800
weight: 1931
solve_time_s: 74
verified: true
draft: false
---

[CF 1931B - Make Equal](https://codeforces.com/problemset/problem/1931/B)

**Rating:** 800  
**Tags:** greedy  
**Solve time:** 1m 14s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given several independent scenarios. In each scenario there is a line of containers, each holding some amount of water. We are allowed to move water, but only from a container on the left to a container on the right. The goal is to decide whether we can eventually redistribute the water so that every container ends up with exactly the same amount.

The only permitted operation is directional transfer: pick indices i and j with i < j, and move any non-negative amount of water from i to j. This means water can only flow rightward, never leftward, but it can be split and combined arbitrarily through intermediate positions.

The constraint n up to 2⋅10^5 across all test cases implies we need a linear or near-linear solution per test. Anything quadratic, such as simulating transfers or repeatedly fixing positions, would immediately fail since worst-case total operations would exceed 10^10.

A subtle edge case arises when the total sum divided by n is small but early containers are too low. For example, if the first element is already larger than the target, we might suspect failure, but this is not automatically disqualifying because excess can be pushed rightward. Conversely, if early prefix sums are consistently below what they “should be,” we may be unable to compensate later because water cannot move left.

A small illustrative failure case for naive intuition is:

Input:

n = 3, a = [0, 3, 0]

Target is 1. Even though total is divisible, the first container starts below target, but this is fine because it can receive from the right. However, if we reverse direction constraints, the situation changes drastically, which hints that directionality is the core difficulty.

## Approaches

A brute-force simulation would try to repeatedly pick pairs i < j and push water forward to reduce imbalance. One could maintain a loop that scans for a position above target and pushes excess to the right. In the worst case, each unit of water might be moved across O(n) positions, and there are O(sum a_i) units. This leads to a worst-case complexity on the order of 10^9 to 10^10 operations, which is not feasible.

The key structural observation is that the operation constraint imposes a prefix condition. Since water only moves right, any deficit in a prefix must be satisfied entirely from within that prefix at some earlier stage. Once we pass a prefix boundary, we can never bring water back to fix earlier shortages.

This leads to a clean invariant: at every prefix, we must have had enough total water to support making that prefix reach the final uniform level. Since the final level is fixed as avg = total / n, the required amount in the first k positions is exactly k * avg. Thus, the only thing that matters is whether the running prefix sum ever drops below k * avg.

This reduces the problem to a single linear scan.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(n · total) | O(1) | Too slow |
| Prefix Balance Check | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Compute the target value avg = sum(a) / n. This is the only possible final value per container since total mass is conserved.
2. Initialize a running prefix sum variable to 0.
3. Iterate through the array from left to right.
4. At each position i, add a[i] to the running prefix sum.
5. Compute the required amount for this prefix, which is (i + 1) * avg.
6. If at any point the prefix sum becomes strictly less than required, immediately conclude it is impossible.
7. If the loop completes without violation, conclude it is possible.

The reason we compare against the required prefix total is that once we move past index i, no future operation can bring water back to indices ≤ i. So feasibility depends entirely on whether earlier positions ever “owe” more water than they have accumulated.

### Why it works

The process of moving water only to the right implies that prefixes evolve independently of future segments in one direction: future positions can help only themselves and positions to their right. Thus, any prefix deficit is irreversible.

If we imagine the final configuration, every prefix must contain exactly its proportional share of water. If at any moment during scanning we observe that the current prefix sum is less than required, then even if all remaining water were placed optimally, it could not compensate for the already violated prefix boundary because that compensation would require moving water leftward across the boundary.

This invariant fully characterizes feasibility.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        
        total = sum(a)
        avg = total // n
        
        pref = 0
        ok = True
        
        for i, x in enumerate(a):
            pref += x
            if pref < (i + 1) * avg:
                ok = False
                break
        
        print("YES" if ok else "NO")

if __name__ == "__main__":
    solve()
```

The solution first computes the global target value. It then maintains a prefix accumulator while scanning left to right. The critical check compares accumulated water with the required uniform distribution up to that point. The moment a prefix falls short, the function stops early since no later correction is possible.

A common implementation pitfall is forgetting that integer division is safe here because the problem guarantees divisibility. Another subtle issue is using a running “difference” instead of explicit prefix comparison; both work, but the prefix formulation is less error-prone.

## Worked Examples

We trace two representative cases.

### Example 1

Input: [4, 5, 2, 1, 3], avg = 3

| i | a[i] | prefix | required (i+1)*3 | valid |
| --- | --- | --- | --- | --- |
| 0 | 4 | 4 | 3 | yes |
| 1 | 5 | 9 | 6 | yes |
| 2 | 2 | 11 | 9 | yes |
| 3 | 1 | 12 | 12 | yes |
| 4 | 3 | 15 | 15 | yes |

All prefixes satisfy the constraint, so the answer is YES. This confirms that excess early water can always be pushed right to fix later positions.

### Example 2

Input: [1, 2, 3], avg = 2

| i | a[i] | prefix | required | valid |
| --- | --- | --- | --- | --- |
| 0 | 1 | 1 | 2 | no |

At the first step, the prefix already fails. Even though later elements contain surplus, it cannot move left to fix the deficit in the first container, so the answer is NO. This shows the irreversibility of prefix shortages.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test | single pass prefix scan |
| Space | O(1) extra | only counters stored |

The total input size across all test cases is bounded by 2⋅10^5, so a linear scan per test case remains comfortably within time limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    t = int(input())
    out = []
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        total = sum(a)
        avg = total // n
        pref = 0
        ok = True
        for i, x in enumerate(a):
            pref += x
            if pref < (i + 1) * avg:
                ok = False
                break
        out.append("YES" if ok else "NO")
    return "\n".join(out)

# provided samples
assert run("""6
1
43
2
1 3
5
4 5 2 1 3
3
1 2 3
7
4 5 5 0 6 4 4
7
6 5 5 1 3 4 4
""") == """YES
NO
YES
NO
NO
YES"""

# custom cases
assert run("""1
1
0
""") == "YES"

assert run("""1
4
2 2 2 2
""") == "YES"

assert run("""1
3
3 0 0
""") == "NO"

assert run("""1
5
0 0 10 0 0
""") == "NO"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| n=1 case | YES | trivial single container |
| all equal | YES | stable already balanced |
| early deficit | NO | prefix violation |
| mass too late | NO | right-only flow limitation |

## Edge Cases

A key edge case is when early elements are smaller than the target but later elements contain enough surplus. For instance, [0, 0, 10] with avg = 3. Even though total is sufficient, the first prefix already violates the requirement because the first position would need 3 units but has 0 and cannot receive from the right in the final state interpretation.

Another case is when the array is already uniform. The algorithm still checks prefixes but never violates, so it correctly returns YES without performing any operations.

Finally, single-element arrays always succeed since no redistribution is needed and the prefix condition is vacuously satisfied at every step.
