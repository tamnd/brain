---
title: "CF 243A - The Brand New Function"
description: "We are given an array of non-negative integers. For every possible subarray, we compute the bitwise OR of all numbers inside that subarray. The task is to count how many different OR results appear across all subarrays."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "bitmasks"]
categories: ["algorithms"]
codeforces_contest: 243
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 150 (Div. 1)"
rating: 1600
weight: 243
solve_time_s: 84
verified: true
draft: false
---

[CF 243A - The Brand New Function](https://codeforces.com/problemset/problem/243/A)

**Rating:** 1600  
**Tags:** bitmasks  
**Solve time:** 1m 24s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of non-negative integers. For every possible subarray, we compute the bitwise OR of all numbers inside that subarray. The task is to count how many different OR results appear across all subarrays.

For example, if the array is `[1, 2, 0]`, the subarray OR values are:

- `[1] -> 1`
- `[1,2] -> 3`
- `[1,2,0] -> 3`
- `[2] -> 2`
- `[2,0] -> 2`
- `[0] -> 0`

The distinct results are `{0,1,2,3}`, so the answer is `4`.

The array length can reach `10^5`, which immediately rules out any solution that explicitly enumerates all subarrays. There are about `n(n+1)/2` subarrays, which is roughly `5 * 10^9` when `n = 10^5`. Even spending constant time per subarray would be far too slow for a 2 second limit.

The values are at most `10^6`, which is small in terms of bit count. Every number fits within about 20 bits because `2^20 = 1,048,576`. That detail is the key to the efficient solution.

A subtle edge case appears when many subarrays produce the same OR value. Consider:

```
3
1 1 1
```

Every subarray OR is `1`, so the correct answer is:

```
1
```

A careless implementation that stores results separately per subarray instead of deduplicating globally would overcount.

Another tricky situation is arrays containing zeroes:

```
4
0 0 0 0
```

Every subarray OR is `0`, so the answer is still `1`.

This matters because OR behaves differently from sum or xor. Adding more elements cannot unset bits. Once a bit becomes `1`, it stays `1`.

A more interesting case is:

```
4
1 2 4 8
```

Different subarrays generate many distinct values:

- `1`
- `2`
- `4`
- `8`
- `1|2 = 3`
- `2|4 = 6`
- `4|8 = 12`
- `1|2|4 = 7`
- `2|4|8 = 14`
- `1|2|4|8 = 15`

The answer is `10`.

This example shows that distinct OR values can grow quickly, but still not fast enough to break the intended solution because OR values stabilize once all bits become set.

## Approaches

The brute-force solution is straightforward. For every starting position `l`, extend the subarray to every ending position `r`, maintain the running OR, and insert the result into a set.

The code idea looks like this:

```
for l in range(n):
    cur = 0
    for r in range(l, n):
        cur |= a[r]
        distinct.add(cur)
```

The running OR update is efficient because each extension only needs one OR operation. The problem is the number of subarrays. The nested loops execute about `n^2 / 2` iterations, which becomes around `5 * 10^9` when `n = 10^5`. That is impossible within the limits.

The important observation is that OR values do not fluctuate arbitrarily. When we extend a subarray, bits only change from `0` to `1`. They never revert back.

Suppose we process the array from left to right and focus on subarrays ending at position `i`.

Let:

- `S[i]` = all distinct OR values of subarrays ending at `i`

Every subarray ending at `i` is either:

- the single element `[a[i]]`
- or some subarray ending at `i-1`, extended by `a[i]`

So the new OR values are:

```
new_value = old_value | a[i]
```

The critical insight is that the number of distinct OR values per position stays small.

Why?

Each OR operation can only turn more bits on. Since numbers contain at most about 20 bits, an OR value can change at most 20 times before stabilizing. That means the size of `S[i]` is bounded by roughly 20 to 21 distinct values, not `O(n)`.

This transforms the solution from quadratic to nearly linear.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n²) in worst case for stored values | Too slow |
| Optimal | O(n * B) where B is number of bits | O(n * B) for global set | Accepted |

Here `B ≈ 20`.

## Algorithm Walkthrough

1. Create an empty global set `ans`.

This stores every distinct OR value seen across all subarrays.
2. Maintain a set `prev`.

`prev` represents all distinct OR values of subarrays ending at the previous index.
3. Process the array from left to right.

Suppose the current value is `x`.
4. Build a new set `cur`.

First insert `x` itself, because the subarray consisting of only the current element always exists.
5. For every value `v` in `prev`, insert `v | x` into `cur`.

This corresponds to extending every subarray ending at the previous position by the current element.
6. Add all values from `cur` into the global answer set.

Every element of `cur` is a valid OR result for some subarray.
7. Replace `prev` with `cur`.

The next iteration will extend these subarrays further.
8. After processing the whole array, output `len(ans)`.

### Why it works

At every index `i`, the set `prev` contains exactly the distinct OR values of all subarrays ending at `i`.

This is true because every such subarray is either:

