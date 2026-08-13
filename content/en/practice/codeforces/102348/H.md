---
title: "CF 102348H - Berland Prospect"
description: "We have a sorted array of lantern coordinates x[0], x[1], ..., x[n-1]. We may keep any subset of these lanterns switched on, but when the chosen coordinates are read from left to right, every consecutive gap must be identical."
date: "2026-08-14T02:24:39+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102348
codeforces_index: "H"
codeforces_contest_name: "ICPC 2019-2020 NERC (NEERC), Southern and Volga Russia Qualifier"
rating: 0
weight: 102348
solve_time_s: 229
verified: false
draft: false
---

[CF 102348H - Berland Prospect](https://codeforces.com/problemset/problem/102348/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 3m 49s  
**Verified:** no  

## Solution
## Problem Understanding

We have a sorted array of lantern coordinates `x[0], x[1], ..., x[n-1]`. We may keep any subset of these lanterns switched on, but when the chosen coordinates are read from left to right, every consecutive gap must be identical. In other words, the chosen coordinates must form an arithmetic progression.

The task is to find the maximum possible number of coordinates from the given array that belong to one arithmetic progression. Because fewer than three selected lanterns are always valid, the answer is at least `2`, and with `n >= 3` we only need to find the longest progression containing at least three coordinates.

The array is already strictly increasing, so the order of the lanterns is fixed and we never have to sort it. The value `n <= 3000` is the key constraint. An `O(n^2)` algorithm performs about 4.5 million pair transitions at the upper bound, which is realistic for a 2 second contest limit in a compiled language and still manageable in Python with careful storage. An `O(n^3)` algorithm would involve billions of operations and is far too slow. The coordinates can reach `10^18`, so the differences cannot safely be stored in a 32-bit integer, although Python integers handle them directly.

There are several edge cases that can make a careless implementation wrong. With exactly three lanterns, for example,

```
3
1 2 4
```

the answer is `3`, even though the gaps are `1` and `2`. A solution that assumes every selected set of three must already have equal gaps would incorrectly reject this, because the problem only requires equal gaps when there are at least three selected lanterns, and here we can select `1, 2, 4` as three lanterns only if their gaps are equal. They are not, so the actual answer is `2`. This is precisely why the special case for fewer than three selected lanterns means the answer for this input is `2`, not `3`.

A more useful boundary example is

```
3
1 2 3
```

where the answer is `3`. A DP that initializes every pair to length `1` instead of `2` would report the wrong value, because every pair of distinct lanterns already forms a valid arithmetic progression of length two.

Another common mistake is assuming the coordinates are small enough for array indexing. For

```
3
0 500000000000000000 1000000000000000000
```

the answer is `3`. The difference is `5 * 10^17`, far outside ordinary coordinate-indexed arrays. The algorithm must use a hash map for coordinate lookup.

Finally, the input guarantees strictly increasing coordinates, so an "all equal values" test such as `1 1 1` is not a valid test case. The closest valid stress case is an array with all gaps equal, such as `0 1 2 3 4`, which deliberately tests the situation where the entire array belongs to one progression.

## Approaches

A direct brute-force solution can choose two lanterns, regard their distance as the candidate common difference, and repeatedly ask whether the next coordinate exists. This is correct because every arithmetic progression is completely determined by its first two coordinates. With a hash set, each membership test is constant expected time.

The problem is the amount of repetition. There are `C(n, 2)` possible starting pairs, and a progression can contain `O(n)` elements. In the worst case, enumerating all possible triples alone already means

`C(3000, 3) = 4,495,501,000`

triple combinations. Extending every pair can lead to the same cubic scale. Billions of operations cannot fit into the time limit.

The useful observation is that once we know the last two coordinates of an arithmetic progression, the coordinate immediately before them is uniquely determined. Suppose the last two chosen coordinates are `x[i]` and `x[j]`, with `i < j`. Their common difference is

`x[j] - x[i]`.

The previous coordinate must consequently be

`x[i] - (x[j] - x[i]) = 2 * x[i] - x[j]`.

So instead of trying to extend a progression forward and repeatedly searching for its next element, we can compute exactly which coordinate would have to precede the current pair and perform one hash-map lookup.

Define `dp[i][j]` as the length of the longest arithmetic progression whose last two elements are `x[i]` and `x[j]`. If the required previous coordinate `2*x[i] - x[j]` exists at index `h`, then

`dp[i][j] = dp[h][i] + 1`.

If it does not exist, the pair `x[i], x[j]` itself is the whole progression, so `dp[i][j] = 2`.

Because the coordinates are sorted and `j > i`, the required previous coordinate is strictly smaller than `x[i]`. Thus, if it exists, its index is automatically smaller than `i`, which means `dp[h][i]` has already been computed.

The brute-force method works because two points determine the progression, but fails because it keeps rediscovering the same prefixes. The DP stores the best prefix once, then reuses it whenever another pair needs that prefix.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^3) | O(n) | Too slow |
| Optimal | O(n^2) | O(n^2) | Accepted |

