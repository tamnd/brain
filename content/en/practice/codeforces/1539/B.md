---
title: "CF 1539B - Love Song"
description: "We are given a lowercase string representing the song and many queries on contiguous substrings of that string. Each letter contributes a value equal to its position in the alphabet. For example, a = 1, b = 2, c = 3, and so on."
date: "2026-06-10T14:42:43+07:00"
tags: ["codeforces", "competitive-programming", "dp", "implementation", "strings"]
categories: ["algorithms"]
codeforces_contest: 1539
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 727 (Div. 2)"
rating: 800
weight: 1539
solve_time_s: 502
verified: false
draft: false
---

[CF 1539B - Love Song](https://codeforces.com/problemset/problem/1539/B)

**Rating:** 800  
**Tags:** dp, implementation, strings  
**Solve time:** 8m 22s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a lowercase string representing the song and many queries on contiguous substrings of that string.

Each letter contributes a value equal to its position in the alphabet. For example, `a = 1`, `b = 2`, `c = 3`, and so on. For a query `[l, r]`, we look at the substring from position `l` to position `r`. Every character is repeated as many times as its alphabet value, and we need the length of the resulting expanded string.

Instead of actually building the expanded string, we can think about how much each character contributes to the final length. If a character is `c`, it contributes `3`. If a character is `z`, it contributes `26`. The answer for a substring is simply the sum of these values over all characters in that range.

The constraints are the key part of the problem. The string length and the number of queries can both reach `100000`. A solution that scans the entire substring for every query would require up to `100000 × 100000 = 10^10` operations in the worst case, which is far beyond what can run within two seconds. We need a way to answer each query in constant or logarithmic time after some preprocessing.

One easy mistake is to interpret the task as counting distinct letters. Consider:

```
s = "aaa"
query = [1, 3]
```

Each `a` contributes `1`, so the answer is:

```
1 + 1 + 1 = 3
```

The correct output is `3`, not `1`.

Another common mistake is using zero-based query indices even though the input uses one-based positions.

Example:

```
s = "ab"
query = [1, 1]
```

The substring is `"a"`, so the answer is `1`.

If we accidentally treat the query as zero-based, we would access the wrong character and produce an incorrect result.

A third subtle case occurs when the query covers the entire string:

```
s = "zzz"
query = [1, 3]
```

The answer is:

```
26 + 26 + 26 = 78
```

Any off-by-one error in the prefix sum boundaries immediately produces the wrong result on such ranges.

## Approaches

The most direct solution is to process every query independently. For a query `[l, r]`, we iterate through all characters in that substring, convert each letter into its alphabet position, sum the values, and print the result.

This approach is correct because the required answer is exactly that sum. The problem is efficiency. A substring can contain up to `100000` characters, and there can be `100000` queries. In the worst case, we would perform about `10^10` character visits, which is far too slow.

The structure of the problem suggests a better approach. Every query asks for the sum of values over a contiguous segment of the same array. Once we convert each character into its alphabet value, the task becomes a classic range-sum query problem.

For range-sum queries on a static array, prefix sums are the standard tool. If `pref[i]` stores the total value of the first `i` characters, then the sum on any interval `[l, r]` can be obtained by subtracting two prefix sums:

```
pref[r] - pref[l - 1]
```

The preprocessing takes linear time, and every query becomes a constant-time computation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nq) | O(1) | Too slow |
| Optimal | O(n + q) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read `n`, `q`, and the string `s`.
2. Create a prefix sum array `pref` of length `n + 1`, with `pref[0] = 0`.
3. Traverse the string from left to right.
4. For each character, compute its alphabet position using:

```
ord(character) - ord('a') + 1
```
5. Store cumulative sums in the prefix array.

`pref[i]` should contain the total value of the first `i` characters.
6. For every query `[l, r]`, compute:

```
answer = pref[r] - pref[l - 1]
```
7. Output the answer.

### Why it works

The prefix array maintains the invariant that `pref[i]` equals the sum of character values in positions `1` through `i`.

When we compute `pref[r] - pref[l - 1]`, the contribution of positions `1` through `l - 1` appears in both terms and cancels out. What remains is exactly the sum of values from position `l` through position `r`, which is the required length of the expanded string. Since every character contributes independently to the final length, this sum is precisely the answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, q = map(int, input().split())
    s = input().strip()

    pref = [0] * (n + 1)

    for i in range(1, n + 1):
        pref[i] = pref[i - 1] + (ord(s[i - 1]) - ord('a') + 1)

    ans = []

    for _ in range(q):
        l, r = map(int, input().split())
        ans.append(str(pref[r] - pref[l - 1]))

    sys.stdout.write("\n".join(ans))

if __name__ == "__main__":
    solve()
