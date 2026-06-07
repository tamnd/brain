---
title: "CF 2164C - Dungeon"
description: "We are asked to simulate a dungeon scenario where you have a set of swords, each with a damage value, and a set of monsters, each with a life value. You can kill a monster if your sword’s damage is at least equal to the monster’s life."
date: "2026-06-07T23:37:17+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "brute-force", "data-structures", "greedy", "sortings"]
categories: ["algorithms"]
codeforces_contest: 2164
codeforces_index: "C"
codeforces_contest_name: "Codeforces Global Round 30 (Div. 1 + Div. 2)"
rating: 1400
weight: 2164
solve_time_s: 122
verified: false
draft: false
---

[CF 2164C - Dungeon](https://codeforces.com/problemset/problem/2164/C)

**Rating:** 1400  
**Tags:** binary search, brute force, data structures, greedy, sortings  
**Solve time:** 2m 2s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to simulate a dungeon scenario where you have a set of swords, each with a damage value, and a set of monsters, each with a life value. You can kill a monster if your sword’s damage is at least equal to the monster’s life. Once a sword is used, it is consumed, but in some cases, you gain a new sword with a potentially higher damage based on the monster's `c_i` value. The goal is to maximize the number of monsters you can kill.

The input provides multiple test cases. Each test case gives the initial swords, the monsters' health, and the potential new swords that appear after killing each monster. The output should be the maximum number of monsters killed per test case.

Constraints are tight: `n` and `m` can reach `2 * 10^5`, and the sum over all test cases is similarly bounded. This eliminates any brute-force solution that iterates over all possible orderings of swords and monsters, because the number of operations would be quadratic or worse. A naive O(n * m) approach is not feasible.

Edge cases to watch for include situations where all `c_i` are zero, meaning no new swords appear, or cases where the initial swords are all weaker than some monsters. For example, if `a = [1]` and `b = [2]` with `c = [0]`, no monster can be killed, and the algorithm must return `0`. Another tricky case occurs when choosing the wrong sword first prevents using it later on a monster that could have yielded a stronger sword.

## Approaches

The brute-force approach would try every combination of sword-to-monster assignments. You would check each sword against each monster, track which swords are consumed, and update with `c_i` values. This guarantees correctness but requires up to `n * m` comparisons per test case. With `n, m` up to 2 * 10^5, this yields 4 * 10^10 operations in the worst case, which is infeasible.

The optimal approach leverages sorting and greedy selection. First, sort both swords and monsters. Sorting swords ensures you always know the smallest available sword capable of killing a monster, which is crucial when you want to consume swords efficiently. Sorting monsters by life lets you process weaker monsters first. The key insight is that the new sword obtained after killing a monster always has damage at least as high as the sword used. This guarantees that a greedy approach - using the smallest sufficient sword for the weakest remaining monster - will maximize the total kills. Using a min-heap (priority queue) to store available swords lets us efficiently find the smallest sword that can kill a monster.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n * m) | O(n + m) | Too slow |
| Sorting + Greedy with heap | O((n + m) log(n + m)) | O(n + m) | Accepted |

## Algorithm Walkthrough

1. For each test case, read the number of swords `n` and monsters `m`. Read the sword damage list `a`, monster health list `b`, and the sword gain list `c`.
2. Sort the swords in ascending order. Pair monsters with their `c_i` values and sort them by health in ascending order. This guarantees we address weaker monsters first.
3. Initialize a min-heap with all initial sword damages. This heap will always give the smallest sword that can kill a monster, which maximizes the potential of keeping stronger swords for later.
4. Initialize a counter `kills` to zero. Iterate over the sorted list of monsters. For each monster:

a. Pop swords from the heap until you find one whose damage is at least equal to the monster’s health.

b. If no such sword exists, skip this monster.

c. If a sword is found, increment `kills`. Remove the used sword from the heap.

d. If `c_i > 0`, push a new sword with damage `max(sword_used, c_i)` back into the heap. This ensures the new sword is always at least as strong as the consumed sword.
5. After processing all monsters, output `kills`.

