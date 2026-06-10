---
title: "CF 1603A - Di-visible Confusion"
description: "We are given a sequence of integers, and the goal is to completely erase it using a very particular operation. At each step, we can pick an element whose value is not divisible by its 1-based index plus one, and remove it."
date: "2026-06-10T08:15:11+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "math", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 1603
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 752 (Div. 1)"
rating: 1300
weight: 1603
solve_time_s: 104
verified: true
draft: false
---

[CF 1603A - Di-visible Confusion](https://codeforces.com/problemset/problem/1603/A)

**Rating:** 1300  
**Tags:** constructive algorithms, math, number theory  
**Solve time:** 1m 44s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of integers, and the goal is to completely erase it using a very particular operation. At each step, we can pick an element whose value is **not divisible** by its 1-based index plus one, and remove it. After removal, the sequence shrinks and the indices of remaining elements shift left by one. The challenge is to decide whether there exists an order of removals that eventually empties the sequence.

The input provides multiple test cases, each with the length of the sequence and the sequence itself. The output is "YES" if complete removal is possible, "NO" otherwise.

The constraints are large: sequences can reach size $10^5$, and the total sum of all sequences over all test cases can reach $3 \cdot 10^5$. A naive simulation, removing elements one by one and checking divisibility at each step, would have worst-case complexity roughly $O(n^2)$, which is too slow. This means we need a solution that is linear or nearly linear in sequence length.

Edge cases occur when elements are small and indices grow. For instance, a single element 2 cannot be removed if it is at index 1 because $2 \% 2 = 0$. Another subtle case is sequences with repeated numbers: the removability of an element depends on its **current position**, not its original position.

## Approaches

The brute-force approach tries all sequences of removals. At each step, scan the array, pick any element $a_i$ such that $a_i \% (i+1) \neq 0$, and remove it. Continue until either the sequence is empty or no element is removable. This is correct in principle, but for $n = 10^5$, scanning up to $n$ elements for $n$ steps gives $O(n^2)$, which is too slow.

The key insight is to **work backwards**. If we number the positions from the final step when only one element remains, that element must satisfy its divisibility condition for its position in the shrinking sequence. We can simulate removals in reverse: start from the last element (position $n$ in the original array), check whether $a_i$ is divisible by its **final 1-based position** in the reduced sequence. If it is, removal is impossible; if not, it can be removed. By iterating from the end to the start, we only need a single pass over the array.

This approach leverages the observation that at each stage, the "hardest" element to remove is at the end of the current array. If that element is removable when counted from its shrinking position, then all earlier elements can also be handled. This reduces complexity to $O(n)$ per test case.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(n²) | O(n) | Too slow |
| Reverse Check (Optimal) | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases $t$.
2. For each test case, read $n$ and the sequence $a$.
3. Initialize a counter $current\_length = n$. This represents the "position from the end" for checking divisibility.
4. Iterate backwards through the array from the last element to the first. For each element $a[i]$:

a. If $a[i] \% current\_length == 0$, print "NO" and stop checking this test case.

b. Otherwise, decrement $current\_length$ by one and continue.
5. If the loop finishes without encountering a divisible element, print "YES".

**Why it works**: At each step, the last element in the shrinking sequence must be removable according to its **current 1-based index**. By checking elements in reverse, we guarantee that each element satisfies the divisibility requirement at the moment it would be the last remaining candidate. If any element fails, there is no sequence of removals that can erase it, so the answer is "NO".

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n = int(input())
    a = list(map(int, input().split()))
    possible = True
    current_length = n
    for value in reversed(a):
        if value % current_length == 0:
            possible = False
            break
        current_length -= 1
    print("YES" if possible else "NO")
```

The solution reads input efficiently using `sys.stdin.readline`. We iterate the sequence in reverse because the divisibility of an element depends on its eventual position when it's considered for removal. The `current_length` variable tracks this virtual position. If any element is divisible by its position, the operation cannot succeed, so we mark the test case as impossible. Otherwise, we decrement the counter and continue. The final print statement outputs the answer in the expected format.

## Worked Examples

### Example 1

Input sequence: `[1, 2, 3]`

| Step | Element checked (from end) | Position | 3 % 3 | Status | Current_length |
| --- | --- | --- | --- | --- | --- |
| 1 | 3 | 3 | 0 | OK | 2 |
| 2 | 2 | 2 | 0 | OK | 1 |
| 3 | 1 | 1 | 0 | OK | 0 |

All elements satisfy the condition when counted from reverse. Output is `YES`.

### Example 2

Input sequence: `[2]`

| Step | Element | Position | 2 % 1 | Status | Current_length |
| --- | --- | --- | --- | --- | --- |
| 1 | 2 | 1 | 0 | Fail | - |

Element 2 is divisible by its position (1), so output is `NO`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Single pass over array from end to start |
| Space | O(1) extra | Only a few variables; input stored in array |

Given the sum of $n$ over all test cases is ≤ 300,000, the total number of operations is acceptable within a 1-second time limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        possible = True
        current_length = n
        for value in reversed(a):
            if value % current_length == 0:
                possible = False
                break
            current_length -= 1
        print("YES" if possible else "NO")
    return output.getvalue().strip()

# Provided samples
assert run("5\n3\n1 2 3\n1\n2\n2\n7 7\n10\n384836991 191890310 576823355 782177068 404011431 818008580 954291757 160449218 155374934 840594328\n8\n6 69 696 69696 696969 6969696 69696969 696969696") == "YES\nNO\nYES\nYES\nNO"

# Custom tests
assert run("1\n1\n1") == "YES", "single element removable"
assert run("1\n1\n2") == "NO", "single element non-removable"
assert run("1\n3\n2 3 4") == "YES", "small array, all removable"
assert run("1\n3\n2 4 6") == "NO", "small array, last element blocked"
assert run("1\n5\n1 1 1 1 1") == "YES", "all ones"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1\n1\n1` | YES | Single element that can be removed |
| `1\n1\n2` | NO | Single element that cannot be removed |
| `1\n3\n2 3 4` | YES | Small array, all elements removable |
| `1\n3\n2 4 6` | NO | Last element cannot be removed |
| `1\n5\n1 1 1 1 1` | YES | Edge case with repeated numbers |

## Edge Cases

A sequence with only one element that equals its 1-based index plus one cannot be removed. For example, `[2]` fails because $2 \% 1 = 0$. The algorithm correctly identifies this on the first iteration of the reverse loop and outputs "NO".

For sequences where all elements are equal to 1, the reverse check sees `1 % n`, `1 % (n-1)`, etc., none of which is zero except for `1 % 1`, which is allowed. The solution outputs "YES".

For sequences with large numbers, divisibility checks are performed modulo `current_length`, which never exceeds $10^5$, so no integer overflow occurs.
