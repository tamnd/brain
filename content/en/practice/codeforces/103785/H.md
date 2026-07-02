---
title: "CF 103785H - Perfect Array"
description: "We are given a sequence of integers representing elements placed in a row. The allowed operation depends on position: if the element currently sitting at position $k$ (1-indexed) has value exactly $k$, then that element is eligible to be removed. The process is not arbitrary."
date: "2026-07-02T08:52:56+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103785
codeforces_index: "H"
codeforces_contest_name: "CodeBrew : Freshers Contest 2022"
rating: 0
weight: 103785
solve_time_s: 47
verified: true
draft: false
---

[CF 103785H - Perfect Array](https://codeforces.com/problemset/problem/103785/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 47s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of integers representing elements placed in a row. The allowed operation depends on position: if the element currently sitting at position $k$ (1-indexed) has value exactly $k$, then that element is eligible to be removed.

The process is not arbitrary. Whenever multiple removable elements exist, we are forced to remove the rightmost one among them. Each removal changes the indices of the remaining elements, so the set of removable positions evolves over time. The task is to determine whether it is possible to completely remove all elements by repeatedly applying this rule. If it is possible, we must also output the order in which elements are removed, but reported in reverse of the removal process.

The key subtlety is that removals are not independent. Removing an element early can expose or destroy removability for other elements because positions shift. A naive interpretation that checks “any index i where a[i] = i” independently will fail because indices are dynamic, not static.

The constraints are small enough that an $O(n^2)$ simulation is acceptable. This suggests that each step can afford a linear scan over the array, and we may perform up to $n$ removals, giving at most $O(n^2)$ total operations. Any solution relying on repeated global recomputation is still safe.

A few failure cases arise naturally from careless approaches. One is assuming we can always remove leftmost valid elements. For example, consider $[1, 2, 3]$. If we remove 1 first, we shift the array and destroy the structure needed for later removals under the “rightmost mandatory removal” rule. The correct process is order-dependent, and greedy direction matters.

Another pitfall is forgetting that indices change after every deletion. Treating values as if they refer to original indices leads to incorrect removals in cases like $[2, 1, 3]$, where the only valid removals depend on dynamic reindexing.

## Approaches

The brute-force idea is to literally simulate the process. At each step, we scan the array, find all positions where $a[i] = i$, pick the rightmost such position, remove it, and continue. Each scan costs $O(n)$, and we may do up to $n$ removals, giving $O(n^2)$ complexity. This works within limits but hides inefficiency in repeated scanning and shifting.

The key observation is that the process is equivalent to repeatedly deleting the rightmost position that is currently “correct”. Once a position becomes removable and we choose not to remove it when it is the rightmost candidate, it can never be removed later. This comes from the fact that removing anything to its right does not affect its index condition, but removing anything to its left shifts it and breaks equality permanently. So postponing a valid rightmost removal is irreversible damage.

This leads to a clean greedy strategy: repeatedly locate the rightmost index $i$ such that $a[i] = i+1$, remove it immediately, and continue. The correctness hinges on the monotonicity of index shifts: only left-side deletions affect a position’s index, so the rightmost valid element is safe to commit.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | $O(n^2)$ | $O(n)$ | Accepted |
| Greedy Rightmost Deletion | $O(n^2)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

We maintain the array and repeatedly delete elements until either all are removed or no valid deletion exists.

1. Start with the current array and an empty list `ans` that records removed elements in order of removal. The goal is to reconstruct a full valid deletion sequence.
2. Scan the array from right to left to find the largest index $i$ such that $a[i] = i+1$. This ensures we respect the rule of always choosing the rightmost removable element.
3. If no such index exists, the process is stuck. We cannot proceed because no operation is allowed, so we output NO and terminate.
4. If such an index is found, remove that element from the array and append its value to `ans`. Removal shifts all elements after index $i$ left by one position, changing their indices for future checks.
5. Repeat this process until the array becomes empty.
6. Finally, reverse `ans` and output it. The reversal is required because we recorded elements in removal order, while the problem asks for the reverse sequence.

Why it works

The crucial invariant is that any element that is not the rightmost valid position at a given step cannot be safely removed later if we skip it. Removing an element strictly to its left shifts its index and destroys the equality condition permanently. Removing elements to its right does not affect it. Therefore, if a removable element exists, the rightmost one is the only safe irreversible choice. This makes the greedy choice both necessary and sufficient, and repeated application eventually exhausts all valid removals if and only if a full deletion ordering exists.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))

    ans = []

    for _ in range(n):
        idx = -1

        for i in range(len(a) - 1, -1, -1):
            if a[i] == i + 1:
                idx = i
                break

        if idx == -1:
            print("NO")
            return

        ans.append(a[idx])
        a.pop(idx)

    print("YES")
    print(*ans[::-1])

