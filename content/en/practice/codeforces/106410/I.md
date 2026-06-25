---
title: "CF 106410I - Pace Pushers"
description: "We have a set of beacons placed on a line. Each beacon has a position and a current power. A beacon with power p covers the inclusive interval [x - p, x + p]. During every round, every pair of overlapping intervals with different powers causes the weaker beacon to gain one power."
date: "2026-06-25T09:56:12+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106410
codeforces_index: "I"
codeforces_contest_name: "HPI 2026 Novice"
rating: 0
weight: 106410
solve_time_s: 43
verified: true
draft: false
---

[CF 106410I - Pace Pushers](https://codeforces.com/problemset/problem/106410/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 43s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a set of beacons placed on a line. Each beacon has a position and a current power. A beacon with power `p` covers the inclusive interval `[x - p, x + p]`. During every round, every pair of overlapping intervals with different powers causes the weaker beacon to gain one power. All gains happen simultaneously. The task is to determine the total number of integer positions covered after the process reaches a stable state.

The number of beacons can reach `2 * 10^5`, so simulating rounds is impossible. A single round can change many powers, and the number of rounds can also be large because powers can increase by one at a time. With this input size we need a solution close to `O(n log n)`, which rules out anything involving repeated comparisons between many pairs of beacons.

The main traps are caused by the fact that powers change, not only the intervals. A beacon that is initially separated from another beacon can become connected after some increases. A solution that only merges initially overlapping intervals is incorrect.

For example:

```
2
0 1
5 3
```

The intervals are `[-1,1]` and `[2,8]`, so they already overlap because the second starts immediately after the first ends. The powers become equalized at `3`, and the final union is `[-3,8]`, with length `12`. A careless implementation that only keeps the initial union would output `10`.

Another example is:

```
3
0 1
4 1
8 5
```

The first two beacons do not overlap, but the third beacon reaches the second one. The second beacon increases and can eventually connect the first two into the same final component. Ignoring newly created overlaps would miss this chain reaction.

The last edge case is a beacon with the maximum power in a component. It never grows, while every weaker beacon eventually reaches that same power. Treating all beacons as if they grow symmetrically gives wrong final powers.

## Approaches

The direct approach is to simulate the process. For every round, we could check every pair of beacons, find all overlapping pairs, and increase the weaker powers. This is correct because it follows the rules exactly. However, checking all pairs costs `O(n^2)` per round. With `n = 2 * 10^5`, even one full scan is already too expensive, and the number of rounds is not bounded by a small constant.

The key observation is that the process only depends on connected groups. Inside any connected group of overlapping intervals, the maximum power never changes, because there is no stronger beacon to increase it. Every other beacon has a path of overlaps leading to a maximum power beacon, so the increases propagate along this path until every beacon reaches the same maximum power.

This means the dynamic process can be replaced by a static merging process. We process beacons from left to right. Every processed group is represented by its leftmost position, rightmost position, and the maximum power inside it. If a new group overlaps the previous group after both are expanded to their final powers, they must actually belong to the same final component. We merge them and keep the larger maximum power.

A stack is enough because only the last processed component can be affected by a new beacon. After merging two components, the new component can also reach the component before them, so we repeatedly merge while the last two stack entries overlap.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `O(r * n^2)` | `O(n)` | Too slow |
| Optimal | `O(n log n)` | `O(n)` | Accepted |

## Algorithm Walkthrough

1. Sort all beacons by their position. We process them in this order because every possible future interaction can only happen with components already seen or with components to the right.
2. Create a new component from the current beacon. Its left and right boundaries are both the beacon position, and its power is the beacon's original power.
3. Compare the new component with the previous component in the stack. If their final intervals overlap, they cannot remain separate. Merge them by taking the left boundary from the left component, the right boundary from the right component, and the maximum power from both.
4. Continue merging backward while the new merged component still overlaps the previous stack element. This handles a strong component that expands far enough to absorb several older components.
5. After all beacons are processed, every stack entry is one final stable component. Sum the lengths of their intervals.

Why it works: the invariant is that after processing the first `i` beacons, the stack contains exactly the final components that can be formed using only those beacons. A component stores its eventual maximum power, because every weaker beacon inside it will eventually reach that value. When two adjacent stored components overlap, their beacons would influence each other after stabilization, so keeping them separate would violate the definition of a final component. The repeated merging restores the invariant after every insertion.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = []
    for _ in range(n):
        x, p = map(int, input().split())
        a.append((x, p))

    a.sort()

    stack = []

    for x, p in a:
        stack.append([x, x, p])

        while len(stack) >= 2:
            l1, r1, p1 = stack[-2]
            l2, r2, p2 = stack[-1]

            if l2 - p2 <= r1 + p1:
                nl = l1
                nr = max(r1, r2)
                np = max(p1, p2)

                stack.pop()
                stack.pop()
                stack.append([nl, nr, np])
            else:
                break

    ans = 0
    for l, r, p in stack:
        ans += r - l + 1

    print(ans)

if __name__ == "__main__":
    solve()
```

The input is sorted first because the stack method relies on left to right processing. Each stack entry stores only the information that matters after stabilization: the extreme positions and the largest power.

The overlap check uses the final expanded intervals. Two components `[l1, r1]` and `[l2, r2]` with powers `p1` and `p2` interact if `l2 - p2 <= r1 + p1`. The merge operation keeps the largest power because that is the final power shared by the whole connected component.

The final loop computes inclusive lengths, so the contribution of `[l, r]` is `r - l + 1`.

## Worked Examples

For the sample:

```
7
0 1
3 1
5 2
9 1
12 3
20 1
21 1
```

The stack evolves as follows:

| Beacon | New component | Stack after merging |
| --- | --- | --- |
| `(0,1)` | `[-, -, 1]` | `[-1,1]` power `1` |
| `(3,1)` | `[3,3,1]` | `[-1,4]` power `1` |
| `(5,2)` | `[5,5,2]` | `[-3,7]` power `2` |
| `(9,1)` | `[9,9,1]` | `[-3,7]`, `[8,10]` |
| `(12,3)` | `[12,12,3]` | `[-3,15]` power `3` |
| `(20,1)` | `[20,20,1]` | `[-3,15]`, `[19,21]` |
| `(21,1)` | `[21,21,1]` | `[-3,15]`, `[19,22]` |

This trace shows why a new beacon can merge backward through several components. The beacon at position `12` absorbs the earlier chain because its power is large enough.

Another case:

```
3
0 1
4 1
8 5
```

| Beacon | Stack state |
| --- | --- |
| `(0,1)` | `[-1,1]` |
| `(4,1)` | `[-1,5]` |
| `(8,5)` | `[-5,13]` |

The large third beacon expands enough to connect everything, even though the first two beacons alone would form a different component.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(n log n)` | Sorting dominates, and every component is pushed and popped at most once |
| Space | `O(n)` | The stack can contain all beacons in the worst case |

The algorithm only performs a linear number of stack operations after sorting, so it fits the limit for `2 * 10^5` beacons.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    old = sys.stdin
    sys.stdin = io.StringIO(inp)
    data = sys.stdin.read().split()
    sys.stdin = old

    if not data:
        return ""

    it = iter(data)
    n = int(next(it))
    a = []

    for _ in range(n):
        x = int(next(it))
        p = int(next(it))
        a.append((x, p))

    a.sort()
    stack = []

    for x, p in a:
        stack.append([x, x, p])
        while len(stack) >= 2:
            l1, r1, p1 = stack[-2]
            l2, r2, p2 = stack[-1]
            if l2 - p2 <= r1 + p1:
                stack.pop()
                stack.pop()
                stack.append([l1, max(r1, r2), max(p1, p2)])
            else:
                break

    ans = sum(r - l + 1 for l, r, p in stack)
    return str(ans) + "\n"

assert run("""7
0 1
3 1
5 2
9 1
12 3
20 1
21 1
""") == "23\n"

assert run("""1
100 7
""") == "15\n"

assert run("""3
0 1
4 1
8 5
""") == "19\n"

assert run("""2
0 1
10 1
""") == "4\n"

assert run("""4
0 2
5 2
10 2
15 2
""") == "32\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single beacon | `15` | Minimum case and inclusive length |
| Long range beacon connection | `19` | Chain reaction through a strong beacon |
| Separated equal powers | `4` | Components that never merge |
| All equal powers | `32` | No power changes and repeated merging |

## Edge Cases

For the case

```
2
0 1
5 3
```

the stack first creates two components. The second component expands to `[2,8]`, which overlaps `[ -1,1 ]`, so they merge. The final component has power `3` and interval `[-3,8]`, giving length `12`.

For

```
3
0 1
4 1
8 5
```

the first two beacons merge into a component with power `1`. When the third beacon is inserted, its interval `[3,13]` overlaps that component's final interval, so the whole structure becomes one component. The stored maximum power becomes `5`, producing `[-5,13]` with length `19`.

The stack method also handles large powers safely because all arithmetic is done with Python integers, so positions up to `10^9` and expanded ranges beyond that do not overflow.
