---
title: "CF 1138A - Sushi for Two"
description: "We are given a row of sushi pieces, where each piece is either type 1 or type 2. We want to choose one contiguous segment of this row. A segment is valid if it consists of two consecutive blocks of different sushi types, and both blocks have the same size."
date: "2026-06-12T03:55:02+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "greedy", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1138
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 545 (Div. 2)"
rating: 900
weight: 1138
solve_time_s: 72
verified: true
draft: false
---

[CF 1138A - Sushi for Two](https://codeforces.com/problemset/problem/1138/A)

**Rating:** 900  
**Tags:** binary search, greedy, implementation  
**Solve time:** 1m 12s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a row of sushi pieces, where each piece is either type `1` or type `2`. We want to choose one contiguous segment of this row.

A segment is valid if it consists of two consecutive blocks of different sushi types, and both blocks have the same size. For example, `[2,2,2,1,1,1]` is valid because it is three `2`s followed by three `1`s. A segment like `[2,2,1,1]` is also valid. A segment like `[1,2,1,2]` is not valid because each half contains both types.

The task is to find the maximum possible length of such a valid contiguous segment.

The array length can be as large as `100000`, which immediately rules out expensive approaches that examine all subarrays. There are roughly `n²` possible subarrays, which would be around `10^10` checks in the worst case. Even an `O(n²)` algorithm is far too slow. We need a solution that processes the array in linear time or close to it.

The tricky part is that the chosen segment does not have to use entire runs of equal values. It may use only part of a run.

Consider:

```
1 1 1 1 2 2
```

The runs have lengths `4` and `2`. The best valid segment is:

```
1 1 2 2
```

with length `4`. A careless implementation that only considers complete runs would incorrectly return `6`.

Another subtle case is:

```
1 2 1 2
```

Every run has length `1`.

The correct answer is `2`, because the best segment is either `[1,2]` or `[2,1]`. There is no longer valid segment. An implementation that tries to merge multiple alternating runs would produce an incorrect result.

One more edge case is:

```
1 1 1 2
```

The run lengths are `3` and `1`.

The answer is `2`, using `[1,2]`. The larger run does not force us to use all its elements. We only need equal counts from the two adjacent runs.

## Approaches

A brute-force solution would enumerate every possible subarray and check whether it consists of exactly two consecutive blocks of different sushi types with equal sizes. Checking a single subarray may take linear time, giving a worst-case complexity around `O(n³)`. Even with optimizations, examining all `O(n²)` subarrays is impossible for `n = 100000`.

The key observation comes from looking at the array as runs of equal values.

For example:

```
2 2 2 1 1 2 2
```

becomes:

```
[3, 2, 2]
```

where each number represents the length of a consecutive block.

Any valid answer must be formed from two adjacent runs. If two neighboring runs have lengths `a` and `b`, we can take:

```
min(a, b)
```

elements from each side.

That creates a valid segment of length:

```
2 * min(a, b)
```

For instance, runs `(3,2)` produce a segment of length `4`, while runs `(5,7)` produce a segment of length `10`.

Since every valid segment must lie across exactly one boundary between two neighboring runs, the problem reduces to finding the maximum value of:

```
2 * min(run[i], run[i+1])
```

over all adjacent run pairs.

Building the run lengths takes one pass through the array, and checking neighboring runs takes another pass. This gives a linear solution.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) to O(n³) | O(1) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Scan the sushi array from left to right and compress it into run lengths.

For example:

```
2 2 2 1 1 2 2
```

becomes:

```
[3, 2, 2]
```

Each number records the size of one maximal block of identical sushi.
2. Iterate through every pair of neighboring runs.

If the lengths are `a` and `b`, the largest valid segment crossing their boundary uses `min(a,b)` pieces from each run.
3. Compute `2 * min(a,b)` for every adjacent pair.

This is the maximum valid segment that can be formed around that boundary.
4. Keep the largest value seen.
5. Output the maximum.

### Why it works

Every valid segment contains exactly two consecutive groups of sushi, one of each type. Such a segment must cross one boundary between two adjacent runs in the compressed representation.

Suppose the neighboring run lengths are `a` and `b`. To keep equal numbers of both sushi types, we can use at most `min(a,b)` pieces from each side. Using more would exceed the size of the smaller run and break the equality condition.

