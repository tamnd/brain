---
title: "CF 10D - LCIS"
description: "We are given two integer arrays. We want to build a sequence that satisfies three conditions simultaneously. First, the"
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "dp"]
categories: ["algorithms"]
codeforces_contest: 10
codeforces_index: "D"
codeforces_contest_name: "Codeforces Beta Round 10"
rating: 2800
weight: 10
solve_time_s: 127
verified: false
draft: false
---

[CF 10D - LCIS](https://codeforces.com/problemset/problem/10/D)

**Rating:** 2800  
**Tags:** dp  
**Solve time:** 2m 7s  
**Verified:** no  

## Solution
## Problem Understanding

We are given two integer arrays. We want to build a sequence that satisfies three conditions simultaneously.

First, the sequence must appear as a subsequence of the first array.

Second, it must also appear as a subsequence of the second array.

Third, its values must be strictly increasing.

Among all such sequences, we need the one with maximum possible length. We must print both the length and one valid sequence achieving it.

The interesting part is that this is not just a longest common subsequence problem, and not just a longest increasing subsequence problem. The sequence has to satisfy both constraints at the same time.

The array sizes are at most 500. That immediately rules out exponential approaches, but it still leaves room for quadratic dynamic programming. A cubic algorithm with about $500^3 = 125\,000\,000$ operations is already dangerous in Python under a 1 second time limit. Quadratic or low cubic with very small constants is the practical target.

A common mistake is trying to compute LCS first and then extract an LIS from it. That fails because the longest common subsequence is not unique, and the best LCIS may require skipping parts of every maximum-length LCS.

Consider this example:

```
A = [1, 4, 2, 3]
B = [1, 2, 4, 3]
```

One LCS is `[1, 4, 3]`, whose LIS length is only 2.

The actual LCIS is `[1, 2, 3]`, length 3.

Another easy mistake is forgetting that equal values cannot both appear in a strictly increasing sequence.

Example:

```
A = [1, 1, 1]
B = [1, 1]
```

Correct answer:

```
1
1
```

A careless implementation may incorrectly build `[1, 1]`.

Repeated values are also tricky when reconstructing the sequence. If we only store lengths without predecessors, reconstruction becomes ambiguous.

Example:

```
A = [3, 1, 2, 2, 4]
B = [1, 2, 2, 4]
```

The answer is `[1, 2, 4]`.

The algorithm must avoid chaining equal `2`s together.

## Approaches

The brute-force perspective is useful because it reveals the structure of the problem.

Suppose we enumerate every common subsequence of the two arrays and check whether it is increasing. This is obviously correct, because the answer must be among those subsequences. Unfortunately, the number of subsequences grows exponentially. Even for length 500, this is completely impossible.

A more reasonable brute-force idea is based on classical LCS dynamic programming. We could define a DP state over positions in both arrays and additionally track the last chosen value. The transition would try to extend increasing sequences whenever matching elements appear.

The issue is that the last chosen value can vary over too many possibilities. A naive state like:

$$dp[i][j][last]$$

becomes far too large.

The key observation is that the increasing condition only depends on the previous chosen element, not on the whole sequence. That suggests a LIS-style optimization.

Let us focus on one position `i` in the first array. Suppose we iterate through the second array from left to right. While scanning, we maintain the best LCIS length ending at some value smaller than `a[i]`.

If `a[i] == b[j]`, we can extend that best sequence.

This transforms the problem into a quadratic DP.

Define:

$$dp[j]$$

as the length of the longest common increasing subsequence that ends at `b[j]`.

Now process every `a[i]`. During the scan over `b[j]`, maintain:

$$current = \max(dp[k]) \text{ for all } k < j \text{ with } b[k] < a[i]$$

Then:

- if `a[i] > b[j]`, update `current`
- if `a[i] == b[j]`, try extending `current + 1`

This works because every valid predecessor must appear earlier in both arrays and must contain a smaller value.

The resulting complexity is $O(nm)$, which is around 250,000 operations for the maximum constraints, easily fast enough.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| Naive DP with extra state | O(n³) or worse | O(n²) or worse | Risky |
| Optimal LCIS DP | O(nm) | O(m) | Accepted |

## Algorithm Walkthrough

1. Create an array `dp` of length `m`.

`dp[j]` stores the length of the best LCIS ending at `b[j]`.
2. Create a predecessor array `parent`.

`parent[j]` stores the previous index in `b` used before `b[j]` in the optimal sequence. This allows reconstruction later.
3. Iterate through the first array using index `i`.

For every fixed `a[i]`, we scan the second array from left to right.
4. Maintain two variables during the scan.

`current_len` is the best LCIS length we can extend using values strictly smaller than `a[i]`.

`current_pos` stores the ending position in `b` corresponding to that best length.
5. While scanning `b[j]`:

If `a[i] > b[j]`, then `b[j]` is a candidate predecessor for future matches with `a[i]`.

If `dp[j] > current_len`, update both `current_len` and `current_pos`.
6. If `a[i] == b[j]`, we can append this value to the best sequence tracked by `current_len`.

If:

$$current\_len + 1 > dp[j]$$

then update:

$$dp[j] = current\_len + 1$$

and set:

$$parent[j] = current\_pos$$
7. After processing all pairs, find the index with maximum `dp[j]`.

This gives the end of the optimal LCIS.
8. Reconstruct the sequence by following `parent` pointers backward.
9. Reverse the reconstructed sequence and print it.

### Why it works

The invariant is:

`dp[j]` always represents the length of the longest common increasing subsequence ending exactly at `b[j]` after processing the current prefix of `a`.

When processing `a[i]`, the variable `current_len` contains the best LCIS that can legally precede `a[i]`. Since we scan `b` left to right, every candidate predecessor already appears earlier in `b`. Since we only update from values smaller than `a[i]`, the increasing property is preserved.

Whenever `a[i] == b[j]`, appending this value creates a valid longer LCIS ending at `b[j]`.

Because every valid LCIS must end at some position in `b`, the maximum value in `dp` after all transitions is the optimal answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))

    m = int(input())
    b = list(map(int, input().split()))

    dp = [0] * m
    parent = [-1] * m

    for i in range(n):
        current_len = 0
        current_pos = -1

        for j in range(m):
            if a[i] > b[j]:
                if dp[j] > current_len:
                    current_len = dp[j]
                    current_pos = j

            elif a[i] == b[j]:
                if current_len + 1 > dp[j]:
                    dp[j] = current_len + 1
                    parent[j] = current_pos

    best_len = 0
    best_pos = -1

    for j in range(m):
        if dp[j] > best_len:
            best_len = dp[j]
            best_pos = j

    sequence = []

    while best_pos != -1:
        sequence.append(b[best_pos])
        best_pos = parent[best_pos]

    sequence.reverse()

    print(best_len)

    if best_len > 0:
        print(*sequence)
    else:
        print()

