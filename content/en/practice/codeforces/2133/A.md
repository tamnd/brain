---
title: "CF 2133A - Redstone?"
description: "We are asked to decide whether a sequence of gears can be arranged in a line such that spinning the leftmost gear at one revolution per second results in the rightmost gear spinning exactly at one revolution per second."
date: "2026-06-08T02:45:12+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "data-structures", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 2133
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 1044 (Div. 2)"
rating: 800
weight: 2133
solve_time_s: 74
verified: true
draft: false
---

[CF 2133A - Redstone?](https://codeforces.com/problemset/problem/2133/A)

**Rating:** 800  
**Tags:** brute force, data structures, implementation, math  
**Solve time:** 1m 14s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to decide whether a sequence of gears can be arranged in a line such that spinning the leftmost gear at one revolution per second results in the rightmost gear spinning exactly at one revolution per second. Each gear has a number of teeth, and the speed of any gear relative to its neighbor is proportional to the ratio of teeth. Concretely, if a gear with $y$ teeth drives a gear with $x$ teeth spinning at speed $z$, the next gear spins at $z \cdot y / x$. We are given multiple test cases, each with up to 100 gears, and the teeth counts are between 2 and 100.

The problem reduces to arranging the integers $a_1, \dots, a_n$ such that the product of successive ratios along the line equals 1. Writing this product explicitly, if the arranged sequence is $b_1, b_2, \dots, b_n$, the final gear speed is

$$1 \cdot \frac{b_1}{b_2} \cdot \frac{b_2}{b_3} \cdots \frac{b_{n-1}}{b_n} = \frac{b_1}{b_n}.$$

So the rightmost gear spins at speed 1 if and only if the first and last gears have the same number of teeth. This is the key simplification: all the intermediate gears cancel out.

Given this, the problem is equivalent to checking whether there exists a gear count that can be placed at both ends of the sequence.

Edge cases include when all gears have the same number of teeth, which is trivially "YES", or when no number appears at least twice, which is "NO". For example, if the gears are `[2, 3]`, neither arrangement satisfies the requirement.

The constraints are small enough to allow simple counting: with $n$ up to 100 and $t$ up to 1000, an $O(n^2)$ brute-force approach is feasible, but counting occurrences is $O(n)$ per test case and much cleaner.

## Approaches

A brute-force approach would attempt all permutations of the gears and simulate the spinning of each. For $n = 100$, there are $100!$ permutations, which is astronomically large and infeasible. Even simulating the ratios for each permutation is unnecessary because the final speed only depends on the first and last gears.

The key observation is that the ratios telescope: the product of successive $\frac{y}{x}$ simplifies to $\frac{b_1}{b_n}$. This reduces the problem from simulating gear motion to a simple check of whether the first and last gears can be equal. Therefore, the optimal solution is to check if any teeth count appears at least twice in the input. If it does, we can place it at both ends and arrange the remaining gears arbitrarily in the middle. If not, there is no arrangement that will satisfy the requirement.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (simulate all permutations) | O(n!) | O(n) | Too slow |
| Count occurrences, check duplicates | O(n) per test case | O(100) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases $t$. Each test case will be handled independently.
2. For each test case, read the number of gears $n$ and their teeth counts in a list $a$.
3. Count the occurrences of each teeth count using a dictionary or array. This will allow us to know which numbers appear multiple times.
4. Check if any count is at least 2. If such a count exists, print "YES". Otherwise, print "NO".
5. Continue to the next test case until all are processed.

Why it works: The speed of the rightmost gear only depends on the first and last gears in the arrangement because the intermediate ratios cancel out. Placing a repeated gear at both ends guarantees that the ratio product equals 1, satisfying the condition. No other arrangement is necessary, and the check is sufficient and necessary.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n = int(input())
    gears = list(map(int, input().split()))
    counts = {}
    found = False
    for x in gears:
        counts[x] = counts.get(x, 0) + 1
        if counts[x] >= 2:
            found = True
            break
    print("YES" if found else "NO")
```

The solution reads each test case, counts occurrences of each teeth number using a dictionary, and breaks early if any number appears twice. The early break ensures we do not unnecessarily process the remaining numbers once a solution is found. We use `dict.get` to simplify incrementing counts without needing a conditional check.

## Worked Examples

Sample input `[2, 5, 5]`:

| Gear | Counts | Found >=2? |
| --- | --- | --- |
| 5 | {5:1} | No |
| 5 | {5:2} | Yes |

The algorithm prints "YES".

Input `[2, 2, 3]`:

| Gear | Counts | Found >=2? |
| --- | --- | --- |
| 2 | {2:1} | No |
| 3 | {2:1, 3:1} | No |

No number appears twice, so the algorithm prints "NO".

These traces show that the algorithm correctly identifies whether a duplicate exists to place at both ends.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Counting occurrences of each gear is linear in the number of gears. |
| Space | O(100) | The maximum distinct teeth counts is 99 (2-100), so the dictionary is bounded. |

With $t \le 1000$ and $n \le 100$, this results in at most 100,000 operations, well within the 1-second limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = []
    t = int(input())
    for _ in range(t):
        n = int(input())
        gears = list(map(int, input().split()))
        counts = {}
        found = False
        for x in gears:
            counts[x] = counts.get(x, 0) + 1
            if counts[x] >= 2:
                found = True
                break
        output.append("YES" if found else "NO")
    return "\n".join(output)

# provided samples
assert run("5\n2\n5 5\n4\n6 3 6 9\n2\n2 3\n7\n30 10 12 10 10 9 18\n5\n2 4 8 16 32\n") == "YES\nYES\nNO\nYES\nNO", "sample 1"

# custom cases
assert run("1\n2\n2 2\n") == "YES", "all equal"
assert run("1\n3\n2 3 4\n") == "NO", "all distinct, small n"
assert run("1\n4\n3 3 4 5\n") == "YES", "one duplicate in middle"
assert run("1\n100\n" + " ".join(str(i) for i in range(2, 102)) + "\n") == "NO", "large n, all distinct"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `[2,2]` | YES | minimum size, all equal |
| `[2,3,4]` | NO | small n, all distinct |
| `[3,3,4,5]` | YES | one duplicate not at ends |
| `[2..101]` | NO | large n, all distinct |

## Edge Cases

The algorithm handles the case where all gears are identical by counting and immediately finding a duplicate. For example, `[5, 5, 5]` yields "YES" because 5 appears three times. When all gears are distinct, such as `[2, 3, 4]`, the dictionary counts show no duplicates, and the algorithm outputs "NO". The maximum-size input with 100 distinct values still produces "NO" efficiently because the counting dictionary remains small and the early break is never triggered.
