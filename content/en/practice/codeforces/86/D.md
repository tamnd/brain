---
title: "CF 86D - Powerful array"
description: "We are given an array of positive integers and many interval queries. For each query [l, r], we look only at the subarray between those indices and compute a value called its power. If a number x appears k times inside the subarray, then x contributes k² x to the answer."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "implementation", "math", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 86
codeforces_index: "D"
codeforces_contest_name: "Yandex.Algorithm 2011: Round 2"
rating: 2200
weight: 86
solve_time_s: 226
verified: true
draft: false
---

[CF 86D - Powerful array](https://codeforces.com/problemset/problem/86/D)

**Rating:** 2200  
**Tags:** data structures, implementation, math, two pointers  
**Solve time:** 3m 46s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of positive integers and many interval queries. For each query `[l, r]`, we look only at the subarray between those indices and compute a value called its power.

If a number `x` appears `k` times inside the subarray, then `x` contributes `k² * x` to the answer. The final result is the sum of these contributions over all distinct values in the interval.

For example, in the subarray `[1, 2, 1, 1, 2]`, the value `1` appears `3` times and contributes `3² * 1 = 9`. The value `2` appears `2` times and contributes `2² * 2 = 8`. The total is `17`.

The array length and the number of queries both reach `200000`. A straightforward solution that processes every query independently is immediately too slow. Even iterating through one full subarray per query would already cost `O(n * q)` in the worst case, which becomes about `4 * 10^10` operations. That is several orders of magnitude beyond what fits in 5 seconds.

The values themselves are at most `10^6`, which is small enough for a frequency array indexed by value. That observation becomes very useful once we process queries in a smarter order.

A subtle detail is that the answer can become large. Suppose all `200000` elements are equal to `10^6`. Then the contribution is:

$$(200000)^2 \cdot 10^6 = 4 \cdot 10^{16}$$

This does not fit in 32-bit integers, so the implementation must use 64-bit arithmetic.

Another easy mistake is updating the contribution incorrectly when frequencies change. Consider the array:

```
[5, 5]
```

For the interval `[1, 2]`, the correct answer is:

```
2² * 5 = 20
```

If we already had one `5` in the current interval, adding another `5` does not increase the answer by just `5`. The contribution changes from:

```
1² * 5 = 5
```

to

```
2² * 5 = 20
```

so the increment is actually `15`.

A final common bug appears at interval boundaries. Suppose the current interval is `[2, 4]` and the next query is `[3, 4]`. If we remove the left endpoint after moving the pointer, we accidentally keep an extra element inside the window. The order of pointer movement and frequency updates must exactly match the intended interval.

## Approaches

The brute-force approach processes every query independently. For each interval `[l, r]`, we count frequencies inside the subarray and compute:

$$\sum cnt[x]^2 \cdot x$$

A hash map or frequency array makes counting straightforward. The method is correct because it directly follows the definition of power.

The problem is the total work. A single query may span the whole array, requiring `O(n)` operations. With `200000` queries, the total complexity becomes `O(nq)`, which is far too large.

The key observation is that neighboring queries often overlap heavily. If two intervals differ by only a few elements, recomputing the entire answer wastes almost all previous work.

This structure is exactly what Mo's algorithm exploits.

Instead of answering queries in input order, we sort them so that consecutive queries have similar ranges. Then we maintain one current interval and adjust it gradually. When the interval expands or shrinks by one element, we update the answer in constant time.

Suppose the current frequency of value `x` is `f`.

Before adding another `x`, its contribution is:

$$f^2 \cdot x$$

After adding it, the contribution becomes:

$$(f+1)^2 \cdot x$$

The increase is:

$$((f+1)^2 - f^2) \cdot x = (2f+1)\cdot x$$

We can update the answer immediately without recomputing anything else.

Removing an element works similarly:

$$f^2 \cdot x - (f-1)^2 \cdot x = (2f-1)\cdot x$$

Since each pointer movement costs `O(1)`, the total complexity becomes approximately `O((n + q)\sqrt n)`, which is fast enough for the constraints.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nq) | O(max(a)) | Too slow |
| Optimal, Mo's Algorithm | O((n + q)√n) | O(max(a) + q) | Accepted |

## Algorithm Walkthrough

1. Read the array and all queries.
2. Convert queries to zero-based indexing because Python lists use zero-based positions.
3. Choose a block size, usually `int(sqrt(n))`.
4. Sort queries by:

first, the block containing the left endpoint,

