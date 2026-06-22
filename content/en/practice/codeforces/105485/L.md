---
title: "CF 105485L - \u6570\u7ec4\u4ea4\u6362"
description: "We are given a single array of odd length. The process runs for exactly half of its length rounded down, and each round always removes the first two elements after allowing a single adjacent swap somewhere in the array."
date: "2026-06-23T01:57:05+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105485
codeforces_index: "L"
codeforces_contest_name: "2024 China Unversity of Geosciences (Wuhan) Freshman Contest"
rating: 0
weight: 105485
solve_time_s: 61
verified: true
draft: false
---

[CF 105485L - \u6570\u7ec4\u4ea4\u6362](https://codeforces.com/problemset/problem/105485/L)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 1s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a single array of odd length. The process runs for exactly half of its length rounded down, and each round always removes the first two elements after allowing a single adjacent swap somewhere in the array.

The swap is unrestricted in position but limited to one adjacent exchange per round. After that, the first two elements are permanently deleted, and the remaining suffix becomes the new array for the next round. This continues until only one element remains, and the task is to maximize that final survivor by choosing swaps optimally.

The key difficulty is that the swap is global in choice but local in effect, and deletions are always fixed at the front. This creates a tension between how fast elements drift toward the front due to repeated deletions and how much we can delay or accelerate that drift using at most one swap per round.

The constraints allow n up to 2 × 10^5, which rules out any simulation that tries all possible swap decisions or tracks all possible states of the array. Any solution that branches on choices per round or per position would explode exponentially or at least quadratically.

A subtle failure case for naive reasoning appears when one assumes the best strategy is always to bubble the maximum element toward the front. That intuition breaks because the front is precisely where deletion happens immediately after swapping. For example, in a small array like [1, 100, 2, 3, 4], repeatedly pushing 100 forward can still fail if it gets caught in the first two positions too early, because deletion is unconditional.

Another misleading case is assuming the answer is always the global maximum. In [10, 6, 2, 1, 5, 3, 4], the maximum is 10 but it is impossible for it to survive, because it is removed too early in the deletion process regardless of swaps.

## Approaches

The brute-force view is to simulate every round, and at each round try all possible adjacent swaps before deleting the first two elements. Even if we only track one array, the choice of swap position creates O(n) branching per round, and there are O(n) rounds, leading to an exponential number of possible sequences. Even a naive simulation that tries all swap positions per round already costs O(n^2) operations in the best deterministic interpretation, which is far too slow for n up to 2 × 10^5.

The key insight is that the process is not really about local rearrangement power, but about survival against a fixed deletion schedule. Every round removes exactly two elements from the front, so each element’s fate depends on how long it can avoid drifting into the first two positions before it is eliminated. The single swap per round only allows an element to shift its effective position by at most one step per round, while deletions shift everything left by two steps per round.

This creates a linear drift model: each element moves left by two due to deletion pressure, and can be pushed right by at most one per round using swaps. The net effect is that each element can only “delay” its death by a bounded amount, and this bound depends only on its initial position, not on the values of other elements. This collapses the problem into identifying which indices are ever capable of surviving until the last round.

Once this perspective is established, the problem reduces to identifying the suffix of positions that can survive all rounds, and then taking the maximum value among them.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(n²) to O(exp(n)) | O(n) | Too slow |
| Position survival analysis | O(n) | O(1) extra | Accepted |

## Algorithm Walkthrough

We now translate the survival reasoning into a direct computation.

### Algorithm Walkthrough

1. Observe that there are (n − 1) / 2 rounds, and each round deletes exactly two elements from the front, so the process removes all but one element.
2. Track an element initially at position i. After k rounds without swaps, it shifts left by 2k positions due to deletions, so its effective position becomes i − 2k.
3. Use the single swap per round as a correction mechanism. Each round allows at most one adjacent swap, so over k rounds an element can be pushed right by at most k positions relative to the deletion drift.
4. Combine both effects. After k rounds, the best-case effective position of an element initially at i is i − 2k + k, which simplifies to i − k.
5. For an element to survive until the final round k = (n − 1) / 2, its effective position must remain positive at that time. This gives the condition i − (n − 1) / 2 > 0.
6. This simplifies to i > (n − 1) / 2, meaning only elements in the second half of the array can possibly survive until the end.
7. The final answer is therefore the maximum value among indices from (n + 1) / 2 to n in 1-based indexing.

### Why it works

The deletion process deterministically removes two elements per round from the front, which creates a rigid leftward drift for every element. The only control offered by the algorithm is a bounded rightward correction of at most one position per round via a single adjacent swap. Because both effects scale linearly with the number of rounds, the net displacement of any element is also linear and fully determined by its starting index.

This means survival is not influenced by relative ordering changes between arbitrary pairs of elements deep in the array, but only by whether an element can avoid entering the deletion zone before the final round. Once an element starts in the first half, its maximum possible rightward correction is insufficient to counteract repeated deletions, so it must eventually be removed. Elements in the second half have enough slack to remain out of the deletion window long enough to survive to the end.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))
    
    start = n // 2  # 0-based index of (n+1)/2 in 1-based
    print(max(a[start:]))

