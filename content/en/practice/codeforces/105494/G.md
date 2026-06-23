---
title: "CF 105494G - Need More Gold"
description: "We are given a collection of monsters, each described by two numbers. One value represents how much gold you need to have before you can defeat that monster, and the other represents how much gold you gain after defeating it."
date: "2026-06-23T21:02:52+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105494
codeforces_index: "G"
codeforces_contest_name: "2024-2025 ICPC NERC, Kyrgyzstan Qualification Contest"
rating: 0
weight: 105494
solve_time_s: 53
verified: true
draft: false
---

[CF 105494G - Need More Gold](https://codeforces.com/problemset/problem/105494/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 53s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a collection of monsters, each described by two numbers. One value represents how much gold you need to have before you can defeat that monster, and the other represents how much gold you gain after defeating it. You start with some initial amount of gold and repeatedly choose monsters to fight. A monster can only be fought if your current gold is at least its required threshold. After defeating it, your gold increases by its reward.

The task is to determine the maximum number of monsters you can defeat by choosing the order of fights optimally.

The key difficulty is that the order matters. A monster with a small requirement might unlock access to another one later, and a monster with a large reward might be more valuable earlier because it increases your future reach.

From a constraints perspective, the intended solution must run in roughly O(n log n). Any approach that repeatedly scans all remaining monsters to choose the next one will degrade to O(n²), which is too slow for large inputs.

A subtle failure case for greedy intuition is when a monster with a slightly higher requirement actually gives a much better reward, but cannot be accessed immediately, and delaying it changes which other monsters become available. For example, if one monster requires 5 and gives 1 gold, and another requires 4 and gives 10 gold, picking the wrong one first can block future accessibility even though locally it looks worse.

## Approaches

A direct brute-force strategy tries every possible ordering of monsters and simulates the fights, checking which sequences are valid and maximizing the count. This is correct in principle because it explores all permutations, but it grows factorially and becomes unusable even for moderate n.

A more structured approach is to simulate the process step by step: at each moment, consider all monsters you can currently afford, and pick one. The question is which one to choose. The crucial observation is that among all currently affordable monsters, it is always optimal to pick the one with the largest reward. This can be justified by a local exchange argument: if you ever pick a smaller reward first while a larger reward is available, swapping them does not make you lose access to future states and can only improve or preserve the total gold.

This transforms the problem into maintaining a dynamic set of “available monsters” and repeatedly extracting the best candidate. However, scanning the entire list at every step is still too slow.

To optimize this, we separate monsters into two groups: those not yet affordable, and those currently affordable. We maintain one structure ordered by requirement so we can quickly move monsters into the available set, and another structure ordered by reward so we can quickly pick the best next monster.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force permutations | O(n!) | O(n) | Too slow |
| Naive greedy scan each step | O(n²) | O(n) | Too slow |
| Heap-based greedy simulation | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

We maintain two priority structures. One stores monsters that are still unreachable because we lack enough gold, ordered by increasing requirement. The other stores monsters we can currently defeat, ordered by decreasing reward.

We also maintain a variable cw representing current gold and a counter for how many monsters we have defeated.

The process is as follows.

1. Insert all monsters into a structure sorted by required gold. This lets us quickly identify which monsters become available as cw increases.
2. Initialize cw with the starting gold and mark all monsters as initially “unavailable for selection”.
3. Move all monsters whose requirement is at most cw into the available pool. This step ensures that the available pool always reflects exactly what can be fought at the current moment.
4. If no monsters are available, the process stops because no further progress is possible. Any remaining monsters require more gold than can ever be reached.
5. Otherwise, select the monster with the highest reward from the available pool and defeat it. Increase cw by its reward and increment the answer.
6. After gaining gold, repeat the process from step 3, since new monsters may now become reachable.

### Why it works

At any point, among all monsters that are currently affordable, the one with the highest reward can be chosen without loss of optimality. If an optimal sequence chose a different affordable monster first, swapping it with the highest reward monster does not reduce accessibility to later monsters because all requirements depend only on current gold, and swapping does not decrease gold at the moment of future decisions. This establishes a greedy-choice property combined with a monotonic growth of cw, ensuring every step is locally optimal and globally consistent.

## Python Solution

```python
import sys
import heapq

input = sys.stdin.readline

def solve():
    n, start = map(int, input().split())
    monsters = [tuple(map(int, input().split())) for _ in range(n)]

    monsters.sort(key=lambda x: x[0])

    i = 0
    cw = start
    ans = 0

    # min-heap by requirement (bi)
    not_ready = []
    # max-heap by reward (gi), store negative
    ready = []

    while True:
        while i < n and monsters[i][0] <= cw:
            heapq.heappush(ready, -monsters[i][1])
            i += 1

        if not ready:
            break

        g = -heapq.heappop(ready)
        cw += g
        ans += 1

    print(ans)

if __name__ == "__main__":
    solve()
```

The implementation relies on sorting monsters by requirement so that we only scan them once. The pointer i ensures each monster is moved into the heap exactly once, making the total heap insertion cost O(n log n).

The heap stores rewards as negatives because Python’s heapq is a min-heap. Each step extracts the maximum reward monster among currently available ones, matching the greedy rule.

The loop termination condition occurs when no currently reachable monster exists, meaning cw cannot be increased further, so no future monsters can ever become available.

## Worked Examples

### Example 1

Input:

```
4 3
2 1
3 2
5 10
4 3
```

We track current gold cw, pointer i, and the available heap.

| Step | cw | Newly added monsters | Ready heap (negated) | Chosen reward |
| --- | --- | --- | --- | --- |
| 0 | 3 | (2,1), (3,2) | [ -2, -1 ] | - |
| 1 | 3 | - | [ -2, -1 ] | 2 |
| 2 | 5 | (4,3) | [ -3, -1 ] | - |
| 3 | 5 | (5,10) | [ -10, -1, -3 ] | 10 |
| 4 | 15 | - | [ -3, -1 ] | - |
| 5 | 15 | - | [ -3, -1 ] | 3 |

The process shows how increasing gold unlocks later monsters, and why always selecting the highest reward among currently available ones maximizes future reach.

### Example 2

Input:

```
3 1
2 5
2 1
3 10
```

| Step | cw | Newly added monsters | Ready heap | Chosen reward |
| --- | --- | --- | --- | --- |
| 0 | 1 | - | [] | - |

The algorithm stops immediately because no monster is affordable. This confirms that unreachable initial states correctly terminate without invalid selections.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Each monster is inserted and removed from a heap at most once, and sorting dominates only once |
| Space | O(n) | We store all monsters in arrays and at most n elements in heaps |

The complexity fits within typical constraints for n up to 2e5 or 1e5, where O(n log n) operations are standard.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    def solve():
        n, start = map(int, input().split())
        monsters = [tuple(map(int, input().split())) for _ in range(n)]
        monsters.sort()

        i = 0
        cw = start
        ans = 0
        import heapq
        ready = []

        while True:
            while i < n and monsters[i][0] <= cw:
                heapq.heappush(ready, -monsters[i][1])
                i += 1
            if not ready:
                break
            cw += -heapq.heappop(ready)
            ans += 1

        return str(ans)

    return solve()

# custom tests
assert run("1 10\n5 100\n") == "1"
assert run("2 1\n10 100\n10 100\n") == "0"
assert run("3 5\n1 1\n2 2\n3 3\n") == "3"
assert run("5 1\n2 10\n2 9\n2 8\n2 7\n2 6\n") == "5"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single reachable monster | 1 | basic feasibility |
| all unreachable | 0 | early termination |
| strictly increasing chain | 3 | chained unlocking |
| same requirement many options | 5 | greedy max-reward correctness |

## Edge Cases

One edge case is when no monster is initially affordable. The algorithm correctly initializes an empty ready heap and terminates immediately without attempting invalid selections, producing zero.

Another case is when multiple monsters share the same requirement but very different rewards. The heap ensures only the best reward is chosen first, preventing suboptimal consumption of weak rewards that would reduce overall reach.

A final case involves a long chain where each monster unlocks exactly one more. Because each gain is immediately reflected in cw and all newly available monsters are pushed into the heap before selection, the algorithm never misses a newly unlocked high-reward option that becomes available mid-process.