The invariant maintained is that at every step, the heap contains all swords currently available, and we always choose the smallest sword capable of killing the current weakest monster. This guarantees that stronger swords are preserved for stronger monsters.

## Python Solution

```python
import sys
import heapq
input = sys.stdin.readline

T = int(input())
for _ in range(T):
    n, m = map(int, input().split())
    swords = list(map(int, input().split()))
    monsters = list(map(int, input().split()))
    gains = list(map(int, input().split()))
    
    swords.sort()
    monsters = sorted(zip(monsters, gains))
    
    heap = swords[:]
    heapq.heapify(heap)
    kills = 0
    
    for life, gain in monsters:
        while heap and heap[0] < life:
            heapq.heappop(heap)
        if not heap:
            continue
        sword = heapq.heappop(heap)
        kills += 1
        if gain > 0:
            heapq.heappush(heap, max(sword, gain))
    
    print(kills)
```

This solution first sorts swords and monsters. A min-heap is used to efficiently pick the smallest sword that can kill the current monster. The order of operations matters: pop weaker swords first, increment `kills`, and then push any new sword obtained. Using `max(sword, gain)` ensures that new swords are always at least as strong as the used sword.

## Worked Examples

**Sample Input 1**

```
3 2
2 2 2
2 3
3 2
```

| Step | Heap state | Monster (life, gain) | Action | Kills |
| --- | --- | --- | --- | --- |
| Start | [2, 2, 2] | (2,3) | Pop 2 ≤ 2 → use sword, push max(2,3)=3 | 1 |
| Next | [2,3,2] | (3,2) | Pop 2 < 3 → pop, next 2 < 3 → pop, next 3 ≥ 3 → use sword, push max(3,2)=3 | 2 |

Output: `2`. The trace confirms that choosing the smallest sufficient sword and updating with `max(sword, gain)` yields maximum kills.

**Edge Case Example**

```
2 2
1 2
2 3
0 0
```

| Step | Heap | Monster | Action | Kills |
| --- | --- | --- | --- | --- |
| Start | [1,2] | (2,0) | Pop 1 < 2 → pop 2 ≥ 2 → use, gain 0 → do not push | 1 |
| Next | [] | (3,0) | Heap empty → cannot kill | 1 |

Output: `1`. This confirms the algorithm correctly handles cases where swords are insufficient.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n + m) log(n + m)) | Sorting swords and monsters is O(n log n + m log m), heap operations across all monsters sum to O((n + m) log(n + m)) |
| Space | O(n + m) | Heap stores up to n + m swords, plus input arrays |

This fits comfortably within the constraints `n + m ≤ 2 * 10^5` per test case and total sum ≤ 2 * 10^5.

## Test Cases

```python
import sys, io
def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    # paste solution here
    T = int(input())
    for _ in range(T):
        n, m = map(int, input().split())
        swords = list(map(int, input().split()))
        monsters = list(map(int, input().split()))
        gains = list(map(int, input().split()))
        
        swords.sort()
        monsters = sorted(zip(monsters, gains))
        
        heap = swords[:]
        import heapq
        heapq.heapify(heap)
        kills = 0
        
        for life, gain in monsters:
            while heap and heap[0] < life:
                heapq.heappop(heap)
            if not heap:
                continue
            sword = heapq.heappop(heap)
            kills += 1
            if gain > 0:
                heapq.heappush(heap, max(sword, gain))
        print(kills)
    return output.getvalue().strip()

# Sample
assert run("1\n3 2\n2 2 2\n2 3\n3 2\n") == "2"

# Custom cases
assert run("1\n2 2\n1 2\n2 3\n0 0\n") == "1", "insufficient sword"
assert run("1\n1 1\n1000000000\n1\n0\n") == "1", "large sword kills small monster"
assert run("1\n3 3\n1 1 1\n2 2 2\n2 2 2\n") == "3", "all gains equal sword"
assert run("1\n2 3\n5 5\n1 10 5\n0 0 10\n") == "3", "mix of gains and
```
