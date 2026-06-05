---
title: "CF 279B - Books"
description: "We have a row of books, and the time needed to read each book is known. Valera may start from any position and then read consecutive books to the right. He cannot skip books, and he only starts a book if he has enough remaining time to finish it completely."
date: "2026-06-05T08:34:56+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "brute-force", "implementation", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 279
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 171 (Div. 2)"
rating: 1400
weight: 279
solve_time_s: 98
verified: true
draft: false
---

[CF 279B - Books](https://codeforces.com/problemset/problem/279/B)

**Rating:** 1400  
**Tags:** binary search, brute force, implementation, two pointers  
**Solve time:** 1m 38s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a row of books, and the time needed to read each book is known. Valera may start from any position and then read consecutive books to the right. He cannot skip books, and he only starts a book if he has enough remaining time to finish it completely.

The task is to find the largest number of consecutive books whose total reading time does not exceed the available time `t`.

The input gives the reading times of all books. The output is a single number, the maximum length of a contiguous segment whose sum is at most `t`.

The constraints are what drive the solution. The number of books can reach `100000`, so any algorithm that checks all possible segments explicitly will be too slow. There are roughly `n² / 2` contiguous segments, which is about five billion when `n = 100000`. Even computing segment sums efficiently with prefix sums would still leave an `O(n²)` enumeration, far beyond what fits in a 2-second limit.

A linear or near-linear solution is needed. Since all reading times are positive, the problem has a useful monotonic structure that allows a sliding window approach.

One easy-to-miss edge case is when even a single book exceeds the available time.

Input:

```
3 2
3 4 5
```

Output:

```
0
```

No valid segment exists. A careless implementation that always assumes at least one book can be read would return `1`.

Another edge case occurs when the optimal segment starts in the middle.

Input:

```
5 5
10 1 1 1 1
```

Output:

```
4
```

Starting from the first book is impossible, but starting from the second book allows reading four books. Greedy approaches that only consider prefixes would fail.

A third case is when the window repeatedly needs to shrink.

Input:

```
5 5
2 2 2 2 2
```

Output:

```
2
```

Every segment of length three has sum six. An implementation that does not correctly remove books from the left side when the sum becomes too large will overcount.

## Approaches

The most direct solution is to try every starting position and extend to the right until the total reading time exceeds `t`. For each starting book, we keep adding books one by one.

This approach is correct because it explicitly evaluates every possible contiguous segment. The problem is its running time. In the worst case, such as when all reading times are `1`, each starting position may examine almost all remaining books. The total work becomes:

```
n + (n - 1) + (n - 2) + ... + 1 = O(n²)
```

With `n = 100000`, this is far too large.

The key observation is that all reading times are positive. Suppose we have a segment whose sum already exceeds `t`. Extending it further can only increase the sum, never decrease it. That means the left boundary of the segment only moves forward, never backward.

This property makes a sliding window possible. We maintain a window `[left, right]` whose sum is tracked continuously. We extend the window by moving `right`. Whenever the sum becomes too large, we move `left` forward until the sum is valid again.

Because each index enters the window once and leaves the window once, the total work is linear.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) | Too slow |
| Optimal Sliding Window | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Initialize `left = 0`, `current_sum = 0`, and `answer = 0`.
2. Iterate `right` from `0` to `n - 1`.
3. Add the reading time of the current book to `current_sum`.
4. If `current_sum` exceeds `t`, repeatedly move `left` forward and subtract those books from `current_sum` until the sum becomes at most `t`.

This step restores the invariant that the current window is a valid segment whose total reading time fits within the available time.
5. The current window length is `right - left + 1`.
6. Update `answer` with the maximum window length seen so far.
7. After processing all books, print `answer`.

### Why it works

At every moment, the window represents the longest valid segment ending at position `right` whose sum does not exceed `t`. When the sum becomes too large, removing books from the left is the only way to make the segment valid again because all reading times are positive.

Since `left` only moves forward, every possible maximal valid window is considered exactly when its right endpoint is processed. The algorithm never misses a candidate segment, and `answer` records the largest valid window length among all of them.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, t = map(int, input().split())
    a = list(map(int, input().split()))

    left = 0
    current_sum = 0
    answer = 0

    for right in range(n):
        current_sum += a[right]

        while current_sum > t:
            current_sum -= a[left]
            left += 1

        answer = max(answer, right - left + 1)

    print(answer)

if __name__ == "__main__":
    solve()
