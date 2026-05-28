---
title: "CF 27A - Next Test"
description: "We are given the indices of tests that already exist in the system. Every index is a positive integer, and all indices are distinct. The task is to find the smallest positive integer that does not appear in the list."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "sortings"]
categories: ["algorithms"]
codeforces_contest: 27
codeforces_index: "A"
codeforces_contest_name: "Codeforces Beta Round 27 (Codeforces format, Div. 2)"
rating: 1200
weight: 27
solve_time_s: 73
verified: true
draft: false
---
[CF 27A - Next Test](https://codeforces.com/problemset/problem/27/A)

**Rating:** 1200  
**Tags:** implementation, sortings  
**Solve time:** 1m 13s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given the indices of tests that already exist in the system. Every index is a positive integer, and all indices are distinct. The task is to find the smallest positive integer that does not appear in the list.

This is the classic "smallest missing positive" idea, but the constraints are small enough that we do not need any advanced data structures. The number of existing tests is at most 3000, and every index is also at most 3000. Even an $O(n^2)$ solution performs around nine million operations in the worst case, which easily fits within a 2 second limit in Python.

The main difficulty is not performance, it is handling the search correctly. The answer is not the largest value plus one unless every smaller positive integer already exists.

Consider this input:

```
3
1 7 2
```

The correct answer is `3`, not `8`. The next index must be the smallest unused positive number.

Another easy mistake is starting the search from `0`. Test indices are positive integers only.

Example:

```
4
2 3 4 5
```

The correct answer is `1` because the smallest positive integer is missing immediately.

A third edge case appears when all values from `1` to `n` are present.

Example:

```
5
1 2 3 4 5
```

The answer becomes `6`. A careless implementation that only checks numbers already present in the array might never print anything.

## Approaches

The brute-force approach is straightforward. Start from `1` and repeatedly check whether the current number exists in the array. The first number that is not found is the answer.

To test whether a value exists, we can scan the entire array linearly. Since there can be at most 3000 candidate values and each search may inspect all 3000 elements, the worst-case complexity becomes $O(n^2)$.

For this problem, even that is fast enough. Around nine million comparisons is acceptable in Python.

Still, the problem structure gives us a cleaner solution. We only care whether a number exists, not where it appears. That means membership queries are the core operation. A set supports membership checks in average $O(1)$ time.

The observation is simple: once the values are stored in a set, we can test numbers `1, 2, 3, ...` one by one until we find the first missing value.

The answer is guaranteed to be at most `n + 1`. If there are `n` distinct positive integers and all numbers from `1` through `n` exist, then `n + 1` is missing. This lets us stop after checking at most `n + 1` candidates.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^2)$ | $O(1)$ | Accepted |
| Optimal | $O(n)$ average | $O(n)$ | Accepted |

## Algorithm Walkthrough

1. Read the integer `n` and the list of existing test indices.
2. Store all indices inside a set.

A set allows fast membership checks, which is exactly what we need when asking "does this number already exist?"
3. Iterate through integers from `1` to `n + 1`.

The answer cannot exceed `n + 1`. If every value from `1` through `n` is present, then the smallest missing positive must be `n + 1`.
4. For each integer `x`, check whether it exists in the set.

If `x` is absent, print `x` immediately and stop.
5. The first missing number encountered during the scan is the required next test index.

### Why it works

The algorithm checks positive integers in increasing order. Before reaching some value `x`, every smaller positive integer has already been verified to exist in the set. When `x` is the first value not found, it is exactly the smallest positive integer missing from the array.

Because the scan proceeds in order and stops at the first gap, the algorithm cannot skip a smaller valid answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

# solution

def solve():
    n = int(input())
    arr = list(map(int, input().split()))

    used = set(arr)

    for x in range(1, n + 2):
        if x not in used:
            print(x)
            return

solve()
```

The first step reads the input array and converts it into a set named `used`. This transformation is the key optimization because membership checks become constant time on average.

The loop runs from `1` through `n + 1` inclusive. The upper bound is important. If all numbers from `1` to `n` are present, the answer must be `n + 1`. Using `range(1, n + 1)` would miss that case.

The moment a missing value is found, the function prints it and returns immediately. There is no need to continue scanning because we process numbers in increasing order.

No integer overflow issues exist here because all values are very small. The implementation is mostly about careful boundaries and correct stopping conditions.

## Worked Examples

### Example 1

Input:

```
3
1 7 2
```

| Current x | Exists in set? | Action |
| --- | --- | --- |
| 1 | Yes | Continue |
| 2 | Yes | Continue |
| 3 | No | Print 3 |

The set contains `{1, 2, 7}`. The algorithm checks numbers in increasing order and immediately stops at the first gap. This demonstrates the core invariant: every smaller positive integer has already been confirmed present before the answer is printed.

### Example 2

Input:

```
5
1 2 3 4 5
```

| Current x | Exists in set? | Action |
| --- | --- | --- |
| 1 | Yes | Continue |
| 2 | Yes | Continue |
| 3 | Yes | Continue |
| 4 | Yes | Continue |
| 5 | Yes | Continue |
| 6 | No | Print 6 |

This trace shows why the loop must continue until `n + 1`. All smaller positive integers exist, so the first missing value appears immediately after the largest consecutive prefix.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ average | Building the set and scanning up to `n + 1` values |
| Space | $O(n)$ | The set stores all indices |

With `n ≤ 3000`, this solution is comfortably within the limits. Even the quadratic approach would pass, but the set-based solution is cleaner and scales better conceptually.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline

    n = int(input())
    arr = list(map(int, input().split()))

    used = set(arr)

    for x in range(1, n + 2):
        if x not in used:
            print(x)
            return

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()

    backup_stdout = sys.stdout
    sys.stdout = out

    solve()

    sys.stdout = backup_stdout
    return out.getvalue().strip()

# provided sample
assert run("3\n1 7 2\n") == "3", "sample 1"

# minimum size input
assert run("1\n1\n") == "2", "single existing value"

# missing 1
assert run("4\n2 3 4 5\n") == "1", "smallest positive missing immediately"

# consecutive sequence
assert run("5\n1 2 3 4 5\n") == "6", "answer is n + 1"

# unordered values
assert run("6\n4 2 1 6 3 7\n") == "5", "handles unsorted input"

# maximum-style boundary pattern
assert run("3\n3000 2999 1\n") == "2", "large values do not matter"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 1` | `2` | Smallest valid input |
| `4 / 2 3 4 5` | `1` | Missing smallest positive |
| `5 / 1 2 3 4 5` | `6` | Answer becomes `n + 1` |
| `6 / 4 2 1 6 3 7` | `5` | Input order is irrelevant |
| `3 / 3000 2999 1` | `2` | Large unrelated values do not affect result |

## Edge Cases

Consider the case where `1` is missing immediately.

Input:

```
4
2 3 4 5
```

The set becomes `{2, 3, 4, 5}`. The algorithm starts checking from `1`. Since `1` is not present, it prints `1` immediately. This handles the smallest possible answer correctly.

Now consider the case where all values from `1` through `n` exist.

Input:

```
5
1 2 3 4 5
```

The algorithm checks `1`, `2`, `3`, `4`, and `5`, all of which exist in the set. It then checks `6`, which is missing, so it prints `6`. This is why the loop must run until `n + 1`.

Finally, consider unordered input with gaps.

Input:

```
6
7 3 1 2 6 4
```

The set becomes `{1, 2, 3, 4, 6, 7}`. The checks proceed as follows:

- `1` exists
- `2` exists
- `3` exists
- `4` exists
- `5` does not exist

The algorithm prints `5`. The original order never matters because the set stores only membership information.
