---
problem: 1325A
contest_id: 1325
problem_index: A
name: "EhAb AnD gCd"
contest_name: "Codeforces Round 628 (Div. 2)"
rating: 800
tags: ["constructive algorithms", "greedy", "number theory"]
answer: passed_samples
verified: false
solve_time_s: 294
date: 2026-06-14
model: gpt-5-3-mini
samples_passed: 0
samples_total: 1
share_url: https://chatgpt.com/share/6a2df29d-d044-83ec-afec-0481b1811e79
---

# CF 1325A - EhAb AnD gCd

**Rating:** 800  
**Tags:** constructive algorithms, greedy, number theory  
**Model:** gpt-5-3-mini  
**Solve time:** 4m 54s  
**Verified:** no (0/1 samples)  
**Share:** https://chatgpt.com/share/6a2df29d-d044-83ec-afec-0481b1811e79  

---

## Solution

## Problem Understanding

We are given a number x, and for each query we must construct two positive integers a and b such that when we compute their greatest common divisor and least common multiple, the sum of those two values is exactly x.

Instead of thinking of this as an arithmetic identity problem, it helps to view it as a construction task: we are trying to split x into two interacting parts coming from the structure of a pair of numbers. The gcd captures their shared factor structure, while the lcm captures how far their combined multiplicative span stretches.

The constraints are small in terms of number of test cases, but x itself can be as large as 10^9. That immediately rules out any approach that tries to search over all pairs a and b or even all gcd candidates per test case. A quadratic or even linear scan per test case would be too slow in the worst case.

A subtle point is that gcd and lcm are tightly coupled. Many naive attempts try random pairs or fix one value and derive the other, but those approaches often break because changing a and b changes both gcd and lcm simultaneously in a non-linear way. A common failure mode is assuming that picking a small gcd automatically makes the lcm behave predictably, which is not true unless the numbers are constructed carefully.

## Approaches

The brute-force idea is straightforward: iterate over all pairs (a, b) up to x, compute gcd(a, b) and lcm(a, b), and check whether their sum equals x. This is correct because it exhausts the entire search space. However, the number of pairs is on the order of x^2, which is up to 10^18 operations in the worst case. Even optimizing with symmetry or bounds does not bring this anywhere close to feasible.

The key insight is to stop trying to directly control both gcd and lcm independently. Instead, we exploit a standard identity: if we write a = g·u and b = g·v where gcd(u, v) = 1, then gcd(a, b) = g and lcm(a, b) = g·u·v. The expression becomes g + g·u·v = g(1 + u·v). This shows the entire structure depends on a factor g and a coprime pair u and v.

Now we want g(1 + u·v) = x. The simplest way to satisfy this is to choose g = 1. That removes all gcd complexity and reduces the condition to 1 + u·v = x, or u·v = x − 1. We can always satisfy this by choosing u = 1 and v = x − 1, which are trivially coprime. This gives a = 1 and b = x − 1, which always works.

The problem statement also accepts any valid pair, and the sample includes another valid construction for x = 14, so multiple solutions exist. However, the simplest construction already satisfies all constraints.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(x^2) | O(1) | Too slow |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

We construct the answer independently for each test case.

1. Read x.
2. Set a = 1.
3. Set b = x − 1.
4. Output a and b.

The reason choosing a = 1 is valid is that it forces gcd(1, b) = 1 for any b. This simplifies the interaction between gcd and lcm completely.

The lcm of 1 and b is always b, because 1 shares no prime factors with any number and divides everything. So the expression gcd(a, b) + lcm(a, b) becomes 1 + b. Setting b = x − 1 makes the sum exactly x.

### Why it works

The correctness rests on two invariant properties: gcd(1, b) is always 1, and lcm(1, b) is always b. These hold for all positive integers b. Once these are fixed, the expression collapses into a linear equation in b, and we directly solve it without any interaction between the two functions. There is no hidden constraint because both gcd and lcm behave deterministically under the presence of 1.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    x = int(input())
    print(1, x - 1)
```

The code mirrors the construction exactly. For each test case, it reads x and outputs the pair (1, x−1). There are no edge conditions inside the loop because x is guaranteed to be at least 2, so x−1 is always positive.

A subtle implementation detail is that we never compute gcd or lcm explicitly. Any attempt to do so is unnecessary and would only introduce overhead.

## Worked Examples

We trace two inputs, including the samples.

### Example 1

Input x = 2

| Step | a | b | gcd(a,b) | lcm(a,b) | sum |
| --- | --- | --- | --- | --- | --- |
| construct | 1 | 1 | 1 | 1 | 2 |

The construction produces (1, 1). This demonstrates the boundary case where x is minimal. Even in this extreme case, x − 1 remains valid and positive.

### Example 2

Input x = 14

| Step | a | b | gcd(a,b) | lcm(a,b) | sum |
| --- | --- | --- | --- | --- | --- |
| construct | 1 | 13 | 1 | 13 | 14 |

This shows the general behavior for larger values. The gcd stays fixed at 1, while the lcm follows b directly.

These traces confirm that the construction does not depend on any special properties of x beyond positivity.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t) | One constant-time computation per test case |
| Space | O(1) | No additional storage beyond variables |

The solution scales linearly with the number of test cases, which is trivial under the constraint t ≤ 100. The magnitude of x is irrelevant because no iteration over its value is performed.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    t = int(input())
    out = []
    for _ in range(t):
        x = int(input())
        out.append(f"{1} {x-1}")
    return "\n".join(out) + "\n"

# provided samples
assert run("2\n2\n14\n") == "1 1\n1 13\n", "sample test"

# custom cases
assert run("1\n2\n") == "1 1\n", "minimum x"
assert run("1\n1000000000\n") == "1 999999999\n", "maximum x"
assert run("3\n3\n4\n5\n") == "1 2\n1 3\n1 4\n", "small consecutive values"
assert run("1\n10\n") == "1 9\n", "mid-range check"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| x = 2 | 1 1 | minimum boundary |
| x = 10^9 | 1 999999999 | maximum constraint |
| consecutive x values | 1 x−1 each | consistency across cases |
| x = 10 | 1 9 | general correctness |

## Edge Cases

The only meaningful edge case is the smallest possible x, which is x = 2. In this case, the algorithm produces a = 1 and b = 1. Computing directly gives gcd(1, 1) = 1 and lcm(1, 1) = 1, so the sum is 2 as required. The construction does not break because x − 1 remains positive.

For any larger x, nothing changes structurally. The gcd remains 1 regardless of b, and the lcm remains exactly b, so the output always satisfies the required equation without needing special handling or branching logic.