```

The variable `current_sum` stores the total reading time of the current window. Every time the right boundary expands, the new book is added to the sum.

The `while` loop is the critical part. A single removal is not always enough. For example, if the window sum is much larger than `t`, several books may need to be removed before the segment becomes valid again.

The window length is computed after the shrinking process finishes. At that moment the segment is guaranteed to satisfy the time limit.

Python integers are unbounded, so there is no overflow concern even though `t` can reach `10^9` and the window sum may temporarily become large.

The implementation uses zero-based indices internally, which keeps the length formula `right - left + 1` straightforward.

## Worked Examples

### Example 1

Input:

```
4 5
3 1 2 1
```

| right | book time | current_sum before shrinking | left after shrinking | current_sum after shrinking | window length | answer |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 3 | 3 | 0 | 3 | 1 | 1 |
| 1 | 1 | 4 | 0 | 4 | 2 | 2 |
| 2 | 2 | 6 | 1 | 3 | 2 | 2 |
| 3 | 1 | 4 | 1 | 4 | 3 | 3 |

Final answer:

```
3
```

The longest valid segment is `[1, 2, 1]`, whose total reading time is `4`.

### Example 2

Input:

```
5 5
2 2 2 2 2
```

| right | book time | current_sum before shrinking | left after shrinking | current_sum after shrinking | window length | answer |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 2 | 2 | 0 | 2 | 1 | 1 |
| 1 | 2 | 4 | 0 | 4 | 2 | 2 |
| 2 | 2 | 6 | 1 | 4 | 2 | 2 |
| 3 | 2 | 6 | 2 | 4 | 2 | 2 |
| 4 | 2 | 6 | 3 | 4 | 2 | 2 |

Final answer:

```
2
```

This trace shows why repeated shrinking is necessary. Every time a third book enters the window, the sum exceeds the limit and the leftmost book must be removed.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each index enters and leaves the window at most once |
| Space | O(1) | Only a few variables are maintained besides the input array |

The linear running time easily handles `100000` books. The memory usage is minimal and comfortably fits within the limit.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline

    n, t = map(int, input().split())
    a = list(map(int, input().split()))

    left = 0
    current_sum = 0
    answer = 0

    for right in range(n):
        current_sum += a[right]

        while current_sum > t:
            current_sum -= a[left]
            left += 1

        answer = max(answer, right - left + 1)

    print(answer)

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    result = sys.stdout.getvalue().strip()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return result

# provided sample
assert run("4 5\n3 1 2 1\n") == "3", "sample 1"

# minimum size
assert run("1 1\n1\n") == "1", "single readable book"

# no readable book
assert run("3 2\n3 4 5\n") == "0", "all books too large"

# all equal values
assert run("5 5\n2 2 2 2 2\n") == "2", "uniform values"

# optimal segment in the middle
assert run("5 5\n10 1 1 1 1\n") == "4", "skip large prefix"

# boundary exact sum
assert run("4 10\n1 2 3 4\n") == "4", "sum equals limit"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 / 1` | `1` | Minimum input size |
| `3 2 / 3 4 5` | `0` | No valid segment exists |
| `5 5 / 2 2 2 2 2` | `2` | Repeated window shrinking |
| `5 5 / 10 1 1 1 1` | `4` | Best segment starts after the first book |
| `4 10 / 1 2 3 4` | `4` | Exact equality with the time limit |

## Edge Cases

Consider the case where every book individually exceeds the available time.

Input:

```
3 2
3 4 5
```

When the first book enters the window, the sum becomes `3`, which is already larger than `2`. The algorithm immediately removes it, leaving an empty window. The same happens for the remaining books. The maximum window length never exceeds `0`, so the output is correctly `0`.

Consider a large unreadable prefix.

Input:

```
5 5
10 1 1 1 1
```

After processing the first book, the window becomes invalid and is shrunk to length zero. The algorithm then builds a new window from the later books. Eventually the window contains the last four books with sum `4`, producing the correct answer `4`. This shows that the algorithm is not biased toward segments starting near the beginning.

Consider a segment whose sum repeatedly crosses the limit.

Input:

```
5 5
2 2 2 2 2
```

Whenever a third book is added, the sum becomes `6`. The `while` loop removes books from the left until the sum returns to `4`. The window always remains valid after shrinking, and the largest valid length found is `2`. This demonstrates why the shrinking step must be a loop rather than a single `if` statement.
