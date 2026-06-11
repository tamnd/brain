---
title: "CF 1393C - Pinkie Pie Eats Patty-cakes"
description: "We are given a multiset of patty-cakes represented by integers. Equal integers mean equal fillings. We may choose any order in which to eat them. For every filling that appears multiple times, we can look at the distances between consecutive occurrences in the eating order."
date: "2026-06-11T10:03:54+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "greedy", "math", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1393
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 662 (Div. 2)"
rating: 1700
weight: 1393
solve_time_s: 662
verified: true
draft: false
---

[CF 1393C - Pinkie Pie Eats Patty-cakes](https://codeforces.com/problemset/problem/1393/C)

**Rating:** 1700  
**Tags:** constructive algorithms, greedy, math, sortings  
**Solve time:** 11m 2s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a multiset of patty-cakes represented by integers. Equal integers mean equal fillings. We may choose any order in which to eat them.

For every filling that appears multiple times, we can look at the distances between consecutive occurrences in the eating order. The distance is defined as the number of patty-cakes strictly between them. For example, in the sequence:

```
1 2 3 1
```

the two occurrences of filling `1` have distance `2`.

Our goal is to arrange all patty-cakes so that the smallest such distance among all equal fillings is as large as possible. We must output that maximum achievable minimum distance.

The number of test cases is at most 100, but the important constraint is that the total number of patty-cakes across all test cases is at most `10^5`. This immediately suggests that solutions around `O(n log n)` per test case are acceptable, while anything quadratic is impossible. A construction that repeatedly simulates rearrangements would be too slow if it performs work proportional to the answer times `n`.

Several edge cases are easy to misjudge.

Consider:

```
3
3 3 3
```

The only possible ordering is:

```
3 3 3
```

The distances are `0` and `0`, so the answer is:

```
0
```

A naive formula based only on the number of distinct fillings would fail here because there is only one filling.

Consider:

```
6
1 1 1 2 2 3
```

The most frequent filling appears three times. One might try to spread the three copies evenly:

```
1 2 1 3 1 2
```

The minimum distance is only `1`. The answer depends on how many elements can be placed into the gaps created by the most frequent value, not merely on the frequency itself.

Another subtle case is:

```
6
2 5 2 3 1 4
```

The sample answer is `4`. Since the value `2` appears twice, we can place all four remaining elements between them:

```
2 5 3 1 4 2
```

The distance becomes `4`. This shows that distances can be much larger than the frequency of the duplicated value.

## Approaches

A brute-force approach would generate permutations of the multiset, compute the minimum distance between equal fillings in each permutation, and take the best value. This is correct because it directly searches the entire solution space. Unfortunately, even for `n = 15`, there are already more than `10^12` permutations. The actual limit is `10^5`, so exhaustive search is completely impossible.

The key observation is that only the fillings with maximum frequency matter.

Suppose the largest frequency is `mx`. Let `cnt` be the number of fillings that occur exactly `mx` times.

Imagine placing all occurrences of those most frequent fillings first. Since each of those fillings appears `mx` times, they create `mx - 1` internal gaps between consecutive copies.

For example, if two fillings each appear four times:

```
A A A A
B B B B
```

then there are `3` layers of gaps that must separate consecutive copies.

Every other patty-cake can only be used to fill these gaps. Let

```
rest = n - mx * cnt
```

be the number of patty-cakes whose frequency is strictly smaller than the maximum.

These `rest` elements can be distributed among the `mx - 1` gap groups. If each gap receives

```
rest // (mx - 1)
```

elements, and some gaps receive one extra element, then the smallest gap size becomes exactly

```
rest // (mx - 1)
```

After accounting for the fact that there are `cnt` maximum-frequency fillings sharing the same structure, the final formula becomes

```
(rest // (mx - 1)) + cnt - 1
```

This is the value proved in the official solution.

The entire problem reduces to counting frequencies.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n!) | O(n) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Count the frequency of every filling.
2. Find the maximum frequency `mx`.
3. Count how many fillings occur exactly `mx` times. Call this value `cnt`.
4. Compute the number of remaining patty-cakes:

```
rest = n - mx * cnt
```
5. If `mx = 1`, every filling is unique. The problem guarantees at least one duplicate, but handling this case makes the formula complete. The answer would be `n - 1`.
6. Otherwise compute:

```
answer = rest // (mx - 1) + cnt - 1
```
7. Output the answer.

The reason step 6 works is that the `mx - 1` mandatory separation layers created by the most frequent fillings are the bottleneck. All remaining elements must be distributed among those layers. The quotient tells us how many fillers every layer can receive, and `cnt - 1` accounts for the additional maximum-frequency fillings that occupy positions inside each layer.

### Why it works

Let the fillings with maximum frequency be the dominant colors. Any valid arrangement must separate consecutive occurrences of each dominant color by some number of elements. Since each dominant color appears `mx` times, there are exactly `mx - 1` intervals that need to be filled.