if __name__ == "__main__":
    solve()
```

The implementation directly applies the derived survival boundary. The only subtlety is indexing: in 0-based indexing, the surviving segment begins at n // 2.

The rest is a straightforward maximum over a suffix. No simulation is required because all dynamic behavior of swaps has already been absorbed into the survival inequality.

## Worked Examples

### Example 1

Input:

```
7
10 6 2 1 5 3 4
```

We track the surviving region.

| Step | Array suffix considered | Reason |
| --- | --- | --- |
| Initial | [10, 6, 2, 1, 5, 3, 4] | full array |
| After boundary | [1, 5, 3, 4] | only last (n+1)/2 elements survive |
| Result | 5 | maximum in suffix |

This confirms that the optimal strategy does not care about the global maximum, but only about which elements are structurally allowed to survive the deletion process.

### Example 2

Input:

```
5
1 2 3 4 5
```

| Step | Array suffix considered | Reason |
| --- | --- | --- |
| Initial | [1, 2, 3, 4, 5] | full array |
| After boundary | [3, 4, 5] | last three elements survive |
| Result | 5 | maximum in suffix |

This shows that even small elements at the front are irrelevant if they fall outside the survivable region, because they are guaranteed to be deleted before the process ends.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | single pass to compute suffix maximum |
| Space | O(1) | only input array storage is used |

The solution fits easily within limits for n up to 2 × 10^5, since it performs only one linear scan and no simulation of the swap-deletion process.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n = int(input())
    a = list(map(int, input().split()))
    start = n // 2
    return str(max(a[start:]))

# provided sample
assert run("7\n10 6 2 1 5 3 4\n") == "5"

# minimum size
assert run("1\n42\n") == "42"

# simple increasing
assert run("5\n1 2 3 4 5\n") == "5"

# all equal
assert run("5\n7 7 7 7 7\n") == "7"

# maximum at front but not reachable
assert run("5\n100 1 1 1 1\n") == "1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| n=1 single element | 42 | trivial base case |
| increasing array | 5 | suffix dominance |
| all equal | 7 | no structural bias |
| large front maximum | 1 | early elements cannot survive |

## Edge Cases

A key edge case is when the maximum element sits in the first half of the array. In that situation, it is tempting to assume swaps can always rescue it, but the drift caused by repeated deletions overwhelms the limited swap budget.

For input:

```
5
100 1 2 3 4
```

the algorithm selects the suffix [2, 3, 4], and returns 4. The element 100 starts at position 1, but every round removes two elements from the front, and the single swap per round cannot compensate for being consistently inside the deletion zone early in the process.

Another edge case is uniform arrays like:

```
5
7 7 7 7 7
```

Here every strategy yields the same final value. The suffix rule still applies, and the algorithm correctly returns 7 by taking the maximum of the last three elements.
