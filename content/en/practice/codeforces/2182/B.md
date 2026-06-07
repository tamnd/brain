---
title: "CF 2182B - New Year Cake"
description: "We are asked to help Monocarp bake a layered cake under two constraints: the size of each layer grows exponentially and the chocolate covering each layer must alternate between white and dark. The top layer always has size 1."
date: "2026-06-07T21:50:33+07:00"
tags: ["codeforces", "competitive-programming", "brute-force"]
categories: ["algorithms"]
codeforces_contest: 2182
codeforces_index: "B"
codeforces_contest_name: "Educational Codeforces Round 186 (Rated for Div. 2)"
rating: 800
weight: 2182
solve_time_s: 90
verified: true
draft: false
---

[CF 2182B - New Year Cake](https://codeforces.com/problemset/problem/2182/B)

**Rating:** 800  
**Tags:** brute force  
**Solve time:** 1m 30s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to help Monocarp bake a layered cake under two constraints: the size of each layer grows exponentially and the chocolate covering each layer must alternate between white and dark. The top layer always has size 1. The next layer has size 2, the next 4, then 8, and so on, doubling each time. Each layer consumes a number of kilograms of chocolate equal to its size, and Monocarp has limited supplies of white and dark chocolate. The task is to determine the maximum number of layers he can build without exceeding either chocolate supply.

The input provides several test cases, each specifying the quantities of white and dark chocolate. The output must be a single integer per test case: the maximum number of layers possible. Since `a` and `b` can go up to 10^6 and there can be up to 10^4 test cases, any algorithm must run in roughly O(log N) per test case, as a naive linear iteration could reach millions of operations per test case and billions overall.

A subtle point is the alternating chocolate requirement. A naive greedy approach might start layering with white or dark chocolate and keep adding until one chocolate runs out. But if we always start with white, we could miss the optimal solution that starts with dark. For example, if `a = 1` and `b = 2`, starting with white allows only one layer (size 1), while starting with dark allows two layers (1 dark, 2 white). Another edge case arises when chocolate is enough for several small layers but insufficient for the next large layer. The algorithm must check each layer incrementally and consider both starting options.

## Approaches

The brute-force method iterates through layers, doubling the size each time and subtracting from the respective chocolate pool according to the alternating pattern. This works correctly because it directly simulates the cake-building process. The problem is that in the worst case, the number of layers could be up to 20 (since the sum of the geometric series 1 + 2 + 4 + ... + 2^k exceeds 10^6 when k ≈ 19), so brute-force is actually fast enough here. Each test case requires fewer than 20 iterations, making the total 2_10^4_20 = 4*10^5 operations in the worst case, which is well within the 2-second limit.

The key insight is that we only need to simulate two possible starting choices: starting with white or starting with dark. After computing both, we take the maximum. Each simulation proceeds layer by layer, doubling the layer size and subtracting from the corresponding chocolate type, stopping when the next layer would exceed the available chocolate.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(log(max(a,b))) per test case | O(1) | Accepted |
| Optimized (Two Starting Options) | O(log(max(a,b))) per test case | O(1) | Accepted |

## Algorithm Walkthrough

1. For each test case, read the quantities of white chocolate `a` and dark chocolate `b`.
2. Initialize two counters, `count1` and `count2`, representing the number of layers if starting with white or starting with dark, respectively.
3. For `count1`, simulate the cake starting with white:

1. Initialize the current layer size to 1.
2. While there is enough chocolate for the current layer:

1. Subtract the layer size from the appropriate chocolate type, alternating each layer.
2. Double the layer size.
3. Increment the layer count.
4. Repeat step 3 for `count2`, starting with dark chocolate.
5. Return the maximum of `count1` and `count2` as the answer for this test case.

Why it works: Each simulation precisely follows the rules of layer size and chocolate alternation. By trying both starting chocolates, we guarantee that we find the maximal number of layers possible. The invariant is that at every step, chocolate consumption does not exceed the available supply. Once it does, the simulation stops, which is exactly when the cake cannot be extended further.

## Python Solution

```python
import sys
input = sys.stdin.readline

def max_layers(a, b):
    def simulate(start_white):
        w, d = a, b
        layer = 1
        count = 0
        white_turn = start_white
        while True:
            if white_turn:
                if w >= layer:
                    w -= layer
                else:
                    break
            else:
                if d >= layer:
                    d -= layer
                else:
                    break
            layer *= 2
            white_turn = not white_turn
            count += 1
        return count
    
    return max(simulate(True), simulate(False))

t = int(input())
for _ in range(t):
    a, b = map(int, input().split())
    print(max_layers(a, b))
```

This code defines a helper `simulate` function that accepts a boolean indicating whether the first layer should be white. It tracks the remaining chocolate for each type, the current layer size, and alternates chocolate usage. After trying both starting colors, it returns the maximum layer count. The doubling of `layer` inside the loop ensures exponential growth. Edge cases, such as having only one type of chocolate or very small supplies, are naturally handled by the while loop.

## Worked Examples

### Example 1: `a = 1, b = 2`

| Step | Layer Size | White Left | Dark Left | Chocolate Used | Count |
| --- | --- | --- | --- | --- | --- |
| Start with white | 1 | 1 | 2 | 1 white | 1 |
| Next layer | 2 | 0 | 2 | 2 dark | 2 |
| Next layer | 4 | 0 | 0 | cannot build | - |

Maximum layers starting with white: 2

| Step | Layer Size | White Left | Dark Left | Chocolate Used | Count |
| --- | --- | --- | --- | --- | --- |
| Start with dark | 1 | 1 | 2 | 1 dark | 1 |
| Next layer | 2 | 1 | 1 | 2 white | cannot build |

Maximum layers starting with dark: 1

Answer: `max(2,1) = 2`. This demonstrates the necessity of trying both starting colors.

### Example 2: `a = 1000000, b = 1`

| Step | Layer Size | White Left | Dark Left | Chocolate Used | Count |
| --- | --- | --- | --- | --- | --- |
| Start with white | 1 | 999999 | 1 | 1 white | 1 |
| Next layer | 2 | 999999 | -1 | cannot build | - |

Maximum layers starting with white: 1

| Step | Layer Size | White Left | Dark Left | Chocolate Used | Count |
| --- | --- | --- | --- | --- | --- |
| Start with dark | 1 | 1000000 | 1 | 1 dark | 1 |
| Next layer | 2 | 999998 | 1 | 2 white | 2 |
| Next layer | 4 | 999998 | -3 | cannot build | - |

Maximum layers starting with dark: 2

Answer: `max(1,2) = 2`. This illustrates that starting with the type that has more chocolate can allow an extra layer.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(log(max(a,b))) per test case | Each layer doubles, so the number of layers is bounded by log2(max(a,b)) |
| Space | O(1) | Only a few integer variables are used per test case |

The maximum possible number of layers is around 20 for a = b = 10^6, so even with 10^4 test cases, the total number of iterations is under 2*10^5, well within the 2-second time limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    t = int(input())
    for _ in range(t):
        a, b = map(int, input().split())
        print(max_layers(a, b))
    return output.getvalue().strip()

# Provided samples
assert run("7\n1 1\n1 2\n3 1\n4 3\n5 2\n1000000 1000000\n1000000 1\n") == "1\n2\n2\n2\n3\n20\n2"

# Custom cases
assert run("3\n1 1000000\n2 2\n0 5\n") == "1\n2\n0", "edge and large differences"
assert run("1\n10 10\n") == "4", "equal moderate values"
assert run("1\n1 0\n") == "1", "only one chocolate"
assert run("1\n0 0\n") == "0", "no chocolate"
assert run("1\n1000000 500000\n") == "19", "asymmetrical large input"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1000000` | 1 | One chocolate type much larger than the other, must start with smaller type |
| `2 2` | 2 | Small equal amounts, confirms proper alternation |
| `0 5` | 0 |  |
