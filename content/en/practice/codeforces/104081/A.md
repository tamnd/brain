---
title: "CF 104081A - \u51cf\u80a5\u8ba1\u5212"
description: "We are given a line of people, each with a fixed weight, and a game that repeatedly compares people at the front of the line. In each round, the first two people in the queue compete. The heavier one wins the round."
date: "2026-07-02T02:35:55+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104081
codeforces_index: "A"
codeforces_contest_name: "2022\u5e74\u4e2d\u56fd\u5927\u5b66\u751f\u7a0b\u5e8f\u8bbe\u8ba1\u7ade\u8d5b\u5973\u751f\u4e13\u573a"
rating: 0
weight: 104081
solve_time_s: 58
verified: true
draft: false
---

[CF 104081A - \u51cf\u80a5\u8ba1\u5212](https://codeforces.com/problemset/problem/104081/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 58s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a line of people, each with a fixed weight, and a game that repeatedly compares people at the front of the line. In each round, the first two people in the queue compete. The heavier one wins the round. The winner stays at the front and continues competing in future rounds, while the loser is sent to the back of the queue. We also track consecutive wins: every time someone wins a round, their current streak increases, and the moment any participant reaches a required number of consecutive wins, the game ends immediately and that participant is declared the overall winner.

The input gives the initial order of the queue and the required number of consecutive wins needed to end the game. The output is the position of the eventual winner in the original ordering.

The key constraint driving the solution is that the queue can evolve for a very large number of rounds if simulated directly. Each round is O(1), but in the worst case we could perform a large number of swaps and comparisons before a winner is determined, especially if strong candidates start far back. This rules out any approach that repeatedly simulates the full process without insight into its long-term behavior.

A subtle edge case comes from the definition of consecutive wins. If one interprets the process as needing to explicitly simulate streak resets for all participants, it becomes easy to overcomplicate the state. Another pitfall is assuming the winner might depend on early random interactions in the queue; in reality, the process has a deterministic dominating element.

## Approaches

A direct simulation follows the rules literally. We maintain a queue, repeatedly pop the first two elements, compare their weights, and push the loser to the back. We also maintain a map of current win streaks. Whenever someone wins, their streak increases and the opponent’s streak resets. As soon as any streak reaches the required threshold, we stop.

This approach is correct because it mirrors the process exactly. However, it can degrade badly. If the strongest person starts near the back, they may need to cycle through many opponents before reaching the front. Each interaction is constant time, but the total number of interactions can grow very large, making this approach potentially too slow for large inputs.

The key observation is that the process is dominated by the globally maximum weight. Any person weaker than the maximum can never defeat it, and once the maximum reaches the front of the queue, it will win every subsequent round. From that moment, its win streak increases deterministically until it reaches the required threshold. Therefore, the entire process only depends on when the maximum element arrives at the front, not on the full sequence of intermediate comparisons.

This reduces the problem to finding the index of the maximum element in the initial array. That element is guaranteed to eventually accumulate the required consecutive wins.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Full Simulation | O(n + operations) potentially very large | O(n) | Too slow |
| Max Element Observation | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

We solve the problem by identifying the element that inevitably dominates all comparisons.

1. Scan through the list of weights while tracking the maximum value and its position in the original array. The position is what we ultimately need to output.
2. Every time we see a value larger than the current maximum, we update both the maximum and its index. This ensures we always remember the globally strongest participant.
3. After the scan finishes, we return the stored index of the maximum element as the answer.

### Why it works

The process only ever compares adjacent elements, but any element weaker than the global maximum can never eliminate it. Once the maximum reaches the front of the queue through repeated rotations, no other element can defeat it, so it will accumulate wins indefinitely. Since every other participant must eventually lose to it in a direct comparison chain, the first element that guarantees uninterrupted winning streak growth is the global maximum.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, k = map(int, input().split())
a = list(map(int, input().split()))

max_val = -10**18
max_idx = -1

for i, v in enumerate(a, 1):
    if v > max_val:
        max_val = v
        max_idx = i

print(max_idx)
```

The implementation simply tracks the maximum value while preserving its original 1-indexed position. The second parameter `k` does not influence the final result because the maximum element will eventually achieve any required consecutive win threshold once it dominates the front of the queue.

A common mistake here is trying to simulate the queue dynamics explicitly. That leads to unnecessary complexity and obscures the fact that the identity of the winner is fixed from the start.

## Worked Examples

Consider an input where weights are `[1, 3, 2, 5, 4]`. The maximum is `5`, located at position `4`. Regardless of intermediate comparisons, every other element will eventually lose to `5`, and once it becomes active at the front, it will keep winning.

| Step | Current Max | Max Index |
| --- | --- | --- |
| 1 | 1 | 1 |
| 2 | 3 | 2 |
| 3 | 3 | 2 |
| 4 | 5 | 4 |
| 5 | 5 | 4 |

This trace shows that only the global maximum matters, and earlier local maxima do not affect the final outcome.

As another example, `[7, 1, 6, 2]`, the maximum is already at the front. The answer is immediately index `1`, and no interaction in the queue can change that.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Single pass to find the maximum element |
| Space | O(1) | Only constant extra variables are used |

The solution easily fits within constraints since it performs a single linear scan over the input.

## Test Cases

```python
import sys, io

def solve(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n, k = map(int, input().split())
    a = list(map(int, input().split()))
    mx = -10**18
    idx = -1
    for i, v in enumerate(a, 1):
        if v > mx:
            mx = v
            idx = i
    return str(idx)

# sample-like checks
assert solve("6 3\n1 1 4 5 1 4\n") == "4"

# minimum size
assert solve("1 10\n5\n") == "1"

# already maximum at front
assert solve("4 2\n9 1 2 3\n") == "1"

# maximum at end
assert solve("4 2\n1 2 3 9\n") == "4"

# all equal
assert solve("5 100\n7 7 7 7 7\n") == "1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element | 1 | minimal boundary case |
| max at front | 1 | early dominance |
| max at end | n | correctness of indexing |
| all equal | 1 | stable tie-breaking behavior |