second, the right endpoint.

This ordering minimizes how far the interval pointers move between consecutive queries.
5. Maintain a current interval `[cur_l, cur_r]` and its current power value.

Initially the interval is empty.
6. Maintain a frequency array `freq[x]` storing how many times value `x` appears inside the current interval.
7. Define an `add(x)` operation.

If the current frequency is `f`, then:

$$answer -= f^2 \cdot x$$

increment the frequency,

$$answer += (f+1)^2 \cdot x$$

This updates the contribution of only the affected value.
8. Define a `remove(x)` operation similarly.

If the current frequency is `f`, remove its old contribution, decrement the frequency, then add the new contribution.
9. Process queries in sorted order.

Move `cur_l` and `cur_r` until the maintained interval exactly matches the target query interval.
10. Once the interval matches, store the current answer in the result array using the query's original index.
11. After all queries are processed, print answers in input order.

### Why it works

At every moment, the maintained interval exactly matches the current query range. The frequency array always stores the true occurrence count of every value inside that interval.

The answer variable equals:

$$\sum freq[x]^2 \cdot x$$

because every add or remove operation updates the contribution of exactly one value while leaving all others unchanged.

Since Mo's ordering guarantees that every query is reached through a sequence of valid interval expansions and contractions, the maintained state is always correct when a query is answered.

## Python Solution

```python
import sys
from math import sqrt

input = sys.stdin.readline

def solve():
    n, q = map(int, input().split())
    arr = list(map(int, input().split()))

    queries = []

    for idx in range(q):
        l, r = map(int, input().split())
        l -= 1
        r -= 1
        queries.append((l, r, idx))

    block_size = int(sqrt(n)) + 1

    queries.sort(
        key=lambda x: (
            x[0] // block_size,
            x[1]
        )
    )

    freq = [0] * (10**6 + 1)
    answers = [0] * q

    current_answer = 0
    cur_l = 0
    cur_r = -1

    def add(value):
        nonlocal current_answer

        f = freq[value]
        current_answer -= f * f * value

        freq[value] += 1
        f += 1

        current_answer += f * f * value

    def remove(value):
        nonlocal current_answer

        f = freq[value]
        current_answer -= f * f * value

        freq[value] -= 1
        f -= 1

        current_answer += f * f * value

    for l, r, idx in queries:

        while cur_l > l:
            cur_l -= 1
            add(arr[cur_l])

        while cur_r < r:
            cur_r += 1
            add(arr[cur_r])

        while cur_l < l:
            remove(arr[cur_l])
            cur_l += 1

        while cur_r > r:
            remove(arr[cur_r])
            cur_r -= 1

        answers[idx] = current_answer

    print("\n".join(map(str, answers)))

solve()
```

The solution begins by reading all queries and attaching their original indices. After sorting queries for Mo's algorithm, we no longer process them in input order, so we must remember where each answer belongs.

The current interval starts empty as `[0, -1]`. This representation avoids special cases because adding the first element simply increments `cur_r`.

The frequency array has size `10^6 + 1` because array values are bounded by `10^6`. Using a list is much faster than a dictionary for this problem.

The `add` and `remove` functions are the core of the implementation. A common mistake is updating the frequency before subtracting the old contribution. The code first removes the old term `f² * value`, changes the frequency, then adds the updated term.

The order of pointer movement also matters. When shrinking from the left, we remove the current left element before incrementing `cur_l`. Reversing that order would remove the wrong value.

All arithmetic uses Python integers, which automatically handle large values safely.

## Worked Examples

### Sample 1

Input:

```
3 2
1 2 1
1 2
1 3
```

After zero-based conversion, the queries are `[0,1]` and `[0,2]`.

| Step | Interval | Action | Frequencies | Current Answer |
| --- | --- | --- | --- | --- |
| Start | [] | empty | {} | 0 |
| Add 1 | [0,0] | add 1 | {1:1} | 1 |
| Add 2 | [0,1] | add 2 | {1:1,2:1} | 3 |
| Answer query 1 | [0,1] | store | {1:1,2:1} | 3 |
| Add 1 | [0,2] | add 1 | {1:2,2:1} | 6 |
| Answer query 2 | [0,2] | store | {1:2,2:1} | 6 |

The trace shows how the answer evolves incrementally. When the second `1` is added, the contribution of `1` changes from `1` to `4`, increasing the total answer by `3`.

### Custom Example

Input:

```
5 2
1 1 2 2 2
1 5
2 4
```

