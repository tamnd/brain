---
title: "CF 104385A - Drill Wood to Make Fire"
description: "We are given a very small simulation repeated multiple times. Each test case describes a scenario where a person is trying to generate fire by drilling wood."
date: "2026-07-01T02:51:45+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104385
codeforces_index: "A"
codeforces_contest_name: "2023 (ICPC) Jiangxi Provincial Contest -- Official Contest"
rating: 0
weight: 104385
solve_time_s: 40
verified: true
draft: false
---

[CF 104385A - Drill Wood to Make Fire](https://codeforces.com/problemset/problem/104385/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 40s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a very small simulation repeated multiple times. Each test case describes a scenario where a person is trying to generate fire by drilling wood. The success of the attempt depends only on three integers: a required threshold value, and two parameters representing how strong the action is and how fast it is performed.

For each test case, we are given a threshold value $N$, a strength $S$, and a speed $V$. The process succeeds if the combined “effectiveness” of drilling, modeled as the product $S \times V$, reaches or exceeds $N$. If the product is large enough, the wood ignites, otherwise it does not.

So each query is independent, and the output is a sequence of binary decisions: print 1 if $S \cdot V \ge N$, otherwise print 0.

The constraints are extremely small: $T \le 100$ and all values are at most 100. This immediately implies that even the most naive computation is trivial in terms of performance. Multiplying two integers per test case is constant work, so even a straightforward loop is sufficient.

The only subtle pitfall comes from interpreting the condition correctly. A common mistake would be to compare $S + V$ against $N$, or to require strict inequality instead of allowing equality. Another possible mistake is overflow in languages with fixed-width integers, but in Python this is irrelevant. A third subtle issue is forgetting that each test case is independent and accidentally carrying state between cases, though this problem does not naturally introduce state.

## Approaches

The brute-force interpretation is direct: for each test case, compute the product $S \times V$ and compare it against $N$. This is already optimal because there is no structure linking test cases and no preprocessing that helps reduce computation further. Each decision depends only on three numbers, so any algorithm must at least read them and perform one multiplication.

The brute-force approach runs in $O(T)$, since each test case requires constant time work. Even if we imagined more complex logic, the input size caps everything so tightly that no optimization beyond direct evaluation is meaningful.

The key observation is that the problem is not about searching or optimization across multiple inputs. It is purely a threshold comparison on a single derived value. Once this is recognized, the solution collapses into a single arithmetic check.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(T) | O(1) | Accepted |
| Optimal | O(T) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases $T$. This determines how many independent checks we will perform.
2. For each test case, read three integers $N$, $S$, and $V$. These fully define the scenario.
3. Compute the product $P = S \times V$. This represents the effective drilling power.
4. Compare $P$ with $N$. If $P \ge N$, output 1 because the ignition threshold is met or exceeded.
5. Otherwise output 0, since the drilling is insufficient to ignite the wood.

### Why it works

Each test case reduces to a single inequality involving only $S$, $V$, and $N$. There are no hidden interactions or sequential effects between cases. The algorithm directly evaluates the defining condition of success, so it exactly matches the problem’s success criterion. Since multiplication and comparison are exact and deterministic operations, the decision is always correct.

## Python Solution

```python
import sys
input = sys.stdin.readline

def main():
    t = int(input())
    out = []
    for _ in range(t):
        n, s, v = map(int, input().split())
        out.append("1" if s * v >= n else "0")
    print("\n".join(out))

if __name__ == "__main__":
    main()
```

The solution reads input efficiently using `sys.stdin.readline` to handle multiple test cases cleanly. Each test case is processed independently inside a loop.

The key computation happens in a single line: `s * v >= n`. This encodes both the multiplication and threshold comparison. The result is stored as a string because output formatting requires one value per line.

Using a list to collect outputs avoids repeated I/O calls inside the loop, which is a standard competitive programming practice even though the constraints here would not strictly require it.

## Worked Examples

Consider the input:

```
3
10 2 5
12 3 3
20 4 4
```

We track each test case:

| N | S | V | S×V | Output |
| --- | --- | --- | --- | --- |
| 10 | 2 | 5 | 10 | 1 |
| 12 | 3 | 3 | 9 | 0 |
| 20 | 4 | 4 | 16 | 0 |

The first case succeeds exactly at the threshold, confirming that equality is accepted. The second and third cases fail because the product does not reach the required value. This shows that the algorithm is strictly driven by a threshold comparison, not relative magnitude.

A second example:

```
4
1 1 1
5 2 3
6 2 3
7 3 3
```

| N | S | V | S×V | Output |
| --- | --- | --- | --- | --- |
| 1 | 1 | 1 | 1 | 1 |
| 5 | 2 | 3 | 6 | 1 |
| 6 | 2 | 3 | 6 | 1 |
| 7 | 3 | 3 | 9 | 1 |

This demonstrates multiple boundary conditions, especially repeated equality at $N = 6$, where the condition still holds.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(T) | Each test case requires one multiplication and one comparison |
| Space | O(1) | Only a few integer variables are stored at any time |

The input bounds ensure that even $T = 100$ is trivial. The algorithm performs at most 100 constant-time operations, which is far below any practical limit.

## Test Cases

```python
import sys, io

def solve():
    import sys
    input = sys.stdin.readline
    t = int(input())
    out = []
    for _ in range(t):
        n, s, v = map(int, input().split())
        out.append("1" if s * v >= n else "0")
    return "\n".join(out)

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return solve()

# provided sample-style tests
assert run("3\n10 2 5\n12 3 3\n20 4 4\n") == "1\n0\n0"

# minimum values
assert run("1\n1 1 1\n") == "1"

# just below threshold
assert run("1\n10 2 4\n") == "0"

# all equal values
assert run("3\n5 2 3\n5 2 3\n5 2 3\n") == "1\n1\n1"

# boundary equality cases
assert run("2\n6 2 3\n7 2 3\n") == "1\n0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 1 | 1 | minimum valid input |
| 10 2 4 | 0 | strict failure just below threshold |
| repeated identical cases | all 1 | consistency across tests |
| equality boundary | 1 then 0 | correctness of ≥ condition |

## Edge Cases

A key edge case is when the product is exactly equal to the threshold. For example, input:

```
1
6 2 3
```

Here $S \times V = 6$, which equals $N$. The algorithm computes the product as 6, compares it to 6, and outputs 1. This confirms that the condition is inclusive, not strict.

Another case is when the product is just one less than required:

```
1
7 2 3
```

The product is 6, which is less than 7, so the output is 0. The algorithm does not attempt any rounding or approximation, it directly evaluates the integer product.

Since all computations are small integers, there are no overflow or precision issues, and every case reduces cleanly to a deterministic comparison.
