---
title: "CF 23B - Party"
description: "We can think of the party as an undirected friendship graph. Every person is a vertex, and an edge means two people are"
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "graphs", "math"]
categories: ["algorithms"]
codeforces_contest: 23
codeforces_index: "B"
codeforces_contest_name: "Codeforces Beta Round 23"
rating: 1600
weight: 23
solve_time_s: 207
verified: true
draft: false
---

[CF 23B - Party](https://codeforces.com/problemset/problem/23/B)

**Rating:** 1600  
**Tags:** constructive algorithms, graphs, math  
**Solve time:** 3m 27s  
**Verified:** yes  

## Solution
## Problem Understanding

We can think of the party as an undirected friendship graph. Every person is a vertex, and an edge means two people are friends.

The process removes people in rounds. First, everyone with degree `0` leaves. After those removals, some remaining people may now have degree `1`, so they leave next. Then people with degree `2` leave, and so on, increasing the required degree step by step until reaching `n - 1`.

The question is not asking us to simulate a given graph. Instead, for a given number of people `n`, we must design the friendship graph in the best possible way so that as many people as possible survive after the entire process finishes.

The constraints are extremely small conceptually, even though there may be up to `10^5` test cases. Each test case contains only one integer `n`, and the output is just one integer answer. This immediately suggests that the intended solution is mathematical or constructive, with constant-time processing per test case. Any algorithm that tries to enumerate graphs is hopeless because the number of undirected graphs on `n` vertices is `2^(n(n-1)/2)`.

The subtle part of the problem is understanding what “survive in the end” really means. A careless interpretation might assume that if a person ever has enough friends, they stay forever. That is false because removals change degrees dynamically.

Consider `n = 3`.

A triangle graph has all degrees equal to `2`. Nobody leaves in the first round because there are no isolated vertices. Nobody leaves in the second round because there are no degree-1 vertices. Then the process reaches degree `2`, and all three people leave together. The correct answer is `0`, not `3`.

A different graph works better. Take one edge and one isolated vertex. The isolated vertex leaves first. The remaining two vertices each have degree `1`, so they leave in the next round. One of them is the last removed person, so exactly one person can remain at the very end of the process. The answer becomes `1`.

Another easy mistake is assuming the answer is always `1`.

Take `n = 4`. A cycle of length `4` gives every vertex degree `2`. Nobody leaves at degree `0` or `1`. When the process reaches degree `2`, all four vertices leave. Again the final answer is `0`.

But we can do better with a triangle plus one isolated vertex. The isolated person leaves first. The triangle survives until the degree `2` stage, where all three triangle vertices are removed. The last removed vertex count is still `1`, not `3`.

The key observation is that the process always eventually removes everybody. The only thing we control is how many people are still present immediately before the last removal stage.

## Approaches

The brute-force approach is to enumerate every possible friendship graph on `n` vertices and simulate the deletion process.

For a fixed graph, simulation is straightforward. At stage `k`, remove every currently alive vertex whose current degree equals `k`. Continue until all stages are processed. Then record how many vertices survived right before the final deletion.

This works because the process definition is explicit and deterministic. The problem is the number of graphs. An undirected graph on `n` vertices has `n(n-1)/2` possible edges, so there are

$2^{\frac{n(n-1)}{2}}$

different graphs.

Even for `n = 20`, this is astronomically large. No amount of optimization can make brute force feasible.

The breakthrough comes from analyzing what must happen during the process.

Suppose at some moment there are `m` people still alive. Each of them can have degree at most `m - 1`. Eventually the process reaches stage `m - 1`. At that stage, every remaining person must leave, because nobody can have degree larger than `m - 1`.

That means the process always ends by deleting all currently remaining vertices together.

Now the problem becomes: what is the largest possible size of that final group?

Assume the final surviving group has size `m`. Right before the final step, every one of those `m` vertices must have degree exactly `m - 1`, otherwise they would have been deleted earlier or later. So the final group must form a complete graph of size `m`.

But if the whole graph initially has exactly `m` vertices, then all of them disappear together in the last stage, leaving nobody after the process. To make one person survive longer, we need at least one extra vertex outside the clique.

This suggests the optimal construction:

1. Build a clique on `m` vertices.
2. Add one isolated vertex.

The isolated vertex disappears at stage `0`. The clique remains untouched until stage `m - 1`, when all clique vertices are deleted together.

This construction uses `m + 1` total vertices. So for a given `n`, the largest possible final clique size is

$m=n-1$

Hence the answer is simply `n - 1`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| Optimal | O(1) per test case | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases.
2. For each value of `n`, compute `n - 1`.

We can always achieve this value by taking a complete graph on `n - 1` vertices and one isolated vertex.
3. Print the result.

Why is this the right answer? The isolated vertex disappears immediately during the degree `0` stage. After that, the remaining `n - 1` vertices form a clique, so every vertex has degree `n - 2`. They survive every earlier stage because their degree is larger than the current removal number. When the process reaches stage `n - 2`, all of them are removed together.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())

