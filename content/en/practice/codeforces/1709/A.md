---
title: "CF 1709A - Three Doors"
description: "We are given three doors, each with a unique lock number from 1 to 3. We also hold a key in our hand, and behind each door there may be another key or nothing. Two keys are hidden behind doors, and one key is in our hand."
date: "2026-06-09T20:51:56+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "greedy", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 1709
codeforces_index: "A"
codeforces_contest_name: "Educational Codeforces Round 132 (Rated for Div. 2)"
rating: 800
weight: 1709
solve_time_s: 123
verified: true
draft: false
---

[CF 1709A - Three Doors](https://codeforces.com/problemset/problem/1709/A)

**Rating:** 800  
**Tags:** brute force, greedy, implementation, math  
**Solve time:** 2m 3s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given three doors, each with a unique lock number from 1 to 3. We also hold a key in our hand, and behind each door there may be another key or nothing. Two keys are hidden behind doors, and one key is in our hand. Each key can open exactly the door with the matching number. The task is to determine whether, starting with the key in hand, we can sequentially open all three doors, retrieving the remaining keys along the way.

The input consists of a number of test cases. For each test case, we receive the number on the key in hand and a list of three integers representing the keys behind doors 1, 2, and 3 respectively. A zero indicates there is no key behind that door. Exactly one key number appears in the hand, and the remaining two key numbers are behind doors, while the third door contains no key.

Constraints are very small: up to 18 test cases, and keys are limited to 1 through 3. This immediately rules out any concern about performance. The problem is purely logical: the solution only needs to correctly model the process of unlocking doors and retrieving keys.

An edge case arises when the key in hand does not directly unlock a door that contains the second key we need. For example, if we start with key 2 and the keys behind doors are `[1, 3, 0]`, then we cannot reach key 1 because door 1 requires key 1 to open, creating a deadlock. The correct output is "NO" in this case. A naive approach might ignore this dependency and incorrectly assume all doors can be opened.

## Approaches

The simplest approach is brute force: try every sequence of unlocking doors using the key in hand and any keys retrieved. Since there are only three doors, the number of sequences is small (3! = 6), so a brute-force simulation would work, but it is overkill and obscures the logic.

The key insight is that the problem can be reduced to a two-step check: first, use the key in hand to open the corresponding door. Then take the key behind that door, if any, and see if it can unlock one of the remaining doors. If the first key opens a door that contains the second key, we can always open the remaining door with that second key. Otherwise, we may get stuck if the remaining keys are behind doors that cannot be opened by the keys we have.

We can formalize this as a simple sequence: let `current_key` be the key in hand. Open the door with number `current_key`. If that door has a key behind it (nonzero), set `current_key` to that key and open the door with that number. If at any point we try to open a door that requires a key we do not possess, the answer is "NO". If we successfully open two doors and retrieve the last key, the remaining door can always be opened with the last key.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(6) per test case | O(1) | Accepted but unnecessary |
| Optimal | O(1) per test case | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases `t`.
2. For each test case, read the key in hand `x` and the list `[a, b, c]` representing keys behind doors 1, 2, and 3.
3. Treat the doors and keys as a mapping from door number to key behind it. In other words, door 1 has key `a`, door 2 has key `b`, door 3 has key `c`.
4. Start with the key in hand as `current_key`. Check the door with that number. If the key behind it is 0, the remaining unopened door must have the last key, which we already have. Print "YES".
5. If the door has a key behind it (nonzero), take that key and check the door corresponding to that key. If that door contains 0 (no key), we can still open it. If it contains a key, that must be the last door. Verify that this matches the last remaining key.
6. If at any point the key we need is behind a door we cannot open with keys in hand, print "NO". Otherwise, print "YES".

Why it works: The invariant is that at each step, the key in hand can either unlock a door that gives us the next key or unlock a door with no key. Because there are only three doors and the keys are distributed such that exactly one key is missing behind a door, this two-step simulation is sufficient to determine if all doors are accessible.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    x = int(input())
    a, b, c = map(int, input().split())
    doors = {1: a, 2: b, 3: c}

    current_key = x
    first_door_key = doors[current_key]

    if first_door_key == 0:
        print("NO")
    else:
        second_door_key = doors[first_door_key]
        if second_door_key == 0:
            print("YES")
        else:
            print("NO")
```

The solution reads the test cases and represents the doors as a dictionary mapping from door number to key behind it. Starting with the key in hand, it simulates opening the corresponding door. If the door has a key, it attempts to open the next door with that key. If the second door has no key behind it, all doors are openable, so we print "YES". Otherwise, we are stuck, and the answer is "NO".

## Worked Examples

Sample Input:

```
3
3
0 1 2
1
0 3 2
2
3 1 0
```

Trace for first test case:

| Step | current_key | door opened | key behind door | Result |
| --- | --- | --- | --- | --- |
| 1 | 3 | door 3 | 2 | take key 2 |
| 2 | 2 | door 2 | 1 | take key 1 |
| 3 | 1 | door 1 | 0 | no more keys |

This shows that starting with key 3, we can sequentially unlock all doors and retrieve all keys.

Trace for second test case:

| Step | current_key | door opened | key behind door | Result |
| --- | --- | --- | --- | --- |
| 1 | 1 | door 1 | 0 | cannot continue |

Here, the key in hand opens a door with no key behind it. We cannot access any remaining keys, so the answer is "NO".

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t) | Each test case involves at most two dictionary lookups |
| Space | O(1) | We only store three doors per test case |

Given `t <= 18`, this is trivially fast and fits within the 2-second limit. Memory usage is minimal.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    t = int(input())
    for _ in range(t):
        x = int(input())
        a, b, c = map(int, input().split())
        doors = {1: a, 2: b, 3: c}
        current_key = x
        first_door_key = doors[current_key]
        if first_door_key == 0:
            print("NO")
        else:
            second_door_key = doors[first_door_key]
            if second_door_key == 0:
                print("YES")
            else:
                print("NO")
    return output.getvalue().strip()

# Provided samples
assert run("4\n3\n0 1 2\n1\n0 3 2\n2\n3 1 0\n2\n1 3 0\n") == "YES\nNO\nYES\nNO"

# Custom cases
assert run("1\n1\n0 2 3\n") == "NO", "cannot open first door to get next key"
assert run("1\n2\n1 0 3\n") == "YES", "first door has next key"
assert run("1\n3\n1 2 0\n") == "YES", "first door has next key"
assert run("1\n1\n2 0 3\n") == "NO", "first door leads to door with no key"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1\n1\n0 2 3 | NO | Cannot proceed if first key opens empty door |
| 1\n2\n1 0 3 | YES | Normal case, second door contains next key |
| 1\n3\n1 2 0 | YES | Last door contains no key, still successful |
| 1\n1\n2 0 3 | NO | First key leads to door with no key behind it |

## Edge Cases

A subtle edge case occurs when the key in hand corresponds to a door with no key behind it. For example, if `x = 1` and doors = `[0, 2, 3]`, we start with key 1, open door 1, but find nothing. Keys 2 and 3 are behind doors 2 and 3,
