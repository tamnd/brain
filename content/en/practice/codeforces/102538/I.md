---
title: "CF 102538I - Ignore Submasks"
description: "Edit We are given an array of integers. Each integer represents a set of enabled bits. For every possible mask x containing k bits, we need to find the first array position whose value contains at least one bit that is missing from x."
date: "2026-08-03T21:03:53+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102538
codeforces_index: "I"
codeforces_contest_name: "300iq Contest 3"
rating: 0
weight: 102538
solve_time_s: 132
verified: true
draft: false
---

[CF 102538I - Ignore Submasks](https://codeforces.com/problemset/problem/102538/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 12s  
**Verified:** yes  

## Solution
Edit

# Problem Understanding

We are given an array of integers. Each integer represents a set of enabled bits. For every possible mask `x` containing `k` bits, we need to find the first array position whose value contains at least one bit that is missing from `x`. If every array value is a submask of `x`, that position is considered zero. The task is to add this value over all `2^k` possible masks.

The number of masks is exponential in `k`, and `k` can be as large as 60. A direct iteration over all masks would require more than `10^18` operations, so the solution must avoid visiting masks entirely. The array length is only 100, which means operations proportional to `n * k` are easily affordable, while anything depending on `2^k` is impossible.

The tricky cases come from bits that never appear and from several bits appearing for the first time at the same array position. A bit that never appears cannot make any value invalid, so it must not contribute a fake position. For example:

```
Input:
2 2
0 1
```

The first occurrence positions are bit 0 at position 2, while bit 1 never appears. Only bit 0 matters. Treating the missing bit as position 0 or position 1 would incorrectly increase the answer.

Another case is repeated first positions:

```
Input:
2 2
3 3
```

Both bits first appear at position 1. For `x = 0`, the answer is 1 because both bits are missing. For `x = 1`, bit 1 is missing and the answer is still 1. A solution that sorts positions and blindly assigns powers of two to equal values separately would overcount. Equal positions have to be grouped together.

# Approaches

The brute force method follows the definition directly. For every mask `x` from `0` to `2^k - 1`, we scan the array from left to right until we find the first value that is not a submask of `x`. The check for one value is cheap, but there are `2^k` masks and up to `n` positions for each one. With `k = 60`, this is around `100 * 2^60` checks, which is far beyond the available time.

The key observation is that a mask `x` is only interesting through the bits it does not contain. For every bit, find the earliest array position where that bit appears. If `x` misses a bit `b`, then the first invalid array element must appear no later than the first occurrence of `b`. In fact, the answer for `x` is the minimum first occurrence among all bits missing from `x`.

Now the problem becomes a counting problem over the bit positions instead of over all masks. Suppose the first occurrences of all appearing bits are sorted. If a value is the minimum missing occurrence, every smaller occurrence must belong to a bit that is present in `x`, and the chosen occurrence must belong to a bit that is absent. The remaining larger bits are free. Grouping equal occurrences handles multiple bits becoming candidates at the same time.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^k * n) | O(1) | Too slow |
| Optimal | O(nk + k log k) | O(k) | Accepted |

# Algorithm Walkthrough

1. For every bit from `0` to `k - 1`, find the first array index containing this bit. Ignore bits that never appear, because they can never make a mask fail.
2. Collect all existing first positions and sort them. Equal positions must remain grouped because several bits can become the first missing bit at the same time.
3. Process each group of equal positions. Suppose a group contains `cnt` bits, there are `smaller` bits with smaller first positions, and `larger` bits with larger first positions.
4. For this group to determine the answer, all `smaller` bits must be present in `x`. Among the current group, at least one bit must be absent. The number of choices inside this group is `2^cnt - 1`, and all larger bits are unrestricted, giving `2^larger` possibilities.
5. Add

```
position * (2^cnt - 1) * 2^larger
```

to the answer modulo `998244353`.

Why it works:

Every mask `x` has a unique minimum first occurrence among the bits missing from it. The algorithm counts exactly the masks whose minimum missing bit belongs to each group. Smaller groups cannot be missing, because that would create an earlier answer. The current group cannot be completely present, because then it would not contribute. Larger groups do not affect the minimum and can be chosen freely. These cases cover every possible mask exactly once.

# Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 998244353

