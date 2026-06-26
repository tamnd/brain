---
title: "CF 105689C - Dragon Dance"
description: "The line of dragon dancers already has a fixed order. James may remove some dancers, but the dancers that remain must still respect the original “who stands behind whom” relationships."
date: "2026-06-26T09:45:17+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105689
codeforces_index: "C"
codeforces_contest_name: "UTPC Contest 1-29-25 Div. 2 (Beginner)"
rating: 0
weight: 105689
solve_time_s: 43
verified: true
draft: false
---

[CF 105689C - Dragon Dance](https://codeforces.com/problemset/problem/105689/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 43s  
**Verified:** yes  

## Solution
# Problem Understanding

The line of dragon dancers already has a fixed order. James may remove some dancers, but the dancers that remain must still respect the original “who stands behind whom” relationships. A dancer can only keep the person immediately in front of them from the original line, unless that dancer becomes the first dancer in the new line.

This means the chosen dancers must form one continuous segment of the original line. If we skip a dancer in the middle, the next chosen dancer would be forced to stand behind someone new, which is not allowed.

The remaining requirement is that neighboring dancers in this segment must have heights close enough. For every pair of consecutive dancers in the chosen segment, the absolute difference between their heights must not exceed `k`. The task is to find the maximum length of such a contiguous segment.

The input contains the number of dancers, the maximum allowed height difference, and the heights of the dancers in their original order. The output is the largest number of dancers that can remain in a valid dragon dance.

The number of dancers can reach `2 * 10^5`, so an algorithm that checks every possible segment is not practical. There are about `n^2 / 2` possible segments, which is around `2 * 10^10` checks in the worst case. A solution must process the line in roughly linear time.

The main edge cases come from treating the problem as a general subsequence problem instead of a contiguous segment problem. For example, consider:

```
5 1
1 10 2 3 4
```

The correct output is:

```
3
```

The valid segment is `2 3 4`. A careless approach might select `1 2 3 4` by skipping `10`, but that would violate the original order relationship because dancer `2` would now stand behind a different person.

Another case is when every adjacent pair is valid:

```
4 100
5 6 7 8
```

The answer is:

```
4
```

The algorithm must not stop early or incorrectly require the segment to have exactly some minimum size.

A final boundary case is:

```
1 0
42
```

The answer is:

```
1
```

A single dancer is always a valid dragon dance because there is no neighboring pair that can violate the height condition.

## Approaches

A direct approach is to try every possible starting dancer and extend the segment to the right until a height difference becomes too large. For each starting position, we may scan almost all remaining dancers. This is correct because it examines every possible contiguous segment, but in the worst case it performs about `n * (n + 1) / 2` comparisons. With `n = 200000`, that is roughly `2 * 10^10` operations, which is far beyond the time limit.

The structure of the problem gives us a simpler view. A segment is valid exactly when every adjacent pair inside it is valid. While scanning from left to right, if the current dancer can stand behind the previous dancer, the current valid segment can be extended. If the height difference is too large, no segment ending at the current dancer can include the previous dancer, so the current dancer must start a new segment.

This turns the problem into maintaining the length of the current valid suffix while keeping track of the best answer seen so far. Each dancer is processed once, so the solution becomes linear.

| Approach | Time Complexity | Space Complexity | Verdict |
|---|---|---|---|
| Brute Force | O(n²) | O(1) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of dancers, the maximum allowed height difference, and the height array.

2. Start with a current segment length of `1` and a best answer of `1`. A single dancer always forms a valid line.

3. Scan the dancers from the second position onward. Compare the current dancer's height with the previous dancer's height.

4. If the absolute difference is at most `k`, extend the current segment by increasing its length. This is valid because the new dancer can stand directly behind the previous dancer.

5. If the difference is larger than `k`, the current dancer cannot stay in the same segment. Start a new segment containing only this dancer.

6. After every update, compare the current segment length with the best answer and keep the maximum.

The reason this works is that the only information needed about a segment is whether its last adjacent pair is valid. If a pair breaks the rule, every segment that includes both dancers is invalid, so the only possible valid segment ending at the current dancer must begin at the current dancer or later. The maintained segment is always the longest valid segment ending at the current position, which means the maximum found during the scan is the global answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, k = map(int, input().split())
    h = list(map(int, input().split()))

    ans = 1
    cur = 1

    for i in range(1, n):
        if abs(h[i] - h[i - 1]) <= k:
            cur += 1
        else:
            cur = 1
        if cur > ans:
            ans = cur

    print(ans)

if __name__ == "__main__":
    solve()
```

The solution keeps only two counters. `cur` represents the length of the valid segment ending at the current dancer. `ans` stores the largest segment length encountered.

The loop begins at index `1` because the first dancer has no previous dancer to compare against. When the adjacent height difference is acceptable, the current segment grows. Otherwise, the previous dancers can no longer be part of a valid segment ending here, so the counter resets to one.

No indexing beyond the array boundaries is used because the scan only accesses `i` and `i - 1` after `i` has reached `1`. Python integers also handle the large height values safely without overflow concerns.

## Worked Examples

### Example 1

Input:

```
7 4
1 2 1 2 6 7 1
```

| Position | Height | Previous Difference | Current Length | Best Answer |
|---|---|---|---|---|
| 1 | 1 | - | 1 | 1 |
| 2 | 2 | 1 | 2 | 2 |
| 3 | 1 | 1 | 3 | 3 |
| 4 | 2 | 1 | 4 | 4 |
| 5 | 6 | 4 | 5 | 5 |
| 6 | 7 | 1 | 6 | 6 |
| 7 | 1 | 6 | 1 | 6 |

The first six dancers form a valid segment. The last dancer cannot join because the height difference from `7` to `1` is too large.

### Example 2

Input:

```
6 3
7 4 7 4 8 9
```

| Position | Height | Previous Difference | Current Length | Best Answer |
|---|---|---|---|---|
| 1 | 7 | - | 1 | 1 |
| 2 | 4 | 3 | 2 | 2 |
| 3 | 7 | 3 | 3 | 3 |
| 4 | 4 | 3 | 4 | 4 |
| 5 | 8 | 4 | 1 | 4 |
| 6 | 9 | 1 | 2 | 4 |

The first four dancers are the longest valid consecutive group. The pair `4, 8` breaks the segment because their difference is larger than `3`.

## Complexity Analysis

| Measure | Complexity | Explanation |
|---|---|---|
| Time | O(n) | Every dancer is visited exactly once. |
| Space | O(1) | Only counters are stored after reading the heights. |

The linear runtime is suitable for `n = 200000` because the algorithm performs only a small constant amount of work per dancer. The memory usage is also minimal apart from storing the input array.

## Test Cases

```python
import sys
import io

def solve_data(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)

    n, k = map(int, sys.stdin.readline().split())
    h = list(map(int, sys.stdin.readline().split()))

    ans = 1
    cur = 1

    for i in range(1, n):
        if abs(h[i] - h[i - 1]) <= k:
            cur += 1
        else:
            cur = 1
        ans = max(ans, cur)

    sys.stdin = old_stdin
    return str(ans)

assert solve_data("7 4\n1 2 1 2 6 7 1\n") == "6"
assert solve_data("6 3\n7 4 7 4 8 9\n") == "4"

assert solve_data("1 0\n42\n") == "1"
assert solve_data("5 1\n1 10 2 3 4\n") == "3"
assert solve_data("4 100\n5 6 7 8\n") == "4"
assert solve_data("5 0\n9 9 8 8 8\n") == "3"
```

| Test input | Expected output | What it validates |
|---|---|---|
| `1 0 / 42` | `1` | Minimum size input with one dancer |
| `5 1 / 1 10 2 3 4` | `3` | Prevents treating the answer as an arbitrary subsequence |
| `4 100 / 5 6 7 8` | `4` | All adjacent pairs are valid |
| `5 0 / 9 9 8 8 8` | `3` | Checks exact equality boundaries and segment resets |

## Edge Cases

For the single dancer case:

```
1 0
42
```

The algorithm initializes both `cur` and `ans` to `1`. The loop never runs, so the answer remains `1`, which matches the fact that one dancer always forms a valid line.

For the skipped-dancer trap:

```
5 1
1 10 2 3 4
```

The scan starts with length `1`. The difference between `1` and `10` is too large, so the segment resets at `10`. The difference between `10` and `2` also resets it. The final three dancers have differences `1` and `1`, giving a valid segment of length `3`. The algorithm never incorrectly joins separated dancers.

For the all-valid case:

```
4 100
5 6 7 8
```

Every adjacent difference is smaller than `100`, so the current length increases from `1` to `4`. The answer becomes `4`, showing that the algorithm can keep extending a segment until the end.

For repeated values with a strict limit:

```
5 0
9 9 8 8 8
```

The first pair of `9`s is valid, giving length `2`. The pair `9` and `8` breaks the segment, so the scan starts again at the first `8`. The final three `8`s form the answer, giving `3`. This checks that the reset happens exactly at the invalid adjacent pair.
