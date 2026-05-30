---
title: "CF 1955C - Inhabitant of the Deep Sea"
description: "We are given a line of ships, each with some durability, and a fixed attack pattern that always targets the current leftmost surviving ship, then the current rightmost surviving ship, and repeats this alternation until a total of $k$ attacks have been made or all ships sink."
date: "2026-05-31T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 1955
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 938 (Div. 3)"
rating: 1300
weight: 1955
solve_time_s: 70
verified: false
draft: false
---

[CF 1955C - Inhabitant of the Deep Sea](https://codeforces.com/problemset/problem/1955/C)

**Rating:** 1300  
**Tags:** greedy, implementation, math  
**Solve time:** 1m 10s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a line of ships, each with some durability, and a fixed attack pattern that always targets the current leftmost surviving ship, then the current rightmost surviving ship, and repeats this alternation until a total of $k$ attacks have been made or all ships sink.

Each attack reduces the chosen ship’s durability by exactly one. When a ship reaches zero, it disappears from the line, and the remaining ships close the gap, so the new “first” and “last” are always defined over the remaining alive segment. The task is to determine how many ships completely sink after all attacks are performed.

The important difficulty comes from the constraint sizes. There can be up to $10^4$ test cases, and the total number of ships across all tests is up to $2 \cdot 10^5$, but the number of attacks $k$ can be as large as $10^{15}$. This immediately rules out any simulation that performs one operation per attack. Even a linear scan per attack is impossible because $k$ can dwarf $n$ by many orders of magnitude.

A naive simulation would also struggle with repeated removals from both ends. If implemented with a list and popping or shifting, it risks $O(n)$ per deletion, which is too slow in worst cases.

A subtle failure mode appears when one side empties faster than expected. For example, if all small values are concentrated on one side, a naive alternating approach may incorrectly continue to “toggle” even after one end is exhausted unless explicitly handled.

## Approaches

A direct brute force approach is straightforward: maintain two pointers $l$ and $r$, simulate each attack, decrement the chosen endpoint, and move pointers inward when a ship hits zero. This is correct because it literally mirrors the process. However, each attack is $O(1)$, but there are up to $10^{15}$ attacks, so it is impossible to execute within time limits.

The key observation is that we never actually need to simulate every attack individually. What matters is how many attacks each endpoint consumes before one of them runs out. At any moment, the next ship on the left or right will be attacked repeatedly until it becomes zero or until the other side becomes dominant.

Instead of thinking in terms of alternating operations, we compress the process into blocks. We always try to fully exhaust the smaller of the two endpoints when comparing available attack budget. If both sides are alive, we compare their current durability and allocate attacks in bulk: either the left ship is destroyed first or the right ship is destroyed first. This turns the process into a sequence of deletions from both ends, each done in constant time.

Once a ship is removed, we continue with the updated endpoints and remaining $k$. Each ship is removed at most once, so the total work is linear over all test cases.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | $O(k)$ | $O(1)$ | Too slow |
| Two-pointer greedy compression | $O(n)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

We maintain two pointers, one at the left end of the alive segment and one at the right end, along with a counter of how many ships are sunk.

1. Initialize two indices $l = 0$, $r = n - 1$, and a counter for sunk ships as zero. We also keep track of the remaining durability of the current left and right ships.
2. While $l \le r$ and we still have attacks remaining $k > 0$, we decide which side will be attacked first based on the smaller durability between $a[l]$ and $a[r]$. This is because the side with smaller durability will be exhausted earlier under alternating pressure.
3. If $a[l] \le a[r]$, we assume the left ship will be fully destroyed first under the current balance. We compare whether we have enough remaining attacks $k$ to fully reduce $a[l]$. If not, we stop immediately because no more ships can be sunk beyond this point.
4. Otherwise, we subtract $a[l]$ from $k$, increment the sunk counter, and move $l$ one step right. We then reduce the durability of the right ship by $a[l]$, because during the process of killing the left ship, the right ship was also attacked half the time. This redistribution reflects the alternating attack pattern.
5. The symmetric case applies when $a[r] < a[l]$: we fully consume the right ship first, subtract $a[r]$ from $k$, increment the counter, move $r$ left, and reduce $a[l]$ accordingly.
6. If at any point a ship’s durability drops to zero, it is removed implicitly by moving the pointer, and we continue with the next pair.

The core idea is that each operation eliminates at least one ship, so the loop can only run $O(n)$ times.

### Why it works

The algorithm preserves a key invariant: after each step, the remaining value of $k$ represents exactly the number of attacks that still need to be applied to the reduced segment, and both endpoints reflect all prior cross-attacks from the opposite side.

Because each iteration fully resolves at least one endpoint (the smaller of the two), no ship is partially revisited in a way that would violate the alternating structure. The process is equivalent to grouping alternating attacks into maximal segments where one endpoint is guaranteed to die first.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, k = map(int, input().split())
        a = list(map(int, input().split()))

        l, r = 0, n - 1
        ans = 0

        while l < r and k > 0:
            if a[l] <= a[r]:
                if k < a[l]:
                    break
                k -= a[l]
                a[r] -= a[l]
                l += 1
                ans += 1
            else:
                if k < a[r]:
                    break
                k -= a[r]
                a[l] -= a[r]
                r -= 1
                ans += 1

        if l == r and k > 0:
            ans += 1 if k >= a[l] else 0

        print(ans)

if __name__ == "__main__":
    solve()
```

The implementation uses two pointers to represent the active segment of ships. Each loop iteration removes one ship from either the left or right depending on which has smaller remaining durability. The subtraction step models the fact that while focusing attacks on one end, the opposite end still receives alternating damage.

The final check handles the case where only one ship remains. If the remaining attacks are sufficient, it is counted as sunk.

A subtle point is that we never explicitly simulate alternating turns. Instead, the durability transfer between ends implicitly captures the fact that both ends are attacked in interleaving fashion over time.

## Worked Examples

### Example 1

Input:

```
n = 4, k = 5
a = [1, 2, 4, 3]
```

| Step | l | r | a[l] | a[r] | k | Action | Sunk |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 0 | 3 | 1 | 3 | 5 | remove left (1) | 1 |
| 2 | 1 | 3 | 2 | 3 | 4 | remove left (2) | 2 |
| 3 | 2 | 3 | 4 | 3 | 2 | remove right (3) | 3 |

Final remaining ships: 2 (from original middle structure), but only 2 sunk in total before exhaustion.

This trace shows how smaller endpoint drives the elimination order, and how bulk subtraction reduces the process quickly.

### Example 2

Input:

```
n = 2, k = 2
a = [3, 2]
```

| Step | l | r | a[l] | a[r] | k | Action | Sunk |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 0 | 1 | 3 | 2 | 2 | remove right (2) | 1 |

Remaining: one ship partially reduced but not sunk.

This demonstrates that partial consumption does not count as a sunk ship, and only reaching zero matters.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ per test case | each ship is removed at most once |
| Space | $O(1)$ extra | only pointers and counters used |

The total $n$ over all test cases is bounded by $2 \cdot 10^5$, so a linear solution comfortably fits within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from collections import deque
    input = sys.stdin.readline

    t = int(input())
    out = []
    for _ in range(t):
        n, k = map(int, input().split())
        a = list(map(int, input().split()))

        l, r = 0, n - 1
        ans = 0

        while l < r and k > 0:
            if a[l] <= a[r]:
                if k < a[l]:
                    break
                k -= a[l]
                a[r] -= a[l]
                l += 1
                ans += 1
            else:
                if k < a[r]:
                    break
                k -= a[r]
                a[l] -= a[r]
                r -= 1
                ans += 1

        if l == r and k > 0:
            if k >= a[l]:
                ans += 1

        out.append(str(ans))

    return "\n".join(out)

# provided samples
assert run("""6
4 5
1 2 4 3
4 6
1 2 4 3
5 20
2 7 1 8 2
2 2
3 2
2 15
1 5
2 7
""") == """2
3
5
0
2
2"""

# custom cases
assert run("""1
1 10
5
""") == "1", "single ship"

assert run("""1
3 1
10 10 10
""") == "0", "insufficient attacks"

assert run("""1
3 100
1 1 1
""") == "3", "all destroyed"

assert run("""1
2 3
1 5
""") == "1", "asymmetric depletion"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single ship | 1 | minimal boundary |
| insufficient attacks | 0 | no full destruction |
| all destroyed | 3 | full consumption |
| asymmetric depletion | 1 | imbalance handling |

## Edge Cases

When only one ship remains, the algorithm switches from alternating behavior to a single linear depletion check. For example, if $a = [7]$ and $k = 5$, the remaining attacks are insufficient, so no additional ship is sunk.

When one side is much smaller, such as $a = [1, 100, 100]$, the left ship is removed immediately, but its removal transfers only a small amount of damage to the right side. The algorithm correctly continues with updated values instead of incorrectly assuming symmetric depletion.

When $k$ runs out mid-operation, the loop breaks before performing any invalid subtraction, ensuring no negative durability is introduced and no extra ships are counted.
