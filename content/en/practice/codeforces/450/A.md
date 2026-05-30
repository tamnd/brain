---
title: "CF 450A - Jzzhu and Children"
description: "We have a line of children. Child i wants a[i] candies in total. Every time a child reaches the front of the line, they receive exactly m candies. If the child has still not received enough candies after that distribution, they move to the back of the line."
date: "2026-05-30T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 450
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 257 (Div. 2)"
rating: 1000
weight: 450
solve_time_s: 94
verified: true
draft: false
---

[CF 450A - Jzzhu and Children](https://codeforces.com/problemset/problem/450/A)

**Rating:** 1000  
**Tags:** implementation  
**Solve time:** 1m 34s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a line of children. Child `i` wants `a[i]` candies in total. Every time a child reaches the front of the line, they receive exactly `m` candies.

If the child has still not received enough candies after that distribution, they move to the back of the line. Otherwise, they leave permanently. The process continues until no children remain.

The task is to determine which child leaves last.

The constraints are very small. There are at most 100 children, and each child wants at most 100 candies. Even a direct simulation easily fits within the time limit because the total number of candy distributions is small. Still, there is a cleaner observation that avoids simulating the queue at all.

The key quantity for each child is how many turns they need before leaving. If a child wants 7 candies and `m = 3`, they need three visits to the front because the sequence of received candies is 3, 6, 9. In general, child `i` needs

$$\left\lceil \frac{a_i}{m} \right\rceil$$

turns.

A subtle case occurs when several children require the same number of turns. For example:

```
3 2
4 4 4
```

Each child needs two turns. Their final departures occur in the original order, so child 3 leaves last. A solution that only finds the maximum number of required turns and returns the first occurrence would incorrectly output 1.

Another easy mistake is mishandling exact multiples of `m`.

```
2 3
3 4
```

Child 1 needs only one turn, not two. The correct turn counts are 1 and 2, so the answer is 2. Using ordinary integer division `a[i] // m` would produce incorrect results.

A final corner case is the minimum input:

```
1 100
1
```

There is only one child, so the answer is 1 regardless of the candy count.

## Approaches

A straightforward solution is to simulate the queue exactly as described. Store pairs `(child_index, remaining_candies)`. Repeatedly remove the front child, subtract `m` candies, and either send them home or place them at the back of the queue.

This simulation is correct because it follows the process literally. Under the given constraints, it is also fast enough. Each child can require at most

$$\left\lceil \frac{100}{1} \right\rceil = 100$$

turns, so the total number of queue operations is at most about 10,000.

There is, however, a simpler way to think about the process.

A child leaves after receiving enough batches of size `m`. The only thing that matters is the number of visits they need:

$$t_i = \left\lceil \frac{a_i}{m} \right\rceil$$

Children requiring more visits stay in the queue longer. The last child to leave is the child with the largest value of `t_i`.

When multiple children have the same maximum value, the later child in the original line leaves later. They complete their final visit after all earlier children with the same requirement.

This means we only need to find the last position whose required turn count is maximal.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Queue Simulation | O(n · max(aᵢ)) | O(n) | Accepted |
| Optimal Turn Counting | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read `n`, `m`, and the array of candy requirements.
2. For each child, compute the number of turns needed:

$$t_i = \left\lceil \frac{a_i}{m} \right\rceil$$

In integer arithmetic this can be written as:

$$t_i = \frac{a_i + m - 1}{m}$$

using floor division.
3. Keep track of the largest turn count seen so far and the corresponding child index.
4. When a child's turn count is greater than or equal to the current maximum, update the answer to this child.

Using `>=` is essential. If two children need the same number of turns, the later one leaves later and should overwrite the previous answer.
5. After processing all children, output the stored index.

### Why it works

For each child, `t_i` represents exactly how many times that child must reach the front before leaving.

Any child with a smaller `t_i` leaves strictly earlier than a child with a larger `t_i`, because they finish after fewer rounds of service.

If two children have the same `t_i`, their relative order never changes. During their final visit, the child who started later in the original queue reaches that visit later as well. Hence among all children with the maximum turn count, the last one in the original order is the last child to go home.

The algorithm explicitly finds the last occurrence of the maximum turn count, which is exactly the required child.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    a = list(map(int, input().split()))

    best_turns = -1
    answer = -1

    for i, candies in enumerate(a, start=1):
        turns = (candies + m - 1) // m

        if turns >= best_turns:
            best_turns = turns
            answer = i

    print(answer)

solve()
```

The solution processes each child exactly once.

The expression `(candies + m - 1) // m` computes the ceiling of `candies / m` using integer arithmetic. This avoids floating point operations and correctly handles values that are not exact multiples of `m`.

The comparison uses `>=` rather than `>`. This is the most important implementation detail. When two children require the same number of turns, the later child must become the current answer because that child leaves later.

Indices are generated with `enumerate(..., start=1)` because the problem numbers children starting from 1 rather than 0.

## Worked Examples

### Example 1

Input:

```
5 2
1 3 1 4 2
```

| Child | Candies Wanted | Turns Needed | Current Maximum | Answer |
| --- | --- | --- | --- | --- |
| 1 | 1 | 1 | 1 | 1 |
| 2 | 3 | 2 | 2 | 2 |
| 3 | 1 | 1 | 2 | 2 |
| 4 | 4 | 2 | 2 | 4 |
| 5 | 2 | 1 | 2 | 4 |

Output:

```
4
```

Children 2 and 4 both need two turns, which is the maximum. Child 4 appears later, so child 4 leaves last.

### Example 2

Input:

```
3 3
9 6 7
```

| Child | Candies Wanted | Turns Needed | Current Maximum | Answer |
| --- | --- | --- | --- | --- |
| 1 | 9 | 3 | 3 | 1 |
| 2 | 6 | 2 | 3 | 1 |
| 3 | 7 | 3 | 3 | 3 |

Output:

```
3
```

Children 1 and 3 both need three turns. The later child, number 3, performs the final departure later and becomes the answer.

This example demonstrates why ties must update the answer.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each child is processed once |
| Space | O(1) | Only a few variables are stored besides the input array |

With `n ≤ 100`, this solution is far below the time and memory limits. Even the simulation approach would pass comfortably, but the turn-counting observation reduces the problem to a single linear scan.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    n, m = map(int, input().split())
    a = list(map(int, input().split()))

    best_turns = -1
    answer = -1

    for i, candies in enumerate(a, start=1):
        turns = (candies + m - 1) // m

        if turns >= best_turns:
            best_turns = turns
            answer = i

    return str(answer)

# provided sample
assert run("5 2\n1 3 1 4 2\n") == "4", "sample 1"

# minimum size
assert run("1 100\n1\n") == "1", "single child"

# all equal values
assert run("3 2\n4 4 4\n") == "3", "last occurrence of maximum"

# exact multiples of m
assert run("2 3\n3 4\n") == "2", "ceiling division"

# maximum turns tie
assert run("4 1\n100 100 100 100\n") == "4", "all need same turns"

# larger maximum appears earlier
assert run("5 4\n8 3 3 3 3\n") == "1", "unique maximum"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 100 / 1` | `1` | Minimum input size |
| `3 2 / 4 4 4` | `3` | Tie handling, last occurrence wins |
| `2 3 / 3 4` | `2` | Correct ceiling division |
| `4 1 / 100 100 100 100` | `4` | Large tie case |
| `5 4 / 8 3 3 3 3` | `1` | Unique maximum turn count |

## Edge Cases

Consider:

```
3 2
4 4 4
```

Each child needs

$$\left\lceil \frac{4}{2} \right\rceil = 2$$

turns. The algorithm processes the children from left to right. Child 1 sets the maximum to 2. Child 2 matches the maximum and becomes the answer. Child 3 also matches the maximum and becomes the final answer. The output is:

```
3
```

which matches the actual queue process.

Now consider:

```
2 3
3 4
```

The turn counts are:

$$\left\lceil \frac{3}{3} \right\rceil = 1$$

and

$$\left\lceil \frac{4}{3} \right\rceil = 2$$

The algorithm outputs child 2. This case confirms that exact multiples of `m` must not be rounded up an extra time.

Finally, consider:

```
1 100
1
```

The single child needs one turn. The scan visits only one element and returns index 1. Since no other child exists, that child is necessarily the last to leave.