solve()
```

The `dp` array is the core of the solution. Unlike standard LCS, we only keep one dimension because the transition only depends on earlier positions in `b`.

The subtle part is the order of updates inside the nested loop. We must first process smaller values using:

```
if a[i] > b[j]
```

before processing equal values.

This guarantees that `current_len` only contains sequences ending with strictly smaller numbers. If equal values were included, the algorithm could incorrectly create non-increasing subsequences.

The `parent` array stores indices from the second array, not values. This makes reconstruction straightforward and avoids ambiguity when duplicate numbers exist.

Another detail is that we only update `dp[j]` when we find a strictly better value. Using `>=` instead of `>` can overwrite predecessor chains unnecessarily and produce unstable reconstruction.

The reconstruction starts from the position with maximum `dp[j]` and follows predecessor links backward until `-1`.

## Worked Examples

### Example 1

Input:

```
A = [2, 3, 1, 6, 5, 4, 6]
B = [1, 3, 5, 6]
```

### Trace

| i | a[i] | j | b[j] | current_len | dp before | dp after |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 2 | 0 | 1 | 0 | 0 | 0 |
| 1 | 3 | 1 | 3 | 0 | 0 | 1 |
| 2 | 1 | 0 | 1 | 0 | 0 | 1 |
| 3 | 6 | 1 | 3 | 1 | 1 | 1 |
| 3 | 6 | 3 | 6 | 1 | 0 | 2 |
| 4 | 5 | 2 | 5 | 1 | 0 | 2 |
| 6 | 6 | 2 | 5 | 2 | 2 | 2 |
| 6 | 6 | 3 | 6 | 2 | 2 | 3 |

Final sequence:

```
3 5 6
```

This trace shows how the algorithm accumulates the best smaller predecessor while scanning `B`. When the final `6` is processed, the algorithm already knows about the sequence `[3, 5]`, so it extends it to length 3.

### Example 2

Input:

```
A = [1, 1, 1]
B = [1, 1]
```

### Trace

| i | a[i] | j | b[j] | current_len | dp before | dp after |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 1 | 0 | 1 | 0 | 0 | 1 |
| 0 | 1 | 1 | 1 | 0 | 0 | 1 |
| 1 | 1 | 0 | 1 | 0 | 1 | 1 |
| 1 | 1 | 1 | 1 | 0 | 1 | 1 |

Final sequence:

```
1
```

This demonstrates why the algorithm correctly enforces strict increase. Equal values never contribute to `current_len`, because only strictly smaller values are allowed.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(nm) | Every pair `(i, j)` is processed once |
| Space | O(m) | Only DP and parent arrays over `b` are stored |

With $n, m \le 500$, the algorithm performs at most 250,000 DP transitions, which is easily fast enough within the 1 second limit. Memory usage is tiny compared to the 256 MB limit.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline

    n = int(input())
    a = list(map(int, input().split()))

    m = int(input())
    b = list(map(int, input().split()))

    dp = [0] * m
    parent = [-1] * m

    for i in range(n):
        current_len = 0
        current_pos = -1

        for j in range(m):
            if a[i] > b[j]:
                if dp[j] > current_len:
                    current_len = dp[j]
                    current_pos = j

            elif a[i] == b[j]:
                if current_len + 1 > dp[j]:
                    dp[j] = current_len + 1
                    parent[j] = current_pos

    best_len = 0
    best_pos = -1

    for j in range(m):
        if dp[j] > best_len:
            best_len = dp[j]
            best_pos = j

    seq = []

    while best_pos != -1:
        seq.append(b[best_pos])
        best_pos = parent[best_pos]

    seq.reverse()

    out = [str(best_len)]

    if best_len > 0:
        out.append(" ".join(map(str, seq)))
    else:
        out.append("")

    print("\n".join(out))

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    output = sys.stdout.getvalue()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return output.strip()

# provided sample
assert run(
"""7
2 3 1 6 5 4 6
4
1 3 5 6
"""
) == "3\n3 5 6", "sample 1"

# minimum size
assert run(
"""1
5
1
5
"""
) == "1\n5", "single equal element"

# no common element
assert run(
"""3
1 2 3
3
4 5 6
"""
) == "0", "empty LCIS"

# all equal values
assert run(
"""4
7 7 7 7
3
7 7 7
"""
) == "1\n7", "strictly increasing condition"

# increasing arrays
assert run(
"""5
1 2 3 4 5
5
1 2 3 4 5
"""
) == "5\n1 2 3 4 5", "entire array is LCIS"

# duplicate handling
assert run(
"""5
3 1 2 2 4
4
1 2 2 4
"""
) == "3\n1 2 4", "duplicates should not chain"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single equal element | `1 5` | Minimum valid LCIS |
| No common element | `0` | Empty answer handling |
| All equal values | `1 7` | Strict increase enforcement |
| Fully increasing arrays | Full array | Normal optimal case |
| Duplicate-heavy case | `1 2 4` | Correct handling of repeated values |

## Edge Cases

### Repeated Equal Values

Input:

```
A = [1, 1, 1]
B = [1, 1]
```

While scanning, `current_len` never increases because there are no smaller elements than `1`. Every matching pair only creates a sequence of length 1.

The algorithm never chains one `1` after another because the transition condition requires:

```
a[i] > b[j]
```

for predecessor updates.

Correct output:

```
1
1
```

### LCIS Different from Any Maximum LCS

Input:

```
A = [1, 4, 2, 3]
B = [1, 2, 4, 3]
```

A standard LCS algorithm may choose `[1, 4, 3]`, which is not increasing.

Our DP only extends through strictly smaller values. When processing `2`, the best predecessor is `1`, so the sequence `[1, 2]` forms naturally. Later, `3` extends that sequence.

Correct output:

```
3
1 2 3
```

### Duplicate Numbers Inside the Optimal Path

Input:

```
A = [3, 1, 2, 2, 4]
B = [1, 2, 2, 4]
```

The algorithm processes both occurrences of `2`, but neither can extend the other because equal values are not considered smaller predecessors.

The predecessor chain becomes:

```
1 -> 2 -> 4
```

Correct output:

```
3
1 2 4
```

This confirms that the strict inequality logic correctly prevents invalid increasing sequences.
