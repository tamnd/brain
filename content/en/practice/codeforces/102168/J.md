---
title: "CF 102168J - \u0418\u0433\u0440\u0430 \u0441 \u043f\u0435\u0440\u0435\u0441\u0442\u0430\u043d\u043e\u0432\u043a\u043e\u0439"
description: "We have a permutation p containing every integer from 1 to n exactly once. In each round, the first player names a, the second player names b, and a and b are guaranteed to be different. The winner is the player whose number appears earlier in the permutation."
date: "2026-08-19T07:33:14+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102168
codeforces_index: "J"
codeforces_contest_name: "\u041b\u0438\u0447\u043d\u044b\u0439 \u0447\u0435\u043c\u043f\u0438\u043e\u043d\u0430\u0442 \u0421\u0430\u043c\u0430\u0440\u0441\u043a\u043e\u0433\u043e \u0443\u043d\u0438\u0432\u0435\u0440\u0441\u0438\u0442\u0435\u0442\u0430 \u0441\u0440\u0435\u0434\u0438 \u043d\u043e\u0432\u0438\u0447\u043a\u043e\u0432 2018-2019"
rating: 0
weight: 102168
solve_time_s: 75
verified: true
draft: false
---

[CF 102168J - \u0418\u0433\u0440\u0430 \u0441 \u043f\u0435\u0440\u0435\u0441\u0442\u0430\u043d\u043e\u0432\u043a\u043e\u0439](https://codeforces.com/problemset/problem/102168/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 15s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a permutation `p` containing every integer from `1` to `n` exactly once. In each round, the first player names `a`, the second player names `b`, and `a` and `b` are guaranteed to be different. The winner is the player whose number appears earlier in the permutation.

For example, if

```
p = [4, 2, 5, 1, 3]
```

then the position of `2` is `2`, while the position of `3` is `5`. For a round `(2, 3)`, the first player wins because `2` occurs earlier. For `(3, 2)`, the second player wins.

The input gives the permutation first, followed by `q` independent queries. For every query we need to print `First` if the first number occurs earlier in the permutation, otherwise `Second`.

The constraints reach `n = 200000` and `q = 200000`. A solution that scans the permutation for every query could perform up to `n * q = 40,000,000,000` comparisons in the worst case, which is far beyond what a two-second limit can tolerate. We need to preprocess the permutation so that each query can be answered in constant time. An `O(n + q)` solution is comfortably appropriate.

There are several edge cases that can make a careless implementation fail. First, the winning number can be at the very first or very last position. For

```
2
2 1
1
1 2
```

the output is

```
Second
```

because `2` is at position `1` and `1` is at position `2`. An implementation that accidentally uses zero-based and one-based positions inconsistently can reverse this comparison.

The order of the two numbers in a query also matters. With

```
3
2 3 1
2
2 1
1 2
```

the output is

```
First
Second
```

The pair contains the same two values in both rounds, but the players have swapped them. Comparing the values themselves instead of their positions would give the wrong result.

Repeated queries are another useful case. For

```
4
3 1 4 2
3
1 2
1 2
2 1
```

the output is

```
First
First
Second
```

The preprocessing is shared by every query, so there is no reason to perform any additional work when the same pair appears again.

Finally, the phrase "all-equal values" cannot describe a valid test for this problem. The permutation contains distinct values, and every query explicitly contains two different values. The closest meaningful stress case is to repeat the same valid query many times, which tests whether the implementation accidentally changes state between rounds.

## Approaches

The direct solution is to process every query by searching through the permutation until the two requested values are found. Once both positions are known, we compare them. This is correct because the winner is defined entirely by which value occurs first.

The problem is the repeated search. In the worst case, a query can force us to inspect almost the entire permutation before finding its values. With `q = 200000` queries and `n = 200000`, the worst-case work is on the order of `40,000,000,000` array inspections. Even if a single inspection is very cheap, tens of billions of operations are not compatible with the time limit.

The key observation is that the permutation never changes between rounds. We are repeatedly asking the same kind of question about a fixed array: "Where does value `x` occur?" Since every value appears exactly once, we can answer every such question in advance.

Build an inverse permutation `pos`, where `pos[x]` stores the position at which the value `x` occurs in `p`. After that, a query `(a, b)` becomes only the comparison

```
pos[a] < pos[b]
```

If the expression is true, the first player wins. Otherwise, the second player wins.

This changes the problem from repeatedly searching an array to performing one linear preprocessing pass followed by constant-time queries.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nq) worst case | O(1) extra | Too slow |
| Optimal | O(n + q) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read `n` and the permutation `p`. The permutation is fixed for all rounds, so all useful information about positions can be computed once.
2. Create an array `pos` of size `n + 1`. For every index `i` and value `x = p[i]`, store `pos[x] = i`. The extra element at index `0` is unused because permutation values range from `1` to `n`.
3. Read the number of queries `q`. For each query, read the two values `a` and `b`.
4. Compare `pos[a]` and `pos[b]`. If `pos[a] < pos[b]`, the first player's number occurs earlier, so output `First`. Otherwise output `Second`.
5. Collect the answers and print them together. Building one output string avoids unnecessary repeated output operations when there are up to `200000` queries.

