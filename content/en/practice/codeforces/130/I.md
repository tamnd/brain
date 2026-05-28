---
title: "CF 130I - Array sorting"
description: "We are given an array of at most 100 integers. Every value lies between 1 and 60. The task is simply to print the array in non-decreasing order."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "*special", "sortings"]
categories: ["algorithms"]
codeforces_contest: 130
codeforces_index: "I"
codeforces_contest_name: "Unknown Language Round 4"
rating: 2300
weight: 130
solve_time_s: 107
verified: true
draft: false
---

[CF 130I - Array sorting](https://codeforces.com/problemset/problem/130/I)

**Rating:** 2300  
**Tags:** *special, sortings  
**Solve time:** 1m 47s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of at most 100 integers. Every value lies between 1 and 60. The task is simply to print the array in non-decreasing order.

At first glance this looks like a standard sorting problem, but the unusually small value range changes the structure of the problem completely. Instead of thinking about rearranging arbitrary numbers, we can think about counting how many times each value appears.

The array length is tiny. Even an $O(n^2)$ sorting algorithm such as bubble sort or insertion sort would comfortably fit inside the limits because $100^2 = 10{,}000$ operations is negligible. The value range is even smaller than the array size, only 60 distinct possible values. That opens the door to a counting-based solution running in linear time with respect to the input size.

The main edge cases come from duplicate values and from values appearing at the boundaries of the allowed range.

Consider this input:

```
5
7
7
7
7
7
```

The correct output is:

```
7 7 7 7 7
```

A careless implementation that stores values in a set would remove duplicates and print only one `7`.

Another easy mistake is forgetting to handle the smallest or largest value correctly.

```
4
1
60
1
60
```

The correct output is:

```
1 1 60 60
```

If the counting array is created with size 60 instead of 61, accessing index `60` will fail or silently produce wrong output depending on the language.

The minimum input size also matters:

```
1
42
```

The output must be:

```
42
```

Some implementations accidentally print extra spaces or forget to print anything when only one element exists.

## Approaches

The brute-force approach is to use a standard comparison sort. We repeatedly compare elements and move smaller values toward the front. Bubble sort, insertion sort, or selection sort all work because sorting by comparisons guarantees the final array order is correct.

For $n = 100$, even $O(n^2)$ complexity is fine. Bubble sort performs at most about $100 \times 100 = 10{,}000$ comparisons, which is trivial for a 2-second limit.

The interesting part of this problem is the bounded value range. Every number is between 1 and 60, which means there are only 60 possible distinct values regardless of the input size. Instead of sorting elements directly, we can count how many times each value appears.

The observation is that if we know value `x` appears `k` times, then the sorted array must contain exactly `k` copies of `x`, and all of them must appear before any larger value.

This transforms the problem into counting frequencies and reconstructing the sorted sequence in ascending order. The algorithm becomes:

1. Count occurrences of each number.
2. Iterate from 1 to 60.
3. Print each number as many times as it appeared.

This is counting sort specialized to a very small range.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) | Accepted |
| Optimal | O(n + 60) | O(60) | Accepted |

## Algorithm Walkthrough

1. Read the integer `n`, the number of elements in the array.
2. Create a frequency array `cnt` of size 61 initialized with zeros.

Index `i` will store how many times value `i` appears. We use size 61 so indices `1` through `60` are directly usable.
3. Read each array element `x`.
4. Increment `cnt[x]`.

After processing all numbers, `cnt[v]` equals the frequency of value `v` in the input array.
5. Create an empty answer list.
6. Iterate through values from `1` to `60`.
7. For each value `v`, append it to the answer list exactly `cnt[v]` times.

Since we process values in increasing order, the reconstructed sequence is automatically sorted.
8. Print the answer list as space-separated integers.

### Why it works

The algorithm maintains the invariant that after processing value `v`, the answer list contains every input element less than or equal to `v`, in sorted order, with exactly the correct multiplicities.

Because every occurrence of a value is counted exactly once and later reproduced exactly once, no element is lost or duplicated. Since values are appended in increasing order, no larger number can appear before a smaller one. That guarantees the final sequence is the sorted array.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())

cnt = [0] * 61

for _ in range(n):
    x = int(input())
    cnt[x] += 1

ans = []

for value in range(1, 61):
    ans.extend([value] * cnt[value])