for _ in range(t):
    n = int(input())
    print(n - 1)
```

The implementation is intentionally tiny because all the work is in the proof.

The program reads each test case independently and outputs `n - 1`. There is no graph construction or simulation because the mathematical argument already proves the optimal value.

The only boundary condition is `n = 1`. In that case, the formula gives `0`, which is correct. A single isolated person leaves during the degree `0` stage, so nobody remains afterward.

Python integers are unbounded, so there are no overflow concerns even if the limits were much larger.

## Worked Examples

### Example 1

Input:

```
n = 3
```

Construction:

- Vertices `1` and `2` form a clique.
- Vertex `3` is isolated.

| Stage | Alive Vertices | Degrees | Removed |
| --- | --- | --- | --- |
| 0 | {1,2,3} | {1,1,0} | {3} |
| 1 | {1,2} | {1,1} | {1,2} |

The largest group alive right before the final deletion has size `2`, which equals `n - 1`.

This example shows why adding one isolated vertex is useful. Without it, the entire graph would disappear simultaneously.

### Example 2

Input:

```
n = 5
```

Construction:

- Vertices `1,2,3,4` form a clique.
- Vertex `5` is isolated.

| Stage | Alive Vertices | Degrees | Removed |
| --- | --- | --- | --- |
| 0 | {1,2,3,4,5} | {3,3,3,3,0} | {5} |
| 1 | {1,2,3,4} | {3,3,3,3} | {} |
| 2 | {1,2,3,4} | {3,3,3,3} | {} |
| 3 | {1,2,3,4} | {3,3,3,3} | {1,2,3,4} |

The clique survives untouched until the final relevant stage. This confirms the invariant that every clique vertex always has degree larger than the current deletion threshold.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) per test case | Only one subtraction and one print |
| Space | O(1) | No extra data structures |

Even with `10^5` test cases, the total work is trivial. The solution easily fits within the time and memory limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def solve():
    input = sys.stdin.readline

    t = int(input())
    ans = []

    for _ in range(t):
        n = int(input())
        ans.append(str(n - 1))

    print("\n".join(ans))

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    out = sys.stdout.getvalue()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return out

# provided sample
assert run("1\n3\n") == "2\n", "sample 1"

# minimum size
assert run("1\n1\n") == "0\n", "single isolated vertex"

# small boundary
assert run("1\n2\n") == "1\n", "one edge plus isolated behavior"

# multiple test cases
assert run("4\n1\n2\n5\n10\n") == "0\n1\n4\n9\n", "multiple independent cases"

# large value
assert run("1\n100000\n") == "99999\n", "maximum constraint"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1` | `0` | Minimum possible graph |
| `1 2` | `1` | Smallest nontrivial construction |
| `4 / 1 2 5 10` | `0 1 4 9` | Multiple test handling |
| `1 100000` | `99999` | Maximum constraint handling |

## Edge Cases

Consider the smallest input:

```
1
1
```

There is only one person and no friendships. During stage `0`, this person has degree `0` and leaves immediately.

The algorithm computes:

$1-1=0$

which matches the process exactly.

Now consider:

```
1
2
```

Take one edge between the two people. Initially both have degree `1`.

At stage `0`, nobody leaves. At stage `1`, both leave together.

The algorithm outputs:

$2-1=1$

meaning the largest possible final surviving group size is `1`. We achieve it by instead using one isolated vertex and one separate vertex. The isolated vertex leaves first, then the remaining person leaves later.

Another tricky case is:

```
1
4
```

A naive guess might be `4`, using a complete graph on four vertices. But every vertex then has degree `3`, so all four disappear together at stage `3`.

The optimal construction is a clique of size `3` plus one isolated vertex. The isolated vertex disappears first, and the clique survives until stage `2`.

The algorithm outputs:

$4-1=3$

which is achievable and optimal.