| Step | Interval | Action | Frequencies | Current Answer |
| --- | --- | --- | --- | --- |
| Start | [] | empty | {} | 0 |
| Add 1 | [0,0] | add 1 | {1:1} | 1 |
| Add 1 | [0,1] | add 1 | {1:2} | 4 |
| Add 2 | [0,2] | add 2 | {1:2,2:1} | 6 |
| Add 2 | [0,3] | add 2 | {1:2,2:2} | 12 |
| Add 2 | [0,4] | add 2 | {1:2,2:3} | 22 |
| Answer query 1 | [0,4] | store | {1:2,2:3} | 22 |
| Remove 1 | [1,4] | remove left | {1:1,2:3} | 19 |
| Remove 2 | [1,3] | remove right | {1:1,2:2} | 9 |
| Answer query 2 | [1,3] | store | {1:1,2:2} | 9 |

This trace demonstrates both expansion and contraction of the interval. Only the affected value changes contribution each time, which is why updates stay constant-time.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n + q)√n) | Each pointer moves at most O(q√n) total positions |
| Space | O(max(a) + q) | Frequency array plus query storage |

With `n` and `q` both up to `200000`, the complexity is well within limits for a carefully implemented Mo's algorithm solution in Python.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io
from math import sqrt

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    n, q = map(int, input().split())
    arr = list(map(int, input().split()))

    queries = []

    for idx in range(q):
        l, r = map(int, input().split())
        queries.append((l - 1, r - 1, idx))

    block = int(sqrt(n)) + 1

    queries.sort(key=lambda x: (x[0] // block, x[1]))

    freq = [0] * (10**6 + 1)
    ans = [0] * q

    cur = 0
    L = 0
    R = -1

    def add(x):
        nonlocal cur
        f = freq[x]
        cur -= f * f * x
        freq[x] += 1
        f += 1
        cur += f * f * x

    def remove(x):
        nonlocal cur
        f = freq[x]
        cur -= f * f * x
        freq[x] -= 1
        f -= 1
        cur += f * f * x

    for l, r, idx in queries:

        while L > l:
            L -= 1
            add(arr[L])

        while R < r:
            R += 1
            add(arr[R])

        while L < l:
            remove(arr[L])
            L += 1

        while R > r:
            remove(arr[R])
            R -= 1

        ans[idx] = cur

    return "\n".join(map(str, ans))

# provided sample
assert run(
"""3 2
1 2 1
1 2
1 3
"""
) == "3\n6"

# minimum size
assert run(
"""1 1
7
1 1
"""
) == "7"

# all equal values
assert run(
"""5 2
4 4 4 4 4
1 5
2 4
"""
) == "100\n36"

# boundary intervals
assert run(
"""5 3
1 2 3 4 5
1 1
5 5
1 5
"""
) == "1\n5\n15"

# off-by-one stress
assert run(
"""4 3
1 2 1 2
1 2
2 3
3 4
"""
) == "3\n3\n3"

print("All tests passed")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single element array | Same value | Correct handling of minimal intervals |
| All equal values | Large quadratic contribution | Frequency updates are correct |
| Queries touching boundaries | Prefix and suffix correctness | Pointer movement at edges |
| Alternating repeated values | Identical answers across shifts | Off-by-one correctness |

## Edge Cases

Consider the smallest possible interval:

```
1 1
9
1 1
```

The interval contains one occurrence of `9`, so the answer is:

```
1² * 9 = 9
```

The algorithm starts with an empty interval and adds exactly one element. The frequency becomes `1`, and the maintained answer becomes `9`.

Now consider all values equal:

```
5 1
3 3 3 3 3
1 5
```

The correct answer is:

```
5² * 3 = 75
```

As elements are added, the contribution evolves:

```
1²*3 = 3
2²*3 = 12
3²*3 = 27
4²*3 = 48
5²*3 = 75
```

The update formula correctly captures the nonlinear growth.

Finally, consider shrinking an interval:

```
4 2
1 2 1 2
1 4
2 3
```

The first interval has frequencies `{1:2, 2:2}` and answer:

```
4 + 8 = 12
```

When moving to `[2,3]`, the algorithm removes the left `1` and right `2`.

After removing the left `1`:

```
{1:1, 2:2}
1 + 8 = 9
```

After removing the right `2`:

```
{1:1, 2:1}
1 + 2 = 3
```

The final answer is correct because removals always update contributions before frequencies are changed further.