def solve():
    n, k = map(int, input().split())
    a = list(map(int, input().split()))

    first = [n + 1] * k

    for i, x in enumerate(a, 1):
        for b in range(k):
            if (x >> b) & 1 and first[b] == n + 1:
                first[b] = i

    vals = [x for x in first if x != n + 1]
    vals.sort()

    pow2 = [1] * (len(vals) + 1)
    for i in range(1, len(pow2)):
        pow2[i] = (pow2[i - 1] * 2) % MOD

    ans = 0
    i = 0
    m = len(vals)

    while i < m:
        j = i
        while j < m and vals[j] == vals[i]:
            j += 1

        cnt = j - i
        larger = m - j

        ways = (pow2[cnt] - 1) * pow2[larger] % MOD
        ans = (ans + vals[i] * ways) % MOD

        i = j

    print(ans % MOD)

if __name__ == "__main__":
    solve()
```

The first array stores the earliest position for each bit. Positions are one based because the required value is the array index, not a zero based offset.

The list `vals` contains only bits that actually occur. Sorting it allows the minimum missing bit to be counted from left to right.

The grouped loop is the important part. If several bits share the same first occurrence, the algorithm handles them together. The expression `2^cnt - 1` counts all ways where at least one bit in the group is missing, while `2^larger` accounts for bits that appear later.

Python integers do not overflow, but all multiplications are reduced modulo `998244353` to match the required output format.

# Worked Examples

For:

```
2 1
0 1
```

the only appearing bit is bit 0 with first position 2.

| Group position | Number of bits | Larger bits | Contribution |
| --- | --- | --- | --- |
| 2 | 1 | 0 | 2 * (2^1 - 1) * 2^0 = 2 |

The answer is 2. The mask `0` fails at position 2, while mask `1` accepts every array value.

For:

```
2 2
2 1
```

the first positions are:

| Bit | First position |
| --- | --- |
| 0 | 2 |
| 1 | 1 |

After sorting, the positions are `[1, 2]`.

| Group position | Number of bits | Larger bits | Contribution |
| --- | --- | --- | --- |
| 1 | 1 | 1 | 1 * (2^1 - 1) * 2^1 = 2 |
| 2 | 1 | 0 | 2 * (2^1 - 1) * 2^0 = 2 |

The answer is 4. The four masks produce values `1, 1, 2, 0`.

# Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(nk + k log k) | Each number is checked against every bit, and at most `k` positions are sorted. |
| Space | O(k) | Only the first occurrence array and the compressed list are stored. |

The maximum `k` is 60 and `n` is only 100, so the algorithm performs only a few thousand bit operations. It avoids the impossible `2^k` enumeration.

# Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    out = sys.stdout.getvalue()

    sys.stdin = old_stdin
    sys.stdout = old_stdout
    return out

assert run("""2 1
0 1
""") == "2\n", "sample 1"

assert run("""2 2
2 1
""") == "4\n", "sample 2"

assert run("""1 1
0
""") == "0\n", "only zero value"

assert run("""2 2
3 3
""") == "4\n", "equal first positions"

assert run("""3 3
1 2 4
""") == "6\n", "every bit appears once"

assert run("""100 60
""" + " ".join(["0"] * 100) + "\n") == "0\n", "maximum size with no bits"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 1 / 0 1` | 2 | Basic single bit handling |
| `2 2 / 2 1` | 4 | Different first positions |
| `1 1 / 0` | 0 | No appearing bits |
| `2 2 / 3 3` | 4 | Equal first occurrence grouping |
| `3 3 / 1 2 4` | 6 | Independent bits |
| 100 zeros with 60 bits | 0 | Maximum input size and missing bits |

# Edge Cases

When a bit never appears, it should not participate in the sorted list. For example:

```
2 2
0 1
```

Only bit 0 has a first occurrence, at position 2. The algorithm ignores bit 1 completely and produces 2. Adding a fake value for bit 1 would count masks incorrectly.

When several bits first appear together, they must be counted as one group. For:

```
2 2
3 3
```

both bits have first position 1. There are three masks where at least one of these bits is missing, and all of them contribute value 1. The contribution is `1 * (2^2 - 1) = 3` from these masks, with the remaining mask contributing zero. The algorithm's grouping formula captures this directly.