print(*ans)
```

The first part reads the input and builds the frequency array. Since values range from 1 to 60 inclusive, a list of size 61 is enough. Index 0 is unused, which keeps the indexing simple and avoids subtracting 1 from every value.

The reconstruction phase iterates through values in ascending order. For each value, we append it exactly as many times as it appeared in the input. The expression:

```
[value] * cnt[value]
```

creates a list containing repeated copies of the current value.

Using `extend` instead of repeated `append` calls keeps the implementation concise.

The final `print(*ans)` automatically prints the elements space-separated, which matches the required output format. This also avoids trailing-space issues.

## Worked Examples

### Example 1

Input:

```
5
7
1
9
7
3
```

Frequency construction:

| Read value | cnt[1] | cnt[3] | cnt[7] | cnt[9] |
| --- | --- | --- | --- | --- |
| 7 | 0 | 0 | 1 | 0 |
| 1 | 1 | 0 | 1 | 0 |
| 9 | 1 | 0 | 1 | 1 |
| 7 | 1 | 0 | 2 | 1 |
| 3 | 1 | 1 | 2 | 1 |

Reconstruction:

| Current value | Frequency | Answer |
| --- | --- | --- |
| 1 | 1 | 1 |
| 2 | 0 | 1 |
| 3 | 1 | 1 3 |
| 4..6 | 0 | 1 3 |
| 7 | 2 | 1 3 7 7 |
| 8 | 0 | 1 3 7 7 |
| 9 | 1 | 1 3 7 7 9 |

Final output:

```
1 3 7 7 9
```

This trace shows how duplicates are preserved correctly because the frequency array stores counts instead of just presence.

### Example 2

Input:

```
6
60
1
60
2
1
2
```

Frequency construction:

| Read value | cnt[1] | cnt[2] | cnt[60] |
| --- | --- | --- | --- |
| 60 | 0 | 0 | 1 |
| 1 | 1 | 0 | 1 |
| 60 | 1 | 0 | 2 |
| 2 | 1 | 1 | 2 |
| 1 | 2 | 1 | 2 |
| 2 | 2 | 2 | 2 |

Reconstruction:

| Current value | Frequency | Answer |
| --- | --- | --- |
| 1 | 2 | 1 1 |
| 2 | 2 | 1 1 2 2 |
| 3..59 | 0 | 1 1 2 2 |
| 60 | 2 | 1 1 2 2 60 60 |

Final output:

```
1 1 2 2 60 60
```

This example exercises both boundaries of the allowed value range.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + 60) | Reading input takes O(n), reconstruction scans values 1 through 60 |
| Space | O(60) | The frequency array stores counts for each possible value |

With $n \le 100$, this solution easily fits within the limits. The runtime is effectively constant because the value range is fixed and tiny.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def solve():
    input = sys.stdin.readline

    n = int(input())
    cnt = [0] * 61

    for _ in range(n):
        x = int(input())
        cnt[x] += 1

    ans = []

    for value in range(1, 61):
        ans.extend([value] * cnt[value])

    print(*ans)

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    output = sys.stdout.getvalue().strip()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return output

# provided sample
assert run(
"""5
7
1
9
7
3
"""
) == "1 3 7 7 9", "sample 1"

# minimum size
assert run(
"""1
42
"""
) == "42", "minimum size"

# all equal values
assert run(
"""5
7
7
7
7
7
"""
) == "7 7 7 7 7", "all equal"

# boundary values
assert run(
"""4
1
60
1
60
"""
) == "1 1 60 60", "boundary values"

# reverse order input
assert run(
"""6
6
5
4
3
2
1
"""
) == "1 2 3 4 5 6", "reverse order"

# duplicates mixed with boundaries
assert run(
"""8
60
1
30
60
1
30
15
15
"""
) == "1 1 15 15 30 30 60 60", "mixed duplicates"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single value `42` | `42` | Minimum input size |
| All values equal to `7` | `7 7 7 7 7` | Duplicate handling |
| Values `1` and `60` | `1 1 60 60` | Boundary indexing correctness |
| Reverse ordered sequence | `1 2 3 4 5 6` | Proper sorting behavior |
| Mixed duplicates and extremes | `1 1 15 15 30 30 60 60` | Frequency reconstruction |

## Edge Cases

Consider the case where all elements are identical:

```
5
7
7
7
7
7
```

The frequency array ends with `cnt[7] = 5`. During reconstruction, the algorithm appends value `7` exactly five times. Since no other frequency is nonzero, the final output becomes:

```
7 7 7 7 7
```

This confirms duplicates are preserved instead of collapsed.

Now consider boundary values:

```
4
1
60
1
60
```

After reading input, we have:

```
cnt[1] = 2
cnt[60] = 2
```

The reconstruction loop scans from 1 through 60 inclusive. When it reaches `1`, it appends two copies. When it reaches `60`, it appends two more copies. The final result is:

```
1 1 60 60
```

Using a frequency array of size 61 is what makes index `60` valid.

Finally, consider the smallest possible input:

```
1
42
```

The algorithm increments `cnt[42]` once. Reconstruction appends one copy of `42`. The output is:

```
42
```

No special handling is needed for a single-element array because the counting approach naturally works for every valid input size.
