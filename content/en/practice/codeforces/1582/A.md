---
title: "CF 1582A - Luntik and Concerts"
description: "We are given a collection of songs split into three types: some last 1 minute, some last 2 minutes, and some last 3 minutes. For each test case, we must assign every song to one of two concerts."
date: "2026-06-14T22:58:53+07:00"
tags: ["codeforces", "competitive-programming", "math"]
categories: ["algorithms"]
codeforces_contest: 1582
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 750 (Div. 2)"
rating: 800
weight: 1582
solve_time_s: 263
verified: true
draft: false
---

[CF 1582A - Luntik and Concerts](https://codeforces.com/problemset/problem/1582/A)

**Rating:** 800  
**Tags:** math  
**Solve time:** 4m 23s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a collection of songs split into three types: some last 1 minute, some last 2 minutes, and some last 3 minutes. For each test case, we must assign every song to one of two concerts. Each song must be used exactly once, and each concert’s duration is simply the sum of durations of the songs assigned to it.

The goal is to split the songs so that the absolute difference between the total durations of the two concerts is as small as possible.

If we think in terms of structure, the problem is really about partitioning a multiset of numbers consisting of many 1s, 2s, and 3s into two groups with balanced sums.

The constraints are large, with each of a, b, and c up to 10^9 and up to 1000 test cases. That immediately rules out any approach that tries to explicitly construct or simulate assignments for individual songs. Any method must work in constant time per test case.

A common subtle edge case appears when the total sum is very small or when one type dominates. For example, if we have only one song type, say a = 1, b = 0, c = 0, then the best we can do is put it entirely in one concert, giving difference 1. Any greedy “pairing” idea must still handle the leftover correctly when perfect pairing is not possible.

Another important edge case is when mixing different song lengths allows exact balancing. For example, one 3-minute song can balance a 1 and a 2-minute song exactly, so local greedy matching matters.

## Approaches

A naive approach would attempt to assign each song one by one into the lighter of the two concerts. This greedy simulation would require iterating over all a + b + c songs, which can be as large as 3 × 10^9 in the worst case. This is completely infeasible.

Another brute-force interpretation is to treat this as a partition problem and try all subsets of songs. That is exponential in the number of songs and immediately impossible.

The key observation is that only the counts of each type matter, not individual songs. We are effectively choosing how many 1s, 2s, and 3s go into the first concert; the rest go to the second. This reduces the problem to balancing two linear combinations of three variables.

The total sum is fixed. If we denote it by S, then minimizing the absolute difference between two subsets is equivalent to finding a subset whose sum is as close as possible to S/2.

The crucial structure is that we are not free to choose arbitrary subset sums; we can only form sums using limited coins of value 1, 2, and 3 with large multiplicities. This makes the reachable sums dense enough that the optimal solution can be characterized by a simple greedy balancing rule.

We try to construct one concert greedily toward half of the total sum. We first use as many large songs as possible (3-minute), then adjust with 2-minute songs, and finally fix the remaining gap using 1-minute songs. Because the values are small and structured, this greedy construction always yields the best achievable balance.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^(a+b+c)) | O(1) | Too slow |
| Greedy balancing | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

We compute the total duration S = a + 2b + 3c, then aim to build a first concert sum as close as possible to S/2.

1. Compute S = a + 2b + 3c. This is the total duration of all songs combined, and any valid partition must split this sum into two parts.
2. Set the target T = S // 2. We want to make one subset as close as possible to this target without exceeding feasibility constraints.
3. Try to use as many 3-minute songs as possible in the first concert, but no more than c and no more than T // 3. This is optimal because 3-minute songs contribute the most per item, so they reduce the gap fastest.
4. Subtract the contribution of chosen 3-minute songs from the remaining target. Then move to 2-minute songs and take as many as possible without exceeding the updated target. The reason is the same: we are greedily filling the remaining gap using the largest available unit.
5. Finally, fill the remaining gap using 1-minute songs, limited by a. At this point, every remaining unit must be 1-minute songs, so we simply take min(a, remaining gap).
6. Let X be the constructed sum of the first concert. The second concert is S − X, so the answer is |S − 2X|.