- `[a[i]]`
- or an earlier subarray ending at `i-1` extended by `a[i]`

The algorithm generates both categories and nothing else.

The reason the solution is fast is that OR values evolve monotonically. Extending a subarray can only add bits, never remove them. Since there are only about 20 bits available, the number of distinct OR states per position remains small.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))

    ans = set()
    prev = set()

    for x in a:
        cur = {x}

        for v in prev:
            cur.add(v | x)

        ans.update(cur)
        prev = cur

    print(len(ans))

solve()
```

The variable `prev` stores all distinct OR values for subarrays ending at the previous position. For each new element `x`, we construct the next set `cur`.

The line:

```
cur = {x}
```

handles the single-element subarray `[x]`.

Then:

```
cur.add(v | x)
```

extends every previous subarray by appending the current element.

Using sets is essential because many different subarrays can produce the same OR result. Without deduplication, the number of states would explode.

The update:

```
ans.update(cur)
```

collects all globally distinct OR values.

One subtle point is that we replace `prev` entirely with `cur`. We do not append to it. `prev` must only describe subarrays ending exactly at the previous index, otherwise invalid combinations would appear.

Python integers safely handle all bit operations here, so there are no overflow concerns.

## Worked Examples

### Example 1

Input:

```
3
1 2 0
```

| Index | Current Value | prev before | cur after processing | Global ans |
| --- | --- | --- | --- | --- |
| 0 | 1 | {} | {1} | {1} |
| 1 | 2 | {1} | {2, 3} | {1, 2, 3} |
| 2 | 0 | {2, 3} | {0, 2, 3} | {0, 1, 2, 3} |

Final answer:

```
4
```

This trace shows how extending subarrays works. At index 1, extending OR value `1` with `2` gives `3`. At index 2, OR with zero preserves previous values.

### Example 2

Input:

```
4
1 2 4 8
```

| Index | Current Value | prev before | cur after processing |
| --- | --- | --- | --- |
| 0 | 1 | {} | {1} |
| 1 | 2 | {1} | {2, 3} |
| 2 | 4 | {2, 3} | {4, 6, 7} |
| 3 | 8 | {4, 6, 7} | {8, 12, 14, 15} |

Global distinct values become:

```
{1,2,3,4,6,7,8,12,14,15}
```

Answer:

```
10
```

This example demonstrates how OR values monotonically gain bits. Once a bit appears, it persists in future extensions.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n * B) | Each position keeps at most about B distinct OR values |
| Space | O(n * B) | Global answer set stores all distinct results |

`B` is the number of bits needed to represent values up to `10^6`, which is about 20.

With `n = 10^5`, the algorithm performs only a few million operations, easily fitting within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def solve():
    input = sys.stdin.readline

    n = int(input())
    a = list(map(int, input().split()))

    ans = set()
    prev = set()

    for x in a:
        cur = {x}

        for v in prev:
            cur.add(v | x)

        ans.update(cur)
        prev = cur

    print(len(ans))

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    output = sys.stdout.getvalue()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return output

# provided sample
assert run("3\n1 2 0\n") == "4\n", "sample 1"

# minimum size
assert run("1\n0\n") == "1\n", "single zero"

# all equal values
assert run("5\n7 7 7 7 7\n") == "1\n", "all OR values identical"

# increasing powers of two
assert run("4\n1 2 4 8\n") == "10\n", "many distinct OR values"

# zeros mixed with numbers
assert run("4\n0 1 0 2\n") == "4\n", "handling zeros correctly"

# boundary-style repeated growth
assert run("5\n1 3 7 15 31\n") == "5\n", "OR stabilizes quickly"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 0` | `1` | Minimum-size array |
| `7 7 7 7 7` | `1` | Duplicate OR results collapse correctly |
| `1 2 4 8` | `10` | Many distinct bit combinations |
| `0 1 0 2` | `4` | Zero handling and OR persistence |
| `1 3 7 15 31` | `5` | OR values stabilize after bits become set |

## Edge Cases

Consider the input:

```
3
1 1 1
```

Processing steps:

- After first `1`, `prev = {1}`
- After second `1`, extending gives `1 | 1 = 1`
- After third `1`, the same happens again

The global set never grows beyond `{1}`.

Final answer:

```
1
```

This case confirms that the set-based deduplication is necessary. Counting subarrays directly would incorrectly produce 6 instead of 1.

Now consider:

```
4
0 0 0 0
```

Trace:

| Index | cur |
| --- | --- |
| 0 | {0} |
| 1 | {0} |
| 2 | {0} |
| 3 | {0} |

The OR of any collection of zeroes remains zero.

Final answer:

```
1
```

This checks that the algorithm handles values that never gain new bits.

Finally, consider:

```
4
1 2 4 8
```

The OR values evolve like:

```
1 -> 3 -> 7 -> 15
```

Each extension adds new bits. The algorithm captures all intermediate OR states while keeping only distinct values per ending position.

Final answer:

```
10
```

This validates the key property behind the optimization, the number of distinct OR states remains small because bits only turn on once.
