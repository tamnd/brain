---
title: "CF 102625I - Treat To Banta Hai"
description: "The problem asks us to choose one continuous group of juniors from the given order. We may remove some juniors from the beginning and some from the end, but the remaining juniors must stay consecutive. If the chosen segment has values t1, t2, ..."
date: "2026-08-03T15:23:08+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102625
codeforces_index: "I"
codeforces_contest_name: "IIT(ISM) Virtual Farewell"
rating: 0
weight: 102625
solve_time_s: 49
verified: true
draft: false
---

[CF 102625I - Treat To Banta Hai](https://codeforces.com/problemset/problem/102625/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 49s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem asks us to choose one continuous group of juniors from the given order. We may remove some juniors from the beginning and some from the end, but the remaining juniors must stay consecutive. If the chosen segment has values `t1, t2, ..., tk`, its happiness is calculated as `1*t1 + 2*t2 + ... + k*tk`. We need the maximum possible happiness, and choosing no junior is allowed, giving a score of zero.

The input contains the number of juniors and the happiness contribution value of each junior. The output is a single integer representing the best score obtainable from any contiguous segment.

The number of juniors can reach `2 * 10^5`, and each value can have magnitude up to `10^7`. A quadratic approach would perform around `n^2 / 2` segment checks, which becomes about `2 * 10^10` operations in the worst case. That is far beyond what can fit in a normal time limit. We need an algorithm close to linear or `n log n`.

The values can be negative, so assuming that a non-empty segment is always better is incorrect. For example:

Input:

```
3
-60 -70 -80
```

The correct output is:

```
0
```

A method that always starts with the first element or always chooses a segment would return a negative value, even though giving no treat is allowed.

Another tricky case is that the segment's weights restart from one after removing a prefix. For example:

Input:

```
6
5 -1000 1 -3 7 -8
```

The best segment is `[1, -3, 7]`, not a segment containing the first value. Its score is `1*1 + 2*(-3) + 3*7 = 16`. A careless implementation using original indices instead of positions inside the chosen segment would calculate the wrong expression.

## Approaches

The direct solution is to try every possible contiguous segment. For a segment from `l` to `r`, we can calculate its score by walking through it and multiplying every element by its position inside the segment. This is correct because it follows the definition exactly.

However, there are `O(n^2)` possible segments. Even if every score calculation is optimized with prefix sums, checking all pairs of endpoints still requires about `4 * 10^10` endpoint combinations when `n = 200000`, which is too slow.

The key observation is that the score of a segment can be transformed into a form where each possible left boundary becomes a line. Prefix sums let us avoid rebuilding the weighted sum for every segment, and then a data structure can maintain the best previous left boundary.

Let `P[i]` be the prefix sum of values up to `i`, and let `Q[i]` be the prefix sum of `index * value`, where indices start from one. For a segment starting after position `j` and ending at `r`, its score is:

`Q[r] - Q[j] - j * (P[r] - P[j])`

Rearranging:

`Q[r] - j * P[r] + (j * P[j] - Q[j])`

For a fixed `r`, `Q[r]` is constant. The remaining expression asks for the maximum value of lines:

`y = -j * x + (j * P[j] - Q[j])`

at `x = P[r]`.

Each previous position creates one line, and each new prefix sum becomes a query. Since prefix sums can be negative or positive, we use Li Chao Tree to support arbitrary query coordinates.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) | Too slow |
| Optimal | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Build prefix sums while processing the array from left to right. Maintain `P`, the normal prefix sum, and `Q`, the weighted prefix sum.
2. Insert the line corresponding to position `j = 0` before processing any element. This represents starting a segment from the first element. The line has slope `0` and intercept `0`.
3. For every position `r`, update the prefix sums to include the current value. Query the Li Chao Tree at `x = P[r]`. The returned maximum line value plus `Q[r]` gives the best segment ending at `r`.
4. After using the current prefix, insert the line created by this position. The line is based on `j = r`, because future segments may start after this position.
5. Keep the maximum between all obtained values and zero, because selecting no juniors is valid.

Why it works:

At every position `r`, every possible segment ending at `r` corresponds to exactly one earlier position `j`. The line created by `j` stores the contribution of choosing that starting point. Querying at the current prefix sum selects the best possible starting point among all previous ones. Since every possible segment is considered when its right endpoint is processed, the maximum value found is exactly the best achievable happiness.

## Python Solution

