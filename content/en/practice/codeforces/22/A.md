---
title: "CF 22A - Second Order Statistics"
description: "We are given a small array of integers and need to find the smallest value that is strictly larger than the minimum element in the array."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "brute-force"]
categories: ["algorithms"]
codeforces_contest: 22
codeforces_index: "A"
codeforces_contest_name: "Codeforces Beta Round 22 (Div. 2 Only)"
rating: 800
weight: 22
solve_time_s: 81
verified: true
draft: false
---
[CF 22A - Second Order Statistics](https://codeforces.com/problemset/problem/22/A)

**Rating:** 800  
**Tags:** brute force  
**Solve time:** 1m 21s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a small array of integers and need to find the smallest value that is strictly larger than the minimum element in the array.

Another way to think about it is this: if we remove duplicate values, sort the remaining numbers, and look at the second element, that value is the answer. If such a value does not exist, we print `NO`.

For example, in the array:

```
1 2 2 -4
```

the minimum value is `-4`. The smallest number greater than `-4` is `1`, so the answer is `1`.

The constraints are tiny. The array length is at most 100, so even quadratic solutions are completely safe. An `O(n^2)` algorithm would perform at most 10,000 comparisons, which is negligible for a 2 second time limit. Memory usage is also irrelevant here because the input is very small.

The tricky part is not performance, it is handling duplicates correctly. The problem asks for the smallest number strictly greater than the minimum, not the second element after sorting the full array.

Consider this input:

```
5
1 1 1 2 3
```

The correct answer is:

```
2
```

If we simply sort the array and take the element at index 1, we would get `1`, which is wrong because duplicates of the minimum do not count.

Another important edge case happens when all values are equal:

```
4
7 7 7 7
```

There is no number larger than the minimum, so the correct output is:

```
NO
```

A careless implementation might still try to access a second element after removing duplicates and crash, or incorrectly print `7`.

Negative values also matter:

```
5
-10 -5 -10 -3
```

The minimum is `-10`, and the smallest value larger than it is `-5`. Sorting logic must work correctly for negative numbers as well.

## Approaches

The most direct brute-force idea is to compare every element against every other element. We can first find the minimum value, then scan the array again and search for the smallest number greater than that minimum. This already works in linear time.

A more literal brute-force version would generate all distinct values, sort them, and take the second one. Since the array contains at most 100 elements, even sorting is perfectly fine. Sorting 100 numbers costs roughly `100 log 100`, which is tiny.

The interesting part of the problem is understanding what "second order statistic" really means here. It does not mean the second position in the sorted original array. It means the second distinct value after sorting.

That observation immediately suggests a clean solution:

1. Remove duplicates.
2. Sort the remaining values.
3. If fewer than two distinct values exist, print `NO`.
4. Otherwise print the second value.

The brute-force works because the input is tiny, but the distinct-value observation makes the implementation much cleaner and less error-prone.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) | Accepted |
| Optimal | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the integer `n` and the array values.
2. Convert the array into a set to remove duplicates.

This step is essential because repeated occurrences of the minimum value should not affect the answer.
3. Convert the set back into a list and sort it in increasing order.

After sorting, the first element is the minimum distinct value and the second element, if it exists, is the answer we need.
4. Check how many distinct values exist.

If the size is smaller than 2, there is no valid second order statistic.
5. If there are at least two distinct values, print the element at index `1`.

Since the array is sorted, this is the smallest value strictly greater than the minimum.

### Why it works

After removing duplicates, every remaining number represents one distinct value from the original array. Sorting these values places them in increasing order. The first value is the minimum distinct element, and the next value is exactly the smallest distinct element larger than it. Since the problem definition matches this property directly, the algorithm always produces the correct answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
arr = list(map(int, input().split()))

distinct = sorted(set(arr))

if len(distinct) < 2:
    print("NO")
else:
    print(distinct[1])
```

The solution starts by reading the array normally using fast input. Fast I/O is not actually necessary for these constraints, but it is standard practice in competitive programming.

The key line is:

```
distinct = sorted(set(arr))
```

The `set` removes duplicate values automatically. This prevents repeated minimum values from incorrectly becoming the answer. After that, `sorted` arranges the remaining numbers in increasing order.

The length check is important because arrays like:

```
5 5 5 5
```

produce only one distinct value after duplicate removal. Accessing index `1` without checking would cause an error.

Finally, if at least two distinct values exist, the second smallest distinct number is exactly `distinct[1]`.

## Worked Examples

### Example 1

Input:

```
4
1 2 2 -4
```

| Step | Value |
| --- | --- |
| Original array | `[1, 2, 2, -4]` |
| After removing duplicates | `{1, 2, -4}` |
| After sorting | `[-4, 1, 2]` |
| Second distinct value | `1` |

The minimum distinct value is `-4`. The next larger distinct value is `1`, which matches the required definition.

### Example 2

Input:

```
5
7 7 7 7 7
```

| Step | Value |
| --- | --- |
| Original array | `[7, 7, 7, 7, 7]` |
| After removing duplicates | `{7}` |
| After sorting | `[7]` |
| Number of distinct values | `1` |
| Output | `NO` |

This example demonstrates the important edge case where no second distinct value exists.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting the distinct values dominates the runtime |
| Space | O(n) | The set and sorted list store distinct elements |

With `n ≤ 100`, this solution easily fits within the limits. Even much slower approaches would still pass comfortably.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline

    n = int(input())
    arr = list(map(int, input().split()))

    distinct = sorted(set(arr))

    if len(distinct) < 2:
        print("NO")
    else:
        print(distinct[1])

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
assert run("4\n1 2 2 -4\n") == "1", "sample 1"

# minimum size input
assert run("1\n5\n") == "NO", "single element"

# all values equal
assert run("5\n7 7 7 7 7\n") == "NO", "all equal"

# negative numbers
assert run("5\n-10 -5 -10 -3 -5\n") == "-5", "negative values"

# already sorted distinct values
assert run("4\n1 2 3 4\n") == "2", "simple increasing"

# duplicates of minimum
assert run("6\n1 1 1 2 3 4\n") == "2", "duplicate minimum"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 5` | `NO` | Minimum possible array size |
| `5 / 7 7 7 7 7` | `NO` | All values identical |
| `5 / -10 -5 -10 -3 -5` | `-5` | Correct handling of negative numbers |
| `4 / 1 2 3 4` | `2` | Basic distinct increasing case |
| `6 / 1 1 1 2 3 4` | `2` | Duplicates of the minimum are ignored |

## Edge Cases

Consider the case where all values are equal:

```
4
7 7 7 7
```

The algorithm converts the array into a set:

```
{7}
```

After sorting:

```
[7]
```

The number of distinct values is only 1, so the algorithm prints:

```
NO
```

This is correct because no value is strictly greater than the minimum.

Now consider repeated minimum values:

```
6
1 1 1 2 3 4
```

The minimum value appears multiple times. After duplicate removal:

```
{1, 2, 3, 4}
```

Sorting gives:

```
[1, 2, 3, 4]
```

The algorithm outputs `2`, which is the smallest value strictly larger than `1`. A naive approach that simply sorted the original array and took the second element would incorrectly return `1`.

Finally, consider negative numbers:

```
5
-10 -5 -10 -3
```

After removing duplicates and sorting:

```
[-10, -5, -3]
```

The second distinct value is `-5`. The algorithm works correctly because integer sorting naturally handles negative values.
