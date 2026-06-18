---
problem: 1269A
contest_id: 1269
problem_index: A
name: "Equation"
contest_name: "Codeforces Round 609 (Div. 2)"
rating: 800
tags: ["brute force", "math"]
answer: passed_samples
verified: true
solve_time_s: 300
date: 2026-06-14
model: gpt-5-3-mini
samples_passed: 1
samples_total: 1
share_url: https://chatgpt.com/share/6a2d8e9f-0c58-83ec-a117-80844521be00
---

# CF 1269A - Equation

**Rating:** 800  
**Tags:** brute force, math  
**Model:** gpt-5-3-mini  
**Solve time:** 5m  
**Verified:** yes (1/1 samples)  
**Share:** https://chatgpt.com/share/6a2d8e9f-0c58-83ec-a117-80844521be00  

---

## Solution

## Problem Understanding

We are asked to construct two composite integers, call them $a$ and $b$, such that their difference is exactly a given number $n$. Both numbers must be at least 2, and both must be composite, meaning each has at least one non-trivial divisor.

The output is not unique, so any valid pair is acceptable as long as it satisfies both the arithmetic constraint $a - b = n$ and the compositeness constraint for both numbers.

The constraint $n \le 10^7$ looks large enough that we should avoid any construction that depends on factoring or checking primality repeatedly up to $n$. However, the output bound is much larger, up to $10^9$, which gives us flexibility to build numbers using small fixed composite patterns.

A naive approach would be to try $b$ from 2 upward and set $a = b + n$, then check whether both are composite. This would work in principle, but in the worst case we might scan many candidates and repeatedly test primality. Even with a fast primality check, this is unnecessary because the structure of the problem guarantees a constant-time construction exists.

Edge cases are mostly about small values of $n$. For example, when $n = 1$, we must ensure both numbers are composite, so pairs like $9$ and $8$ work, but pairs like $3$ and $2$ fail since both are prime. Similarly, $n = 2$ or $n = 3$ require care because small offsets can easily land on primes if we are not systematic.

The key challenge is not finding a solution for large $n$, but ensuring a uniform construction that always produces composite numbers regardless of parity or size.

## Approaches

A brute-force strategy starts by fixing $b$ and checking whether both $b$ and $b + n$ are composite. Since $n$ can be up to $10^7$, and valid $a, b$ can be up to $10^9$, we could in principle try many values of $b$. For each candidate, we perform primality checks in roughly $O(\sqrt{x})$ time. Even if we only test a few thousand values, this is already unnecessary overhead given the existence of a constant construction.

The inefficiency comes from treating this as a search problem. The structure is simpler: we are not trying to optimize anything or search a sparse solution space, we just need any pair satisfying a linear relation and a weak number-theoretic property.

The key observation is that composite numbers are extremely dense among large integers, and we can deliberately construct them using small fixed composite building blocks. For example, $8 = 2 \cdot 2 \cdot 2$, $9 = 3 \cdot 3$, and $10 = 2 \cdot 5$. Once we have a small fixed composite anchor, we can shift it safely.

A standard construction is to choose a fixed composite $b$, then set $a = b + n$, and ensure $a$ is also composite by embedding a factorization pattern. The clean trick is to use numbers like $8$ and $9$, since they are composite and differ by 1. From there, shifting both by $n$ preserves the difference while keeping compositeness.

One robust pattern is:

choose $b = 8$, $a = 8 + n$. If $a$ is composite, we are done. If not, we adjust by using a slightly larger base like $b = 9$, since $9 + n$ will almost always be composite for valid constraints, and in worst-case small adjustments guarantee validity.

A more deterministic construction used in editorial solutions is:

set $b = 8$, $a = n + 8$, but if needed adjust by using $b = 9$, $a = n + 9$. At least one of these pairs will always yield both composite numbers due to the density of composite integers and the fact that we only need to avoid finitely many prime exceptions.

Thus the problem reduces to a constant-time construction.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(k \sqrt{n})$ | $O(1)$ | Too slow |
| Optimal | $O(1)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

We construct a valid pair directly without searching.

1. Fix a small composite base value, typically $b = 8$. This ensures $b$ is composite and stable across all inputs.
2. Set $a = b + n$. This guarantees the required difference $a - b = n$.
3. Check whether $a$ is composite. If it is, we can output $a, b$ immediately.
4. If $a$ is prime, adjust the construction by choosing another fixed composite base such as $b = 9$, and set $a = 9 + n$.
5. Output the resulting pair.

The key idea is that we only need to avoid the rare case where $b + n$ lands on a prime. Since we have at least two fixed composite anchors, and primes are sparse, one of these anchors will always produce a composite $a$ within constraints.

### Why it works

The correctness rests on two facts. First, the chosen base values are guaranteed composite. Second, for any $n \ge 1$, at least one of $n + 8$ or $n + 9$ is composite. This follows because consecutive integers cannot both be prime except for $2$ and $3$, and here both candidates are at least $9$ or larger, eliminating the only exceptional small region. Thus, at least one construction avoids primality on both ends, ensuring a valid pair always exists.

## Python Solution

```
PythonRun
```

The implementation directly encodes the constructive idea. We attempt two fixed composite anchors, 8 and 9, and for each we compute the corresponding $a$. A small primality check is used only to verify compositeness of $a$. We do not need to test $b$ because both 8 and 9 are known composite constants.

The loop is ordered so that we always find a valid solution in constant time. The square root check is safe because $a \le 10^9 + 9$, which is well within limits for a single check.

A common pitfall would be assuming a single base always works. The fallback ensures correctness without needing a more complex number theory argument.

## Worked Examples

### Example 1: $n = 1$

We try $b = 8$, so $a = 9$.

| step | b | a |
| --- | --- | --- |
| try 8 | 8 | 9 |

Here, 9 is composite and 8 is composite, so we output $9, 8$.

This confirms the simplest case where adjacent composites already satisfy the condition.

### Example 2: $n = 3$

Try $b = 8$, so $a = 11$, which is prime and invalid.

| step | b | a | valid |
| --- | --- | --- | --- |
| try 8 | 8 | 11 | no |
| try 9 | 9 | 12 | yes |

For $b = 9$, we get $a = 12$, which is composite. Both numbers are valid, so we output $12, 9$.

This demonstrates why the fallback is necessary: a single fixed base can fail for some $n$, but two nearby composite anchors guarantee success.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(\sqrt{n})$ worst-case (constant attempts) | At most two primality checks on numbers up to $10^7$ offset by constants |
| Space | $O(1)$ | Only a few integers are stored |

The computation is trivial under the constraints. Even the square root checks are negligible since they are executed at most twice.

## Test Cases

```
PythonRun
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 | 9 8 | smallest edge case |
| 2 | valid pair | minimal shift behavior |
| 3 | valid pair | fallback necessity |
| 10000000 | valid pair | large constraint stability |

## Edge Cases

For $n = 1$, the construction with $b = 8$ gives $a = 9$. Both numbers are composite, so the algorithm immediately succeeds without fallback.

For $n = 3$, $b = 8$ produces $a = 11$, which is prime, so the first attempt fails. The algorithm then tries $b = 9$, producing $a = 12$, which is composite. This demonstrates the role of multiple anchors in avoiding isolated prime collisions.

For large values like $n = 10^7$, $b = 8$ yields $a = 10000008$, which is divisible by 2, so it is composite. The algorithm terminates on the first attempt, showing that large inputs are actually easier than small pathological cases.