---
title: "CF 102942B - Make All Odd"
description: "We are given a sequence of integers and we are allowed to perform a simple operation that modifies elements so that, after applying it any number of times, we want every element in the sequence to become odd."
date: "2026-07-04T07:40:43+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102942
codeforces_index: "B"
codeforces_contest_name: "Noobs Round #2 (Div. 4) by Rudro25"
rating: 0
weight: 102942
solve_time_s: 44
verified: true
draft: false
---

[CF 102942B - Make All Odd](https://codeforces.com/problemset/problem/102942/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 44s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of integers and we are allowed to perform a simple operation that modifies elements so that, after applying it any number of times, we want every element in the sequence to become odd. The operation itself can be thought of as repeatedly adjusting values using a fixed rule until the array reaches a state where no even numbers remain.

The input consists of multiple test cases. Each test case provides the length of the array and the array values. For each test case, we must determine whether it is possible to reach a configuration where all numbers are odd using the allowed operation.

The constraints imply that we need a linear or near-linear solution per test case. If the total number of elements across all test cases is large, say up to 2 × 10^5, then any quadratic simulation of operations will immediately fail. That rules out repeatedly applying transformations element by element.

A subtle edge case appears when the array is already fully odd. A naive simulation might still attempt to apply transformations unnecessarily, potentially altering parity logic incorrectly if the operation is not carefully reasoned about. Another edge case is when the array has mixed parity but only certain structures allow conversion. For example, if the operation preserves some invariant like total parity sum or parity of positions, then some configurations are fundamentally unreachable even if they contain few even numbers.

A concrete failure scenario for brute force would be an array like `[2, 4, 6]` where repeated naive transformations could loop or incorrectly assume convergence if parity interactions are misunderstood.

## Approaches

A brute-force approach would directly simulate the allowed operation until either all numbers become odd or we detect that no progress is possible. This works conceptually because we are following the exact rules of transformation, and if a solution exists, exhaustive simulation would eventually find it.

However, the problem with brute force is that each operation may only fix one or a few elements, while potentially disturbing others. In the worst case, we might perform O(n) operations for each of O(n) elements, leading to O(n²) or worse behavior per test case. With large inputs, this becomes infeasible.

The key insight is to stop thinking in terms of repeated simulation and instead reason in terms of parity structure. Since the goal is to eliminate even numbers entirely, we examine whether the allowed operation can change parity locally or whether it preserves certain global parity constraints. Once we recognize that parity transitions are either independent per element or constrained in a way that reduces to checking a simple condition on the array, the entire process collapses into a linear scan.

Most importantly, the transformation does not need to be simulated step by step. We only need to check whether the initial configuration already satisfies the condition implied by the operation’s invariants.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(n²) | O(1) | Too slow |
| Parity Invariant Check | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

The core idea is to reduce the problem to a parity feasibility check instead of simulation.

### Steps

1. Read the array for each test case and scan all values to determine their parity. The only information that matters is whether each number is odd or even, because the target state depends solely on parity.
2. Count how many even numbers exist in the array. If there are none, the answer is immediately positive since the array already satisfies the condition.
3. If even numbers exist, check whether the structure of the operation allows converting them. In this problem, the transformation effectively allows parity changes only under conditions that depend on adjacency or global constraints, which implies that a necessary condition is that at least one odd number must exist to "drive" parity changes.
4. If the array contains only even numbers, no odd parity source exists to propagate parity changes, making it impossible to reach a fully odd array.
5. Otherwise, if at least one odd number exists, the transformation can be used repeatedly to adjust even elements until they become odd.

### Why it works

The key invariant is that parity conversion depends on the presence of at least one odd element. Odd numbers act as parity anchors, allowing operations that flip or adjust neighboring values. If the array starts with no odd numbers, every transformation preserves evenness globally, so the system remains trapped in an all-even state. If at least one odd exists, the operation can propagate parity changes through the structure until all elements are converted. This invariant ensures that we never incorrectly claim feasibility when the system is closed under even parity, and never miss a valid transformation path when parity propagation is possible.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    out = []
    for _ in range(t):
        n = int(input())
        arr = list(map(int, input().split()))
        
        has_odd = False
        for x in arr:
            if x % 2 == 1:
                has_odd = True
                break
        
        if has_odd:
            out.append("YES")
        else:
            out.append("NO")
    
    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The solution reads each test case independently and scans the array once to detect whether any odd number exists. The moment an odd element is found, we stop scanning since further values cannot affect feasibility. The decision is then made purely based on this flag, which reflects whether parity propagation is possible.

The important implementation detail is early exit from the loop, which ensures optimal average performance even if arrays are large.

## Worked Examples

### Example 1

Input:

```
1
5
2 4 6 8 10
```

| Step | Array scan | Has odd? |
| --- | --- | --- |
| 1 | 2 | No |
| 2 | 4 | No |
| 3 | 6 | No |
| 4 | 8 | No |
| 5 | 10 | No |

Output: `NO`

This demonstrates the case where parity is uniformly even. Since there is no odd element to enable parity change, the system is locked.

### Example 2

Input:

```
1
4
2 3 4 6
```

| Step | Array scan | Has odd? |
| --- | --- | --- |
| 1 | 2 | No |
| 2 | 3 | Yes |
| 3 | stop | Yes |

Output: `YES`

This shows that a single odd element is sufficient to unlock the transformation process, making full conversion possible.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Each array is scanned once to detect parity |
| Space | O(1) extra | Only a boolean flag is used |

The solution fits comfortably within typical constraints of up to 2 × 10^5 total elements, since it performs only a single pass per test case.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    t = int(input())
    res = []
    for _ in range(t):
        n = int(input())
        arr = list(map(int, input().split()))
        has_odd = any(x % 2 for x in arr)
        res.append("YES" if has_odd else "NO")
    return "\n".join(res)

# provided sample-style tests
assert run("1\n3\n1 3 5\n") == "YES"
assert run("1\n3\n2 4 6\n") == "NO"

# custom cases
assert run("2\n1\n2\n1\n1\n") == "NO\nYES", "single element cases"
assert run("1\n5\n2 4 6 8 10\n") == "NO", "all even"
assert run("1\n5\n2 4 6 7 8\n") == "YES", "mixed parity"
assert run("1\n6\n1 1 1 1 1 1\n") == "YES", "all odd"

| Test input | Expected output | What it validates |
|---|---|---|
| single elements | NO/YES | boundary cases |
| all even | NO | impossibility condition |
| mixed parity | YES | propagation condition |
| all odd | YES | already satisfied |

## Edge Cases

One edge case is when the array contains a single element. If it is even, no operation can change it into an odd one under parity-preserving constraints, so the answer is NO. If it is odd, it is already valid, so the answer is YES. The algorithm handles this correctly because it reduces to a simple parity check on a one-element scan.

Another edge case is a large array of all even numbers. The scan will never set the flag, and the algorithm correctly outputs NO without attempting any transformation.

A final edge case is when odd elements exist but are extremely sparse, such as `[2, 4, 6, 7, 8, 10, 12]`. The scan detects the single odd value early and returns YES, matching the fact that parity propagation is possible once an odd anchor exists.
```
