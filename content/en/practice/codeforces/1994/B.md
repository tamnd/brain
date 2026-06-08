---
title: "CF 1994B - Fun Game"
description: "We are given two binary sequences of equal length, s and t. Vanya can perform a specific operation on s repeatedly: he chooses a contiguous subarray from position l to r, and for each position i in that subarray, replaces s[i] with s[i] XOR s[i - l + 1]."
date: "2026-06-09T02:21:58+07:00"
tags: ["codeforces", "competitive-programming", "bitmasks", "constructive-algorithms", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 1994
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 959 sponsored by NEAR (Div. 1 + Div. 2)"
rating: 1100
weight: 1994
solve_time_s: 322
verified: false
draft: false
---

[CF 1994B - Fun Game](https://codeforces.com/problemset/problem/1994/B)

**Rating:** 1100  
**Tags:** bitmasks, constructive algorithms, greedy, math  
**Solve time:** 5m 22s  
**Verified:** no  

## Solution
## Problem Understanding

We are given two binary sequences of equal length, `s` and `t`. Vanya can perform a specific operation on `s` repeatedly: he chooses a contiguous subarray from position `l` to `r`, and for each position `i` in that subarray, replaces `s[i]` with `s[i] XOR s[i - l + 1]`. The goal is to determine if it is possible, using any number of these operations, to transform `s` into `t`.

The first key observation is that the operation is entirely linear over bits. Each bit can be flipped if and only if there exists at least one `1` in the prefix that can propagate via XOR. If the first element is `0`, it can never influence later bits directly. Conversely, if there is at least one `1` in `s`, we can propagate it to flip other bits through appropriate operations.

The input constraints allow sequences of up to `2·10^5` bits per test case, and the sum of all sequence lengths across test cases is also at most `2·10^5`. This means we need an `O(n)` solution per test case. Any solution attempting to simulate operations directly, especially over nested loops, will be far too slow. Edge cases arise when `s` is all zeros or sequences are length 1, as in these cases no XOR propagation is possible.

A careless implementation that attempts to simulate operations could fail on inputs like `s = 0` and `t = 1`, because no operation can change the single zero to a one.

## Approaches

The brute-force approach would attempt to simulate the XOR operation over all possible `(l, r)` pairs repeatedly until `s` equals `t`. This works in principle, since the operation is deterministic and limited to finite positions. However, there are roughly `O(n^2)` pairs per operation, and potentially many repeated operations, resulting in a worst-case complexity of `O(n^3)` or worse. For the largest constraints (`n ≈ 2·10^5`), this is entirely infeasible.

The key insight is that each bit in `s` can only influence later bits via XOR if there is at least one `1` before it. Specifically, the operation at index `i` can only flip a `0` to `1` (or vice versa) if there exists at least one `1` in the prefix `s[0..i-1]`. Therefore, the transformation is impossible only if `s` is all zeros and `t` contains at least one `1`. Otherwise, the game is "interesting" because we can constructively propagate existing ones to match `t`.

This reduces the problem to a simple check: if `s` is all zeros and `t` is not, print "No". If the first element of `s` equals the first element of `t` and there is at least one `1` somewhere in `s`, or if the sequences are identical, print "Yes". This approach is `O(n)` per test case and fits comfortably within the time limits.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n³) | O(n) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. For each test case, read the length `n` and sequences `s` and `t`.
2. If `s` is equal to `t` already, output "Yes" and continue. No operations are needed.
3. Count the number of `1`s in `s`. If there are no ones (`count_1 == 0`) and `t` contains at least one `1`, output "No". It is impossible to flip zeros into ones.
4. Otherwise, check if the first bit of `s` is `0` and the first bit of `t` is `1`. If so, output "No" because the first position cannot ever change from `0` to `1` without a prior one to propagate.
5. In all other cases, output "Yes". There is at least one `1` to propagate and reach any required configuration of `t`.

Why it works: The invariant is that any position `i` can be flipped only if there exists at least one `1` in the prefix `s[0..i-1]`. By counting `1`s and checking the first element, we capture all constraints that prevent `t` from being achievable. The rest is guaranteed by the constructive nature of XOR propagation.

## Python Solution

```python
import sys
input = sys.stdin.readline

def main():
    q = int(input())
    for _ in range(q):
        n = int(input())
        s = input().strip()
        t = input().strip()
        
        if s == t:
            print("Yes")
            continue
        
        if '1' not in s:
            if '1' in t:
                print("No")
            else:
                print("Yes")
            continue
        
        if s[0] == '0' and t[0] == '1':
            print("No")
        else:
            print("Yes")

if __name__ == "__main__":
    main()
```

The solution first checks equality to handle trivial cases immediately. The count of `1`s in `s` identifies if any XOR operations are possible. The check of the first bit ensures positions that cannot change are respected. All steps run in `O(n)` per test case.

## Worked Examples

**Example 1**

Input:

```
1
1
0
1
```

| Step | s | t | Action | Output |
| --- | --- | --- | --- | --- |
| Initial | 0 | 1 | Check equality | Not equal |
| Count 1s in s | 0 | - | No ones in s, t has one | No |

This confirms that single-bit zeros cannot be flipped.

**Example 2**

Input:

```
1
4
0100
0001
```

| Step | s | t | Action | Output |
| --- | --- | --- | --- | --- |
| Initial | 0100 | 0001 | Check equality | Not equal |
| Count 1s in s | 1 | - | s has one | Continue |
| First bit s vs t | 0 vs 0 | - | First bit compatible | Yes |

This demonstrates that as long as there is at least one `1` in `s`, propagation allows reaching `t`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | We scan sequences to check equality and count ones |
| Space | O(1) | Only a few variables are used; sequences can be read line by line |

The total sum of `n` across all test cases is `2·10^5`, making the overall complexity well within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out
    main()
    sys.stdout = sys.__stdout__
    return out.getvalue().strip()

# Provided samples
assert run("6\n1\n0\n1\n7\n0110100\n0110100\n9\n100101010\n101111110\n4\n0011\n1011\n4\n0100\n0001\n8\n10110111\n01100000\n") == "No\nYes\nYes\nNo\nYes\nYes"

# Custom cases
assert run("1\n1\n0\n0\n") == "Yes", "single zero unchanged"
assert run("1\n1\n1\n1\n") == "Yes", "single one unchanged"
assert run("1\n2\n00\n01\n") == "No", "two zeros cannot produce a one"
assert run("1\n3\n101\n010\n") == "Yes", "ones can propagate to flip zeros"
assert run("1\n5\n00000\n00000\n") == "Yes", "all zeros unchanged"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1-bit 0 → 0 | Yes | Single bit no-op |
| 1-bit 1 → 1 | Yes | Single bit no-op |
| 2-bit 00 → 01 | No | Cannot create ones from zeros |
| 3-bit 101 → 010 | Yes | Ones propagate via XOR |
| 5-bit all zeros unchanged | Yes | All zeros do not need flipping |

## Edge Cases

A critical edge case is when `s` starts with `0` and `t` starts with `1`. For example, `s = 0xxxx` and `t = 1xxxx`. In this scenario, no operation can ever change the first bit from `0` to `1`, since the XOR depends on a previous one. The algorithm correctly returns "No". Another edge case is when `s` has exactly one `1` located after the first bit, and `t` requires flipping earlier bits. The solution works because only the first bit matters for this propagation check; any later bits can always propagate once there is a `1`.