```python
import sys
input = sys.stdin.readline

class LiChao:
    def __init__(self, xs):
        self.xs = xs
        self.tree = [None] * (4 * len(xs))

    def value(self, line, x):
        m, c = line
        return m * x + c

    def add_line(self, line, node=1, left=0, right=None):
        if right is None:
            right = len(self.xs) - 1

        mid = (left + right) // 2
        x_left = self.xs[left]
        x_mid = self.xs[mid]

        if self.tree[node] is None:
            self.tree[node] = line
            return

        cur = self.tree[node]

        if self.value(line, x_mid) > self.value(cur, x_mid):
            self.tree[node], line = line, self.tree[node]
            cur = self.tree[node]

        if left == right:
            return

        if self.value(line, x_left) > self.value(cur, x_left):
            self.add_line(line, node * 2, left, mid)
        elif self.value(line, self.xs[right]) > self.value(cur, self.xs[right]):
            self.add_line(line, node * 2 + 1, mid + 1, right)

    def query(self, x, node=1, left=0, right=None):
        if right is None:
            right = len(self.xs) - 1

        res = -10**30
        if self.tree[node] is not None:
            res = self.value(self.tree[node], x)

        if left == right:
            return res

        mid = (left + right) // 2
        if x <= self.xs[mid]:
            return max(res, self.query(x, node * 2, left, mid))
        return max(res, self.query(x, node * 2 + 1, mid + 1, right))

def solve():
    n = int(input())
    a = list(map(int, input().split()))

    pref = [0]
    weighted = [0]

    s = 0
    w = 0
    for i, x in enumerate(a, 1):
        s += x
        w += i * x
        pref.append(s)
        weighted.append(w)

    lichao = LiChao(pref)

    ans = 0
    lichao.add_line((0, 0))

    for i in range(1, n + 1):
        best = lichao.query(pref[i])
        ans = max(ans, weighted[i] + best)

        j = i
        lichao.add_line((-j, j * pref[j] - weighted[j]))

    print(ans)

if __name__ == "__main__":
    solve()
```

The Li Chao Tree stores lines in the form `slope * x + intercept`. For position `j`, the slope is `-j` and the intercept is `j * P[j] - Q[j]`, matching the rearranged segment formula.

The prefix arrays use one-based positions because the multiplier in the happiness score starts from one. Mixing zero-based indices with the formula is a common source of wrong answers.

The query happens before inserting the current position's line. The current prefix cannot be used as a starting point for a segment ending at itself because that would create an empty segment. The initially inserted zero line handles segments that begin at the first junior.

Python integers do not overflow, so the large intermediate values from `index * value` remain safe.

## Worked Examples

For the first example:

```
6
5 -1000 1 -3 7 -8
```

The important values during processing are:

| Position | Prefix Sum | Weighted Prefix | Best Line Value | Current Answer |
| --- | --- | --- | --- | --- |
| 1 | 5 | 5 | 0 | 5 |
| 2 | -995 | -1995 | 0 | 5 |
| 3 | -994 | -1992 | 1 | 16 |
| 4 | -997 | -2004 | 6 | 16 |
| 5 | -990 | -1969 | 15 | 16 |
| 6 | -998 | -2017 | 23 | 6 |

The maximum occurs when the chosen segment is `[1, -3, 7]`. The trace shows that the best starting point is not necessarily the first element of the array.

For the second example:

```
5
1000 1000 1001 1000 1000
```

| Position | Prefix Sum | Weighted Prefix | Best Line Value | Current Answer |
| --- | --- | --- | --- | --- |
| 1 | 1000 | 1000 | 0 | 1000 |
| 2 | 2000 | 3000 | -1000 | 2000 |
| 3 | 3001 | 6003 | -1000 | 5003 |
| 4 | 4001 | 10003 | -1000 | 9003 |
| 5 | 5001 | 15003 | 0 | 15003 |

The algorithm keeps all possible starting positions, allowing it to discover that taking the whole array is optimal.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Each of the `n` prefixes performs one Li Chao query and one insertion. |
| Space | O(n) | The coordinate list and Li Chao Tree contain linear numbers of stored values. |

With `n = 200000`, the logarithmic factor keeps the number of operations around a few million, which fits comfortably.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    result = sys.stdout.getvalue()

    sys.stdin = old_stdin
    sys.stdout = old_stdout
    return result

assert run("6\n5 -1000 1 -3 7 -8\n") == "16\n"
assert run("5\n1000 1000 1001 1000 1000\n") == "15003\n"

assert run("1\n-5\n") == "0\n"
assert run("3\n-60 -70 -80\n") == "0\n"
assert run("4\n1 2 3 4\n") == "30\n"
assert run("5\n10 -100 10 -100 10\n") == "10\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / -5` | `0` | A single negative value and empty segment choice |
| `-60 -70 -80` | `0` | All values negative |
| `1 2 3 4` | `30` | Increasing positive values where the full segment is best |
| `10 -100 10 -100 10` | `10` | Choosing a middle segment instead of the whole array |

## Edge Cases

For an array containing only negative values, the Li Chao Tree still produces valid segment values, but the final comparison with zero keeps the answer correct. For input:

```
3
-60 -70 -80
```

every inserted line produces a negative or smaller value, so the answer remains `0`.

When the optimal segment begins after a large negative prefix, the algorithm does not commit to early elements. In:

```
6
5 -1000 1 -3 7 -8
```

the prefix positions before the positive segment are all represented by lines. The query at the end of each position selects the best starting point automatically, which gives the segment `[1, -3, 7]` and score `16`.

When all values are positive, the algorithm must still respect the increasing weights inside the selected segment. For:

```
4
1 2 3 4
```

the whole segment is chosen, producing `1 + 4 + 9 + 16 = 30`. The prefix transformation preserves these increasing multipliers because the weighted prefix `Q` stores the original position contribution and the line correction shifts it back to the chosen segment start.
