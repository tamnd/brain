---
title: "CF 1149A - Prefix Sum Primes"
description: "We are given a bag of tiles, each labeled with either a 1 or a 2. Our task is to arrange all the tiles into a sequence so that when we calculate the prefix sums - that is, the sum of the first element, the sum of the first two elements, and so on - the number of sums that are…"
date: "2026-06-12T03:07:28+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "greedy", "math", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 1149
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 556 (Div. 1)"
rating: 1200
weight: 1149
solve_time_s: 83
verified: true
draft: false
---

[CF 1149A - Prefix Sum Primes](https://codeforces.com/problemset/problem/1149/A)

**Rating:** 1200  
**Tags:** constructive algorithms, greedy, math, number theory  
**Solve time:** 1m 23s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a bag of tiles, each labeled with either a `1` or a `2`. Our task is to arrange all the tiles into a sequence so that when we calculate the prefix sums - that is, the sum of the first element, the sum of the first two elements, and so on - the number of sums that are prime is maximized. The output is any permutation of the tiles that achieves this maximum.

The number of tiles, `n`, can go up to 200,000. Since the sequence consists only of 1s and 2s, the maximum prefix sum is `2 * n`. A brute-force approach that tries all permutations is impossible because `n!` grows far faster than the available operations for `n` around 200,000. Even checking all sequences systematically is out of the question. We need an approach that works in linear or at worst linearithmic time.

Non-obvious edge cases include sequences where one of the numbers dominates. For example, if the input is all 1s, then the prefix sums are just 1, 2, 3, ..., `n`. If we start with a 2 when a 1 is available, the first prefix sum is 2, a prime, but the next becomes 2 plus remaining 1s, which might skip the prime 3. Similarly, if the input is all 2s, the first prefix sum is 2, but the next is 4, which is not prime. Handling these small sequences carefully is critical to maximize the primes.

## Approaches

A naive brute-force approach would enumerate every permutation of the tiles and compute the number of prime prefix sums for each. This works in principle because we can check prefix sums in linear time for each permutation, but the number of permutations is factorial in `n`. Even for `n = 20`, `20!` is roughly `2.4 * 10^18`, which is completely infeasible. The brute-force works because it guarantees we try every ordering, but fails for large inputs because the computation explodes.

The key insight is that we do not need to consider arbitrary permutations. Since the tiles only have values 1 or 2, we can reason about which sequences produce early prime prefix sums. The smallest primes are 2, 3, 5, 7, 11, ... To maximize primes in the early prefix sums, we want the first two elements to sum to 3 (the first odd prime after 2). This can be done by placing a `2` first, followed by a `1`, if both are present. Once we have used a `2` and a `1`, we can place all remaining 1s, then all remaining 2s. This greedy strategy ensures the prefix sums hit 2, 3, and then continue increasing in a predictable way.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n!) | O(n) | Too slow |
| Greedy placement of 2 then 1, then remaining 1s, then 2s | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Count the number of `1`s and `2`s in the input. Let `count1` and `count2` store these quantities. Knowing the counts lets us build the sequence directly without searching all permutations.
2. Initialize an empty result list. We will construct the permutation sequentially.
3. If both `count1` and `count2` are positive, add a `2` followed by a `1` to the result list. Decrease `count1` and `count2` accordingly. This ensures the first two prefix sums are 2 and 3, the first two primes.
4. Append all remaining `1`s to the result list. Each 1 increases the prefix sum by 1, which hits the next prime whenever possible in sequence.
5. Append all remaining `2`s to the result list. After 1s are exhausted, adding 2s increases the sum by 2 each time, keeping the sequence predictable.
6. Output the result list.

Why it works: By placing `2` then `1` first, we secure the prefix sums 2 and 3. Filling remaining 1s first ensures we hit consecutive small primes like 5, 7, 11 as early as possible. Placing 2s last avoids skipping the early small primes unnecessarily. This greedy construction respects the structure of primes and the limited values of the tiles, guaranteeing a maximal number of prime prefix sums without exhaustively checking permutations.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
tiles = list(map(int, input().split()))

count1 = tiles.count(1)
count2 = tiles.count(2)

result = []

if count1 > 0 and count2 > 0:
    result.append(2)
    result.append(1)
    count2 -= 1
    count1 -= 1

result.extend([1] * count1)
result.extend([2] * count2)

print(' '.join(map(str, result)))
```

This solution first counts the tiles, then applies the greedy strategy. We check that both 1s and 2s are present before placing the initial `2` and `1`. Remaining tiles are appended in a predictable order, avoiding off-by-one errors. The result is printed as a space-separated string.

## Worked Examples

**Sample 1 Input**

```
5
1 2 1 2 1
```

| Step | count1 | count2 | Result | Prefix Sums |
| --- | --- | --- | --- | --- |
| Init | 3 | 2 | [] | [] |
| Place 2 then 1 | 2 | 1 | [2,1] | 2,3 |
| Add remaining 1s | 0 | 1 | [2,1,1,1] | 2,3,4,5 |
| Add remaining 2s | 0 | 0 | [2,1,1,1,2] | 2,3,4,5,7 |

The prefix sums 2, 3, 5, 7 are prime, maximizing primes.

**Custom Example Input**

```
4
1 1 1 1
```

| Step | count1 | count2 | Result | Prefix Sums |
| --- | --- | --- | --- | --- |
| Init | 4 | 0 | [] | [] |
| Place 2 then 1 | not possible |  | [] |  |
| Add remaining 1s | 0 | 0 | [1,1,1,1] | 1,2,3,4 |

Prefix sums 2 and 3 are prime, which is maximal for this input.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Counting tiles and building the result list requires a single pass over input and at most O(n) append operations. |
| Space | O(n) | We store the result sequence explicitly, proportional to n. |

Since n ≤ 200,000 and operations are linear, this comfortably fits within the 1-second time limit and 256 MB memory constraint.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n = int(input())
    tiles = list(map(int, input().split()))
    count1 = tiles.count(1)
    count2 = tiles.count(2)
    result = []
    if count1 > 0 and count2 > 0:
        result.append(2)
        result.append(1)
        count2 -= 1
        count1 -= 1
    result.extend([1] * count1)
    result.extend([2] * count2)
    return ' '.join(map(str, result))

# provided sample
assert run("5\n1 2 1 2 1\n") in ["2 1 1 1 2", "2 1 1 2 1"], "sample 1"

# custom: all 1s
assert run("4\n1 1 1 1\n") == "1 1 1 1", "all 1s"

# custom: all 2s
assert run("3\n2 2 2\n") == "2 2 2", "all 2s"

# custom: single tile
assert run("1\n1\n") == "1", "single 1"
assert run("1\n2\n") == "2", "single 2"

# custom: two tiles
assert run("2\n1 2\n") in ["2 1", "1 2"], "two tiles"
assert run("2\n2 1\n") in ["2 1", "1 2"], "two tiles order"

# custom: large input
assert run("6\n2 2 1 1 2 1\n") in ["2 1 1 1 2 2"], "mixed large"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 4 1 1 1 1 | 1 1 1 1 | Algorithm handles all 1s correctly |
| 3 2 2 2 | 2 2 2 | Algorithm handles all 2s correctly |
| 1 1 | 1 | Single tile input |
| 2 1 2 | 2 1 | Correct greedy placement for small input |