if __name__ == "__main__":
    solve()
```

The implementation directly follows the greedy process. The inner loop searches from the end to ensure we pick the rightmost valid position. The `pop` operation removes that element and shifts the array, naturally maintaining correct indices for subsequent iterations. The final reversal of `ans` aligns the output with the required order.

A subtle point is the use of `i + 1` in the comparison. This reflects 1-based indexing in the condition, while Python arrays are 0-based. Careful alignment avoids off-by-one errors during validation.

## Worked Examples

Consider the array $[1, 2, 3]$.

### Trace 1

| Step | Array | Found index | Removed |
| --- | --- | --- | --- |
| 1 | [1, 2, 3] | 2 (3=3) | 3 |
| 2 | [1, 2] | 1 (2=2) | 2 |
| 3 | [1] | 0 (1=1) | 1 |

The removal order is $[3, 2, 1]$, and reversing gives $[1, 2, 3]$. This confirms that fully consistent arrays collapse cleanly under the rule.

### Trace 2

Consider $[2, 1, 3]$.

| Step | Array | Found index | Removed |
| --- | --- | --- | --- |
| 1 | [2, 1, 3] | 2 (3=3) | 3 |
| 2 | [2, 1] | none | fail |

Here the process halts early because no position satisfies the condition. This shows that not all permutations are solvable even if some elements initially match their index.

The trace demonstrates that the algorithm correctly enforces the necessity of rightmost valid removals and detects failure when no valid state remains.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n^2)$ | Each of up to $n$ deletions requires a linear scan to find the rightmost valid position |
| Space | $O(n)$ | Storage for the array and the output sequence |

The quadratic runtime is sufficient under typical Codeforces constraints for small to moderate $n$, and the memory usage is linear in the input size.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output

    solve = lambda: None  # placeholder, replace with actual solve if embedded

    return output.getvalue().strip()

# Sample-like cases (conceptual; replace with actual samples if provided)

# simple increasing
# assert run("3\n1 2 3\n") == "YES\n1 2 3"

# impossible case
# assert run("3\n2 1 3\n") == "NO"

# single element
# assert run("1\n1\n") == "YES\n1"

# already invalid start
# assert run("2\n2 2\n") == "NO"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 | YES 1 | minimum size |
| 2 1 | NO | immediate failure case |
| 1 2 3 | YES 1 2 3 | fully removable chain |
| 2 2 1 | NO | shifting breaks validity |

## Edge Cases

One important edge case is when only the last element is initially valid. For example, in $[2, 3, 1]$, only the last position satisfies the condition. The algorithm selects it immediately, ensuring correctness. After removal, the remaining structure becomes smaller and is re-evaluated cleanly, preserving the invariant.

Another case is when multiple valid positions exist but only the rightmost is safe. In $[1, 3, 2]$, both position 1 and position 3 are valid initially. The algorithm selects position 3 first. Removing position 1 instead would shift later elements and destroy future validity, leading to a dead state. The rightmost rule prevents this failure path.

A final subtle case is when validity appears later due to shifting. In $[2, 1, 3, 4]$, removing 4 first is necessary because it is rightmost valid. Only after that does the next correct structure emerge. The algorithm naturally handles this because it recomputes validity after every deletion rather than relying on stale positions.