## Algorithm Walkthrough

1. Store every coordinate in a dictionary mapping `coordinate -> index`. We need this because, for a pair `(i, j)`, the recurrence gives us a coordinate value and we need to determine whether that coordinate is present and where it occurs.
2. Allocate a DP table where `dp[i][j]` represents the longest arithmetic progression ending with `x[i], x[j]`. Every pair starts as a progression of length two, so the default value is `2`.
3. Process the second endpoint `j` from left to right, and for each `j`, process every `i < j`. This order guarantees that any state `dp[h][i]` required by the recurrence has already been calculated.
4. Compute the coordinate that would have to come immediately before `x[i]` if `x[i], x[j]` are consecutive elements of the progression. Its value is `2*x[i] - x[j]`.
5. Look up that coordinate in the index dictionary. If it does not exist, leave `dp[i][j]` equal to `2`, because no longer progression can end with this pair.
6. If the coordinate exists at index `h`, set `dp[i][j] = dp[h][i] + 1`. The progression represented by `dp[h][i]` can be extended by `x[j]`, because the two consecutive differences are equal.
7. Update the global answer with `dp[i][j]`. The largest value over all pairs is exactly the maximum number of lanterns that can be switched on.

### Why it works

The invariant is that after processing a pair `(i, j)`, `dp[i][j]` is exactly the longest arithmetic progression ending at those two coordinates. Any such progression either contains only those two coordinates, giving length `2`, or has another coordinate immediately before `x[i]`. That previous coordinate is uniquely forced to be `2*x[i] - x[j]`. If it exists at index `h`, every valid progression ending at `(i, j)` corresponds to a valid progression ending at `(h, i)` followed by `x[j]`, so its maximum length is exactly `dp[h][i] + 1`. Since `h < i < j`, that state was already computed. Taking the maximum over every possible final pair consequently finds the globally longest arithmetic progression.

## Python Solution

```python
import sys
from array import array

input = sys.stdin.readline

def solve():
    n = int(input())
    x = list(map(int, input().split()))

    pos = {value: i for i, value in enumerate(x)}

    # uint16 is sufficient because n <= 3000.
    # A flat n*n table uses about 18 MB instead of Python integers
    # consuming hundreds of megabytes.
    dp = array('H', [2]) * (n * n)

    ans = 2

    for j in range(n):
        xj = x[j]
        base_j = j * n

        for i in range(j):
            prev = 2 * x[i] - xj
            h = pos.get(prev)

            if h is not None:
                length = dp[h * n + i] + 1
                dp[i * n + j] = length

                if length > ans:
                    ans = length

    print(ans)

if __name__ == "__main__":
    solve()
```

The dictionary `pos` is built once, so every required predecessor coordinate can be located in expected `O(1)` time. The coordinates are unique because the input is strictly increasing, so one index per coordinate is sufficient.

The DP table uses an unsigned 16-bit integer rather than Python's ordinary integer objects. The longest possible progression contains at most `3000` elements, so every DP value fits into this type. A normal Python list of 9 million references and integer objects would consume substantially more memory, while `array('H')` stores each state in exactly two bytes.

The table is flattened into one dimension. The state `dp[i][j]` is stored at `i*n + j`. This avoids creating thousands of nested Python lists and also keeps the memory representation compact.

