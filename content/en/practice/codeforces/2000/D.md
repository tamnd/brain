---
title: "CF 2000D - Right Left Wrong"
description: "We have a line of cells. Each cell contains a positive value a[i] and a character, either L or R. An operation chooses a pair of positions (l, r) with l < r, where position l currently contains L and position r currently contains R."
date: "2026-06-09T02:33:23+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "implementation", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 2000
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 966 (Div. 3)"
rating: 1200
weight: 2000
solve_time_s: 364
verified: false
draft: false
---

[CF 2000D - Right Left Wrong](https://codeforces.com/problemset/problem/2000/D)

**Rating:** 1200  
**Tags:** greedy, implementation, two pointers  
**Solve time:** 6m 4s  
**Verified:** no  

## Solution
## Problem Understanding

We have a line of cells. Each cell contains a positive value `a[i]` and a character, either `L` or `R`.

An operation chooses a pair of positions `(l, r)` with `l < r`, where position `l` currently contains `L` and position `r` currently contains `R`. We gain the sum of all values between them, inclusive. After that, every position in the interval `[l, r]` becomes unusable.

The intervals created by different operations can never overlap because once an interval is chosen, all of its positions disappear from future consideration.

The goal is to maximize the total score.

The constraints immediately suggest that we need something close to linear time. Across all test cases, the total number of cells is at most `2 · 10^5`, which means an `O(n)` or `O(n log n)` solution is easily fast enough. An `O(n²)` approach would require roughly `4 · 10^10` operations in the worst case, which is completely infeasible.

The main difficulty is that choosing one interval removes many positions, which affects what intervals can be chosen later. A greedy strategy that always takes the largest currently available interval is not obviously correct.

Several edge cases deserve attention.

Consider:

```
3
1 2 3
LLL
```

There is no `R` at all. No valid operation exists, so the answer is `0`.

A careless implementation that assumes every `L` can be matched would fail here.

Consider:

```
4
5 5 5 5
LRLR
```

The optimal choice is the whole interval `[1,4]`, giving `20`.

Choosing `[1,2]` first gives only `10`, after which `[3,4]` gives another `10`. The total is still `20`, showing that different decompositions can produce the same result.

Now consider:

```
4
1 100 100 1
LRRL
```

The only valid pair using the last `L` is impossible because there is no `R` to its right. The best choice is `[1,3]`, worth `201`.

A solution that tries to match characters locally without considering position order can incorrectly count invalid pairs.

Another subtle case is:

```
5
1 2 3 4 5
RLLLR
```

The leftmost character is `R`, so it can never serve as a left endpoint. The only useful interval is `[2,5]`, worth `14`.

The algorithm must ignore unmatched characters at the boundaries.

## Approaches

A brute-force viewpoint is to think recursively. At any moment we can choose any valid pair `(l,r)`, gain the corresponding interval sum, remove that interval, and continue on the remaining pieces. Exploring all possible choices eventually finds the optimum.

This is correct because it examines every legal sequence of operations.

The problem is the number of possibilities. Even deciding which valid interval to take first can involve `O(n²)` choices, and every choice branches into more possibilities. The search space grows exponentially and becomes hopeless long before `n = 2 · 10^5`.

To find something faster, we need to understand what an optimal solution looks like.

Suppose we pick an interval `[l,r]`. Every position inside it disappears. Since all values are positive, whenever we can enlarge an interval without violating the endpoint requirements, the gained score only increases.

This observation changes the way we look at the problem. Imagine taking the leftmost available `L` and the rightmost available `R`. If the `L` lies before the `R`, then using these two endpoints captures the largest possible interval among all currently remaining positions.

What happens after removing that interval? Every position inside is gone, so any future operation must occur completely outside it. Since we already used the outermost possible endpoints, the remaining problem becomes exactly the same problem on the cells that remain outside.

This naturally leads to a two-pointer process.

Place one pointer at the left end and another at the right end.

Move the left pointer until it reaches an `L`.

Move the right pointer until it reaches an `R`.

If the left pointer is still before the right pointer, we should pair them. Because all numbers are positive, taking the outermost valid pair captures every value between them and cannot be worse than splitting that region into smaller intervals.

The score of an interval can be obtained in `O(1)` time using prefix sums.

After using the pair, move both pointers inward and repeat.

The entire array is scanned only once.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | O(n) | Too slow |
| Optimal Two Pointers + Prefix Sums | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Build a prefix sum array so that the sum of any interval `[l,r]` can be computed in constant time.
2. Initialize two pointers, `i = 0` and `j = n - 1`.
3. Move `i` to the right until it points to an `L` or passes `j`.
4. Move `j` to the left until it points to an `R` or passes `i`.
5. If `i >= j`, no valid pair remains, so stop.
6. Add the sum of the interval `[i, j]` to the answer using the prefix sums.
7. Increment `i` and decrement `j`.
8. Repeat from step 3.

The key action is step 6. Once the leftmost remaining `L` and the rightmost remaining `R` are found, pairing them immediately captures the largest possible interval in the current remaining segment. Since every value is positive, excluding any cells from that interval can only decrease the score.

### Why it works

At any stage, consider the leftmost remaining `L` and the rightmost remaining `R`. Any valid operation must use a left endpoint no further left than that `L` and a right endpoint no further right than that `R`.

The interval formed by these outermost valid endpoints contains every interval that could be formed using other remaining endpoints. Since all array values are positive, the sum of the larger interval is at least as large as the sum of any smaller interval inside it.

After choosing this outermost interval, all positions inside it disappear. Any future operation must lie completely outside that interval. Thus the remaining subproblem is independent of the interval we just took.

Repeating this argument at every step shows that the greedy choice is always safe, and the algorithm produces the maximum possible score.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())

    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        s = input().strip()

        pref = [0] * (n + 1)
        for i in range(n):
            pref[i + 1] = pref[i] + a[i]

        i = 0
        j = n - 1
        ans = 0

        while True:
            while i < n and s[i] != 'L':
                i += 1

            while j >= 0 and s[j] != 'R':
                j -= 1

            if i >= j:
                break

            ans += pref[j + 1] - pref[i]

            i += 1
            j -= 1

        print(ans)