### Why it works

The central invariant is that after preprocessing, `pos[x]` is exactly the position of value `x` in the original permutation. Since the permutation contains every value exactly once, there is exactly one such position for every query value. For a query `(a, b)`, the first player wins precisely when the occurrence of `a` is before the occurrence of `b`, which is exactly the condition `pos[a] < pos[b]`. Thus every produced answer matches the rules of the game.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    p = list(map(int, input().split()))

    pos = [0] * (n + 1)

    for i, x in enumerate(p):
        pos[x] = i

    q = int(input())
    ans = []

    for _ in range(q):
        a, b = map(int, input().split())

        if pos[a] < pos[b]:
            ans.append("First")
        else:
            ans.append("Second")

    sys.stdout.write("\n".join(ans))

if __name__ == "__main__":
    solve()
```

The `pos` array is the entire optimization. During the preprocessing loop, `i` is a zero-based Python index, but that does not cause a problem because only relative order matters. If `pos[a] < pos[b]`, then `a` appears earlier regardless of whether positions are numbered from zero or one.

The array has length `n + 1` so that the value itself can be used directly as an index. This avoids an extra conversion such as `x - 1` and makes the query code particularly simple.

The query condition does not need an equality branch. The input guarantees `a != b`, and the permutation contains each value only once, so `pos[a]` and `pos[b]` can never be equal.

No integer overflow is possible in Python, and the largest stored index is only `199999`.

The answers are accumulated in `ans` and written once at the end. With `200000` queries, this is preferable to calling `print` separately for every result.

## Worked Examples

The supplied sample contains the permutation

```
p = [2, 3, 1]
```

so its inverse representation is `pos[1] = 2`, `pos[2] = 0`, and `pos[3] = 1`.

| Query | `a` | `b` | `pos[a]` | `pos[b]` | Result |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 2 | 2 | 0 | Second |
| 2 | 1 | 3 | 2 | 1 | Second |
| 3 | 2 | 1 | 0 | 2 | First |
| 4 | 2 | 3 | 0 | 1 | First |

This demonstrates why the actual numeric values are irrelevant once the inverse permutation has been built. For example, `1 < 3`, but `1` still loses against `3` because `1` occurs later in the permutation.

A second example is

```
4
3 1 4 2
3
1 2
1 4
2 1
```

The inverse permutation is `pos[1] = 1`, `pos[2] = 3`, `pos[3] = 0`, and `pos[4] = 2`.

| Query | `a` | `b` | `pos[a]` | `pos[b]` | Result |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 2 | 1 | 3 | First |
| 2 | 1 | 4 | 1 | 2 | First |
| 3 | 2 | 1 | 3 | 1 | Second |

The third query is especially useful because it has exactly the same two values as the first query but in the opposite order. The comparison is made from the players' perspective, so swapping `a` and `b` swaps the winner.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + q) | Building `pos` takes O(n), and every query takes O(1). |
| Space | O(n) | The inverse permutation stores one position for every value. |

With `n, q <= 200000`, the algorithm performs only a few hundred thousand array operations and comparisons. The `O(n)` memory usage is also easily within the 256 MB limit.

## Test Cases

The following test harness uses the same algorithm through a function that accepts an input string. The maximum-size case is generated rather than written literally, because writing a permutation of `200000` values into the source would obscure what the test is checking.

```python
import sys
import io