For each pair, `prev = 2*x[i] - x[j]` may be as small as `-10^18` or as large as `10^18`, but Python integers have arbitrary precision. There is consequently no overflow issue.

The loop only considers `i < j`, so every pair of distinct lanterns is processed exactly once. The recurrence accesses `dp[h*n+i]`, where `h < i`, so the needed state has already been filled.

The special case of two lanterns does not require separate handling. Every pair starts with DP value `2`, and since `n >= 3`, the final answer is initialized to `2`.

## Worked Examples

### Sample 1

The input is

```
3
1 2 3
```

The pair `(0, 1)` has coordinates `1, 2`. Its required predecessor is `0`, which is absent, so its length is `2`.

For `(0, 2)`, the required predecessor is `2*1 - 3 = -1`, also absent, so its length remains `2`.

For `(1, 2)`, the required predecessor is `2*2 - 3 = 1`, which is at index `0`. The previous state `dp[0][1]` is `2`, so the new state has length `3`.

| j | i | x[i] | x[j] | Required predecessor | h | dp[i][j] | ans |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 0 | 1 | 2 | 0 | absent | 2 | 2 |
| 2 | 0 | 1 | 3 | -1 | absent | 2 | 2 |
| 2 | 1 | 2 | 3 | 1 | 0 | 3 | 3 |

The final state corresponds to coordinates `1, 2, 3`, confirming that the entire array forms an arithmetic progression.

### Sample 2

The input is

```
5
1 2 4 6 7
```

Consider the pairs ending at coordinate `7`. For `(1, 7)`, the required predecessor is `-5`, so no progression longer than two can end there. For `(2, 7)`, the predecessor is `1`, giving the progression `1, 4, 7` with length `3`. For `(4, 7)`, the predecessor is `5`, which is absent.

The relevant states are:

| j | i | Pair | Required predecessor | h | Previous state | dp[i][j] | ans |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 0 | 1, 2 | 0 | absent | none | 2 | 2 |
| 2 | 0 | 1, 4 | -2 | absent | none | 2 | 2 |
| 2 | 1 | 2, 4 | 0 | absent | none | 2 | 2 |
| 3 | 0 | 1, 6 | -4 | absent | none | 2 | 2 |
| 3 | 1 | 2, 6 | -2 | absent | none | 2 | 2 |
| 3 | 2 | 4, 6 | 2 | 1 | dp[1][2] = 2 | 3 | 3 |
| 4 | 0 | 1, 7 | -5 | absent | none | 2 | 3 |
| 4 | 1 | 2, 7 | -3 | absent | none | 2 | 3 |
| 4 | 2 | 4, 7 | 1 | 0 | dp[0][2] = 2 | 3 | 3 |
| 4 | 3 | 6, 7 | 5 | absent | none | 2 | 3 |

The answer is `3`. One optimal choice is `1, 4, 7`, while another is `2, 4, 6`. The DP finds both without enumerating candidate subsets.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n^2) expected | There are `n(n-1)/2` pairs, and each pair performs constant-time arithmetic, dictionary lookup, and DP access. |
| Space | O(n^2) | The DP table contains `n^2` 16-bit states, plus the coordinate dictionary. |

For `n = 3000`, there are only about 4.5 million pair states. The flat 16-bit DP table requires about 18 MB, comfortably below the 512 MB memory limit. Python's dictionary and other interpreter overhead add memory, but the total remains well within the limit. The algorithm avoids the cubic work that would make the 2 second limit impractical.

## Test Cases

