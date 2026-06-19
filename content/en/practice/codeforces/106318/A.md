---
title: "CF 106318A - \u0414\u0432\u0435 \u0434\u043e\u043c\u0438\u043d\u043e\u0448\u043a\u0438"
description: "We are given two domino tiles. Each tile has two numbers written on its ends. We are allowed to rotate a tile, meaning we can swap its two ends, but we cannot change the numbers themselves."
date: "2026-06-19T14:44:26+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106318
codeforces_index: "A"
codeforces_contest_name: "\u0420\u0435\u0441\u043f\u0443\u0431\u043b\u0438\u043a\u0430\u043d\u0441\u043a\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430 \u0448\u043a\u043e\u043b\u044c\u043d\u0438\u043a\u043e\u0432 \u041f\u0443\u0442\u044c \u043a \u041e\u043b\u0438\u043c\u043f\u0443 2026"
rating: 0
weight: 106318
solve_time_s: 49
verified: true
draft: false
---

[CF 106318A - \u0414\u0432\u0435 \u0434\u043e\u043c\u0438\u043d\u043e\u0448\u043a\u0438](https://codeforces.com/problemset/problem/106318/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 49s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two domino tiles. Each tile has two numbers written on its ends. We are allowed to rotate a tile, meaning we can swap its two ends, but we cannot change the numbers themselves.

The task is to determine whether these two dominoes can be placed in a line so that the touching ends have the same number. Since there are only two tiles, this reduces to checking whether we can choose an orientation for each tile so that the right end of the first matches the left end of the second.

A more direct way to see the problem is to treat each domino as a small set of two values. We want to know whether these two sets have any common element. If they do, we can align both dominoes so that the shared value becomes the connecting point.

The input is minimal, consisting of four integers describing the two dominoes. The output is a single decision: whether a valid arrangement exists.

Because the input size is constant, there are no performance constraints that drive the algorithm design. The solution must simply be correct and handle all orientation choices.

Edge cases are mainly about repeated numbers and identical dominoes.

A common mistake is to only check one fixed orientation, for example comparing the second number of the first domino with the first number of the second domino. This fails when a match exists only after rotation.

For example, consider input:

```
1 2 3 1
```

Dominoes are (1,2) and (3,1). A naive check might compare 2 with 3 and conclude no match. But rotating the second domino gives (1,3), and now 2 is still not matching, but more importantly 1 appears in both dominoes, so a valid connection exists.

Correct output:

```
YES
```

Another failure case is:

```
4 4 4 5
```

Here both dominoes share the value 4, even though it appears twice in the first tile. Any correct solution must treat each tile as a set of possible endpoints, not as ordered pairs.

## Approaches

The brute-force way is to try every possible orientation of both dominoes. Each domino has two orientations, so there are four total configurations. For each configuration, we check whether the right end of the first equals the left end of the second.

This is correct because it explicitly enumerates all placements, but it is more work than necessary. The number of checks is constant, so it already runs in O(1), but it hides the underlying structure of the problem.

The key observation is that orientation does not matter for existence of a connection. A domino can always be flipped, so each domino is effectively a set of two values. The problem reduces to checking whether the intersection of these two sets is non-empty.

This reduces the entire problem to a single membership test over four numbers.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (all orientations) | O(1) | O(1) | Accepted |
| Set Intersection Check | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

We reduce each domino into the set of values it can expose on either side, then test whether there is any overlap.

1. Read four integers representing the two dominoes, first domino (a, b) and second domino (c, d).
2. Treat the first domino as having two possible connection values, a and b. Treat the second domino as having two possible connection values, c and d. This represents all possible orientations implicitly.
3. Check whether any value in {a, b} appears in {c, d}. This is the only condition needed for a valid chain, because that shared value can be made the connecting endpoint by flipping one or both dominoes.
4. If at least one common value exists, output YES. Otherwise, output NO.

### Why it works

Each domino can be independently flipped, so both ends are interchangeable. The only constraint for a valid chain of two tiles is equality at the joining point. Since any of the two values on each domino can be chosen as the connecting side, the existence of a solution is equivalent to the existence of a shared number between the two dominoes. No other structural constraint exists in a length-two chain.

## Python Solution

```python
import sys
input = sys.stdin.readline

a, b, c, d = map(int, input().split())

first = {a, b}
second = {c, d}

if first & second:
    print("YES")
else:
    print("NO")
```

The solution builds two small sets and uses intersection to detect a common element. This directly encodes the idea that any matching value can serve as the joining point after appropriate rotations.

A subtle detail is that using sets automatically handles duplicates, so cases like (4, 4) are naturally simplified without extra logic.

## Worked Examples

### Example 1

Input:

```
1 2 3 1
```

We construct:

- first = {1, 2}
- second = {3, 1}

| Step | first | second | intersection |
| --- | --- | --- | --- |
| init | {1,2} | {3,1} | {1} |

The intersection is non-empty, so the answer is YES.

This trace shows that we do not care about ordering. The shared value 1 is enough to guarantee a valid arrangement.

### Example 2

Input:

```
2 5 3 4
```

We construct:

- first = {2, 5}
- second = {3, 4}

| Step | first | second | intersection |
| --- | --- | --- | --- |
| init | {2,5} | {3,4} | ∅ |

No common element exists, so no rotation can create a connection, and the answer is NO.

This confirms that the algorithm correctly rejects cases where all four endpoints are distinct.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only a constant number of comparisons or a set intersection on four elements |
| Space | O(1) | Only two small sets of fixed size are created |

The constraints are trivial, so this constant-time solution is optimal and easily fits within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    a, b, c, d = map(int, sys.stdin.readline().split())
    first = {a, b}
    second = {c, d}
    return "YES" if first & second else "NO"

# basic samples
assert run("1 2 3 1") == "YES"
assert run("2 5 3 4") == "NO"

# identical dominoes
assert run("4 4 4 4") == "YES"

# duplicate only in one domino
assert run("7 7 1 2") == "NO"

# match after rotation
assert run("1 9 9 3") == "YES"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 4 4 4 4 | YES | identical dominoes and duplicates |
| 7 7 1 2 | NO | repeated value not misleading match |
| 1 9 9 3 | YES | match only via rotation |

## Edge Cases

A subtle case is when both numbers on a domino are identical. For example:

```
4 4 1 2
```

The algorithm converts the first domino into {4} and the second into {1, 2}. The intersection is empty, so the answer is NO. This is correct because no rotation can introduce a new value.

Another case is when the shared value appears twice in one domino but only once in the other:

```
6 6 6 7
```

Here sets become {6} and {6, 7}. The intersection is {6}, so the algorithm correctly outputs YES, reflecting that the repeated value still serves as a valid connection point.
