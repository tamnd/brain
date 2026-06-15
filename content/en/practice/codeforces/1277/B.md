---
title: "CF 1277B - Make Them Odd"
description: "We are given several independent test cases. In each test case, we start with a list of positive integers. One operation lets us pick a value $c$, but only if it is even, and then we simultaneously replace every occurrence of $c$ in the array by $c/2$."
date: "2026-06-16T01:52:23+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 1277
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 606 (Div. 2, based on Technocup 2020 Elimination Round 4)"
rating: 1200
weight: 1277
solve_time_s: 590
verified: true
draft: false
---

[CF 1277B - Make Them Odd](https://codeforces.com/problemset/problem/1277/B)

**Rating:** 1200  
**Tags:** greedy, number theory  
**Solve time:** 9m 50s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given several independent test cases. In each test case, we start with a list of positive integers. One operation lets us pick a value $c$, but only if it is even, and then we simultaneously replace every occurrence of $c$ in the array by $c/2$.

The goal is to repeat this operation as few times as possible until every number in the array becomes odd.

A useful way to interpret the process is that each value evolves independently by repeated division by two, but the key restriction is that we cannot target an individual position, we only affect all occurrences of a chosen even value at once.

The constraints allow up to $2 \cdot 10^5$ total numbers across all test cases, so any solution that tries to simulate each operation step by step on the full array or repeatedly scans the array per operation will not pass. A solution must essentially process each element a constant number of times, or compress repeated structure into a single pass per test case.

A subtle edge case appears when many numbers share overlapping intermediate values during their halving chains. For example, $40$ and $20$ interact because $40 \to 20 \to 10 \to 5$ while $20 \to 10 \to 5$. A naive approach that processes elements independently would underestimate the cost because it ignores that shared intermediate values still require separate operations unless carefully accounted for.

## Approaches

A brute-force idea is to simulate the process directly. While there exists at least one even value in the array, we pick some even $c$, divide all occurrences of $c$ by two, and repeat until all values become odd. Each step requires scanning or maintaining a frequency map of values to decide which even number to operate on. In the worst case, values like $2^k$ generate long chains of halvings, and multiple distinct values may repeatedly reappear after transformations. This leads to potentially $O(n \log A)$ operations, and each operation may require updating counts across a large structure, making it too slow.

The key observation is that each number contributes a “chain” of even values it passes through before becoming odd. For a number $x$, we can repeatedly divide by two until it becomes odd, recording all intermediate even values along the path. For example, $40$ produces the chain $40, 20, 10$. Each distinct value in this chain represents a required operation at some point: at least one operation must be performed for each distinct even number that appears in any chain.

Now the critical structure becomes visible: the answer is exactly the number of distinct even integers that appear anywhere in any halving chain of the array. Each such value must be chosen at least once, and choosing it once is sufficient because that operation simultaneously processes all occurrences of that value across all elements.

This reduces the problem to collecting all intermediate even values across all numbers and counting unique ones.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | $O(n \cdot \text{operations})$ | $O(n)$ | Too slow |
| Track unique even chain values | $O(n \log A)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

1. For each test case, create an empty set to store values that correspond to required operations. This set represents all even numbers that appear in any halving chain.
2. Iterate through every number in the array.
3. While the current number is even, insert it into the set and divide it by two. This simulates following the number’s trajectory until it becomes odd. Each insertion marks that we will need at least one operation targeting that value.
4. Continue this process independently for all numbers.
5. After processing all elements, the size of the set is the answer for the test case.

The reason we only record even numbers is that odd numbers are already in their final form and never require operations.

### Why it works

Each operation targets a single even value and reduces all occurrences of it simultaneously. Therefore, every distinct even value that appears at any stage in any element’s halving process must be eliminated at least once. Conversely, performing one operation per distinct even value is sufficient because once we process a value $c$, all occurrences of $c$ immediately become $c/2$, and we never need to process $c$ again. This creates a one-to-one correspondence between distinct even values encountered and required moves.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        
        seen = set()
        
        for x in a:
            while x % 2 == 0:
                seen.add(x)
                x //= 2
        
        print(len(seen))

if __name__ == "__main__":
    solve()
```

The solution iterates through each number and repeatedly divides it by two while it remains even. Each intermediate even value is stored in a set so duplicates across the array do not inflate the answer. The final result is simply the number of unique even values encountered.

A common mistake is to stop at the first occurrence of a value or to count per element instead of globally. That would overcount or undercount because multiple elements may share the same even ancestor, and each such ancestor corresponds to a single required operation.

## Worked Examples

### Example 1

Input array: $[40, 6, 40, 3, 20, 1]$

| Element | Even chain produced | Set after processing |
| --- | --- | --- |
| 40 | 40, 20, 10 | {40, 20, 10} |
| 6 | 6, 3 | {40, 20, 10, 6} |
| 40 | 40, 20, 10 | {40, 20, 10, 6} |
| 3 | none | {40, 20, 10, 6} |
| 20 | 20, 10 | {40, 20, 10, 6} |
| 1 | none | {40, 20, 10, 6} |

Final answer is 4.

This shows that repeated occurrences of the same halving chain do not increase the number of required operations. The set compresses all redundancy.

### Example 2

Input array: $[2, 4, 8, 16]$

| Element | Even chain produced | Set after processing |
| --- | --- | --- |
| 2 | 2 | {2} |
| 4 | 4, 2 | {2, 4} |
| 8 | 8, 4, 2 | {2, 4, 8} |
| 16 | 16, 8, 4, 2 | {2, 4, 8, 16} |

Final answer is 4.

This demonstrates the worst-case behavior where chains fully overlap but still contribute distinct levels.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \log A)$ | Each number is divided by two until it becomes odd, contributing logarithmic steps |
| Space | $O(n \log A)$ | In worst case, all intermediate even values are stored in a set |

The total input size is at most $2 \cdot 10^5$, and each number produces at most about 30 halving steps since $A \le 10^9$. This makes the solution comfortably efficient.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    def solve():
        t = int(input())
        out = []
        for _ in range(t):
            n = int(input())
            a = list(map(int, input().split()))
            seen = set()
            for x in a:
                while x % 2 == 0:
                    seen.add(x)
                    x //= 2
            out.append(str(len(seen)))
        return "\n".join(out)

    return solve()

# provided samples
assert run("""4
6
40 6 40 3 20 1
1
1024
4
2 4 8 16
3
3 1 7
""") == """4
10
4
0"""

# custom cases
assert run("""1
1
1
""") == "0"

assert run("""1
3
2 2 2
""") == "1"

assert run("""1
3
6 10 14
""") == "3"

assert run("""1
2
12 3
""") == "2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1, [1] | 0 | already all odd |
| 2,2,2 | 1 | duplicates do not increase operations |
| 6,10,14 | 3 | disjoint chains |
| 12,3 | 2 | mixed even and odd behavior |

## Edge Cases

A key edge case is when the array contains only odd numbers. In that situation, the loop never executes and the set remains empty, correctly producing zero operations.

Another case is when all numbers are powers of two, such as $[1024]$. The chain becomes $1024 \to 512 \to \dots \to 2$. The algorithm collects every intermediate even value, and each level corresponds to a necessary operation. This ensures the answer equals the exponent of the largest power of two in the input.

Finally, repeated identical values such as $[6, 6, 6]$ only contribute a single chain $\{6, 3\}$. Since 3 is odd, only 6 is counted, and the set ensures we do not overcount repeated work.
