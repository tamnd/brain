---
title: "CF 902A - Visiting a Friend"
description: "We are given a set of teleporters placed along a one-dimensional number line. Pig starts at position 0 and wants to reach position m."
date: "2026-06-15T11:52:05+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "implementation"]
categories: ["algorithms"]
codeforces_contest: 902
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 453 (Div. 2)"
rating: 1100
weight: 902
solve_time_s: 316
verified: true
draft: false
---

[CF 902A - Visiting a Friend](https://codeforces.com/problemset/problem/902/A)

**Rating:** 1100  
**Tags:** greedy, implementation  
**Solve time:** 5m 16s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a set of teleporters placed along a one-dimensional number line. Pig starts at position 0 and wants to reach position m. Each teleporter is located at some coordinate ai, and if Pig arrives at that coordinate, he can choose any destination within the interval from ai up to bi.

The teleports are presented in an order where their starting positions ai never decrease as we move down the list. This ordering matters because it allows us to process them from left to right without reconsidering earlier structure.

The task is to determine whether there exists a sequence of teleport uses that starts from 0 and eventually reaches m.

The constraints are small. With at most 100 teleports, even an O(n²) simulation would pass easily, but the structure suggests a simpler linear scan is enough. The key difficulty is not computation time but understanding how reachability evolves as new teleports become available.

A naive misunderstanding often comes from treating each teleport independently. For example, assuming that being able to reach a teleport at ai immediately means you must use it, or assuming you can only use teleports in strict order of use rather than availability. Another subtle mistake is ignoring that a teleport may extend reach beyond its own position, enabling later teleports to become usable.

A concrete failure case looks like this:

Input:

```
2 5
0 1
2 5
```

A careless approach might try to chain strictly and fail to realize that reaching only up to 1 does not allow access to the second teleport at 2, so the answer is NO. But a correct reach-tracking approach sees that the first teleport caps reach at 1, which is insufficient, so progression stops.

Another edge case:

Input:

```
2 5
0 3
1 2
```

Even though the second teleport appears to go “backward” in usefulness, it is irrelevant if we already reach farther with the first one. Correct logic must always prefer the maximum reachable extension, not the most recently encountered teleport.

## Approaches

The brute-force idea is to treat this as a reachability problem where from a current position we try every teleport that is usable, recursively exploring all possible destinations within its allowed interval. This effectively builds a graph where each point in every interval is a node, and teleports create dense directed connections. While conceptually correct, this explodes because each teleport can generate a continuum of reachable points, and even if discretized, we may repeatedly revisit states. In the worst case, exploring all combinations of teleport usage leads to exponential behavior.

The key observation is that we never need to track all reachable positions, only the farthest point Pig can currently reach. If we can reach ai, then the best possible use of that teleport is to extend reach to bi. Since all movement is monotonic in terms of position (we never need to go backward), the problem reduces to greedily expanding a frontier.

We process teleports in increasing order of ai. Whenever a teleport’s starting point is within our current reachable range, we can use it to extend that range. If a teleport starts beyond what we can currently reach, we cannot use it yet, and since future teleports start even further right (due to ordering), we stop checking further extensions when we hit such a gap.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (state search) | Exponential | High | Too slow |
| Greedy reach expansion | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

We maintain a single value representing the farthest position Pig can currently reach.

1. Initialize the reachable position as 0 because Pig starts there.
2. Iterate through each teleport in the given order.
3. If the teleport’s starting point ai is greater than the current reachable position, stop processing further teleports. This works because later teleports start even further right and are therefore also unreachable.
4. If ai is within the reachable range, update the reachable position to max(current reach, bi). This reflects using the teleport optimally to extend as far right as possible.
5. After processing all usable teleports, check whether the reachable position is at least m. If yes, Pig can reach the friend; otherwise he cannot.

### Why it works

At every step, the algorithm maintains the invariant that the reachable position is the maximum rightmost point Pig can reach using any sequence of teleports from the processed prefix. Because teleports are sorted by ai, once we encounter a teleport whose starting point lies beyond current reach, no future teleport can ever be activated. Among all usable teleports, taking bi greedily is optimal because any intermediate choice within [ai, bi] can only reduce or equal future reach, never improve it.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    
    reach = 0
    
    for _ in range(n):
        a, b = map(int, input().split())
        
        if a > reach:
            break
        
        if a <= reach:
            if b > reach:
                reach = b
    
    print("YES" if reach >= m else "NO")

if __name__ == "__main__":
    solve()
```

The implementation directly mirrors the greedy idea. The variable `reach` stores the furthest position reachable so far. The early break is important: once a teleport is out of reach, later ones cannot help due to sorted ai. The max update ensures we always expand reach as far as possible.

A common mistake is removing the break and continuing to scan, which is still correct but slower in larger variants. Another mistake is updating reach with ai instead of bi, which would ignore the expansion capability of each teleport.

## Worked Examples

### Sample 1

Input:

```
3 5
0 2
2 4
3 5
```

| Step | ai | bi | Reach before | Decision | Reach after |
| --- | --- | --- | --- | --- | --- |
| 1 | 0 | 2 | 0 | usable | 2 |
| 2 | 2 | 4 | 2 | usable | 4 |
| 3 | 3 | 5 | 4 | usable | 5 |

Pig progressively extends reachable distance until reaching 5.

This confirms the invariant that reach always reflects the best achievable position after each usable teleport.

### Sample 2

Input:

```
2 5
0 3
4 5
```

| Step | ai | bi | Reach before | Decision | Reach after |
| --- | --- | --- | --- | --- | --- |
| 1 | 0 | 3 | 0 | usable | 3 |
| 2 | 4 | 5 | 3 | blocked | 3 |

The second teleport is never usable because Pig cannot reach its starting point. This demonstrates why reach-based gating is essential.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each teleport is processed once until reach blocks further scanning |
| Space | O(1) | Only a single variable is used for tracking reach |

The constraints allow up to 100 teleports, so even the linear scan is far below the limit. The solution is effectively constant-time in practice.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    from math import *
    
    n, m = map(int, sys.stdin.readline().split())
    reach = 0
    
    for _ in range(n):
        a, b = map(int, sys.stdin.readline().split())
        if a > reach:
            break
        if b > reach:
            reach = b
    
    return "YES\n" if reach >= m else "NO\n"

# provided sample 1
assert run("3 5\n0 2\n2 4\n3 5\n") == "YES\n"

# sample 2
assert run("2 5\n0 3\n4 5\n") == "NO\n"

# custom case: already at target
assert run("1 1\n0 5\n") == "YES\n"

# custom case: cannot start
assert run("2 10\n1 5\n2 9\n") == "NO\n"

# custom case: chained reach
assert run("4 10\n0 2\n2 5\n5 7\n7 10\n") == "YES\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single large jump | YES | immediate success case |
| unreachable start | NO | first teleport not usable |
| chained coverage | YES | greedy expansion correctness |

## Edge Cases

One edge case is when the first teleport does not start at 0. For example, if the first ai is 1, Pig cannot move at all, so the answer is immediately NO. The algorithm handles this naturally because reach starts at 0 and the first check a > reach causes termination.

Another case is when multiple teleports overlap heavily. Even if a later teleport has a smaller interval, it does not matter because reach only grows via max updates. The algorithm ignores useless regressions safely because it never decreases reach.
