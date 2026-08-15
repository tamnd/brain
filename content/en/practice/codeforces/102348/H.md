---
title: "CF 102348H - Berland Prospect"
description: "We have n lanterns placed at strictly increasing integer coordinates x[0], x[1], ..., x[n-1]. We may switch on any subset of them. The chosen coordinates must form an arithmetic progression, meaning every consecutive chosen coordinate has the same difference."
date: "2026-08-15T17:27:44+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102348
codeforces_index: "H"
codeforces_contest_name: "ICPC 2019-2020 NERC (NEERC), Southern and Volga Russia Qualifier"
rating: 0
weight: 102348
solve_time_s: 242
verified: false
draft: false
---

[CF 102348H - Berland Prospect](https://codeforces.com/problemset/problem/102348/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 4m 2s  
**Verified:** no  

## Solution
## Problem Understanding

We have `n` lanterns placed at strictly increasing integer coordinates `x[0], x[1], ..., x[n-1]`. We may switch on any subset of them. The chosen coordinates must form an arithmetic progression, meaning every consecutive chosen coordinate has the same difference. Any set of one or two lanterns is automatically valid, so the real task is to find the longest arithmetic-progression subsequence of the sorted coordinate array.

The original constraints give `n <= 3000` and coordinates up to `10^18`. The large coordinate bound rules out techniques that depend on a small coordinate range, but it does not hurt arithmetic itself because Python integers handle these values exactly. The size `3000` is the key constraint. An `O(n^2)` algorithm performs about 4.5 million pair transitions, which is appropriate for the 2 second limit when implemented carefully. An `O(n^3)` algorithm would already have roughly 27 billion iterations in its loose worst-case bound, far beyond the limit. The official statement confirms these limits and the strictly increasing order of the coordinates.

There are several cases where an implementation can silently go wrong. First, three arbitrary lanterns do not necessarily form a valid progression. For example, `3 5 9` has only two equal-free gaps, `2` and `4`, so the answer is `2`, not `3`. A careless implementation that treats every pair extension as automatically valid would overcount.

Second, the best progression can skip many lanterns. For `1 2 4 6 7`, the answer is `3`, using `1, 4, 7`. Looking only at consecutive lanterns would miss this progression because the original gaps are `1, 2, 2, 1`.

Third, the input coordinates can be close to `10^18`. For example, `0 500000000000000000 1000000000000000000` has answer `3`. A fixed-width implementation must use a type wide enough for expressions such as `2*x[i]`, although Python's arbitrary-precision integers make this issue straightforward.

Finally, the phrase "all-equal values" cannot literally produce a valid test under this problem's input constraints because coordinates are strictly increasing. The meaningful version of that stress case is an array with all equal gaps, such as `0 1 2 3 4`, where every coordinate belongs to one arithmetic progression.

## Approaches

A direct brute-force approach can choose a first and second lantern, determine their difference, and then search for every subsequent coordinate that continues the same progression. If we scan all possible next positions naively, there are `O(n^2)` choices of the first two lanterns and up to `O(n)` work for each one, giving `O(n^3)` time. Equivalently, checking every triple already means examining `C(3000, 3) = 4,495,501,000` triples in the worst case. The brute force is correct because every arithmetic progression has a first pair, so trying every pair eventually considers its exact common difference. It simply repeats too much work.

The useful observation is that once the last two selected coordinates are known, the next coordinate is completely determined. Suppose an arithmetic progression currently ends at coordinates `x[h], x[i]`. Its next coordinate must be

`x[j] = x[i] + (x[i] - x[h]) = 2*x[i] - x[h]`.

That turns the problem into a dynamic program on pairs of endpoints. Let `dp[i][j]` be the maximum length of an arithmetic progression whose last two coordinates are `x[i]` and `x[j]`, with `i < j`. If the required predecessor coordinate `2*x[i] - x[j]` exists at index `h`, then the progression can be extended from the state ending at `(h, i)`:

`dp[i][j] = dp[h][i] + 1`.

If that predecessor does not exist, the pair `(i, j)` itself is a valid progression of length `2`, so `dp[i][j] = 2`.

The sorted order gives an additional useful property. Because `j > i`, the required predecessor `2*x[i] - x[j]` is strictly smaller than `x[i]`, so its index `h` must satisfy `h < i`. All information needed by the transition has already been computed when processing `i`.

We can find `h` without a hash table. For a fixed `i`, as `j` increases, `x[j]` increases, so `2*x[i] - x[j]` decreases. A pointer scanning backward through the coordinates therefore moves only backward during the whole inner loop. Across a fixed `i`, the pointer moves at most `i` times, so the total pointer movement over all `i` is `O(n^2)`.

The DP contains `n(n-1)/2` pair states. In Python, storing each state as a normal integer inside nested lists can consume a substantial amount of memory. The maximum DP value is at most `3000`, so an unsigned 16-bit integer is sufficient. Python's `array('H')` stores each state in two bytes, keeping the roughly 4.5 million states within a small memory footprint.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `O(n^3)` | `O(1)` or `O(n)` | Too slow |
| Pair DP with monotone predecessor pointer | `O(n^2)` | `O(n^2)` states, about 2 bytes each | Accepted |

## Algorithm Walkthrough

1. Read the sorted coordinates and initialize the answer to `2`. Every pair of distinct lanterns is a valid choice, so the answer is always at least `2`.
2. For every index `i`, create a DP row containing the states `dp[i][j]` for all `j > i`. Initialize every state to `2`, because any pair of lanterns forms an arithmetic progression of length two.
3. Fix the middle endpoint `i` and start a predecessor pointer `k = i - 1`. For every `j > i`, the coordinate required immediately before `x[i]` is `target = 2*x[i] - x[j]`.
4. Move `k` left while `x[k] > target`. Since `target` only decreases as `j` increases, `k` never needs to move right again. If `x[k] == target`, index `k` is exactly the required predecessor.
5. When the predecessor exists, read the already computed state ending at `(k, i)` and set `dp[i][j] = dp[k][i] + 1`. The previous state has one fewer element, and appending `x[j]` preserves the common difference because `x[i] - x[k] = x[j] - x[i]`.
6. Update the global answer with the new state. If the predecessor does not exist, the initialized value `2` remains correct.
7. Process every possible `i`. At the end, the largest DP value is the longest arithmetic-progression subsequence and is the required answer.

### Why it works

Consider any arithmetic progression ending at `x[i], x[j]`. Its previous coordinate, if it has one, must be exactly `2*x[i] - x[j]`. Because the coordinates are sorted and `j > i`, that predecessor lies before `i`. Thus every progression of length at least three has a unique earlier DP state from which it can be extended. The recurrence considers exactly that predecessor when it exists, and otherwise correctly leaves the pair at length two. By induction on the position of the final endpoint, every DP state stores the maximum valid progression ending at that pair. Taking the maximum over all pairs consequently gives the global optimum.

## Python Solution

```python
import sys
from array import array

input = sys.stdin.readline

def solve():
    n = int(input())
    x = list(map(int, input().split()))

    if n <= 2:
        print(n)
        return

    # rows[i][j - i - 1] stores dp[i][j] for j > i.
    # Every state starts at 2 because every pair is valid.
    rows = [None] * n
    answer = 2

    for i in range(n - 1):
        length = n - i - 1
        row = array('H', [2]) * length

        # For fixed i, target = 2*x[i] - x[j] decreases as j grows.
        # Hence k only moves to the left.
        k = i - 1
        xi = x[i]

        for j in range(i + 1, n):
            target = 2 * xi - x[j]

            while k >= 0 and x[k] > target:
                k -= 1

            if k >= 0 and x[k] == target:
                value = rows[k][i - k - 1] + 1
                row[j - i - 1] = value

                if value > answer:
                    answer = value

        rows[i] = row

    print(answer)

if __name__ == "__main__":
    solve()
```

The `rows` structure stores only states with `i < j`. For a fixed `i`, the state `dp[i][j]` is stored at offset `j - i - 1`, so the row contains exactly `n-i-1` entries.

The expression `rows[k][i-k-1]` retrieves `dp[k][i]`. The offset is easy to get wrong because each row begins at its own first valid second endpoint. For example, in row `k`, the state whose second index is `i` is the `(i-k-1)`-th element.

The predecessor pointer starts at `i-1`, the largest possible predecessor index. For each new `j`, the required coordinate decreases. The `while` loop moves the pointer until either the exact coordinate is found or every possible predecessor has become too large. It never needs to restart from `i-1`, which is what keeps the search quadratic rather than cubic.

The `array('H')` type is sufficient because no progression can contain more than `n <= 3000` lanterns. A 16-bit unsigned integer can represent values through `65535`, so every DP state fits comfortably. This saves a large amount of memory compared with Python's full integer objects.

Python integers also safely evaluate `2 * x[i]` even when `x[i]` is near `10^18`, so there is no overflow issue.

The input has exactly one test case, so there is no outer test-case loop.

## Worked Examples

### Sample 1

The input is `1 2 3`. Initially every pair has DP value `2`. When the pair `(1, 2)` is considered in zero-based indices `(0, 1)`, there is no predecessor. For the pair `(2, 3)`, the required predecessor is `1`, which exists, so the length becomes `dp[0][1] + 1 = 3`.

| `i` | `j` | `target = 2*x[i]-x[j]` | `k` after search | State | Answer |
| --- | --- | --- | --- | --- | --- |
| 0 | 1 | 0 | -1 | `2` | `2` |
| 0 | 2 | -1 | -1 | `2` | `2` |
| 1 | 2 | 1 | 0 | `dp[0][1]+1 = 3` | `3` |

The final answer is `3`. The important part of the trace is the transition from the pair `(1, 2)` to `(1, 2, 3)`: the predecessor coordinate is reconstructed algebraically instead of scanning all earlier lanterns.

### Sample 2

The coordinates are `1 2 4 6 7`. The optimal progression is `1, 4, 7`, whose common difference is `3`.

| `i` | `j` | `target` | `k` | State | Answer |
| --- | --- | --- | --- | --- | --- |
| 0 | 1 | 0 | -1 | `2` | `2` |
| 0 | 2 | -2 | -1 | `2` | `2` |
| 0 | 3 | -4 | -1 | `2` | `2` |
| 0 | 4 | -5 | -1 | `2` | `2` |
| 1 | 2 | 0 | -1 | `2` | `2` |
| 1 | 3 | -2 | -1 | `2` | `2` |
| 1 | 4 | -3 | -1 | `2` | `2` |
| 2 | 3 | 2 | 1 | `dp[1][2]+1 = 3` | `3` |
| 2 | 4 | 1 | 0 | `dp[0][2]+1 = 3` | `3` |
| 3 | 4 | 5 | 2 | no exact predecessor | `3` |

The state for `(i,j) = (2,4)` corresponds to coordinates `4` and `7`. Its required predecessor is `1`, which is present at index `0`. Since `dp[0][2]` represents the pair `1,4`, the new state correctly represents `1,4,7`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(n^2)` | There are `O(n^2)` pairs, and each predecessor pointer only moves left across its row |
| Space | `O(n^2)` | There are `n(n-1)/2` pair states, stored as 16-bit integers |

For `n = 3000`, there are only about 4.5 million DP states. At two bytes per state, the DP storage itself is about 9 MB, well below the 512 MB memory limit. The number of pair transitions is also about 4.5 million, so the quadratic approach is appropriate for the given 2 second limit.

## Test Cases

```python
import sys
import io
from array import array

def solve():
    input = sys.stdin.readline

    n = int(input())
    x = list(map(int, input().split()))

    if n <= 2:
        print(n)
        return

    rows = [None] * n
    answer = 2

    for i in range(n - 1):
        length = n - i - 1
        row = array('H', [2]) * length

        k = i - 1
        xi = x[i]

        for j in range(i + 1, n):
            target = 2 * xi - x[j]

            while k >= 0 and x[k] > target:
                k -= 1

            if k >= 0 and x[k] == target:
                value = rows[k][i - k - 1] + 1
                row[j - i - 1] = value
                if value > answer:
                    answer = value

        rows[i] = row

    print(answer)

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

# Provided samples
assert run("3\n1 2 3\n") == "3\n", "sample 1"
assert run("5\n1 2 4 6 7\n") == "3\n", "sample 2"
assert run("10\n5 10 15 20 35 60 80 85 110 120\n") == "5\n", "sample 3"

# Minimum-size input with no arithmetic progression of length 3.
assert run("3\n0 1 3\n") == "2\n", "minimum-size non-AP case"

# Boundary coordinates near both ends of the allowed range.
assert run("3\n0 500000000000000000 1000000000000000000\n") == "3\n", "large-coordinate arithmetic progression"

# Long progression with irrelevant gaps around it.
assert run("5\n0 3 6 9 20\n") == "4\n", "extension through several DP states"

# Maximum-size stress case, all gaps equal.
n = 3000
coords = " ".join(map(str, range(n)))
assert run(f"{n}\n{coords}\n") == "3000\n", "maximum-size all-equal-gap case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `3 / 0 1 3` | `2` | Minimum-size input and the rule that two arbitrary lanterns are always valid |
| `3 / 0 500000000000000000 1000000000000000000` | `3` | Large coordinates and exact integer arithmetic |
| `5 / 0 3 6 9 20` | `4` | Repeated DP extensions and skipping an unrelated final lantern |
| `3000 / 0 1 2 ... 2999` | `3000` | Maximum `n`, equal gaps, and the maximum possible answer |

## Edge Cases

For `0 1 3`, the only possible three-lantern choice has gaps `1` and `2`, so the answer is `2`. The algorithm starts every pair at value `2`. When it examines the pair `(1,3)`, the required predecessor is `-1`, which is outside the coordinate array, so the state remains `2`. No state reaches `3`, and the final answer stays `2`.

For `0 500000000000000000 1000000000000000000`, the middle coordinate is exactly the average of the endpoints. When `i` points to the middle coordinate and `j` points to the final coordinate, the target is `2 * 500000000000000000 - 1000000000000000000 = 0`. The predecessor pointer finds coordinate `0`, so the state becomes `3`. This confirms that the calculation remains exact even near the upper coordinate boundary.

For `0 3 6 9 20`, the progression `0,3,6,9` is built incrementally. The state for `(0,3)` has length `2`. When considering `(3,6)`, the required predecessor is `0`, so its value becomes `3`. Finally, `(6,9)` requires predecessor `3`, whose corresponding state has length `3`, giving length `4`. The final coordinate `20` cannot extend that progression, so the answer is `4`.

For the maximum-size case `0 1 2 ... 2999`, every pair belongs to a progression that can be extended repeatedly. For example, the states ending at `(0,1)`, `(1,2)`, `(2,3)`, and so on all extend to longer states. The final state reaches length `3000`. This also exercises the 16-bit DP representation, since `3000` is safely below `65535`.

A literal input containing equal coordinates, such as `1 1 1`, is not a valid test for this problem because the input guarantees strict increase. The implementation relies on that property when it concludes that the required predecessor of `(i,j)` must have an index smaller than `i`. Equal coordinates would introduce zero differences and violate the stated input model.
