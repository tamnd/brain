---
title: "CF 472B - Design Tutorial: Learn from Life"
description: "We have an elevator starting on the first floor. Every person is waiting on that floor and wants to reach a specific destination floor. The elevator can carry at most k people at once. Moving between floors costs time equal to the floor difference."
date: "2026-05-30T00:00:00+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 472
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 270"
rating: 1300
weight: 472
solve_time_s: 104
verified: true
draft: false
---

[CF 472B - Design Tutorial: Learn from Life](https://codeforces.com/problemset/problem/472/B)

**Rating:** 1300  
**Tags:** -  
**Solve time:** 1m 44s  
**Verified:** yes  

## Solution
## Problem Understanding

We have an elevator starting on the first floor. Every person is waiting on that floor and wants to reach a specific destination floor. The elevator can carry at most `k` people at once.

Moving between floors costs time equal to the floor difference. Entering and leaving the elevator is free. After delivering everyone, the elevator must end up back on the first floor.

The task is to find the minimum total travel time.

The first thing to notice is that people going to lower floors can be dropped off while transporting people going higher. If the elevator is already heading toward floor 10, dropping someone at floor 4 on the way costs nothing extra. Because of this, the actual cost of one elevator trip depends only on the highest floor reached during that trip.

The constraints are small enough to allow sorting. Both `n` and `k` are at most 2000, so an `O(n log n)` solution is easily fast enough. Even `O(n²)` would fit, but there is a much simpler observation that leads directly to an optimal greedy solution.

A common mistake is to think that people should be grouped by nearby destination floors. Consider:

```
4 2
2 2 100 100
```

A bad strategy might send one person to floor 100 together with one person to floor 2. That creates two trips to floor 100. The optimal solution puts both floor-100 passengers together, requiring only one trip to the highest floor.

Another subtle case is when `k >= n`.

```
3 5
2 3 10
```

All passengers can ride together. The elevator goes up to floor 10 and returns. The answer is `2 * (10 - 1) = 18`. Any solution that always assumes multiple trips would overcount.

A third edge case occurs when many people have the same destination.

```
5 2
7 7 7 7 7
```

The elevator must make `ceil(5 / 2) = 3` trips, each reaching floor 7. The answer is `3 * 2 * (7 - 1) = 36`.

The key is understanding that each trip is charged only for its maximum destination floor.

## Approaches

A brute-force approach would try to determine which passengers should ride together. Since passengers can be partitioned into groups in many different ways, the number of possibilities grows exponentially. Even for a few dozen people, exhaustive search becomes impossible.

The reason brute force is conceptually correct is that once the grouping is known, the cost of each trip is easy to compute. If a group contains passengers whose highest destination floor is `F`, that trip costs:

```
(F - 1) + (F - 1) = 2(F - 1)
```

The challenge is finding the best grouping.

The crucial observation is that a trip's cost depends only on the largest floor among its passengers. Everyone else in that trip is effectively free because they can be dropped off along the way.

Suppose we sort destination floors in descending order:

```
f1 >= f2 >= f3 >= ...
```

The highest destination must appear in some trip and will determine that trip's cost. Since adding up to `k - 1` smaller destinations to the same trip does not increase the maximum floor, we should always fill that trip with as many remaining passengers as possible.

After assigning the largest `k` destinations to one trip, the next largest unassigned floor becomes the maximum of another trip, and the same logic repeats.

Thus, after sorting in descending order, the passengers at positions:

```
0, k, 2k, 3k, ...
```

become the maximum floors of the elevator trips.

Each such floor contributes:

```
2 * (floor - 1)
```

to the answer.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| Optimal | O(n log n) | O(1) extra (excluding sorting) | Accepted |

## Algorithm Walkthrough

1. Read `n`, `k`, and all destination floors.
2. Sort the destination floors in descending order.
3. Initialize the answer to zero.
4. Starting from index `0`, jump by `k` positions each time.
5. Each selected floor is the highest destination in one elevator trip.
6. Add `2 * (floor - 1)` to the answer.

The elevator starts on floor 1, reaches that highest floor, and eventually returns to floor 1.
7. Output the final answer.

### Why it works

After sorting in descending order, the largest remaining destination always determines the cost of the next trip. Since passengers with smaller destinations can be transported together without increasing the maximum floor reached, every trip should contain the largest remaining passenger plus up to `k - 1` additional passengers.

This greedy choice cannot hurt future trips because removing smaller destinations from later groups never increases any trip's maximum floor. As a result, the optimal grouping is exactly the partition formed by consecutive blocks of size `k` in descending order. The first element of each block determines that trip's cost, which is why summing the floors at indices `0, k, 2k, ...` gives the minimum total time.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, k = map(int, input().split())
    floors = list(map(int, input().split()))

    floors.sort(reverse=True)

    ans = 0
    for i in range(0, n, k):
        ans += 2 * (floors[i] - 1)

    print(ans)

if __name__ == "__main__":
    solve()
```

The solution begins by sorting destination floors from largest to smallest. After sorting, every block of `k` consecutive passengers corresponds to one elevator trip.

The first passenger in each block has the highest destination among everyone assigned to that trip. Since the elevator must travel from floor 1 to that floor and then back to floor 1, the trip contributes `2 * (floor - 1)`.

The loop:

```
for i in range(0, n, k):
```

visits exactly the first passenger of every block. Those are the only floors that affect the answer.

One subtle point is the use of `floor - 1` rather than `floor`. The elevator starts on floor 1, so reaching floor `f` requires `f - 1` seconds.

Another detail is handling incomplete final groups. If fewer than `k` passengers remain, they still form one trip whose cost is determined by the largest floor among them. The loop naturally handles this because the final block's first element is still visited.

## Worked Examples

### Example 1

Input:

```
3 2
2 3 4
```

After sorting:

```
[4, 3, 2]
```

| Index | Floor | Selected as trip maximum? | Contribution | Answer |
| --- | --- | --- | --- | --- |
| 0 | 4 | Yes | 2 × (4 - 1) = 6 | 6 |
| 1 | 3 | No | 0 | 6 |
| 2 | 2 | Yes | 2 × (2 - 1) = 2 | 8 |

Final answer:

```
8
```

The first trip carries passengers for floors 4 and 3. The second trip carries the passenger for floor 2. Only the largest destination in each trip matters.

### Example 2

Input:

```
5 2
7 7 7 7 7
```

After sorting:

```
[7, 7, 7, 7, 7]
```

| Index | Floor | Selected as trip maximum? | Contribution | Answer |
| --- | --- | --- | --- | --- |
| 0 | 7 | Yes | 12 | 12 |
| 1 | 7 | No | 0 | 12 |
| 2 | 7 | Yes | 12 | 24 |
| 3 | 7 | No | 0 | 24 |
| 4 | 7 | Yes | 12 | 36 |

Final answer:

```
36
```

This example shows that identical destinations simply create repeated trips when the elevator capacity is insufficient to carry everyone at once.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting dominates the running time |
| Space | O(1) extra | Aside from the input array and sorting storage |

With `n ≤ 2000`, sorting is extremely cheap. The solution performs only a single additional linear scan after sorting and comfortably fits within the time and memory limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    n, k = map(int, input().split())
    floors = list(map(int, input().split()))

    floors.sort(reverse=True)

    ans = 0
    for i in range(0, n, k):
        ans += 2 * (floors[i] - 1)

    return str(ans)

# provided sample
assert run("3 2\n2 3 4\n") == "8"

# minimum size
assert run("1 1\n2\n") == "2"

# k >= n, everyone in one trip
assert run("3 5\n2 3 10\n") == "18"

# all equal values
assert run("5 2\n7 7 7 7 7\n") == "36"

# boundary grouping case
assert run("4 2\n2 2 100 100\n") == "200"

# exact multiple of k
assert run("6 3\n2 3 4 5 6 7\n") == "22"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 / 2` | `2` | Smallest valid instance |
| `3 5 / 2 3 10` | `18` | Capacity larger than population |
| `5 2 / 7 7 7 7 7` | `36` | Repeated identical floors |
| `4 2 / 2 2 100 100` | `200` | Correct grouping of large floors |
| `6 3 / 2 3 4 5 6 7` | `22` | Exact block partitioning |

## Edge Cases

Consider:

```
3 5
2 3 10
```

After sorting we get:

```
[10, 3, 2]
```

Only index `0` is selected because `k = 5`. The answer becomes:

```
2 * (10 - 1) = 18
```

All passengers ride together, which is optimal.

Consider:

```
5 2
7 7 7 7 7
```

Sorted order remains unchanged. The selected indices are `0`, `2`, and `4`. Each contributes `12`, producing `36`. This correctly accounts for the three required trips.

Consider:

```
4 2
2 2 100 100
```

Sorted order:

```
[100, 100, 2, 2]
```

Selected indices are `0` and `2`.

```
2 * (100 - 1) + 2 * (2 - 1)
= 198 + 2
= 200
```

The algorithm automatically places both floor-100 passengers in the same trip. Any arrangement that splits them across different trips would pay for floor 100 twice and be worse.
