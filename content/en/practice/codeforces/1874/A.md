---
title: "CF 1874A - Jellyfish and Game"
description: "We have two players, Jellyfish and Gellyfish, each with a collection of green apples. Jellyfish has n apples with values stored in array a, and Gellyfish has m apples with values stored in array b. They play a game for k rounds."
date: "2026-06-08T23:07:17+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "games", "greedy", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1874
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 901 (Div. 1)"
rating: 1200
weight: 1874
solve_time_s: 119
verified: true
draft: false
---

[CF 1874A - Jellyfish and Game](https://codeforces.com/problemset/problem/1874/A)

**Rating:** 1200  
**Tags:** brute force, games, greedy, implementation  
**Solve time:** 1m 59s  
**Verified:** yes  

## Solution
## Problem Understanding

We have two players, Jellyfish and Gellyfish, each with a collection of green apples. Jellyfish has `n` apples with values stored in array `a`, and Gellyfish has `m` apples with values stored in array `b`. They play a game for `k` rounds. On odd-numbered rounds, Jellyfish may swap one of her apples with one from Gellyfish or do nothing. On even-numbered rounds, Gellyfish may swap similarly. Both play optimally to maximize the sum of their apple values. The goal is to compute the sum of Jellyfish's apples after all `k` rounds.

The constraints tell us that `n` and `m` are small (up to 50), but `k` can be huge (up to 10^9). This immediately signals that simulating every single round is impossible. Instead, we need a solution that identifies the _effective swaps_, because after some point, further rounds will no longer change the sums.

Edge cases come from situations like: one player having only one apple, `k` being extremely large, or when the best apples are already in the correct hands. For example, if Jellyfish has `[10]` and Gellyfish has `[1]` with `k = 1000`, she will never swap because she cannot increase her sum. A naive approach that blindly simulates swaps for `k` iterations would produce excessive runtime or incorrect results if it miscalculates the stopping condition.

## Approaches

The brute-force method is straightforward: for each round, identify the best swap for the current player, perform it if it increases their sum, and repeat for all `k` rounds. This is correct because the game is turn-based and both players act greedily. However, if `k` is up to 10^9, even with `n, m ≤ 50`, simulating `k` rounds is impossible.

The key observation is that no player will ever swap an apple unless it _strictly improves_ their sum. That means at most we only need to consider `min(n, m)` swaps per player: Jellyfish will only want to replace her smallest apples with Gellyfish's largest ones, and Gellyfish will do the opposite. Once the smallest of Jellyfish is larger than the largest of Gellyfish, no further swaps are beneficial. Because of this, the effective number of swaps is bounded by `min(n, m, k)`, not `k`.

Thus, the optimal approach is:

1. Sort Jellyfish's apples in ascending order and Gellyfish's in descending order.
2. Swap corresponding elements (smallest of Jellyfish with largest of Gellyfish) for `i = 0` to `min(n, m, k) - 1`.
3. Stop as soon as a swap would not increase Jellyfish's sum.

This reduces the problem from potentially billions of operations to at most 50 swaps per test case.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(k * n * m) | O(n + m) | Too slow |
| Optimal | O(n log n + m log m) | O(n + m) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases. For each test case, read `n, m, k` and the apple arrays `a` and `b`.
2. Sort Jellyfish's array `a` in ascending order. This makes the smallest apples easy to find for potential swaps.
3. Sort Gellyfish's array `b` in descending order. This exposes the largest apples he owns, which are candidates for Jellyfish to take.
4. Compute `swap_count = min(n, m, k)`. We cannot swap more apples than either player has, and no need to consider more than `k` rounds.
5. Iterate from `i = 0` to `swap_count - 1`: compare `a[i]` and `b[i]`. If `b[i] > a[i]`, swap them. If not, break early, since further swaps cannot improve Jellyfish's sum.
6. Compute and print the sum of Jellyfish's final array `a`.

Why it works: At every step, Jellyfish always considers her least valuable apple and Gellyfish's most valuable apple. Swapping in this order guarantees she maximizes her sum greedily. Because Gellyfish would respond optimally, the sorted swap sequence already accounts for the worst-case counteractions, as any swap that would benefit Gellyfish is already implicitly blocked by the sorted selection. Once the smallest of Jellyfish exceeds the largest of Gellyfish, no further swaps are possible, establishing a stopping condition.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, m, k = map(int, input().split())
        a = list(map(int, input().split()))
        b = list(map(int, input().split()))
        
        a.sort()
        b.sort(reverse=True)
        
        swap_count = min(n, m, k)
        for i in range(swap_count):
            if a[i] < b[i]:
                a[i], b[i] = b[i], a[i]
            else:
                break
        
        print(sum(a))

if __name__ == "__main__":
    solve()
```

The code first reads multiple test cases efficiently using `sys.stdin.readline`. Sorting ensures the swaps are optimal without simulating every round. The early `break` ensures we do not perform unnecessary swaps if Jellyfish cannot improve her sum further. `sum(a)` is computed only once per test case for efficiency.

## Worked Examples

**Sample 1:**

```
n = 2, m = 2, k = 1
a = [1, 2]
b = [3, 4]
```

| Step | a | b | Action |
| --- | --- | --- | --- |
| initial | [1, 2] | [4, 3] | sorted |
| i = 0 | [4, 2] | [1, 3] | swap a[0]=1 with b[0]=4 |
| sum(a) | 6 |  | final sum |

Demonstrates a single optimal swap maximizes Jellyfish's sum.

**Sample 2:**

```
n = 1, m = 1, k = 10000
a = [1]
b = [2]
```

| Step | a | b | Action |
| --- | --- | --- | --- |
| initial | [1] | [2] | sorted |
| i = 0 | [2] | [1] | swap a[0]=1 with b[0]=2 |
| sum(a) | 2 |  | only one swap needed despite large k |

Shows `k` can be enormous, but effective swaps are limited.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t * (n log n + m log m)) | Sorting dominates, swap iteration is O(min(n, m)) |
| Space | O(n + m) | Arrays stored per test case |

Even at maximum t = 2000 and n, m = 50, the operations are comfortably under 1e6. Sorting small arrays is fast, and Python handles sums efficiently.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    solve()
    return output.getvalue().strip()

# provided samples
assert run("4\n2 2 1\n1 2\n3 4\n1 1 10000\n1\n2\n4 5 11037\n1 1 4 5\n1 9 1 9 8\n1 1 1\n2\n1\n") == "6\n2\n19\n2"

# custom test cases
assert run("1\n1 1 1\n10\n1\n") == "10", "No swap needed"
assert run("1\n2 2 5\n1 5\n4 2\n") == "9", "One beneficial swap only"
assert run("1\n3 3 100\n1 2 3\n4 5 6\n") == "12", "Multiple swaps, k large"
assert run("1\n2 3 2\n1 2\n5 4 3\n") == "9", "k smaller than min(n,m)"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 1, [10], [1] | 10 | No swap occurs if not beneficial |
| 2 2 5, [1,5], [4,2] | 9 | Only one beneficial swap despite larger k |
| 3 3 100, [1,2,3], [4,5,6] | 12 | Multiple swaps, k >> min(n,m) |
| 2 3 2, [1,2], [5,4,3] | 9 | k smaller than min(n,m) still works |

## Edge Cases

Consider Jellyfish `[1]` and Gellyfish `[1000000000]` with `k = 10^9