Thus the best segment associated with that boundary has length `2 * min(a,b)`. Since every valid segment corresponds to some adjacent run pair, taking the maximum value over all neighboring runs examines every possible answer and returns the optimum.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    t = list(map(int, input().split()))

    runs = []
    cnt = 1

    for i in range(1, n):
        if t[i] == t[i - 1]:
            cnt += 1
        else:
            runs.append(cnt)
            cnt = 1

    runs.append(cnt)

    ans = 0
    for i in range(len(runs) - 1):
        ans = max(ans, 2 * min(runs[i], runs[i + 1]))

    print(ans)

solve()
```

The first part of the code constructs the run-length encoding of the sushi sequence. The variable `cnt` tracks the current block size. Whenever the sushi type changes, the completed run is stored and a new run begins.

After the scan finishes, the final run must also be appended. Forgetting this step is a common bug because the last run is never followed by a change.

The second loop examines every neighboring pair of runs. For each pair, the expression `2 * min(runs[i], runs[i + 1])` gives the largest valid segment crossing that boundary.

The answer is simply the maximum of these values.

No special handling is needed for boundaries of the original array because every valid segment is represented by some pair of adjacent runs.

## Worked Examples

### Example 1

Input:

```
7
2 2 2 1 1 2 2
```

Run lengths:

```
[3, 2, 2]
```

| Adjacent Runs | min(a,b) | Candidate Length | Best So Far |
| --- | --- | --- | --- |
| (3, 2) | 2 | 4 | 4 |
| (2, 2) | 2 | 4 | 4 |

Final answer:

```
4
```

This example shows that only neighboring runs matter. The optimal segment can be formed around either boundary.

### Example 2

Input:

```
2
2 1
```

Run lengths:

```
[1, 1]
```

| Adjacent Runs | min(a,b) | Candidate Length | Best So Far |
| --- | --- | --- | --- |
| (1, 1) | 1 | 2 | 2 |

Final answer:

```
2
```

This is the smallest possible valid input. The entire array forms the answer.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | One pass builds runs, one pass checks adjacent runs |
| Space | O(n) | In the worst case every element starts a new run |

The solution performs only a constant amount of work per array element. With `n ≤ 100000`, linear time easily fits within the time limit, and the run-length array requires at most `100000` integers, which is well within the memory limit.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    n = int(input())
    t = list(map(int, input().split()))

    runs = []
    cnt = 1

    for i in range(1, n):
        if t[i] == t[i - 1]:
            cnt += 1
        else:
            runs.append(cnt)
            cnt = 1

    runs.append(cnt)

    ans = 0
    for i in range(len(runs) - 1):
        ans = max(ans, 2 * min(runs[i], runs[i + 1]))

    return str(ans) + "\n"

# provided sample
assert run("7\n2 2 2 1 1 2 2\n") == "4\n", "sample 1"

# minimum size
assert run("2\n1 2\n") == "2\n", "minimum size"

# unequal neighboring runs
assert run("6\n1 1 1 1 2 2\n") == "4\n", "take only part of larger run"

# alternating values
assert run("4\n1 2 1 2\n") == "2\n", "many runs of length one"

# larger balanced runs
assert run("8\n1 1 1 2 2 2 2 2\n") == "6\n", "min of adjacent runs"

# off-by-one around final run
assert run("7\n1 1 2 2 2 2 1\n") == "4\n", "last run handled correctly"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 2` | `2` | Minimum valid instance |
| `1 1 1 1 2 2` | `4` | Larger run must be trimmed |
| `1 2 1 2` | `2` | Alternating runs |
| `1 1 1 2 2 2 2 2` | `6` | Uses `2 * min(a,b)` |
| `1 1 2 2 2 2 1` | `4` | Correct handling of final run |

## Edge Cases

Consider:

```
4
1 1 1 2
```

The run lengths are:

```
[3, 1]
```

The algorithm computes:

```
2 * min(3, 1) = 2
```

and returns `2`. This corresponds to the valid segment `[1,2]`. The larger run cannot contribute more than one element because the smaller run only contains one sushi.

Now consider:

```
4
1 2 1 2
```

The run lengths are:

```
[1, 1, 1, 1]
```

The candidate values are:

```
2, 2, 2
```

and the answer is `2`. The algorithm correctly avoids combining more than two consecutive runs.

Finally, consider:

```
8
1 1 1 1 2 2 2 2
```

The run lengths are:

```
[4, 4]
```

The answer is:

```
2 * min(4, 4) = 8
```

The entire array is valid, and the algorithm returns the full length.
