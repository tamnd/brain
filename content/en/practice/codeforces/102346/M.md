---
title: "CF 102346M - Maratona Brasileira de Popcorn"
description: "We have an array of N popcorn bags, where P[i] is the amount of popcorn in bag i. There are C competitors, and every competitor can eat at most T popcorn per second. The bags must be divided into contiguous segments."
date: "2026-08-13T01:55:30+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102346
codeforces_index: "M"
codeforces_contest_name: "2019-2020 ACM-ICPC Brazil Subregional Programming Contest"
rating: 0
weight: 102346
solve_time_s: 499
verified: true
draft: false
---

[CF 102346M - Maratona Brasileira de Popcorn](https://codeforces.com/problemset/problem/102346/M)

**Rating:** -  
**Tags:** -  
**Solve time:** 8m 19s  
**Verified:** yes  

## Solution
## Problem Understanding

We have an array of `N` popcorn bags, where `P[i]` is the amount of popcorn in bag `i`. There are `C` competitors, and every competitor can eat at most `T` popcorn per second.

The bags must be divided into contiguous segments. A competitor receives one segment, and a competitor may receive an empty segment, so using fewer than `C` nonempty segments is allowed. Since a bag cannot be split between competitors, each segment's total popcorn must be eaten by one competitor. All competitors work simultaneously, so the total competition time is determined by the slowest competitor.

For a segment containing `S` popcorn, its eating time is `ceil(S / T)`. We need to choose the contiguous partition that minimizes the largest such time and output that minimum number of seconds.

The array can contain up to `10^5` bags. Each bag contains at most `10^4` popcorn, so the total amount can reach `10^9`. A quadratic algorithm already performs around `10^10` operations in the worst case, which is far beyond what is reasonable. We need something close to linear or `O(N log N)`. The number of competitors can also be as large as `10^5`, so an approach depending quadratically on `C` is unsuitable.

There are several boundary cases that can expose an incorrect implementation. If there is only one bag, such as

```
1 3 4
5
```

the answer is `2`, because one competitor needs `ceil(5 / 4) = 2` seconds. A careless partition-based solution might incorrectly try to distribute the single bag among several competitors, which is forbidden because a bag must belong entirely to one competitor.

Another case is when there are more competitors than bags:

```
2 5 3
4 7
```

The answer is `3`. The two bags can be assigned to two competitors and the other three competitors simply do nothing. Treating the number of competitors as exactly the number of required nonempty groups would reject this valid arrangement.

A third edge case occurs when one bag is larger than every other possible group:

```
3 2 1
1 1 5
```

The answer is `5`. The bag containing `5` popcorn already requires five seconds, regardless of how the other bags are distributed. Any algorithm that only balances the total amount, without respecting individual bag sizes, can incorrectly predict a smaller answer.

Finally, rounding must happen after computing a competitor's total. For

```
2 2 4
5 5
```

each competitor needs `ceil(5 / 4) = 2` seconds, so the answer is `2`, not `ceil(10 / (2 * 4)) = 2` by coincidence. In other cases the distinction matters, so the solution should reason about an integer time limit directly rather than averaging popcorn across competitors.

## Approaches

A direct brute-force solution considers every possible way to place boundaries between consecutive bags. There are `N - 1` possible boundaries, and each can either be selected or not, giving `2^(N-1)` different partitions. For each partition we can calculate the total popcorn assigned to every competitor and keep the largest required eating time. Taking the minimum over all partitions is correct because every legal contiguous assignment corresponds to exactly one such set of boundaries.

The problem is the number of partitions. When `N = 10^5`, the number of possibilities is `2^99999`, which is astronomically large. Even if evaluating each partition took only constant time, the search would already be impossible. With a straightforward `O(N)` evaluation per partition, the worst-case work is `O(N * 2^N)`. This approach is useful only for tiny arrays and gives us the definition of the optimum, not a practical algorithm.

The useful observation is that we do not actually need to construct the optimal partition immediately. Instead, suppose we guess that the entire competition must finish within `X` seconds. In that case, every competitor can eat at most `X * T` popcorn. The question becomes much simpler: can the array be divided into at most `C` contiguous groups, each having sum at most `X * T`?

For a fixed capacity, there is a greedy way to answer that question. Scan the array from left to right and keep adding bags to the current competitor while the capacity is not exceeded. When the next bag would make the sum too large, start a new competitor. Because all popcorn amounts are positive, putting more bags into the current segment can never reduce the amount of competitors needed later. Thus the greedy partition uses the minimum possible number of segments for that capacity.

Feasibility is also monotonic. If `X` seconds are enough, then any larger number of seconds is enough as well, because every competitor gets a larger capacity. If `X` seconds are impossible, every smaller value is impossible. That monotonic property allows binary search over the answer.

We can binary search between `1` second and `ceil(sum(P) / T)` seconds. For each candidate time, we multiply it by `T` to obtain the maximum popcorn one competitor may handle and run the greedy feasibility check. The resulting complexity is `O(N log(sum(P) / T))`, which is easily fast enough for `N = 10^5`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `O(N * 2^N)` | `O(N)` | Too slow |
| Binary Search + Greedy | `O(N log(sum(P) / T))` | `O(N)` | Accepted |

## Algorithm Walkthrough

1. Read `N`, `C`, `T` and the array of popcorn amounts. Compute the total popcorn as well, because it gives us an upper bound for the answer.
2. Set the binary-search lower bound to `1` second and the upper bound to `ceil(sum(P) / T)` seconds. The upper bound corresponds to giving all bags to one competitor. Even though there may be `C` competitors, having only one nonempty competitor is allowed.
3. For a candidate time `mid`, compute the capacity of one competitor as `mid * T`. We now ask whether all bags can be assigned to at most `C` contiguous groups whose sums do not exceed this capacity.
4. Scan the array from left to right. Maintain the amount of popcorn assigned to the current competitor. If adding the next bag stays within the capacity, keep it in the current segment. If it exceeds the capacity, start a new segment with that bag and increment the number of competitors used.
5. If any individual bag is larger than the capacity, the candidate time is immediately impossible. Otherwise, after scanning the entire array, the candidate is feasible exactly when the number of required nonempty segments is at most `C`.
6. If the candidate is feasible, search the lower half because the answer may be smaller. If it is not feasible, search the upper half because more time is necessary.
7. Continue until the binary-search interval contains one value. That value is the minimum number of seconds for which a valid partition exists.

### Why it works

For any fixed capacity, the greedy scan creates a segment as large as possible before starting the next one. Consider the first segment of any valid partition. Since all bag amounts are positive, extending that first segment with another bag while staying within capacity cannot make the remaining suffix harder to partition than leaving that bag for the next competitor. Repeating this argument means the greedy method minimizes the number of segments required for the entire array.

Thus the feasibility check is correct. The predicate "can finish within `X` seconds" is monotonic because increasing `X` only increases every competitor's capacity. Binary search therefore finds the smallest feasible `X`, which is exactly the optimal competition time.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, c, t = map(int, input().split())
    p = list(map(int, input().split()))

    total = sum(p)

    def feasible(seconds):
        capacity = seconds * t
        competitors = 1
        current = 0

        for x in p:
            if x > capacity:
                return False

            if current + x <= capacity:
                current += x
            else:
                competitors += 1
                current = x

                if competitors > c:
                    return False

        return True

    lo = 1
    hi = (total + t - 1) // t

    while lo < hi:
        mid = (lo + hi) // 2

        if feasible(mid):
            hi = mid
        else:
            lo = mid + 1

    print(lo)

if __name__ == "__main__":
    solve()
```

The `feasible` function implements the greedy partition from the algorithm. `capacity` is the maximum amount one competitor can eat during the candidate number of seconds. The variable `current` stores the popcorn assigned to the current competitor, while `competitors` counts how many nonempty segments have been created.

The test `x > capacity` is necessary because no partition can split a bag. Even if there are many unused competitors, a single bag larger than the candidate capacity cannot be assigned legally.

When `current + x` exceeds the capacity, the current segment is closed and a new one begins with `x`. There is no reason to move an earlier bag to the new competitor, because that would only make the first segment smaller and cannot decrease the number of segments required by the remaining suffix.

The upper bound uses integer ceiling division, `(total + t - 1) // t`. The value represents the time needed if one competitor ate all popcorn. It is always a valid upper bound because unused competitors are permitted.

The binary search uses `lo < hi`, so when the loop ends both bounds represent the same smallest feasible time. Python integers have arbitrary precision, so multiplication such as `seconds * t` cannot overflow.

## Worked Examples

### Sample 1

The input is

```
5 3 4
5 8 3 10 7
```

For three competitors and four popcorn per second, consider a candidate of `4` seconds. Each competitor can eat at most `16` popcorn.

The greedy scan behaves as follows.

| Bag | Current segment sum | Competitors used | Decision |
| --- | --- | --- | --- |
| 5 | 5 | 1 | Add to current segment |
| 8 | 13 | 1 | Add to current segment |
| 3 | 16 | 1 | Add to current segment |
| 10 | 10 | 2 | Start new segment |
| 7 | 7 | 3 | Start new segment |

Three competitors are enough, so `4` seconds is feasible.

Now consider `3` seconds. The capacity becomes `12`.

| Bag | Current segment sum | Competitors used | Decision |
| --- | --- | --- | --- |
| 5 | 5 | 1 | Add to current segment |
| 8 | 8 | 2 | Start new segment |
| 3 | 11 | 2 | Add to current segment |
| 10 | 10 | 3 | Start new segment |
| 7 | 7 | 4 | Start new segment |

Four competitors would be required, so `3` seconds is impossible. Binary search consequently returns `4`.

This trace also shows why the answer is not obtained by simply dividing the total popcorn among the competitors. The contiguous restriction forces the array into groups, and the group containing `8 + 3` or the isolated `10` affects the maximum time.

### Sample 2

The input is

```
3 2 1
1 5 1
```

With two competitors and one popcorn per second, test `5` seconds. The capacity is `5`.

| Bag | Current segment sum | Competitors used | Decision |
| --- | --- | --- | --- |
| 1 | 1 | 1 | Add to current segment |
| 5 | 5 | 2 | Start new segment |
| 1 | 1 | 3 | Start new segment |

Three competitors are required, so `5` seconds is not feasible.

Test `6` seconds. The capacity is `6`.

| Bag | Current segment sum | Competitors used | Decision |
| --- | --- | --- | --- |
| 1 | 1 | 1 | Add to current segment |
| 5 | 6 | 1 | Add to current segment |
| 1 | 1 | 2 | Start new segment |

Only two competitors are needed, so `6` seconds is feasible. The answer is `6`.

This example demonstrates why a large middle bag can force an unfavorable partition. The best split is `[1, 5] | [1]`, whose largest group contains six popcorn.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(N log(sum(P) / T))` | Each feasibility check scans all `N` bags, and binary search performs logarithmically many checks |
| Space | `O(N)` | The array of popcorn amounts is stored in memory |

The total popcorn is at most `10^5 * 10^4 = 10^9`, so the binary search has only about thirty iterations. Each iteration performs a linear scan over at most `10^5` bags, giving roughly a few million simple operations. This is comfortably within the intended range for the constraints.

## Test Cases

```python
import sys
import io

def solve():
    input = sys.stdin.readline

    n, c, t = map(int, input().split())
    p = list(map(int, input().split()))

    total = sum(p)

    def feasible(seconds):
        capacity = seconds * t
        competitors = 1
        current = 0

        for x in p:
            if x > capacity:
                return False

            if current + x <= capacity:
                current += x
            else:
                competitors += 1
                current = x

                if competitors > c:
                    return False

        return True

    lo = 1
    hi = (total + t - 1) // t

    while lo < hi:
        mid = (lo + hi) // 2
        if feasible(mid):
            hi = mid
        else:
            lo = mid + 1

    print(lo)

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    try:
        sys.stdin = io.StringIO(inp)
        sys.stdout = io.StringIO()
        solve()
        return sys.stdout.getvalue().strip()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

assert run("""5 3 4
5 8 3 10 7
""") == "4", "sample 1"

assert run("""3 2 1
1 5 1
""") == "6", "sample 2"

assert run("""3 2 1
1 1 5
""") == "5", "sample 3"

assert run("""1 1 1
1
""") == "1", "minimum-size input"

assert run("""1 5 4
5
""") == "2", "one bag with unused competitors"

assert run("""4 4 10
7 7 7 7
""") == "1", "one competitor per equal bag"

assert run("""5 2 1
1 1 1 1 1
""") == "3", "contiguous partition boundary"

assert run("""100000 100000 50
""" + " ".join(["10000"] * 100000) + "\n") == "200", "maximum-size input"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `5 3 4 / 5 8 3 10 7` | `4` | Provided sample and general partitioning |
| `3 2 1 / 1 5 1` | `6` | Large middle bag and contiguous grouping |
| `3 2 1 / 1 1 5` | `5` | A dominant bag determines the answer |
| `1 1 1 / 1` | `1` | Minimum-size input |
| `1 5 4 / 5` | `2` | More competitors than bags |
| `4 4 10 / 7 7 7 7` | `1` | Equal values and enough competitors |
| `5 2 1 / 1 1 1 1 1` | `3` | Contiguous partition and boundary handling |
| `100000 100000 50 / 10000 ...` | `200` | Maximum `N` and large values |

The maximum-size test contains `100000` bags, each with `10000` popcorn. Since there are also `100000` competitors, every bag can be assigned to its own competitor. Each bag takes `ceil(10000 / 50) = 200` seconds, so the expected answer is `200`.

## Edge Cases

### A single bag

Consider

```
1 3 4
5
```

The binary search eventually tests `2` seconds, giving capacity `8`. The only bag fits, and the greedy check uses one competitor, which is at most three. The result is `2`.

The algorithm never attempts to split the bag across competitors. The entire bag is processed by the same greedy segment, which directly respects the indivisibility rule.

### More competitors than bags

Consider

```
2 5 3
4 7
```

The total popcorn is `11`, giving an upper bound of `4` seconds. At `3` seconds, each competitor can handle `9` popcorn. The greedy partition is `[4] | [7]`, requiring two competitors. Since `2 <= 5`, the candidate is feasible and the answer is `3`.

The check deliberately uses `competitors <= C` rather than `competitors == C`. Empty competitors are legal, so requiring exactly five nonempty segments would incorrectly reject this case.

### A bag larger than the candidate capacity

Consider

```
3 2 1
1 1 5
```

For `4` seconds, the capacity is `4`. When the greedy scan reaches the final bag containing `5`, the condition `x > capacity` immediately makes the candidate infeasible. No rearrangement can help because the bags must remain in order and the bag itself cannot be divided.

At `5` seconds the capacity becomes `5`. The greedy partition is `[1, 1] | [5]`, requiring exactly two competitors, so `5` is feasible and is the minimum.

### Contiguous grouping matters

Consider

```
5 2 1
1 1 1 1 1
```

With two competitors, three seconds are sufficient because the array can be split as `[1, 1, 1] | [1, 1]`. The largest segment contains three popcorn, so the answer is `3`.

Two seconds would require both competitors to handle exactly two popcorn, leaving one bag unassigned. A non-contiguous assignment might appear to balance the