```

The first part reads the input and converts the string into cumulative alphabet-value sums. The expression `ord(s[i - 1]) - ord('a') + 1` maps `a` to `1`, `b` to `2`, and so on.

The prefix array uses one-based indexing. This choice matches the query format and makes the range formula straightforward. The value at `pref[0]` is zero, which allows queries starting at position `1` to be handled without special cases.

For each query, the answer is obtained with a single subtraction. No characters from the substring are scanned again.

A common implementation mistake is mixing string indices and prefix indices. The string itself is zero-based, so character `i` in the prefix construction corresponds to `s[i - 1]`.

## Worked Examples

### Sample 1

Input:

```
7 3
abacaba
1 3
2 5
1 7
```

Character values:

| Position | Character | Value | Prefix Sum |
| --- | --- | --- | --- |
| 0 | - | - | 0 |
| 1 | a | 1 | 1 |
| 2 | b | 2 | 3 |
| 3 | a | 1 | 4 |
| 4 | c | 3 | 7 |
| 5 | a | 1 | 8 |
| 6 | b | 2 | 10 |
| 7 | a | 1 | 11 |

Queries:

| l | r | Calculation | Answer |
| --- | --- | --- | --- |
| 1 | 3 | 4 - 0 | 4 |
| 2 | 5 | 8 - 1 | 7 |
| 1 | 7 | 11 - 0 | 11 |

Output:

```
4
7
11
```

This example shows how every query becomes a subtraction of two prefix sums, regardless of substring length.

### Custom Example

Input:

```
5 2
abcde
1 5
3 4
```

Prefix sums:

| Position | Character | Value | Prefix Sum |
| --- | --- | --- | --- |
| 0 | - | - | 0 |
| 1 | a | 1 | 1 |
| 2 | b | 2 | 3 |
| 3 | c | 3 | 6 |
| 4 | d | 4 | 10 |
| 5 | e | 5 | 15 |

Queries:

| l | r | Calculation | Answer |
| --- | --- | --- | --- |
| 1 | 5 | 15 - 0 | 15 |
| 3 | 4 | 10 - 3 | 7 |

Output:

```
15
7
```

This trace demonstrates that interior ranges work exactly the same way as ranges touching the boundaries.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + q) | Building the prefix array takes O(n), each query takes O(1) |
| Space | O(n) | The prefix sum array stores n + 1 integers |

With `n` and `q` both as large as `100000`, the algorithm performs only a few hundred thousand operations. This comfortably fits within the time limit, and the memory usage is small compared to the available 256 MB.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    n, q = map(int, input().split())
    s = input().strip()

    pref = [0] * (n + 1)

    for i in range(1, n + 1):
        pref[i] = pref[i - 1] + (ord(s[i - 1]) - ord('a') + 1)

    ans = []

    for _ in range(q):
        l, r = map(int, input().split())
        ans.append(str(pref[r] - pref[l - 1]))

    return "\n".join(ans)

# provided sample
assert run(
"""7 3
abacaba
1 3
2 5
1 7
"""
) == "4\n7\n11", "sample"

# minimum size
assert run(
"""1 1
a
1 1
"""
) == "1", "single character"

# all equal letters
assert run(
"""4 2
bbbb
1 4
2 3
"""
) == "8\n4", "repeated letters"

# entire range and suffix range
assert run(
"""3 2
zzz
1 3
2 3
"""
) == "78\n52", "large letter values"

# off-by-one boundary check
assert run(
"""2 2
ab
1 1
2 2
"""
) == "1\n2", "boundary positions"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `a`, query `[1,1]` | `1` | Minimum valid input |
| `bbbb` with multiple queries | `8`, `4` | Repeated letters and range sums |
| `zzz` | `78`, `52` | Large alphabet values |
| `ab` with single-position queries | `1`, `2` | Boundary handling and indexing correctness |

## Edge Cases

Consider the smallest possible input:

```
1 1
a
1 1
```

The prefix array becomes:

```
pref = [0, 1]
```

The answer is:

```
pref[1] - pref[0] = 1
```

The algorithm correctly handles ranges that begin at position `1` because `pref[0]` exists.

Now consider a range covering the entire string:

```
3 1
zzz
1 3
```

The prefix array is:

```
pref = [0, 26, 52, 78]
```

The query result is:

```
78 - 0 = 78
```

No special handling is needed for full-range queries.

Finally, consider a query ending at the last character but not starting at the first:

```
5 1
abcde
3 5
```

The prefix sums are:

```
[0, 1, 3, 6, 10, 15]
```

The answer becomes:

```
15 - 3 = 12
```

which equals `3 + 4 + 5`. This confirms that subtracting `pref[l - 1]` removes exactly the unwanted prefix and leaves only the requested substring contribution.
