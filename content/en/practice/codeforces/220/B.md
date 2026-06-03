---
title: "CF 220B - Little Elephant and Array"
description: "We are given an array of positive integers and many range queries. For each query [l, r], we look only at the subarray between those positions and count how many values x satisfy a very specific condition: Inside that subarray, the value x appears exactly x times."
date: "2026-06-04T02:00:02+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "data-structures"]
categories: ["algorithms"]
codeforces_contest: 220
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 136 (Div. 1)"
rating: 1800
weight: 220
solve_time_s: 118
verified: true
draft: false
---

[CF 220B - Little Elephant and Array](https://codeforces.com/problemset/problem/220/B)

**Rating:** 1800  
**Tags:** constructive algorithms, data structures  
**Solve time:** 1m 58s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of positive integers and many range queries. For each query `[l, r]`, we look only at the subarray between those positions and count how many values `x` satisfy a very specific condition:

Inside that subarray, the value `x` appears exactly `x` times.

For example, in the subarray

```
[3, 1, 2, 2, 3, 3, 7]
```

the frequencies are:

```
1 -> 1
2 -> 2
3 -> 3
7 -> 1
```

Values `1`, `2`, and `3` each appear exactly as many times as their own value, so the answer is `3`.

The array length and the number of queries are both as large as `100000`. A straightforward solution that recomputes frequencies for every query is immediately ruled out. Even an `O(length of range)` solution per query would require roughly `10^10` operations in the worst case.

The values themselves can be as large as `10^9`. This means we cannot build frequency structures indexed directly by value. We only care about values that actually appear in the array.

A subtle observation is that any value larger than `n` can never contribute to an answer. A value must appear exactly `x` times, but no frequency inside any range can exceed `n`. If `x > n`, matching frequency `x` is impossible.

Consider:

```
n = 5
array = [100, 100, 100, 100, 100]
```

The frequency of `100` is `5`, not `100`, so it never contributes.

Another easy mistake is to count occurrences instead of qualifying values. For example:

```
array = [2, 2]
query = [1, 2]
```

Value `2` appears exactly twice, so the answer is:

```
1
```

not

```
2
```

because we count values satisfying the condition, not positions.

A third pitfall appears when frequencies cross the target value while expanding or shrinking a range.

Suppose the current frequency of value `3` changes:

```
2 -> 3 -> 4
```

When it reaches `3`, the answer should increase by one. When it becomes `4`, the answer should decrease by one. Forgetting one of these transitions causes incorrect results.

## Approaches

The brute-force solution processes each query independently. For a query `[l, r]`, we scan the entire subarray, compute frequencies with a hash map, then count how many values satisfy:

```
frequency[value] == value
```

This is correct because it directly implements the definition.

Unfortunately, a query may cover almost the entire array. With `100000` queries and ranges of length `100000`, the work becomes roughly:

```
100000 × 100000 = 10^10
```

which is far beyond the time limit.

The key observation is that queries ask about many overlapping ranges. Consecutive queries often differ only by a few elements. Recomputing all frequencies from scratch wastes work.

This is exactly the setting where Mo's algorithm shines. We sort queries in a special order so that the current range changes gradually. While moving from one query to the next, we only add or remove a small number of elements from the current range.

The challenge becomes maintaining the answer dynamically as frequencies change.

Suppose value `v` currently has frequency `cnt[v]`.

Before increasing its frequency, we check whether it already contributes. If:

```
cnt[v] == v
```

then removing that equality must decrease the answer.

After updating the frequency, we check again. If the new frequency equals `v`, the value starts contributing and the answer increases.

Each add/remove operation becomes `O(1)`, and Mo's ordering guarantees only about `O((n+m)√n)` total range adjustments.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nm) | O(n) | Too slow |
| Optimal (Mo's Algorithm) | O((n+m)√n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the array and queries.
2. Replace every value greater than `n` with a special irrelevant value.

Such values can never satisfy `frequency = value`, so we do not need to track them in the answer logic.
3. Store each query together with its original index.
4. Choose a block size approximately equal to `√n`.
5. Sort queries using Mo's ordering.

Queries in the same left block are ordered by right endpoint. This minimizes pointer movement.
6. Maintain a current range `[curL, curR]`.

Initially the range is empty.
7. Maintain a frequency array `cnt`.

`cnt[x]` stores how many times value `x` appears in the current range.
8. Maintain a variable `answer`.

This equals the number of values whose frequency currently matches their value.
9. When adding value `v`:

First check whether `cnt[v] == v`. If true, decrement `answer` because the equality is about to break.

Increase `cnt[v]`.

Check again whether `cnt[v] == v`. If true, increment `answer`.
10. When removing value `v`:

First check whether `cnt[v] == v`. If true, decrement `answer`.

Decrease `cnt[v]`.

Check again whether `cnt[v] == v`. If true, increment `answer`.
11. For each query in Mo order, move `curL` and `curR` until the current range matches the query range.
12. Store the current `answer` as the result for that query.
13. Output answers in original query order.

### Why it works

At every moment, `cnt[x]` equals the frequency of value `x` inside the current range maintained by Mo's algorithm.

The variable `answer` counts exactly those values satisfying:

```
cnt[x] = x
```

Whenever a frequency changes, only one value is affected. The add/remove routines update `answer` precisely when that value enters or leaves the equality condition.

Since Mo's algorithm eventually visits every query range exactly and the maintained frequencies are always correct for the current range, the stored answer for each query is exactly the number of values appearing a number of times equal to their value.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    a = list(map(int, input().split()))

    # Values > n can never satisfy freq == value
    a = [x if x <= n else 0 for x in a]

    block = int(n ** 0.5) + 1

    queries = []
    for idx in range(m):
        l, r = map(int, input().split())
        l -= 1
        r -= 1
        queries.append((l, r, idx))

    queries.sort(key=lambda q: (q[0] // block, q[1]))

    cnt = [0] * (n + 1)
    answers = [0] * m
    current_answer = 0

    def add(pos):
        nonlocal current_answer
        v = a[pos]

        if v == 0:
            return

        if cnt[v] == v:
            current_answer -= 1

        cnt[v] += 1

        if cnt[v] == v:
            current_answer += 1

    def remove(pos):
        nonlocal current_answer
        v = a[pos]

        if v == 0:
            return

        if cnt[v] == v:
            current_answer -= 1

        cnt[v] -= 1

        if cnt[v] == v:
            current_answer += 1

    cur_l = 0
    cur_r = -1

    for l, r, idx in queries:
        while cur_l > l:
            cur_l -= 1
            add(cur_l)

        while cur_r < r:
            cur_r += 1
            add(cur_r)

        while cur_l < l:
            remove(cur_l)
            cur_l += 1

        while cur_r > r:
            remove(cur_r)
            cur_r -= 1

        answers[idx] = current_answer

    sys.stdout.write("\n".join(map(str, answers)))

if __name__ == "__main__":
    solve()
```

The first preprocessing step replaces all values larger than `n` with `0`. Such values can never contribute because no frequency can exceed `n`. This avoids wasting time maintaining frequencies that can never satisfy the condition.

The `cnt` array stores frequencies only for values from `1` to `n`. Value `0` is ignored completely.

The most delicate part is the update logic. When a frequency changes, we must remove its old contribution before modifying the count, then add its new contribution afterward. Reversing that order leads to off-by-one errors whenever a frequency crosses its target value.

The range maintained by Mo's algorithm is inclusive on both ends. The implementation starts with an empty range `[0, -1]`, then expands or shrinks until it matches each query.

## Worked Examples

### Example 1

Input:

```
7 2
3 1 2 2 3 3 7
1 7
3 4
```

Queries in sorted order happen to match the input order.

For range `[1,7]`:

| Value | Frequency | Contributes? |
| --- | --- | --- |
| 1 | 1 | Yes |
| 2 | 2 | Yes |
| 3 | 3 | Yes |
| 7 | 1 | No |

Answer = 3.

For range `[3,4]`:

```
[2, 2]
```

| Value | Frequency | Contributes? |
| --- | --- | --- |
| 2 | 2 | Yes |

Answer = 1.

Output:

```
3
1
```

This example demonstrates the core condition. A value contributes only when its frequency equals the value itself.

### Example 2

Input:

```
5 1
1 1 1 1 1
1 5
```

Current range becomes the whole array.

| Value | Frequency | Contributes? |
| --- | --- | --- |
| 1 | 5 | No |

Answer:

```
0
```

The trace shows that matching the value exactly matters. Having frequency larger than the value does not count.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n + m)√n) | Mo's algorithm performs O((n+m)√n) pointer movements, each updated in O(1) |
| Space | O(n + m) | Frequency array, query storage, and answer storage |

With `n,m ≤ 100000`, we have `√n ≈ 316`. The resulting number of updates is well within the limits of a 4-second Codeforces problem, and the memory usage is comfortably below 256 MB.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    import math

    input = sys.stdin.readline

    n, m = map(int, input().split())
    a = list(map(int, input().split()))
    a = [x if x <= n else 0 for x in a]

    block = int(n ** 0.5) + 1

    queries = []
    for idx in range(m):
        l, r = map(int, input().split())
        queries.append((l - 1, r - 1, idx))

    queries.sort(key=lambda q: (q[0] // block, q[1]))

    cnt = [0] * (n + 1)
    ans = [0] * m
    cur_ans = 0

    def add(pos):
        nonlocal cur_ans
        v = a[pos]
        if v == 0:
            return
        if cnt[v] == v:
            cur_ans -= 1
        cnt[v] += 1
        if cnt[v] == v:
            cur_ans += 1

    def remove(pos):
        nonlocal cur_ans
        v = a[pos]
        if v == 0:
            return
        if cnt[v] == v:
            cur_ans -= 1
        cnt[v] -= 1
        if cnt[v] == v:
            cur_ans += 1

    lcur, rcur = 0, -1

    for l, r, idx in queries:
        while lcur > l:
            lcur -= 1
            add(lcur)

        while rcur < r:
            rcur += 1
            add(rcur)

        while lcur < l:
            remove(lcur)
            lcur += 1

        while rcur > r:
            remove(rcur)
            rcur -= 1

        ans[idx] = cur_ans

    return "\n".join(map(str, ans))

# provided sample
assert run(
"""7 2
3 1 2 2 3 3 7
1 7
3 4
"""
) == "3\n1"

# minimum size
assert run(
"""1 1
1
1 1
"""
) == "1"

# value larger than n
assert run(
"""3 1
100 100 100
1 3
"""
) == "0"

# all equal values
assert run(
"""5 1
2 2 2 2 2
1 5
"""
) == "0"

# exact frequency match
assert run(
"""4 1
2 2 1 3
1 2
"""
) == "1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single element `[1]` | `1` | Minimum constraints |
| All values `100` with `n=3` | `0` | Values larger than `n` are irrelevant |
| `[2,2,2,2,2]` | `0` | Frequency larger than value does not count |
| Range `[2,2]` | `1` | Exact frequency match |
| Official sample | `3,1` | General correctness |

## Edge Cases

Consider:

```
3 1
100 100 100
1 3
```

Since `100 > n`, the value can never appear exactly `100` times. The preprocessing converts all entries to `0`, the update routines ignore them, and the maintained answer remains `0`.

Consider:

```
2 1
2 2
1 2
```

The frequency of value `2` is exactly `2`. During insertion, the count changes:

```
0 -> 1 -> 2
```

When it reaches `2`, the answer increases by one. The final output is:

```
1
```

which is correct because only the value `2` qualifies.

Consider:

```
4 1
3 3 3 3
1 4
```

The frequency transitions:

```
0 -> 1 -> 2 -> 3 -> 4
```

At frequency `3`, the value contributes. At frequency `4`, it stops contributing. The update logic removes the contribution before increasing the count and restores it only if equality still holds afterward. The final answer is:

```
0
```

which matches the definition exactly.
