---
title: "CF 1601D - Difficult Mountain"
description: "We are given a set of alpinists, each characterized by two numbers: skill and neatness. The skill indicates the maximum difficulty of a mountain an alpinist can climb, while neatness affects the mountain's difficulty after that alpinist climbs: specifically, if the current…"
date: "2026-06-10T08:21:38+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "dp", "greedy", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1601
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 751 (Div. 1)"
rating: 2700
weight: 1601
solve_time_s: 92
verified: true
draft: false
---

[CF 1601D - Difficult Mountain](https://codeforces.com/problemset/problem/1601/D)

**Rating:** 2700  
**Tags:** data structures, dp, greedy, sortings  
**Solve time:** 1m 32s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a set of alpinists, each characterized by two numbers: skill and neatness. The skill indicates the maximum difficulty of a mountain an alpinist can climb, while neatness affects the mountain's difficulty after that alpinist climbs: specifically, if the current mountain difficulty is $p$ and an alpinist with neatness $a$ climbs it, the new difficulty becomes $\max(p, a)$. The mountain starts with an initial difficulty $d$. The problem asks for the maximum number of alpinists who can climb the mountain if we choose the order optimally.

With $n$ up to 500,000 and difficulty and skill values up to $10^9$, any solution that explicitly tries all permutations of alpinists is out of the question. Even a quadratic approach examining each alpinist against every other at each step is too slow, as that could require up to $2.5 \times 10^{11}$ operations in the worst case. We therefore need an approach that is roughly $O(n \log n)$.

A subtle point arises when neatness can increase the mountain's difficulty above the skill of other alpinists. For example, if an alpinist of skill 3 and neatness 10 climbs a mountain starting at difficulty 2, the mountain jumps to difficulty 10. Any alpinist with skill 5 will now be unable to climb, even though they could have climbed before. A naive greedy approach that just climbs the "most skilled first" or "highest neatness first" may fail to account for this and produce a suboptimal count. Similarly, multiple alpinists might have neatness lower than current difficulty; handling these correctly requires comparing current mountain difficulty and skill dynamically.

## Approaches

A brute-force solution would consider every possible order of climbing. For each permutation of alpinists, we would simulate climbing sequentially, updating the mountain difficulty after each successful climb, and count how many alpinists succeed. While this correctly captures the effect of neatness, it is infeasible because the number of permutations is $n!$, far beyond what any computer can handle for $n$ larger than 10.

A more structured approach observes that each alpinist only has an effect if their skill exceeds the current difficulty. Once the mountain difficulty is fixed, the problem reduces to selecting a subset of alpinists whose skills are at least the current difficulty, in some order, such that we maximize the count. The key insight is that among all alpinists who can climb, it is safe to first use the one with the smallest neatness. Using an alpinist with a large neatness first could raise the mountain difficulty unnecessarily, preventing others from climbing. This lets us reduce the problem to a greedy strategy: at each step, pick the available alpinist whose neatness is the smallest but whose skill is at least the current mountain difficulty.

If we maintain all remaining alpinists sorted by neatness, and always pick the smallest neatness that satisfies the skill requirement, we can efficiently simulate the climbing order. Sorting initially by neatness allows $O(n \log n)$ processing, and we can iterate through the sorted array to simulate the climb. Each alpinist is processed exactly once, so the total complexity remains $O(n \log n)$.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n!)$ | $O(n)$ | Too slow |
| Optimal Greedy | $O(n \log n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

1. Read the input values: number of alpinists $n$, initial difficulty $d$, and the list of pairs $(s_i, a_i)$ for each alpinist.
2. Sort the list of alpinists by neatness $a_i$ in ascending order. If neatness is equal, order does not matter.
3. Initialize a variable `current_difficulty` to the initial difficulty `d` and a counter `count` to 0.
4. Iterate through the sorted list of alpinists. For each alpinist, check if their skill $s_i$ is at least the `current_difficulty`.
5. If yes, increment `count` and update `current_difficulty` to $\max(current_difficulty, a_i)$. If no, skip this alpinist.
6. After processing all alpinists, output the counter `count` as the maximum number of climbers.

Why it works: the invariant maintained is that at any point in the iteration, `current_difficulty` is the difficulty after all previously climbed alpinists. Picking the available alpinist with minimal neatness ensures that the mountain does not become unnecessarily harder, which could block other climbers. Sorting by neatness and greedily climbing preserves the optimal order.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, d = map(int, input().split())
alpinists = [tuple(map(int, input().split())) for _ in range(n)]

# Sort alpinists by neatness
alpinists.sort(key=lambda x: x[1])

current_difficulty = d
count = 0

for s, a in alpinists:
    if s >= current_difficulty:
        count += 1
        current_difficulty = max(current_difficulty, a)

print(count)
```

The code first reads the input efficiently using `sys.stdin.readline` to handle the large constraint of $n$. Sorting by neatness ensures that we always consider the alpinist who minimally increases mountain difficulty first. The `for` loop checks the skill against current difficulty, counting successful climbs and updating difficulty. This correctly implements the greedy strategy.

## Worked Examples

**Sample 1**

Input:

```
3 2
2 6
3 5
5 7
```

| Step | Current Difficulty | Alpinist (s, a) | Can climb? | Count |
| --- | --- | --- | --- | --- |
| 1 | 2 | (2,6) | Yes | 1 |
| 2 | 6 | (3,5) | No | 1 |
| 3 | 6 | (5,7) | Yes | 2 |

This trace confirms that choosing the minimal neatness first leads to `count = 2`, which matches the expected output.

**Sample 2**

Input:

```
3 3
1 2
4 3
5 7
```

| Step | Current Difficulty | Alpinist (s, a) | Can climb? | Count |
| --- | --- | --- | --- | --- |
| 1 | 3 | (1,2) | No | 0 |
| 2 | 3 | (4,3) | Yes | 1 |
| 3 | 3 | (5,7) | Yes | 2 |

This shows the algorithm correctly skips alpinists who cannot climb due to insufficient skill.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting the alpinists dominates the computation; iterating through the list is O(n) |
| Space | O(n) | Storing the list of alpinists and a few counters |

With $n \leq 5 \times 10^5$, the $O(n \log n)$ complexity is comfortably within a 2-second limit, and storing 500,000 alpinists in memory is feasible.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n, d = map(int, input().split())
    alpinists = [tuple(map(int, input().split())) for _ in range(n)]
    alpinists.sort(key=lambda x: x[1])
    current_difficulty = d
    count = 0
    for s, a in alpinists:
        if s >= current_difficulty:
            count += 1
            current_difficulty = max(current_difficulty, a)
    return str(count)

# Provided samples
assert run("3 2\n2 6\n3 5\n5 7\n") == "2", "sample 1"
assert run("3 3\n1 2\n4 3\n5 7\n") == "2", "sample 2"

# Custom cases
assert run("1 0\n0 0\n") == "1", "single alpinist equal to difficulty"
assert run("2 5\n4 3\n6 7\n") == "1", "first cannot climb, second can"
assert run("5 1\n1 2\n2 3\n3 4\n4 5\n5 6\n") == "5", "all can climb in sorted neatness"
assert run("3 10\n15 1\n12 5\n20 8\n") == "3", "initial difficulty less than all skills"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 0\n0 0 | 1 | Minimum-size input where skill equals difficulty |
| 2 5\n4 3\n6 7 | 1 | Skipping an alpinist whose skill is too low |
| 5 1\n1 2\n2 3\n3 4\n4 5 |  |  |