The total supply of non-dominant elements is `rest`. Distributing them as evenly as possible maximizes the smallest interval. No arrangement can make every interval larger than `rest // (mx - 1)`, because there are only `rest` filler elements available.

When multiple dominant colors exist, they can interleave with each other. This effectively contributes `cnt - 1` extra positions to every interval. The resulting value is both achievable and optimal, giving:

```
rest // (mx - 1) + cnt - 1
```

## Python Solution

```python
import sys
from collections import Counter

input = sys.stdin.readline

def solve():
    t = int(input())

    ans = []

    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))

        freq = Counter(a)

        mx = max(freq.values())
        cnt = sum(1 for v in freq.values() if v == mx)

        rest = n - mx * cnt

        answer = rest // (mx - 1) + cnt - 1
        ans.append(str(answer))

    sys.stdout.write("\n".join(ans))

if __name__ == "__main__":
    solve()
```

The implementation follows the mathematical formula directly.

`Counter` computes all frequencies in linear time. The variable `mx` stores the largest frequency. The variable `cnt` counts how many fillings achieve that frequency.

The expression

```
rest = n - mx * cnt
```

removes all occurrences of the maximum-frequency fillings. What remains are exactly the elements available to fill the gaps.

The final formula uses integer division. This is important because we are distributing filler elements across `mx - 1` gaps, and only complete groups contribute to the minimum gap size.

All computations fit comfortably in standard Python integers.

## Worked Examples

### Sample 1

Input:

```
7
1 7 1 6 4 4 6
```

Frequency table:

| Filling | Frequency |
| --- | --- |
| 1 | 2 |
| 4 | 2 |
| 6 | 2 |
| 7 | 1 |

Now compute the variables.

| Variable | Value |
| --- | --- |
| n | 7 |
| mx | 2 |
| cnt | 3 |
| rest | 1 |
| answer | 1 // 1 + 3 - 1 = 3 |

Output:

```
3
```

Three fillings tie for maximum frequency. They can be interleaved, and the lone remaining element contributes one extra separation.

### Sample 2

Input:

```
8
1 1 4 6 4 6 4 7
```

Frequency table:

| Filling | Frequency |
| --- | --- |
| 1 | 2 |
| 4 | 3 |
| 6 | 2 |
| 7 | 1 |

Computation:

| Variable | Value |
| --- | --- |
| n | 8 |
| mx | 3 |
| cnt | 1 |
| rest | 5 |
| answer | 5 // 2 + 1 - 1 = 2 |

Output:

```
2
```

The filling `4` dominates the arrangement. The five remaining elements must be distributed across the two gaps between its three copies.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Frequency counting and scanning frequencies |
| Space | O(n) | Frequency map in the worst case |

Since the total number of patty-cakes across all test cases is at most `10^5`, linear processing easily fits within the time limit. The frequency table also stays within the memory limit.

## Test Cases

```python
import sys
import io
from collections import Counter

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    t = int(input())
    out = []

    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))

        freq = Counter(a)
        mx = max(freq.values())
        cnt = sum(1 for v in freq.values() if v == mx)

        rest = n - mx * cnt
        out.append(str(rest // (mx - 1) + cnt - 1))

    return "\n".join(out)

# provided samples
assert run("""4
7
1 7 1 6 4 4 6
8
1 1 4 6 4 6 4 7
3
3 3 3
6
2 5 2 3 1 4
""") == """3
2
0
4"""

# all equal
assert run("""1
5
7 7 7 7 7
""") == "0"

# two values tied for maximum frequency
assert run("""1
6
1 1 1 2 2 2
""") == "1"

# one dominant value
assert run("""1
6
1 1 1 2 3 4
""") == "1"

# smallest valid duplicated case
assert run("""1
2
5 5
""") == "0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `7 7 7 7 7` | `0` | All elements identical |
| `1 1 1 2 2 2` | `1` | Multiple maximum-frequency fillings |
| `1 1 1 2 3 4` | `1` | Single dominant filling |
| `5 5` | `0` | Smallest possible duplicated array |

## Edge Cases

Consider:

```
1
3
5 5 5
```

Here `mx = 3`, `cnt = 1`, and `rest = 0`. The formula gives:

```
0 // 2 + 1 - 1 = 0
```

No rearrangement can create a positive distance because every position contains the same filling.

Consider:

```
1
6
1 1 1 2 2 2
```

We have `mx = 3`, `cnt = 2`, and `rest = 0`.

The formula gives:

```
0 // 2 + 2 - 1 = 1
```

An arrangement such as:

```
1 2 1 2 1 2
```

achieves minimum distance `1`, and no larger value is possible because there are no extra fillings available to enlarge the gaps.

Consider:

```
1
6
2 5 2 3 1 4
```

We have `mx = 2`, `cnt = 1`, and `rest = 4`.

The formula gives:

```
4 // 1 + 1 - 1 = 4
```

The arrangement:

```
2 5 3 1 4 2
```

places all four remaining patty-cakes between the two copies of `2`, producing distance `4`, which matches the optimal answer.
