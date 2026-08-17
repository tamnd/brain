---
title: "CF 102203B - \u0421\u0440\u043e\u0447\u043d\u043e\u0435 \u0441\u043e\u043e\u0431\u0449\u0435\u043d\u0438\u0435"
description: "We have a binary string describing what happens during each nanosecond of message reception. A 0 means that the receiver successfully gets the message at that moment, while a 1 means interference prevents reception."
date: "2026-08-18T00:36:27+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102203
codeforces_index: "B"
codeforces_contest_name: "\u0427\u0435\u0442\u0432\u0435\u0440\u0442\u0430\u044f \u041b\u0438\u043f\u0435\u0446\u043a\u0430\u044f \u043a\u043e\u043c\u0430\u043d\u0434\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430 \u0448\u043a\u043e\u043b\u044c\u043d\u0438\u043a\u043e\u0432 \u043f\u043e \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044e (8-11 \u043a\u043b\u0430\u0441\u0441\u044b)"
rating: 0
weight: 102203
solve_time_s: 73
verified: true
draft: false
---

[CF 102203B - \u0421\u0440\u043e\u0447\u043d\u043e\u0435 \u0441\u043e\u043e\u0431\u0449\u0435\u043d\u0438\u0435](https://codeforces.com/problemset/problem/102203/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 13s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a binary string describing what happens during each nanosecond of message reception. A `0` means that the receiver successfully gets the message at that moment, while a `1` means interference prevents reception. The first and last positions are guaranteed to be `0`, so the message has a recognized beginning and end.

For every query value `k`, the receiver is allowed to encounter interference for strictly fewer than `k` consecutive nanoseconds. If some block of interference contains `k` or more consecutive `1`s, the message cannot be received completely. We need to answer whether the entire string is receivable for each of the given values of `k`.

The input contains the string length `n`, the number of queries `m`, the binary string itself, and then `m` values of `k`. Each output line is `YES` when every consecutive block of `1`s has length less than `k`, and `NO` otherwise.

The length of the string can reach `10^6`, while the number of queries can reach `3 \cdot 10^5`. This immediately rules out doing a full scan of the string for every query. Such an approach would perform up to `10^6 * 3 * 10^5 = 3 * 10^11` character checks, which is far beyond what can fit into a one-second limit. We need to extract all information relevant to every query in essentially one pass over the string.

The edge cases come from the strict inequality in the condition. For example, consider

```
2 2
00
1
2
```

There are no interference positions at all, so both queries must produce `YES`. A careless solution that looks for a positive gap and treats an absent run as length one could incorrectly reject `k = 1`.

Another boundary case is

```
4 3
0110
1
2
3
```

The longest block of interference has length `2`, so the output is

```
NO
NO
YES
```

The second query is rejected because the rule requires the run length to be strictly less than `k`. A solution using `run <= k` would incorrectly print `YES` for `k = 2`.

A third useful case is

```
3 2
010
1
2
```

Every block of `1`s has length exactly `1`, so the answers are

```
NO
YES
```

Again, `k = 1` does not allow even a single noisy nanosecond.

## Approaches

The direct solution is to process every query independently. For a particular `k`, scan the string while maintaining the current number of consecutive `1`s. If that number ever reaches `k`, the answer is immediately `NO`; if the scan finishes, the answer is `YES`. This is correct because the only thing that can invalidate a query is a sufficiently long consecutive block of interference.

The problem is the repeated scan. In the worst case, the string has `10^6` characters and there are `3 \cdot 10^5` queries. If every query requires inspecting the whole string, the worst case is about `3 \cdot 10^11` operations. Even though each individual scan is simple, repeating it this many times is impossible under the time limit.

The key observation is that all queries ask the same question about the same string. We do not need to know the lengths of all runs separately for each query. Let `mx` be the length of the longest consecutive block of `1`s in the entire string. Every other block is no longer than `mx`, so a query succeeds exactly when

`mx < k`.

Thus the whole string can be summarized by a single integer. We find `mx` once in `O(n)` time, then every query is answered with one comparison in `O(1)` time.

The brute-force method works because it directly checks every possible obstruction for each `k`, but it fails because the obstruction does not actually depend on `k`. The observation that the longest noisy block completely determines every query reduces the problem from repeatedly scanning the string to one preprocessing pass followed by constant-time queries.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `O(nm)` | `O(1)` | Too slow |
| Optimal | `O(n + m)` | `O(1)` besides input storage | Accepted |

## Algorithm Walkthrough

1. Read `n`, `m`, and the binary string `s`. The string contains all information needed to determine the worst interference period.
2. Scan `s` from left to right while maintaining `cur`, the length of the current consecutive block of `1`s. When the current character is `1`, increment `cur`. When it is `0`, the current noisy block has ended, so reset `cur` to zero.
3. During the same scan, maintain `mx`, the largest value that `cur` has ever reached. This is the longest period during which the receiver gets continuous interference.
4. Read each query `k` and compare it with `mx`. Print `YES` exactly when `mx < k`, because the allowed number of consecutive noisy nanoseconds is strictly less than `k`.
5. Collect the answers and print them together. Building one output string avoids unnecessary repeated output operations when there are up to `3 \cdot 10^5` queries.

### Why it works

The value `mx` is the maximum length of any consecutive block of `1`s. A query with value `k` is valid precisely when no interference block has length `k` or more. Since `mx` is the largest such block, all blocks have length less than `k` exactly when `mx < k`. The preprocessing computes the true maximum, so the comparison gives the correct answer for every query independently.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    s = input().strip()

    mx = 0
    cur = 0

    for ch in s:
        if ch == '1':
            cur += 1
            if cur > mx:
                mx = cur
        else:
            cur = 0

    ans = []

    for _ in range(m):
        k = int(input())
        if mx < k:
            ans.append("YES")
        else:
            ans.append("NO")

    sys.stdout.write("\n".join(ans))

if __name__ == "__main__":
    solve()
```

The scan uses `cur` to represent the current run of interference. Incrementing it only on `1` and resetting it on `0` makes every consecutive run independent of the others. Whenever `cur` becomes larger than `mx`, we update the global maximum.

The comparison is deliberately `mx < k`, not `mx <= k`. The statement allows strictly fewer than `k` consecutive noisy nanoseconds. For a maximum run of length `3`, `k = 3` must produce `NO`, while `k = 4` produces `YES`.

The guaranteed first and last characters are `0`, but the algorithm does not rely on this for correctness. It would also correctly process a string containing a run of `1`s at either boundary.

There is no integer overflow issue because the largest counter is only `n`, at most `10^6`, which Python handles directly anyway. The string itself is stored once, and the answer list contains at most `3 \cdot 10^5` short strings.

## Worked Examples

### Example 1

The statement's example has a seven-character message with three consecutive noisy positions. We can represent it as `0111000`, with queries `1`, `4`, and `3`.

The scan behaves as follows.

| Position | Character | `cur` | `mx` |
| --- | --- | --- | --- |
| 1 | `0` | 0 | 0 |
| 2 | `1` | 1 | 1 |
| 3 | `1` | 2 | 2 |
| 4 | `1` | 3 | 3 |
| 5 | `0` | 0 | 3 |
| 6 | `0` | 0 | 3 |
| 7 | `0` | 0 | 3 |

The final maximum interference run is `mx = 3`. For `k = 1`, `3 < 1` is false, so the answer is `NO`. For `k = 4`, `3 < 4` is true, so the answer is `YES`. For `k = 3`, the inequality is again false, giving `NO`.

The resulting output is

```
NO
YES
NO
```

This example specifically demonstrates why the comparison must be strict.

### Example 2

Consider

```
5 4
01010
1
2
3
100
```

There are two separate interference blocks, each of length `1`.

| Position | Character | `cur` | `mx` |
| --- | --- | --- | --- |
| 1 | `0` | 0 | 0 |
| 2 | `1` | 1 | 1 |
| 3 | `0` | 0 | 1 |
| 4 | `1` | 1 | 1 |
| 5 | `0` | 0 | 1 |

The final value is `mx = 1`. The queries are answered using only this value.

| `k` | Condition | Answer |
| --- | --- | --- |
| 1 | `1 < 1` | `NO` |
| 2 | `1 < 2` | `YES` |
| 3 | `1 < 3` | `YES` |
| 100 | `1 < 100` | `YES` |

This demonstrates that the number of noisy blocks does not matter. Only the longest one affects the answer.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(n + m)` | The string is scanned once and every query takes constant time. |
| Space | `O(n + m)` | The input string and the collected output are stored; the algorithm itself uses `O(1)` auxiliary state. |

With `n <= 10^6` and `m <= 3 \cdot 10^5`, the algorithm performs roughly one million character operations followed by at most three hundred thousand comparisons. This is comfortably within the intended scale, unlike the `O(nm)` brute-force approach.

## Test Cases

```python
import sys
import io

def solve():
    input = sys.stdin.readline

    n, m = map(int, input().split())
    s = input().strip()

    mx = 0
    cur = 0

    for ch in s:
        if ch == '1':
            cur += 1
            mx = max(mx, cur)
        else:
            cur = 0

    ans = []
    for _ in range(m):
        k = int(input())
        ans.append("YES" if mx < k else "NO")

    sys.stdout.write("\n".join(ans))

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    try:
        solve()
        return sys.stdout.getvalue()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

# Provided sample, whose string is 0111000 according to the statement's description.
assert run(
    "7 3\n"
    "0111000\n"
    "1\n"
    "4\n"
    "3\n"
) == "NO\nYES\nNO", "sample 1"

# Minimum-size string, with no interference.
assert run(
    "2 3\n"
    "00\n"
    "1\n"
    "2\n"
    "100\n"
) == "YES\nYES\nYES", "minimum size and all zeros"

# One noisy position, testing the exact boundary mx == k.
assert run(
    "3 3\n"
    "010\n"
    "1\n"
    "2\n"
    "3\n"
) == "NO\nYES\nYES", "single noisy position"

# Several runs, with the longest one in the middle.
assert run(
    "9 4\n"
    "011011110\n"
    "1\n"
    "4\n"
    "5\n"
    "6\n"
) == "NO\nNO\nYES\nYES", "longest run is four"

# Large input, checking that the solution remains linear.
n = 1000000
s = "0" + "1" * 999998 + "0"
large_input = (
    f"{n} 3\n"
    f"{s}\n"
    "999998\n"
    "999999\n"
    "1000000\n"
)
assert run(large_input) == "NO\nYES\nYES", "maximum string length"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 3 / 00 / 1, 2, 100` | `YES / YES / YES` | Minimum length and absence of any noisy block |
| `3 3 / 010 / 1, 2, 3` | `NO / YES / YES` | Exact boundary when the longest run has length `1` |
| `9 4 / 011011110 / 1, 4, 5, 6` | `NO / NO / YES / YES` | Multiple runs and strict inequality at `k = 4` |
| `1000000 3 / 0 + 999998 ones + 0 / 999998, 999999, 1000000` | `NO / YES / YES` | Maximum string size and largest possible run |

## Edge Cases

The all-zero case is handled by leaving `mx` equal to zero throughout the scan. For the input

```
2 2
00
1
2
```

the algorithm never increments `cur`, so `mx = 0`. Both `0 < 1` and `0 < 2` are true, producing `YES` for both queries. This avoids inventing a nonexistent noisy block.

The exact-boundary case is handled by the strict comparison. For

```
4 3
0110
1
2
3
```

the scan finds `mx = 2`. The query `k = 1` fails, `k = 2` also fails because `2` is not strictly smaller than `2`, and `k = 3` succeeds. The output is

```
NO
NO
YES
```

The case with a single noisy position,

```
3 2
010
1
2
```

produces `mx = 1`. A limit of `1` is insufficient because the condition requires fewer than one consecutive noisy nanosecond, while a limit of `2` permits a run of length one. The output is `NO` followed by `YES`.

Multiple separated noisy blocks do not require separate query processing. For

```
9 4
011011110
1
4
5
6
```

the run lengths are `2`, `1`, and `4`, so `mx = 4`. The first two queries fail, while `4 < 5` and `4 < 6` succeed. The algorithm reaches the same result without storing the individual run lengths, because only their maximum can affect any query.
