---
title: "CF 253A - Boys and Girls"
description: "We are asked to arrange a sequence consisting of two kinds of objects, boys and girls, into a single line. The only freedom we have is the order."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "greedy"]
categories: ["algorithms"]
codeforces_contest: 253
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 154 (Div. 2)"
rating: 1100
weight: 253
solve_time_s: 67
verified: true
draft: false
---

[CF 253A - Boys and Girls](https://codeforces.com/problemset/problem/253/A)

**Rating:** 1100  
**Tags:** greedy  
**Solve time:** 1m 7s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to arrange a sequence consisting of two kinds of objects, boys and girls, into a single line. The only freedom we have is the order. The quality of an arrangement is measured by how often adjacent positions contain different genders, so how many times a boy sits next to a girl.

The goal is to construct any valid ordering that makes these “alternating boundaries” as frequent as possible, while respecting that we must use exactly all given boys and girls.

The input gives two small integers, the number of boys and the number of girls. The output is a single string of that total length, composed of two symbols representing the two genders.

The constraints are small, with both counts at most 100. That immediately rules out any need for heavy optimization. Even a solution that tries all permutations would be far too slow, since the total number of arrangements grows factorially and becomes enormous even for moderate sizes like 10 or 15. Anything beyond linear or near-linear behavior is sufficient here.

The main subtlety is that a greedy idea might feel plausible but still needs justification: when one group is much larger than the other, forcing alternation is impossible beyond a point. A naive alternating construction like strict “BGBGBG...” breaks when one side runs out, and different ways of finishing the leftover characters can affect correctness if done inconsistently. Another potential mistake is starting with the wrong gender when counts differ significantly, which can reduce the number of alternating adjacencies.

For example, if we have 1 boy and 5 girls, a careless alternating attempt like starting with boy produces “BGBGGG”, which quickly exhausts boys and then collapses into a long block of girls. Starting with the larger group “GBGGGG” achieves the same or better alternation count and avoids unnecessary early failure of alternation.

So the real task is deciding how to interleave two multisets to maximize adjacency changes.

## Approaches

A brute-force approach would try every possible permutation of the multiset containing n copies of one character and m of the other, compute the number of adjacent mismatches for each, and keep the best. This is correct because it evaluates all configurations directly. However, the number of permutations is $\frac{(n+m)!}{n!m!}$, which is already huge even for moderate inputs. For n = m = 100, this value is astronomically large, making enumeration completely infeasible.

The key observation is that the only way to create a mismatch between adjacent positions is to place different characters next to each other. To maximize this, we want to alternate as long as both types are available. The best possible structure is therefore a sequence that alternates until one type runs out, after which the remainder must form a single block. The only remaining decision is whether we start with the more frequent or less frequent character.

Starting with the majority character is optimal because it delays exhaustion of that character, which is the limiting resource. If we start with the minority character, we may run out of it earlier in a way that creates unnecessary same-character adjacency at the boundary.

So the optimal construction is greedy: always place the currently more frequent remaining character if it helps maintain alternation, but in practice this simplifies to starting with the larger count and alternating until one side is exhausted.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O((n+m)!) | O(n+m) | Too slow |
| Optimal Greedy | O(n+m) | O(n+m) | Accepted |

## Algorithm Walkthrough

We build the string step by step, always trying to keep adjacent characters different for as long as possible.

1. Identify which group is larger at the start. We compare the number of boys and girls, because the larger group should generally dominate the starting position. This choice prevents early exhaustion of the smaller group from breaking alternation prematurely.
2. Initialize two counters representing remaining boys and girls. We also decide the starting character as the one with higher count. This choice maximizes how long we can alternate without being forced into repetition.
3. Repeatedly append characters while both counts are positive. At each step, we append the character different from the last appended one, but only if that character still has remaining quota. If the preferred alternating choice is unavailable, we are forced to use the remaining type.
4. Once one of the counts becomes zero, append all remaining characters of the other type. At this stage, no further alternation is possible, so we accept a single block of identical characters.

The construction ensures that we alternate whenever possible, which directly corresponds to creating a mismatch between adjacent positions.

### Why it works

At every step where both types are available, placing two identical characters next to each other can never improve the answer, because it consumes flexibility without increasing future alternation opportunities. As long as both counters are positive, there always exists a choice that keeps adjacency alternating. Once one counter hits zero, no further alternation is structurally possible, so the remaining segment cannot be improved by rearrangement. This makes the greedy decision locally optimal at every step and globally optimal for the entire sequence.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    
    # 'B' for boys, 'G' for girls
    if n >= m:
        b, g = n, m
        first, second = 'B', 'G'
    else:
        b, g = m, n
        first, second = 'G', 'B'
    
    res = []
    
    turn = first  # start with majority
    
    while b > 0 or g > 0:
        if turn == first:
            if b > 0:
                res.append(first)
                b -= 1
            else:
                res.append(second)
                g -= 1
        else:
            if g > 0:
                res.append(second)
                g -= 1
            else:
                res.append(first)
                b -= 1
        
        # try to alternate next
        if turn == first:
            turn = second
        else:
            turn = first
    
    print("".join(res))

if __name__ == "__main__":
    solve()
```

The implementation mirrors the greedy process directly. We first normalize which character is treated as “majority” to simplify the logic. The variable `turn` represents what we ideally want to place next to maintain alternation. If that character is unavailable, we automatically fall back to the other.

A subtle point is that we never explicitly count alternating pairs. Instead, the construction guarantees maximal alternation structurally, so no scoring is required. The loop runs exactly n + m iterations, so there is no hidden inefficiency.

## Worked Examples

### Example 1

Input: `3 3`

We treat either side as majority since counts are equal, assume we start with `B`.

| Step | Remaining B | Remaining G | Turn | Output |
| --- | --- | --- | --- | --- |
| 1 | 2 | 3 | B | B |
| 2 | 2 | 2 | G | BG |
| 3 | 1 | 2 | B | BGB |
| 4 | 1 | 1 | G | BGBG |
| 5 | 0 | 1 | B | BGBGB |
| 6 | 0 | 0 | G | BGBGBG |

This trace shows that alternation is maintained fully until both sides are exhausted, which is the ideal scenario.

### Example 2

Input: `1 4`

We treat girls as majority, so start with G.

| Step | Remaining B | Remaining G | Turn | Output |
| --- | --- | --- | --- | --- |
| 1 | 1 | 3 | G | G |
| 2 | 1 | 2 | B | GB |
| 3 | 0 | 2 | G | GBG |
| 4 | 0 | 1 | B | GBGG |
| 5 | 0 | 0 | G | GBGGG |

Here alternation continues only until the single boy is consumed. After that, only girls remain, forming a final block. Any other ordering would create the same unavoidable non-alternating suffix, but starting with the majority minimizes disruption earlier.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m) | Each character is appended exactly once |
| Space | O(n + m) | Output string storage |

The bounds n, m ≤ 100 make this trivial in terms of performance. Even if the limits were much larger, the same linear construction would still be optimal.

## Test Cases

```python
import sys, io

def solve():
    n, m = map(int, input().split())
    
    if n >= m:
        b, g = n, m
        first, second = 'B', 'G'
    else:
        b, g = m, n
        first, second = 'G', 'B'
    
    res = []
    turn = first
    
    while b > 0 or g > 0:
        if turn == first:
            if b > 0:
                res.append(first)
                b -= 1
            else:
                res.append(second)
                g -= 1
        else:
            if g > 0:
                res.append(second)
                g -= 1
            else:
                res.append(first)
                b -= 1
        
        turn = second if turn == first else first
    
    print("".join(res))

def run(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    
    solve()
    
    out = sys.stdout.getvalue().strip()
    sys.stdin = old_stdin
    sys.stdout = old_stdout
    return out

# provided samples
assert run("3 3") in ["GBGBGB", "BGBGBG"], "sample 1"

# custom cases
assert run("1 1") in ["BG", "GB"], "minimum balanced"
assert run("1 4") == "GBGGG", "unbalanced small"
assert run("4 1") == "BGBBB", "symmetric unbalanced"
assert run("2 2") in ["BGBG", "GBGB"], "even split"
assert len(run("100 100")) == 200, "max size length check"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 | BG or GB | minimal alternating structure |
| 1 4 | GBGGG | handling majority overflow |
| 4 1 | BGBBB | symmetric imbalance |
| 2 2 | BGBG or GBGB | perfect alternation |
| 100 100 | length 200 string | performance and bounds |

## Edge Cases

When one side differs by exactly one, such as `2 1`, the algorithm alternates as long as possible and then appends the remaining character. For `2 1`, starting with the larger side yields a sequence like `BGB`, which already achieves the maximum possible two alternating boundaries.

When one side is much larger, such as `1 5`, the first step creates a single alternation, and everything after becomes a block. The algorithm correctly ensures that the single minority element is not wasted in the middle in a way that could reduce early alternation opportunities.

When counts are equal, either starting choice is valid. The implementation may produce either alternating pattern, and both achieve the maximum possible number of transitions because no imbalance forces early collapse.
