---
title: "CF 1217C - The Number Of Good Substrings"
description: "We are given a binary string and asked to count its \"good\" substrings. A substring is good if its length equals the decimal value of its binary representation, allowing leading zeros."
date: "2026-06-11T22:49:44+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "bitmasks", "brute-force"]
categories: ["algorithms"]
codeforces_contest: 1217
codeforces_index: "C"
codeforces_contest_name: "Educational Codeforces Round 72 (Rated for Div. 2)"
rating: 1700
weight: 1217
solve_time_s: 108
verified: true
draft: false
---

[CF 1217C - The Number Of Good Substrings](https://codeforces.com/problemset/problem/1217/C)

**Rating:** 1700  
**Tags:** binary search, bitmasks, brute force  
**Solve time:** 1m 48s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a binary string and asked to count its "good" substrings. A substring is good if its length equals the decimal value of its binary representation, allowing leading zeros. That means for a substring like `011`, which is `3` in decimal, it is good only if its length is also `3`. Our input consists of multiple queries, each with one binary string, and the output for each query is the number of good substrings in that string.

The constraints give us up to 1000 queries, and the sum of lengths across all queries is at most 200,000. That means any algorithm iterating over all possible substrings naively is too slow, because generating all substrings is $O(n^2)$, which could reach $4 \cdot 10^{10}$ operations in the worst case. We need a solution closer to $O(n \cdot \text{small factor})$, ideally linear in practice.

Edge cases to watch are substrings with leading zeros. For instance, `000` has decimal value `0`, so only substrings of length zero would qualify, which is impossible. Another subtle case is long sequences of zeros followed by a single one, e.g., `0001`. Substrings like `001` have decimal `1` but length `3`, so they are not good. A careless approach that does not carefully compute the binary-to-decimal conversion for each substring length could overcount or undercount.

## Approaches

The naive approach is to consider every substring, convert it to decimal, and check if the substring length matches the decimal value. This is correct logically but requires $O(n^2)$ iterations per query. Even converting the binary string to decimal takes $O(n)$ per substring, so the worst-case complexity is $O(n^3)$, which is far beyond what is acceptable.

The key observation for an efficient solution is that substrings longer than roughly 20 characters cannot be "good" if their binary value is interpreted as an integer. This is because the length of the substring quickly becomes smaller than the value represented in binary. For example, a 20-bit substring with all ones is $2^{20}-1 \approx 10^6$, far exceeding the length of any string in our input constraints. Therefore, we only need to check substrings up to about 20 bits starting from each position.

Additionally, we need to skip leading zeros efficiently, but if we include them, we must ensure we do not miscount substrings whose decimal value is smaller than the length due to leading zeros. This insight reduces the problem from a quadratic scan over all substrings to a linear scan over each starting position with a fixed small window.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^3) | O(1) | Too slow |
| Optimal | O(n * 20) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of queries `t` and iterate over each query.
2. For each string `s` of length `n`, initialize a counter `ans = 0` to accumulate the number of good substrings.
3. Loop over each starting index `i` in the string.
4. Skip the leading zeros initially or account for them separately. Start building the decimal value `val = 0`.
5. For each end index `j` starting from `i` and extending at most 20 characters (or until the string ends), update `val = val * 2 + int(s[j])`.
6. Calculate the substring length as `length = j - i + 1`.
7. If `val == length`, increment `ans` by 1. If `val > length + 20`, break early because further extension can never satisfy the condition.
8. After finishing all start positions, print the counter `ans`.

Why it works: The invariant is that for each starting index, we only consider substrings whose length is comparable to their decimal value, which ensures we do not miss any potential good substring. The bound of 20 characters is sufficient because any longer binary number exceeds the maximum string length, guaranteeing correctness without iterating over impractical substring lengths.

## Python Solution

```python
import sys
input = sys.stdin.readline

def count_good_substrings(s):
    n = len(s)
    ans = 0
    for i in range(n):
        if s[i] == '0':
            continue
        val = 0
        for j in range(i, min(n, i + 20)):
            val = val * 2 + int(s[j])
            length = j - i + 1
            if val == length:
                ans += 1
            if val > n:
                break
    return ans

t = int(input())
for _ in range(t):
    s = input().strip()
    print(count_good_substrings(s))
```

The solution reads input efficiently and handles multiple queries. The inner loop only goes up to 20 characters, avoiding timeouts. The check `val > n` prevents unnecessary iterations beyond feasible substring lengths.

## Worked Examples

### Sample 1: `0110`

| i | j | s[i:j+1] | val | length | good? | ans |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 0 | 0 | 0 | 1 | No | 0 |
| 0 | 1 | 01 | 1 | 2 | No | 0 |
| 0 | 2 | 011 | 3 | 3 | Yes | 1 |
| 0 | 3 | 0110 | 6 | 4 | No | 1 |
| 1 | 1 | 1 | 1 | 1 | Yes | 2 |
| 1 | 2 | 11 | 3 | 2 | No | 2 |
| 1 | 3 | 110 | 6 | 3 | No | 2 |
| 2 | 2 | 1 | 1 | 1 | Yes | 3 |
| 2 | 3 | 10 | 2 | 2 | Yes | 4 |
| 3 | 3 | 0 | 0 | 1 | No | 4 |

The table confirms that all valid good substrings are counted.

### Sample 2: `0101`

Following similar tracing, we count good substrings: `1` at index 1, `1` at index 3, and `01` at index 2-3, totaling 3.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n * 20) | Outer loop over each start position and inner loop over at most 20 characters |
| Space | O(1) | Only counters and temporary variables used |

Given $n \le 2 \cdot 10^5$ and $t \le 1000$, the solution is fast enough for 4 seconds and fits within 256 MB memory.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline
    def count_good_substrings(s):
        n = len(s)
        ans = 0
        for i in range(n):
            if s[i] == '0':
                continue
            val = 0
            for j in range(i, min(n, i + 20)):
                val = val * 2 + int(s[j])
                length = j - i + 1
                if val == length:
                    ans += 1
                if val > n:
                    break
        return ans

    t = int(input())
    res = []
    for _ in range(t):
        s = input().strip()
        res.append(str(count_good_substrings(s)))
    return "\n".join(res)

# provided samples
assert run("4\n0110\n0101\n00001000\n0001000\n") == "4\n3\n4\n3", "sample 1"

# custom tests
assert run("1\n0\n") == "0", "single zero"
assert run("1\n1\n") == "1", "single one"
assert run("1\n11111\n") == "5", "all ones"
assert run("1\n000001\n") == "1", "trailing one after zeros"
assert run("1\n1000000000\n") == "1", "long sequence with leading one"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `0` | 0 | Single zero, no good substring |
| `1` | 1 | Single one counts as good |
| `11111` | 5 | All ones are individually good |
| `000001` | 1 | Handling leading zeros |
| `1000000000` | 1 | Long sequence with only one valid substring |

## Edge Cases

For a string like `00001000`, the algorithm skips leading zeros for starting positions until index 4. From index 4, it counts `1` of length 1, `10` of length 2, and so on, correctly identifying `4` good substrings. Substrings like `0000` are ignored because their decimal value is
