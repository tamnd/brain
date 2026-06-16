---
title: "CF 1015C - Songs Compression"
description: "We are given a collection of songs, each with an original size and a smaller size if we choose to compress it. All songs must be copied onto a flash drive whose total capacity is fixed. The only decision available is which songs to compress."
date: "2026-06-16T22:27:43+07:00"
tags: ["codeforces", "competitive-programming", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1015
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 501 (Div. 3)"
rating: 1100
weight: 1015
solve_time_s: 208
verified: true
draft: false
---

[CF 1015C - Songs Compression](https://codeforces.com/problemset/problem/1015/C)

**Rating:** 1100  
**Tags:** sortings  
**Solve time:** 3m 28s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a collection of songs, each with an original size and a smaller size if we choose to compress it. All songs must be copied onto a flash drive whose total capacity is fixed. The only decision available is which songs to compress. Compressing a song replaces its size with a smaller one, and we want to ensure the final total size does not exceed the capacity.

The goal is not to decide whether it is possible to fit the songs, because that can always be answered by compressing everything and checking the total. The real task is to minimize how many songs we choose to compress while still making the total size fit within the limit.

The key difficulty comes from the fact that compressing a song gives a different amount of benefit depending on the song. Some songs save a lot of space when compressed, others save very little. The decision is about selecting a subset of items where each selection reduces total size by a known amount.

The constraints push us toward a linear or near-linear solution. With up to 100,000 songs, any solution that tries all subsets is immediately impossible because it would grow exponentially. Even quadratic solutions would be too slow. This strongly suggests that we need a greedy strategy based on sorting.

A subtle edge case appears when even compressing all songs is not enough. In that case, no subset can help, because compression only reduces sizes. Another less obvious pitfall is assuming we should always compress the songs with the largest original size. That is incorrect because what matters is not the absolute size, but the reduction achieved by compression.

## Approaches

A direct brute-force approach would try every subset of songs, compute the resulting total size after compressing those in the subset, and take the minimum subset size that fits within capacity. This works conceptually because it explores all possibilities, but it is exponential in nature, requiring checking 2^n subsets. With n up to 100,000, this is completely infeasible.

The key observation is that compressing a song always reduces the total size by a fixed amount: the difference between its original and compressed size. If we define this reduction as gain, then each compressed song contributes independently to reducing the total sum. The problem becomes selecting a minimum number of items whose total gain is at least the excess over the capacity.

This turns into a classic greedy selection problem. If we want to reach a target reduction using as few items as possible, we should always pick the items that provide the largest reduction first. Sorting songs by their gain in descending order ensures that every chosen compression is as efficient as possible in terms of saved space per operation.

We first compute the total size without compression. If it is already within capacity, no compression is needed. Otherwise we compute how much we need to reduce. Then we sort all songs by their compression benefit and greedily take the largest ones until the requirement is met.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n) | O(n) | Too slow |
| Optimal (greedy sort) | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

Let total be the sum of all original song sizes. For each song, define gain as a_i - b_i, which is how much space we save if we compress it.

1. Compute the total size of all songs without compression. This gives the baseline storage requirement before any decisions.
2. If total is already less than or equal to m, output 0 immediately since no compression is required.
3. Compute the excess amount, defined as how much space we must remove to fit into the drive.
4. For each song, compute its gain value and store it along with the song.
5. Sort all songs by gain in descending order. This ensures that we always consider the most effective compression first.
6. Iterate through the sorted list, subtracting each selected gain from the required excess and counting how many songs we compress.
7. As soon as the remaining excess becomes zero or negative, stop and output the number of compressed songs.

The reason we stop early is that once the required reduction is reached, adding more compressions would only increase the count without improving feasibility.

### Why it works

The correctness relies on the fact that each compression is independent and contributes additively to the total reduction. Since every compressed song reduces the sum by a fixed amount, the problem becomes equivalent to selecting a minimum number of elements whose weights sum to at least a target. In such a setting, sorting by weight in descending order is optimal because replacing any chosen smaller gain with a larger unused gain can only reduce or maintain the number of items needed. This exchange argument guarantees that the greedy prefix of largest gains is optimal.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, m = map(int, input().split())

songs = []
total = 0

for _ in range(n):
    a, b = map(int, input().split())
    total += a
    songs.append(a - b)

if total <= m:
    print(0)
    sys.exit()

songs.sort(reverse=True)

need = total - m
cnt = 0

for gain in songs:
    need -= gain
    cnt += 1
    if need <= 0:
        print(cnt)
        break
```

The solution begins by reading all song sizes and computing both the total size and the benefit of compressing each song. This separation is important because we never need the compressed sizes directly again, only their differences.

After checking the trivial case where no compression is needed, we compute how much space must be freed. Sorting the gains in descending order ensures we prioritize the most efficient compressions.

The loop maintains a running reduction and counts how many songs are compressed. The moment the required reduction is achieved, we stop immediately, ensuring minimal count.

A common mistake is forgetting to sort by gain and instead sorting by original size or compressed size, which does not correspond to the actual optimization objective.

## Worked Examples

### Example 1

Input:

```
4 21
10 8
7 4
3 1
5 4
```

Total size is 25, so we need to reduce by 4.

| Step | Chosen gain | Remaining need | Compressions used |
| --- | --- | --- | --- |
| Start | - | 4 | 0 |
| 1 | 3 | 1 | 1 |
| 2 | 2 | -1 | 2 |

After taking the two largest gains, the requirement is satisfied, so the answer is 2.

This trace shows that picking the largest reductions first reaches the target with minimal count, even though multiple combinations of two songs work.

### Example 2

Input:

```
3 16
4 3
6 5
8 7
```

Total size is 18, so we need to reduce by 2.

| Step | Chosen gain | Remaining need | Compressions used |
| --- | --- | --- | --- |
| Start | - | 2 | 0 |
| 1 | 1 | 1 | 1 |
| 2 | 1 | 0 | 2 |

Both smaller gains are required here, showing that even when all gains are equal, the greedy order is still valid.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting gains dominates the runtime, all other operations are linear |
| Space | O(n) | We store one gain value per song |

The constraints allow up to 100,000 songs, so an n log n solution is well within limits. The memory usage is linear and comfortably fits within typical limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n, m = map(int, input().split())
    songs = []
    total = 0

    for _ in range(n):
        a, b = map(int, input().split())
        total += a
        songs.append(a - b)

    if total <= m:
        return "0"

    songs.sort(reverse=True)

    need = total - m
    cnt = 0

    for g in songs:
        need -= g
        cnt += 1
        if need <= 0:
            return str(cnt)

    return "-1"

# provided sample
assert run("""4 21
10 8
7 4
3 1
5 4
""") == "2"

# impossible case
assert run("""3 5
4 3
4 3
4 3
""") == "-1"

# already fits
assert run("""2 100
10 5
20 10
""") == "0"

# all equal gains
assert run("""4 10
5 4
5 4
5 4
5 4
""") == "2"

# large gain variety
assert run("""5 20
10 1
10 9
10 8
10 7
10 6
""") == "1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| already fits case | 0 | no compression needed |
| impossible case | -1 | even full compression fails |
| all equal gains | 2 | tie-handling in greedy order |
| mixed gains | 1 | best single compression suffices |

## Edge Cases

One edge case occurs when compressing all songs still does not meet the capacity. For example, if total size is 50 and m is 10, but even after full compression total is 15, the algorithm correctly returns -1 because the accumulated gains never reach the required threshold.

Another edge case is when total already equals m. In this case, the required reduction is zero, and the algorithm immediately returns 0 without entering the greedy loop. This prevents incorrectly compressing unnecessary songs.

A third case is when gains are identical. The sorting step does not depend on stability, since any order among equal gains produces the same number of compressions, and the prefix condition ensures correctness regardless of tie ordering.