solve()
```

The prefix sum array allows interval sums to be computed in constant time. The value of interval `[i, j]` is:

```
pref[j + 1] - pref[i]
```

The two pointers search for the next usable `L` from the left and the next usable `R` from the right.

After a pair is used, both pointers move inward. This effectively removes that entire interval from future consideration, matching the greedy argument from the proof.

One easy mistake is using `pref[j] - pref[i]`, which would exclude `a[j]`. Another common error is forgetting that the pointers must continue searching after being moved inward, because the next positions may not be valid endpoints.

Python integers are unbounded, so there is no overflow issue. The maximum possible answer can be much larger than `32-bit` integer limits.

## Worked Examples

### Example 1

Input:

```
6
3 5 1 4 3 2
LRLLLR
```

Prefix sums:

```
[0, 3, 8, 9, 13, 16, 18]
```

| Step | i | j | Interval | Gain | Total |
| --- | --- | --- | --- | --- | --- |
| 1 | 0 | 5 | [0,5] | 18 | 18 |
| Stop | 1 | 4 | no valid pair | 0 | 18 |

The first character is already `L` and the last character is already `R`, so the greedy choice immediately takes the entire strip. Since all values are positive, no alternative decomposition can exceed the total sum of the whole array.

### Example 2

Input:

```
5
1 2 3 4 5
LRLRR
```

Prefix sums:

```
[0,1,3,6,10,15]
```

| Step | i | j | Interval | Gain | Total |
| --- | --- | --- | --- | --- | --- |
| 1 | 0 | 4 | [0,4] | 15 | 15 |
| 2 | 2 | 3 | [2,3] | 7 | 22 |
| Stop | 3 | 2 | no valid pair | 0 | 22 |

The first operation uses the outermost endpoints and gains `15`. After moving inward, another valid pair remains, producing an additional `7`. The final answer is `22`.

This example demonstrates that intervals are not required to be disjoint in the original array. The greedy process is operating on the remaining unremoved endpoints, which corresponds exactly to the intended game.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each pointer moves across the array at most once |
| Space | O(n) | Prefix sum array stores `n + 1` values |

The total length across all test cases is at most `2 · 10^5`. A linear scan per test case performs only a few hundred thousand operations overall, which is comfortably within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    out = []

    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        s = input().strip()

        pref = [0] * (n + 1)
        for i in range(n):
            pref[i + 1] = pref[i] + a[i]

        l, r = 0, n - 1
        ans = 0

        while True:
            while l < n and s[l] != 'L':
                l += 1

            while r >= 0 and s[r] != 'R':
                r -= 1

            if l >= r:
                break

            ans += pref[r + 1] - pref[l]

            l += 1
            r -= 1

        out.append(str(ans))

    return "\n".join(out) + "\n"

# provided samples
assert run(
"""4
6
3 5 1 4 3 2
LRLLLR
2
2 8
LR
2
3 9
RL
5
1 2 3 4 5
LRLRR
"""
) == "18\n10\n0\n22\n"

# minimum size, valid pair
assert run(
"""1
2
1 1
LR
"""
) == "2\n"

# minimum size, invalid pair
assert run(
"""1
2
1 1
RL
"""
) == "0\n"

# all L
assert run(
"""1
5
1 2 3 4 5
LLLLL
"""
) == "0\n"

# all R
assert run(
"""1
5
1 2 3 4 5
RRRRR
"""
) == "0\n"

# nested pair structure
assert run(
"""1
4
5 5 5 5
LRLR
"""
) == "20\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `n=2, LR` | `2` | Smallest valid instance |
| `n=2, RL` | `0` | No valid pair exists |
| All `L` | `0` | Missing right endpoints |
| All `R` | `0` | Missing left endpoints |
| `LRLR` with equal values | `20` | Multiple greedy pairings and interval sums |

## Edge Cases

Consider:

```
1
2
3 9
RL
```

The left pointer searches for an `L` and finds position `2`. The right pointer searches for an `R` and finds position `1`. Since `i >= j`, no valid interval exists.

The algorithm outputs:

```
0
```

which is correct.

Consider:

```
1
5
1 2 3 4 5
LLLLL
```

The right pointer never finds an `R`. It moves past the beginning of the array, causing `i >= j`. The algorithm terminates immediately and returns `0`.

Consider:

```
1
5
1 2 3 4 5
RLLLR
```

The left pointer skips the first character because it is `R`. It eventually stops at position `2`, while the right pointer stops at position `5`.

The chosen interval is:

```
[2,5]
```

with value:

```
2 + 3 + 4 + 5 = 14
```

The algorithm outputs `14`, correctly ignoring the unmatched `R` at the beginning.

Finally, consider:

```
1
4
5 5 5 5
LRLR
```

The first pair uses positions `(1,4)` and gains `20`. After moving inward, the remaining endpoints cross and the process stops.

The output is:

```
20
```

which matches the maximum possible score and illustrates why taking the outermost valid pair is optimal.
