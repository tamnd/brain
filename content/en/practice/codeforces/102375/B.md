---
title: "CF 102375B - \u0411\u043e\u043b\u044c\u0448\u0438\u0435 \u043f\u0435\u0440\u0435\u043c\u0435\u043d\u044b"
description: "We have (N) labeled cities and must build a connected undirected graph using exactly (N-1) distinct airline connections. Since a connected graph on (N) vertices with exactly (N-1) edges is a tree, the problem is really about labeled trees."
date: "2026-08-14T13:00:24+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102375
codeforces_index: "B"
codeforces_contest_name: "\u041a\u0432\u0430\u043b\u0438\u0444\u0438\u043a\u0430\u0446\u0438\u043e\u043d\u043d\u044b\u0439 \u0440\u0430\u0443\u043d\u0434 \u0427\u0435\u043c\u043f\u0438\u043e\u043d\u0430\u0442\u0430 \u0421\u0435\u0432\u0435\u0440\u043e-\u0417\u0430\u043f\u0430\u0434\u0430 \u0420\u043e\u0441\u0441\u0438\u0438 \u0438 \u041c\u043e\u0441\u043a\u0432\u044b ICPC 2019"
rating: 0
weight: 102375
solve_time_s: 588
verified: false
draft: false
---

[CF 102375B - \u0411\u043e\u043b\u044c\u0448\u0438\u0435 \u043f\u0435\u0440\u0435\u043c\u0435\u043d\u044b](https://codeforces.com/problemset/problem/102375/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 9m 48s  
**Verified:** no  

## Solution
## Problem Understanding

We have (N) labeled cities and must build a connected undirected graph using exactly (N-1) distinct airline connections. Since a connected graph on (N) vertices with exactly (N-1) edges is a tree, the problem is really about labeled trees.

The accessibility of a city is simply its degree, so we want to consider trees whose maximum vertex degree is as large as possible. The task is to count how many different labeled trees attain that maximum possible degree.

The input contains one integer (N), with (2 \le N \le 10^9). The upper bound is the main clue: constructing a graph, enumerating vertices, or even running a loop proportional to (N) is unnecessary and would be inappropriate. The answer has to come from a structural observation and be computed in constant time.

The smallest case deserves special attention. For (N=2), there is exactly one possible tree, consisting of the single edge between the two cities. Its two vertices both have degree (1), so the maximum degree is (1), and the answer is (1). A formula that simply returns (N) would incorrectly give (2).

For (N=3), the maximum possible degree is (2). Every tree on three labeled vertices is a path, and each such tree has one vertex of degree (2). There are three choices for that central vertex, so the answer is (3), matching the sample.

## Approaches

A direct brute-force solution could enumerate every possible set of (N-1) edges from the (\binom N2) possible pairs of cities, check whether the resulting graph is connected, calculate all degrees, and keep the trees with the largest maximum degree. The number of candidate edge sets is exactly

[
\binom{\binom N2}{N-1},
]

so this becomes hopeless even for fairly small (N). An alternative brute-force based on Cayley's formula could enumerate all (N^{N-2}) labeled trees, but that is still exponentially large. With (N) allowed to reach (10^9), either interpretation is completely unusable.

The key observation is that a vertex can be connected directly to at most all other (N-1) cities. Hence no tree can have maximum degree greater than (N-1). This upper bound is achievable: choose one city and connect it to every other city. The resulting graph is a star, which is connected and contains exactly (N-1) edges.

For (N\ge3), every tree attaining maximum degree (N-1) must be exactly such a star. If some vertex has degree (N-1), it is adjacent to every other vertex, already using all (N-1) available edges. No additional edge can exist because the tree has exactly (N-1) edges. Thus the only choice is which city is the center, giving (N) different trees.

The case (N=2) is the only exception. Both vertices are incident to the unique edge, so choosing either vertex as a supposed center does not produce a different tree. There is only one distinct construction.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O\left(\binom{\binom N2}{N-1}\cdot N\right)) | (O(N^2)) | Too slow |
| Optimal | (O(1)) | (O(1)) | Accepted |

## Algorithm Walkthrough

1. Read (N). Since the answer depends only on whether (N=2) or (N\ge3), there is no need to construct any graph.
2. If (N=2), output (1). There is only one possible edge and consequently only one possible tree.
3. If (N\ge3), output (N). The largest possible degree is (N-1), and a tree reaches it exactly when one chosen city is connected to every other city. Each of the (N) cities can independently be that unique center.