```python
import sys
import io
from array import array

def solve():
    n = int(input())
    x = list(map(int, input().split()))

    pos = {value: i for i, value in enumerate(x)}
    dp = array('H', [2]) * (n * n)

    ans = 2

    for j in range(n):
        xj = x[j]

        for i in range(j):
            prev = 2 * x[i] - xj
            h = pos.get(prev)

            if h is not None:
                length = dp[h * n + i] + 1
                dp[i * n + j] = length
                if length > ans:
                    ans = length

    print(ans)

def run(inp: str) -> str:
    global input

    old_stdin = sys.stdin
    old_input = input

    try:
        sys.stdin = io.StringIO(inp)
        input = sys.stdin.readline

        old_stdout = sys.stdout
        sys.stdout = io.StringIO()

        try:
            solve()
            return sys.stdout.getvalue().strip()
        finally:
            sys.stdout = old_stdout
    finally:
        sys.stdin = old_stdin
        input = old_input

# Provided samples
assert run("""3
1 2 3
""") == "3", "sample 1"

assert run("""5
1 2 4 6 7
""") == "3", "sample 2"

assert run("""10
5 10 15 20 35 60 80 85 110 120
""") == "5", "sample 3"

# Minimum-size valid input, where no three coordinates form an AP.
assert run("""3
0 1 3
""") == "2", "minimum size with no arithmetic triple"

# Very large coordinates and an arithmetic progression with huge difference.
assert run("""5
0 250000000000000000 500000000000000000 750000000000000000 1000000000000000000
""") == "5", "large coordinates"

# Boundary coordinates 0 and 10^18, with the middle coordinate forming an AP.
assert run("""3
0 500000000000000000 1000000000000000000
""") == "3", "coordinate boundaries"

# Off-by-one case: the best progression is a suffix, not the whole array.
assert run("""6
1 2 4 6 8 10
""") == "4", "progression starts after the first coordinate"

# Maximum-size valid input, all gaps equal.
maximum_case = "3000\n" + " ".join(map(str, range(3000))) + "\n"
assert run(maximum_case) == "3000", "maximum n"

# An all-equal coordinate test would violate the strict-increasing input
# condition, so it is deliberately not included as a valid assertion.
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `3 / 0 1 3` | `2` | Minimum input size and the fact that every pair is valid even when no triple is an AP |
| `5 / 0 250000000000000000 ... 1000000000000000000` | `5` | Very large coordinates and large integer differences |
| `3 / 0 500000000000000000 1000000000000000000` | `3` | Both coordinate boundaries and exact midpoint arithmetic |
| `6 / 1 2 4 6 8 10` | `4` | A longest progression that does not start at the first lantern |
| `3000 / 0 1 2 ... 2999` | `3000` | Maximum `n` and the worst case where every pair can participate in a long progression |

The all-equal case requested in the checklist cannot be a valid input because the problem explicitly requires `x_1 < x_2 < ... < x_n`. Testing `1 1 1` would test behavior outside the problem's contract rather than the submitted algorithm.

## Edge Cases

For the minimum-size case

```
3
0 1 3
```

the algorithm initializes every pair to length `2`. The pair `(0, 1)` would need predecessor `-1`, while `(0, 2)` would need `-3`, and `(1, 2)` would need `-1`. None exists, so every DP state remains `2` and the answer is `2`. This exercises the fact that an arbitrary pair is always valid, while three coordinates require equal gaps.

For the boundary case

```
3
0 500000000000000000 1000000000000000000
```

the final pair has coordinates `5*10^17` and `10^18`. Its required predecessor is `2*(5*10^17) - 10^18 = 0`, which is present at index `0`. The DP state for the first two coordinates is `2`, so the final state becomes `3`. Python's arbitrary-precision integers represent the calculation exactly.

For the suffix progression

```
6
1 2 4 6 8 10
```

the coordinates `4, 6, 8, 10` form an arithmetic progression of length `4`. When processing `(6, 8)`, the required predecessor is `4`, so the state becomes `3`. When processing `(8, 10)`, the required predecessor is `6`, and the previous state has length `3`, so the final state becomes `4`. The answer is consequently `4`, even though the first two coordinates do not belong to the optimal progression.

For the maximum-size progression, the input

```
3000
0 1 2 3 ... 2999
```

has every coordinate in one arithmetic progression. For every pair `(i, j)`, the predecessor `2*x[i] - x[j]` is present whenever the corresponding index lies before `i`. The DP eventually reaches length `3000`, which confirms both the recurrence and the storage bound. A 16-bit unsigned integer is sufficient because `3000 < 65536`.

An all-equal input such as

```
3
5 5 5
```

must not be used to validate a solution. The coordinates are required to be strictly increasing, so this input is invalid. A correct implementation is allowed to rely on uniqueness when constructing the coordinate-to-index dictionary.