The reason this works is that the structure of reachable sums is contiguous enough that locally optimal choices at each step do not block any better global arrangement. Since we always pick the largest possible contribution without exceeding the target, we never waste high-value items on small gaps that could be filled by smaller items.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        a, b, c = map(int, input().split())
        
        S = a + 2*b + 3*c
        target = S // 2
        
        take3 = min(c, target // 3)
        target -= 3 * take3
        
        take2 = min(b, target // 2)
        target -= 2 * take2
        
        take1 = min(a, target)
        target -= take1
        
        X = 3 * take3 + 2 * take2 + take1
        print(abs(S - 2 * X))

if __name__ == "__main__":
    solve()
```

The code computes the total sum and then greedily constructs the closest achievable subset sum to half of it. The subtraction steps ensure we never exceed the target. The final formula converts the constructed subset into the absolute difference between two partitions.

The only subtle detail is that we do not need to explicitly track the second concert. Once we know one side, the other is determined.

## Worked Examples

### Example 1

Input:

```
1
1 1 1
```

Total sum S = 6, target = 3.

| Step | 3-min used | 2-min used | 1-min used | Current sum |
| --- | --- | --- | --- | --- |
| Start | 0 | 0 | 0 | 0 |
| Use 3-min | 1 | 0 | 0 | 3 |
| Use 2-min | 1 | 0 | 0 | 3 |
| Use 1-min | 1 | 0 | 0 | 3 |

Answer = |6 − 2×3| = 0.

This confirms perfect balancing is possible when a 1-minute and a 2-minute song together match a 3-minute song.

### Example 2

Input:

```
2
2 1 3
```

Total sum S = 2 + 2 + 9 = 13, target = 6.

| Step | 3-min used | 2-min used | 1-min used | Current sum |
| --- | --- | --- | --- | --- |
| Start | 0 | 0 | 0 | 0 |
| Use 3-min | 2 | 0 | 0 | 6 |
| Use 2-min | 2 | 0 | 0 | 6 |
| Use 1-min | 2 | 0 | 0 | 6 |

Answer = |13 − 12| = 1.

This shows that when exact balance is impossible, the greedy construction still achieves the closest reachable sum to half.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) per test case | Only a constant number of arithmetic operations are performed |
| Space | O(1) | No additional storage beyond a few integers |

The solution is easily fast enough for up to 1000 test cases, since each test case is handled in constant time.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    t = int(input())
    out = []
    for _ in range(t):
        a, b, c = map(int, input().split())
        S = a + 2*b + 3*c
        target = S // 2

        take3 = min(c, target // 3)
        target -= 3 * take3

        take2 = min(b, target // 2)
        target -= 2 * take2

        take1 = min(a, target)
        target -= take1

        X = 3 * take3 + 2 * take2 + take1
        out.append(str(abs(S - 2 * X)))

    return "\n".join(out)

assert run("4\n1 1 1\n2 1 3\n5 5 5\n1 1 2\n") == "0\n1\n0\n1"
assert run("1\n1 0 0\n") == "1"
assert run("1\n0 0 1\n") == "1"
assert run("1\n10 10 10\n") in {"0", "1"}
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 0 0 | 1 | Single smallest non-zero imbalance |
| 0 0 1 | 1 | Single 3-minute song split case |
| 10 10 10 | 0 or 1 | Large balanced symmetric case |

## Edge Cases

When only one type of song exists, such as only 1-minute songs, the greedy construction simply takes half of them implicitly through the min(a, target) step. For example, with a = 5, b = 0, c = 0, total is 5 and target is 2. The algorithm takes 2 ones, leaving 3 in the other concert, and correctly returns a difference of 1.

When one large song dominates, such as c being large and a = b = 0, the algorithm takes floor(c/2) of them into one side as it fills toward S/2. For example, c = 3 gives total 9, target 4. The algorithm takes one 3-minute song, leaving target 1, which cannot be filled, leading to a final difference of 3, matching the unavoidable imbalance.

When perfect cancellation exists, such as (1, 1, 1), the greedy matching ensures 1 + 2 cancels with 3 exactly because 3-minute songs are used first to anchor the target, and smaller songs fill the remaining gap without overshooting, producing exact equality.