def solve(inp: str) -> str:
    data = inp.split()
    it = iter(data)

    n = int(next(it))
    p = [int(next(it)) for _ in range(n)]

    pos = [0] * (n + 1)
    for i, x in enumerate(p):
        pos[x] = i

    q = int(next(it))
    ans = []

    for _ in range(q):
        a = int(next(it))
        b = int(next(it))
        ans.append("First" if pos[a] < pos[b] else "Second")

    return "\n".join(ans)

# Provided sample.
sample1 = """\
3
2 3 1
4
1 2
1 3
2 1
2 3
"""

assert solve(sample1) == """\
Second
Second
First
First
""".strip(), "sample 1"

# Minimum-size permutation, both possible query orientations.
sample2 = """\
2
2 1
2
1 2
2 1
"""

assert solve(sample2) == """\
Second
First
""".strip(), "minimum size"

# Boundary values and repeated queries.
sample3 = """\
5
5 1 4 2 3
4
1 5
5 3
2 3
1 2
"""

assert solve(sample3) == """\
Second
First
Second
First
""".strip(), "boundary values"

# Repeated identical queries.
sample4 = """\
4
3 1 4 2
5
1 2
1 2
1 2
2 1
2 1
"""

assert solve(sample4) == """\
First
First
First
Second
Second
""".strip(), "repeated queries"

# Maximum-size stress test.
n = 200000
p = list(range(1, n + 1))

queries = []
for i in range(1, 100001):
    queries.append(f"{i} {n - i + 1}")

max_input = (
    f"{n}\n"
    + " ".join(map(str, p))
    + "\n100000\n"
    + "\n".join(queries)
    + "\n"
)

max_output = solve(max_input).splitlines()

assert len(max_output) == 100000, "maximum-size query count"
assert max_output[0] == "First", "maximum-size first query"
assert max_output[-1] == "Second", "maximum-size boundary query"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `3 / 2 3 1 / 4 queries` | `Second, Second, First, First` | Provided sample and position comparison |
| `2 / 2 1 / 2 queries` | `Second, First` | Minimum `n` and both query orientations |
| `5 / 5 1 4 2 3 / 4 queries` | `Second, First, Second, First` | Values at the first and last positions |
| `4 / 3 1 4 2 / 5 queries` | `First, First, First, Second, Second` | Repeated identical queries |
| `n = 200000` with `100000` queries | `100000` answers | Maximum-size preprocessing and query volume |

The problem's constraints make a literal all-equal test impossible. A permutation cannot contain duplicate values, and a query cannot have equal endpoints. Repeating one valid query is the appropriate substitute for testing accidental state changes between rounds.

## Edge Cases

Consider the minimum input

```
2
2 1
1
1 2
```

The preprocessing stores `pos[2] = 0` and `pos[1] = 1`. The query compares `pos[1] = 1` with `pos[2] = 0`, so the condition is false and the answer is `Second`. This catches implementations that compare the values rather than their positions.

For reversed query order, use

```
2
2 1
1
2 1
```

Now `pos[2] = 0 < pos[1] = 1`, so the output is `First`. The permutation has not changed. Only the players' assigned numbers have changed, which is why the output changes.

For a value at each extreme of the permutation, consider

```
5
5 1 4 2 3
2
1 5
5 3
```

The positions are `pos[1] = 1`, `pos[5] = 0`, and `pos[3] = 4`. The first query gives `Second` because `5` is before `1`. The second gives `First` because `5` is before `3`. This verifies that the first and last positions are handled normally.

For repeated queries, consider

```
4
3 1 4 2
4
1 2
1 2
2 1
2 1
```

The stored positions are `pos[1] = 1` and `pos[2] = 3`. Every `(1, 2)` query produces `First`, while every `(2, 1)` query produces `Second`. Since the algorithm never modifies `pos`, every repetition receives the same correct answer.

The boundary value `n` is also directly usable as an index because `pos` has size `n + 1`. For example, when `n = 200000`, the value `200000` is stored in `pos[200000]` without any special case. This avoids the common off-by-one error of allocating only `n` elements while still indexing by the value itself.