The crucial invariant is that a tree with a vertex of degree (N-1) has already used all (N-1) edges required by a tree. Consequently, such a tree must be a star, and every optimal tree is uniquely determined by its center when (N\ge3). The special case (N=2) has no unique center, which is why it must be handled separately.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())

if n == 2:
    print(1)
else:
    print(n)
```

The first line reads the number of cities. The condition `n == 2` handles the only case where the number of possible centers does not equal the number of distinct optimal trees.

For every (n\ge3), the program prints `n`, because there is exactly one optimal star for each choice of its center. There are no loops over the cities and no graph data structure, so the implementation remains constant time even when (N=10^9).

Python integers easily represent the answer because the answer is at most (10^9), so there are no overflow concerns. The comparison must use `n == 2`, not `n <= 2`, although the input guarantees (N\ge2).

## Worked Examples

### Sample 1: (N=3)

There are three possible choices for the center. Choosing city (1), (2), or (3) produces three different labeled stars.

| Step | (N) | Condition | Answer |
| --- | --- | --- | --- |
| Read input | 3 | (N=2) is false |  |
| Choose formula | 3 | (N\ge3) | 3 |
| Output | 3 |  | 3 |

The result is (3), exactly as in the sample. This also demonstrates why the center uniquely identifies the optimal tree once there are at least three cities.

### Custom example: (N=2)

There is only one possible connection, between cities (1) and (2).

| Step | (N) | Condition | Answer |
| --- | --- | --- | --- |
| Read input | 2 | (N=2) is true |  |
| Handle special case | 2 | Unique tree | 1 |
| Output | 2 |  | 1 |

This trace exercises the only boundary case where returning (N) would be incorrect. Although either endpoint could be called a center, both choices describe the same single edge, so there is only one distinct construction.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(1)) | Only one comparison and one output operation are needed. |
| Space | (O(1)) | The algorithm stores only the input integer. |

The constant-time solution is particularly appropriate for (N\le10^9). The algorithm never depends on the number of cities through iteration or graph construction, so the upper bound has no practical impact on execution time or memory usage.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline
    n = int(input())

    if n == 2:
        print(1)
    else:
        print(n)

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()
    result = sys.stdout.getvalue().strip()

    sys.stdin = old_stdin
    sys.stdout = old_stdout

    return result

# provided sample
assert run("3\n") == "3", "sample 1"

# minimum input
assert run("2\n") == "1", "minimum N"

# smallest non-special case
assert run("3\n") == "3", "first case with a unique center"

# boundary near a large value
assert run("999999999\n") == "999999999", "large boundary"

# maximum input
assert run("1000000000\n") == "1000000000", "maximum N"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `3` | `3` | Provided sample and ordinary star counting |
| `2` | `1` | Minimum input and special case |
| `3` | `3` | Boundary between the special case and general formula |
| `999999999` | `999999999` | Large value without overflow or iteration |
| `1000000000` | `1000000000` | Maximum allowed input |

There is no meaningful "all-equal values" case because the input contains a single integer rather than an array or collection of values. The relevant analogue is testing repeated invocations with different values, which the test set above does through several independent single-value inputs.

## Edge Cases

For (N=2), the exact input is `2`. The only possible tree contains the edge ((1,2)), so the maximum degree is (1). The algorithm enters the special branch and outputs `1`. A careless implementation of `print(n)` would output `2`, effectively counting the same tree twice by treating its two endpoints as different centers.

For (N=3), the input is `3`. The largest possible degree is (2=N-1). Any optimal tree must contain a vertex adjacent to both other vertices, and there are exactly three choices for that vertex. The algorithm takes the general branch and outputs `3`. This confirms that the transition from the special case to the formula (N) happens exactly at (N=3).

For the maximum input, `1000000000`, constructing even a list of all cities would already require unnecessary memory, and enumerating edges would be impossible. The algorithm performs only one comparison and prints `1000000000`. The result follows directly from the fact that each of the (10^9) cities can serve as the center of one distinct optimal star.

The structural argument also rules out hidden graph cases. If an optimal tree for (N\ge3) has maximum degree (N-1), its center is adjacent to every other city. Those (N-1) incident edges already account for the entire edge set of the tree, so there cannot be another edge between two non-center cities. Thus no optimal construction is missed and no non-star construction is counted.
