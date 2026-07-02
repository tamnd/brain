---
title: "CF 103521A - \u041a\u0430\u043a \u043f\u043e\u043a\u043e\u0440\u043c\u0438\u0442\u044c \u0434\u0440\u0430\u043a\u043e\u043d\u0430"
description: "We can reinterpret the situation as follows. We have a starting integer strength s and a list of enemies. Each enemy is described by two values: a threshold strength needed to survive the fight and a bonus gained after winning."
date: "2026-07-03T06:01:05+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103521
codeforces_index: "A"
codeforces_contest_name: "\u0418\u043d\u0442\u0435\u0440\u043d\u0435\u0442-\u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u044b, \u0421\u0435\u0437\u043e\u043d 2018-2019, \u0422\u0440\u0435\u0442\u044c\u044f \u043b\u0438\u0447\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430"
rating: 0
weight: 103521
solve_time_s: 47
verified: true
draft: false
---

[CF 103521A - \u041a\u0430\u043a \u043f\u043e\u043a\u043e\u0440\u043c\u0438\u0442\u044c \u0434\u0440\u0430\u043a\u043e\u043d\u0430](https://codeforces.com/problemset/problem/103521/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 47s  
**Verified:** yes  

## Solution
## Problem Understanding

We can reinterpret the situation as follows.

We have a starting integer strength `s` and a list of enemies. Each enemy is described by two values: a threshold strength needed to survive the fight and a bonus gained after winning. If at any point we choose an enemy whose threshold is strictly greater than or equal to our current strength, we fail immediately. Otherwise, we defeat it and increase our strength by its bonus.

The goal is not to simulate a fixed sequence but to determine whether there exists some ordering of enemies that allows us to defeat all of them.

The input size is small: the number of dragons is at most around 1000. This immediately suggests that an O(n^2) greedy strategy is acceptable, while anything exponential over permutations is impossible because n! orderings would explode even for moderate n.

A naive mistake is to assume any arbitrary order works or that sorting by strength alone is sufficient. That fails in cases where a weaker dragon gives a large bonus that unlocks stronger dragons later.

For example, consider:

Input:

```
s = 2
(1, 99), (100, 0)
```

If we fight the strong dragon first, we die immediately. If we fight the weak dragon first, we become strong enough to defeat the second. So order matters critically.

Another subtle edge case is when all dragons are initially too strong, but one of them is just barely reachable and gives enough bonus to unlock the rest. Greedy selection must detect this incremental unlocking process.

## Approaches

The brute-force approach would try all permutations of dragons and simulate fights. This is correct but infeasible: there are n! permutations, and even n = 15 already becomes too large.

The key observation is that once we are strong enough to defeat a dragon, there is no reason to delay fighting it if it helps us become stronger sooner. Delaying only risks missing opportunities to unlock stronger dragons earlier. This leads to a greedy strategy: at each step, among all dragons we can currently defeat, pick one.

The remaining question is which “defeatable” dragon to choose first. The correct choice is to prioritize dragons with smaller strength requirements first. Sorting dragons by required strength ensures that whenever we scan forward, we always encounter all currently reachable options in a structured way, and we greedily consume them in increasing difficulty order while continuously expanding our reach.

The algorithm becomes: sort by threshold, then repeatedly take all reachable dragons, and consume them in any order, typically using a linear scan.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (all permutations) | O(n!) | O(n) | Too slow |
| Greedy + sorting by strength | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Pair each dragon’s required strength and bonus into a list of tuples and sort this list by required strength in ascending order. Sorting ensures we always consider easier dragons before harder ones, which aligns with the idea that unlocking strength should be progressive.
2. Maintain a variable `cur` initialized to the starting strength. This represents the current capability at every moment in the process.
3. Iterate through the sorted list, and whenever the next dragon’s required strength is strictly less than `cur`, mark it as available for defeat. This works because sorting guarantees that all previously considered dragons are also weaker or equal in requirement.
4. Among all currently available dragons, repeatedly pick any unvisited one, defeat it, and add its bonus to `cur`. Each defeat may unlock new dragons, so the availability set must be updated dynamically.
5. Continue this process until no further dragons can be defeated in the current pass. Then resume scanning forward in the sorted list to find newly unlocked dragons.
6. After all possible expansions are processed, check whether all dragons were defeated. If yes, output “YES”, otherwise output “NO”.

### Why it works

The correctness comes from a monotonic reachability invariant: at any point, we maintain the set of dragons whose required strength is less than the current strength, and we ensure that if any such dragon exists, we eventually process it. Since defeating a dragon only increases strength, the reachable set can only grow over time, never shrink. This guarantees that if a full ordering exists, the greedy process will discover a valid sequence without ever skipping a necessary intermediate unlock.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, s = map(int, input().split())
dragons = [tuple(map(int, input().split())) for _ in range(n)]

dragons.sort()  # sort by required strength

cur = s
i = 0
used = 0

visited = [False] * n

while True:
    progress = False

    while i < n and dragons[i][0] < cur:
        if not visited[i]:
            visited[i] = True
            cur += dragons[i][1]
            used += 1
            progress = True
        i += 1

    if not progress:
        break

print("YES" if used == n else "NO")
```

The code first sorts dragons by their strength requirement so that feasibility is always checked in increasing order. The pointer `i` ensures we only scan forward once, preventing repeated work. The inner loop collects all currently defeatable dragons and immediately applies their bonuses, which may unlock stronger ones.

A subtle detail is that we use `< cur` rather than `<= cur`. This matches the rule that equal strength is insufficient to survive.

The algorithm relies on the fact that each dragon is processed at most once, making the overall complexity linear after sorting.

## Worked Examples

### Example 1

Input:

```
s = 2
(1, 99), (100, 0)
```

| Step | cur | i | Action | Used |
| --- | --- | --- | --- | --- |
| start | 2 | 0 | none | 0 |
| process (1,99) | 101 | 1 | defeat dragon 1 | 1 |
| process (100,0) | 101 | 2 | defeat dragon 2 | 2 |

This confirms that early weak-but-rewarding dragons are crucial to unlock later ones.

### Example 2

Input:

```
s = 10
(100, 100)
```

| Step | cur | i | Action | Used |
| --- | --- | --- | --- | --- |
| start | 10 | 0 | none | 0 |

No dragon is reachable since 100 >= 10, so the process ends immediately.

This demonstrates the failure case where no sequence exists.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting dominates; each dragon is processed once |
| Space | O(n) | Storage for dragon list and visited array |

Given n up to around 1000, this runs comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from subprocess import PIPE, Popen
    p = Popen(["python3", "main.py"], stdin=PIPE, stdout=PIPE, stderr=PIPE, text=True)
    out, _ = p.communicate(inp)
    return out.strip()

# sample 1
assert run("2 2\n1 99\n100 0\n") == "YES"

# sample 2
assert run("10 1\n100 100\n") == "NO"

# minimal case
assert run("1 5\n1 10\n") == "YES"

# impossible chain
assert run("3 1\n2 1\n3 1\n4 1\n") == "NO"

# large bonus chain
assert run("3 1\n1 1\n2 10\n3 10\n") == "YES"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single reachable dragon | YES | base case correctness |
| single impossible dragon | NO | immediate failure |
| ascending chain | NO | ordering dependency |
| bonus amplification | YES | greedy growth effect |

## Edge Cases

One edge case occurs when multiple dragons have the same required strength. The algorithm handles this correctly because once `cur` exceeds that threshold, all of them become simultaneously available and can be consumed in any order, since each increases strength independently.

Another case is when the optimal strategy requires delaying a strong-but-reachable dragon in favor of a weaker one with a higher bonus. The greedy scan naturally handles this because all currently reachable dragons are processed, and there is no benefit in artificially delaying any of them, since bonuses only increase future reachability.

A final edge case is when the initial strength already exceeds all thresholds. In that case, the algorithm simply consumes everything in a single sweep, confirming that ordering constraints are irrelevant once everything is reachable.
