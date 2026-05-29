---
title: "CF 276C - Little Girl and Maximum Sum"
description: "We are given an array and several range queries. Each query asks for the sum of all elements between two indices."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "greedy", "implementation", "sortings"]
categories: ["algorithms"]
codeforces_contest: 276
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 169 (Div. 2)"
rating: 1500
weight: 276
solve_time_s: 102
verified: true
draft: false
---

[CF 276C - Little Girl and Maximum Sum](https://codeforces.com/problemset/problem/276/C)

**Rating:** 1500  
**Tags:** data structures, greedy, implementation, sortings  
**Solve time:** 1m 42s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array and several range queries. Each query asks for the sum of all elements between two indices. The unusual part is that we are allowed to rearrange the array before answering the queries, and we want the total of all query answers to become as large as possible.

The queries themselves never change. Only the positions of the array values can change. That means the real question is: which positions are used most often across all ranges, and which numbers should be placed there?

Suppose an index appears in many queries. Any value placed at that index contributes repeatedly to the final total. Large numbers should clearly go to heavily used positions, while small numbers can go to positions that are rarely used.

The constraints are large enough that a direct simulation of every query over every element is impossible. Both `n` and `q` can reach `2 * 10^5`. An `O(n * q)` solution would require about `4 * 10^10` operations in the worst case, far beyond what fits in one second. Even `O(n^2)` is completely unrealistic. The target complexity is roughly `O(n log n + q)` or something similar.

A subtle point is that the same index may belong to many overlapping ranges. A careless implementation that processes every query by incrementing all covered positions individually would already be too slow. For example:

```
5 3
1 2 3 4 5
1 5
1 5
1 5
```

Every position is covered three times. Updating all positions for every query takes `O(nq)` time.

Another easy mistake is forgetting that rearrangement changes only the values, not the query structure. Consider:

```
3 2
1 100 2
1 1
2 3
```

The frequencies of positions are:

```
index 1 -> used once
index 2 -> used once
index 3 -> used once
```

All positions are equally important, so rearranging changes nothing. The answer is always:

```
1 + (100 + 2) = 103
```

A greedy approach that tries to move the largest number into the longest range would fail because ranges overlap through positions, not as whole intervals.

There is also a risk of integer overflow in languages with 32-bit integers. Suppose every value is `2 * 10^5`, and every position participates in `2 * 10^5` queries. The total can exceed `10^15`. Python handles this automatically, but C++ solutions must use `long long`.

## Approaches

The brute-force idea is straightforward. For every possible rearrangement of the array, compute the total contribution of all queries and keep the maximum. This is obviously correct because it checks every arrangement. Unfortunately, there are `n!` permutations, which becomes impossible almost immediately.

A more reasonable brute-force attempt avoids permutations and instead computes how many times each position is used. Once we know the usage count of every index, the total answer becomes:

```
sum(a[i] * freq[i])
```

where `freq[i]` is the number of queries covering position `i`.

The naive way to compute frequencies is to process every query and increment all positions inside the interval:

```
for l, r:
    for i in range(l, r + 1):
        freq[i] += 1
```

This works logically, but in the worst case each query spans the entire array. With `2 * 10^5` queries and `2 * 10^5` positions, this becomes `4 * 10^10` updates.

The key observation is that range increments can be processed with a difference array. Instead of incrementing every position inside `[l, r]`, we record:

```
diff[l] += 1
diff[r + 1] -= 1
```

After processing all queries, a prefix sum reconstructs the actual frequencies.

Once frequencies are known, the remaining step becomes a greedy matching problem. Each position contributes:

```
value * usage_count
```

To maximize the total sum, the largest values should be paired with the largest frequencies. This is a classic rearrangement inequality situation. Sorting both arrays in the same order gives the maximum possible dot product.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force frequency updates | O(nq) | O(n) | Too slow |
| Optimal difference array + sorting | O(n log n + q) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the array values.
2. Create a difference array of size `n + 1`, initialized with zeros.
3. For every query `[l, r]`, increment `diff[l - 1]` by `1`.

We convert to zero-based indexing because Python lists use zero-based positions.
4. If `r < n`, decrement `diff[r]` by `1`.

This marks the end of the range contribution. Later prefix sums will spread the increment across the whole interval.
5. Build the frequency array using prefix sums.

Each position now stores how many queries include that index.
6. Sort the original array.
7. Sort the frequency array.
8. Multiply corresponding elements and add them together.

The largest number is paired with the largest frequency, the second largest with the second largest, and so on.
9. Print the final sum.

### Why it works

Each array position contributes independently to the final answer. If position `i` is used `freq[i]` times, then placing value `x` there adds `x * freq[i]` to the total.

The only remaining decision is how to assign values to frequencies. Suppose we have two values `a <= b` and two frequencies `x <= y`. Compare the two assignments:

```
a*x + b*y
a*y + b*x
```

Their difference is:

```
(a*x + b*y) - (a*y + b*x)
= (b - a)(y - x)
```

This is nonnegative, so matching larger values with larger frequencies is always at least as good. Repeating this argument across all pairs proves that sorting both arrays in the same order gives the optimal arrangement.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, q = map(int, input().split())
    arr = list(map(int, input().split()))

    diff = [0] * (n + 1)

    for _ in range(q):
        l, r = map(int, input().split())

        diff[l - 1] += 1

        if r < n:
            diff[r] -= 1

    freq = [0] * n
    current = 0

    for i in range(n):
        current += diff[i]
        freq[i] = current

    arr.sort()
    freq.sort()

    ans = 0

    for a, f in zip(arr, freq):
        ans += a * f

    print(ans)

solve()
```

The difference array is the core optimization. Instead of touching every element inside a query range, we mark only where the range starts and where it stops contributing. The prefix sum reconstruction later expands those markers into full frequencies.

The condition `if r < n:` is easy to get wrong. Since we use zero-based indexing internally, decrementing at `diff[r]` correctly ends the interval after index `r - 1`. When `r == n`, the interval reaches the last position, so there is no valid index after it inside the array.

Sorting both arrays before multiplication implements the greedy proof directly. Without sorting frequencies, large numbers could end up assigned to rarely used positions.

The final answer may become very large. Python integers expand automatically, so there is no overflow issue here.

## Worked Examples

### Sample 1

Input:

```
3 3
5 3 2
1 2
2 3
1 3
```

### Building frequencies

| Query | diff after update |
| --- | --- |
| [1,2] | [1, 0, -1, 0] |
| [2,3] | [1, 1, -1, 0] |
| [1,3] | [2, 1, -1, 0] |

### Prefix sum reconstruction

| Index | Running sum | Frequency |
| --- | --- | --- |
| 0 | 2 | 2 |
| 1 | 3 | 3 |
| 2 | 2 | 2 |

So the frequencies are:

```
[2, 3, 2]
```

### Sorting and pairing

| Sorted values | Sorted frequencies | Contribution |
| --- | --- | --- |
| 2 | 2 | 4 |
| 3 | 2 | 6 |
| 5 | 3 | 15 |

Final answer:

```
4 + 6 + 15 = 25
```

This example demonstrates the main greedy idea. The value `5` is placed at the most frequently used position.

### Custom Example

Input:

```
5 2
1 2 3 4 5
1 3
2 5
```

### Building frequencies

| Query | diff after update |
| --- | --- |
| [1,3] | [1, 0, 0, -1, 0, 0] |
| [2,5] | [1, 1, 0, -1, 0, 0] |

### Prefix sum reconstruction

| Index | Running sum | Frequency |
| --- | --- | --- |
| 0 | 1 | 1 |
| 1 | 2 | 2 |
| 2 | 2 | 2 |
| 3 | 1 | 1 |
| 4 | 1 | 1 |

Sorted values:

```
[1, 2, 3, 4, 5]
```

Sorted frequencies:

```
[1, 1, 1, 2, 2]
```

### Final pairing

| Value | Frequency | Contribution |
| --- | --- | --- |
| 1 | 1 | 1 |
| 2 | 1 | 2 |
| 3 | 1 | 3 |
| 4 | 2 | 8 |
| 5 | 2 | 10 |

Final answer:

```
24
```

This trace shows how overlapping intervals naturally produce higher frequencies in the middle positions.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n + q) | Difference array processing is linear, sorting dominates |
| Space | O(n) | Arrays for values, differences, and frequencies |

The largest input size is `2 * 10^5`, and sorting that many elements is easily fast enough within one second in Python. The memory usage also stays comfortably within limits because all auxiliary arrays are linear in size.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline

    n, q = map(int, input().split())
    arr = list(map(int, input().split()))

    diff = [0] * (n + 1)

    for _ in range(q):
        l, r = map(int, input().split())

        diff[l - 1] += 1

        if r < n:
            diff[r] -= 1

    freq = [0] * n
    current = 0

    for i in range(n):
        current += diff[i]
        freq[i] = current

    arr.sort()
    freq.sort()

    ans = 0

    for a, f in zip(arr, freq):
        ans += a * f

    print(ans)

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    out = io.StringIO()
    backup_stdout = sys.stdout
    sys.stdout = out

    solve()

    sys.stdout = backup_stdout

    return out.getvalue().strip()

# provided sample
assert run(
"""3 3
5 3 2
1 2
2 3
1 3
"""
) == "25", "sample 1"

# minimum size
assert run(
"""1 1
7
1 1
"""
) == "7", "minimum case"

# all equal values
assert run(
"""4 2
5 5 5 5
1 2
3 4
"""
) == "20", "all equal values"

# full overlap
assert run(
"""5 3
1 2 3 4 5
1 5
1 5
1 5
"""
) == "45", "all positions same frequency"

# off-by-one boundary
assert run(
"""5 1
1 2 3 4 5
5 5
"""
) == "5", "last position only"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single element array | 7 | Minimum valid input |
| All values equal | 20 | Sorting should not affect correctness |
| All queries cover full array | 45 | Uniform frequencies across positions |
| Query `[5,5]` | 5 | Correct handling of last index boundary |

## Edge Cases

Consider the case where every query spans the entire array:

```
5 3
1 2 3 4 5
1 5
1 5
1 5
```

The difference array updates become:

```
diff[0] += 1 three times
```

No decrement happens because every query ends at `n`. The reconstructed frequencies are:

```
[3, 3, 3, 3, 3]
```

Since all frequencies are identical, any ordering produces the same answer:

```
3 * (1 + 2 + 3 + 4 + 5) = 45
```

This confirms the boundary condition `if r < n:` is handled correctly.

Now consider a case where only the last index is queried:

```
5 1
1 2 3 4 5
5 5
```

The updates are:

```
diff[4] += 1
```

Again no decrement is needed because the range ends at the array boundary.

The prefix sums produce:

```
[0, 0, 0, 0, 1]
```

After sorting:

```
values      = [1, 2, 3, 4, 5]
frequencies = [0, 0, 0, 0, 1]
```

The answer becomes:

```
5
```

This case catches off-by-one mistakes in difference array handling. A wrong decrement position would incorrectly erase the contribution of the final index.

Finally, consider overlapping middle ranges:

```
5 2
10 20 30 40 50
2 4
2 4
```

Frequencies become:

```
[0, 2, 2, 2, 0]
```

The optimal arrangement places the three largest numbers into the three middle positions:

```
[10, 30, 40, 50, 20]
```

The total answer is:

```
2 * (30 + 40 + 50) = 240
```

This demonstrates why sorting frequencies and values together is optimal. Large values must occupy the most frequently queried positions.
