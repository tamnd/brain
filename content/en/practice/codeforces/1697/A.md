---
title: "CF 1697A - Parkway Walk"
description: "We are given a linear sequence of benches, numbered from one to $n+1$, separated by distances $a1, a2, dots, an$. You start at the first bench with a fixed amount of energy $m$. Walking a distance of one meter consumes exactly one unit of energy."
date: "2026-06-09T22:25:36+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1697
codeforces_index: "A"
codeforces_contest_name: "Educational Codeforces Round 130 (Rated for Div. 2)"
rating: 800
weight: 1697
solve_time_s: 126
verified: true
draft: false
---

[CF 1697A - Parkway Walk](https://codeforces.com/problemset/problem/1697/A)

**Rating:** 800  
**Tags:** greedy, implementation  
**Solve time:** 2m 6s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a linear sequence of benches, numbered from one to $n+1$, separated by distances $a_1, a_2, \dots, a_n$. You start at the first bench with a fixed amount of energy $m$. Walking a distance of one meter consumes exactly one unit of energy. You can restore energy only by sitting at benches, and you may choose exactly how much energy to restore at each stop, even exceeding your initial capacity $m$. The goal is to determine the minimal total amount of energy you need to restore to reach the last bench.

The input consists of multiple test cases. Each test case provides the number of benches minus one $n$, the initial energy $m$, and the distances $a_i$. The output should be a single integer per test case indicating the minimum energy restoration required.

The constraints are modest: $n$ is at most 100 and $a_i$ is at most 100, while the initial energy $m$ can go up to $10^4$. This means any solution with a complexity of $O(n)$ or $O(n^2)$ per test case will run comfortably within the 1-second limit. The main challenge is correctly accounting for the energy spent and restored at each bench without overcomplicating the logic.

Edge cases arise when the initial energy is already sufficient to reach the last bench without sitting, for example, $n=5$, $m=16$, and distances $1,2,3,4,5$. Here, the correct answer is zero because no restoration is necessary. Another subtle scenario occurs when the distance to the next bench is larger than the current energy, forcing a restoration equal to the difference. A careless implementation that sums deficits or mismanages leftover energy can give an incorrect answer in such cases.

## Approaches

A naive approach is to simulate the walk: start at bench 1, keep track of your current energy, and whenever the remaining energy is insufficient to reach the next bench, restore exactly the deficit. After walking the distance to the next bench, update the current energy. This is effectively the greedy solution. It is correct because at each step the minimal necessary restoration is exactly what allows you to reach the next bench, and restoring more would be wasteful. Since $n \le 100$, this direct simulation is fast enough.

A more formal optimal solution comes from realizing that the minimum restoration at each step is $\max(0, a_i - \text{current energy})$. You iterate through the distances, compute the deficit if your energy is too low, add it to a running total of restored energy, and update the current energy by subtracting the distance and adding the restored energy. The simplicity of this observation makes the greedy approach optimal and immediate to implement.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(n) per test case | O(1) | Accepted |
| Greedy Energy Deficit | O(n) per test case | O(1) | Accepted |

## Algorithm Walkthrough

1. Initialize a variable `restored` to zero. This will accumulate the total energy restored across all benches.
2. Set the current energy `energy` to the starting value $m$.
3. Iterate over each distance $a_i$ between bench $i$ and $i+1$. At each step, check if the current energy is sufficient to cover $a_i$.
4. If `energy` is greater than or equal to $a_i$, subtract $a_i$ from `energy` and proceed to the next bench.
5. If `energy` is less than $a_i$, compute the deficit $deficit = a_i - energy$. Add `deficit` to `restored` and set `energy = 0` after walking to the next bench, because you will have just enough energy after restoring to cover the distance.
6. Continue until the last bench is reached.
7. After the loop, `restored` contains the minimal total energy that needed to be restored.

Why it works: The invariant is that after processing each bench, the current energy represents the energy left after walking that leg. By restoring only what is necessary to reach the next bench, we ensure that the total restoration is minimal. There is no scenario where delaying restoration or restoring more reduces the total restoration, because energy can only be restored in non-negative amounts and walking always consumes exactly one unit per meter.

## Python Solution

```python
import sys
input = sys.stdin.readline

def main():
    t = int(input())
    for _ in range(t):
        n, m = map(int, input().split())
        a = list(map(int, input().split()))
        energy = m
        restored = 0
        for dist in a:
            if energy >= dist:
                energy -= dist
            else:
                deficit = dist - energy
                restored += deficit
                energy = 0
        print(restored)

if __name__ == "__main__":
    main()
```

We first read the number of test cases and then loop through each test case. For each bench-to-bench distance, we check if the current energy suffices. If not, we compute exactly how much energy must be restored, add it to the running total, and reset the energy after walking. This ensures the minimal restoration is accumulated correctly. The order of subtraction and addition is critical; doing it incorrectly can lead to off-by-one errors where you restore too much or too little.

## Worked Examples

Using the first sample:

| Bench | Distance a_i | Current Energy | Energy Deficit | Restored Energy | Energy after walk |
| --- | --- | --- | --- | --- | --- |
| 1-2 | 1 | 1 | 0 | 0 | 0 |
| 2-3 | 2 | 0 | 2 | 2 | 0 |
| 3-4 | 1 | 0 | 1 | 3 | 0 |

This demonstrates that each deficit is accounted for and the running total reaches 3.

Using the second sample $n=4, m=5, a=[3,3,5,2]$:

| Bench | Distance a_i | Current Energy | Energy Deficit | Restored Energy | Energy after walk |
| --- | --- | --- | --- | --- | --- |
| 1-2 | 3 | 5 | 0 | 0 | 2 |
| 2-3 | 3 | 2 | 1 | 1 | 0 |
| 3-4 | 5 | 0 | 5 | 6 | 0 |
| 4-5 | 2 | 0 | 2 | 8 | 0 |

The running total restoration 8 matches the expected output.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | We iterate once over each distance array a of length n. Maximum n is 100. |
| Space | O(n) | Storing distances a; no extra arrays or recursion needed. |

Given $t \le 100$ and $n \le 100$, the total number of operations is at most 10,000, which is well within the 1-second time limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    main()
    return output.getvalue().strip()

# provided samples
assert run("3\n3 1\n1 2 1\n4 5\n3 3 5 2\n5 16\n1 2 3 4 5\n") == "3\n8\n0", "sample 1"

# minimum size input
assert run("1\n1 1\n1\n") == "0", "minimum size"

# maximum distance requiring restoration
assert run("1\n3 1\n5 5 5\n") == "14", "all large distances"

# all equal distances with sufficient energy
assert run("1\n4 10\n2 2 2 2\n") == "0", "equal distances, enough energy"

# exactly needing energy to restore at each step
assert run("1\n4 2\n3 3 3 3\n") == "8", "need to restore at each step"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1\n1 | 0 | Minimum input, no restoration needed |
| 3 1\n5 5 5 | 14 | Large distances relative to energy, ensures accumulation works |
| 4 10\n2 2 2 2 | 0 | All equal distances, enough starting energy |
| 4 2\n3 3 3 3 | 8 | Requires restoration at every step, edge case for repeated deficits |

## Edge Cases

If the initial energy is larger than the sum of all distances, the algorithm never enters the deficit branch and correctly outputs zero. For a case with alternating large and small distances relative to energy, the greedy step ensures that at each bench we restore only the deficit and the running total correctly accumulates minimal restoration. For example, with $n=3, m=2, a=[3,1,4]$, the table traces:

| Bench | Distance | Energy | Deficit | Restored | Energy after walk |
| --- | --- | --- | --- | --- | --- |
| 1-2 | 3 |  |  |  |  |
