---
problem: 1324B
contest_id: 1324
problem_index: B
name: "Yet Another Palindrome Problem"
contest_name: "Codeforces Round 627 (Div. 3)"
rating: 1100
tags: ["brute force", "strings"]
answer: passed_samples
verified: true
solve_time_s: 181
date: 2026-06-14
model: gpt-5-3-mini
samples_passed: 1
samples_total: 1
share_url: https://chatgpt.com/share/6a2df146-8624-83ec-aa29-eb24bce32801
---

# CF 1324B - Yet Another Palindrome Problem

**Rating:** 1100  
**Tags:** brute force, strings  
**Model:** gpt-5-3-mini  
**Solve time:** 3m 1s  
**Verified:** yes (1/1 samples)  
**Share:** https://chatgpt.com/share/6a2df146-8624-83ec-aa29-eb24bce32801  

---

## Solution

## Problem Understanding

We are given several independent arrays of integers, and for each one we need to decide whether we can extract a subsequence of length at least three that reads the same from left to right and right to left.

A subsequence here means we are allowed to delete elements but we cannot reorder what remains. So the task is not about contiguous segments, but about choosing a few elements while preserving their original order. Among all such choices, we want to know whether at least one palindrome of length three or more exists.

The constraints are small in a global sense. Each test case has up to 5000 elements total across all cases. This immediately suggests that an $O(n^2)$ solution per test case is fine, but anything cubic or worse over all tests would be risky if implemented carelessly. However, the real breakthrough comes from realizing that we do not need to construct subsequences explicitly.

A naive mindset would try to generate all subsequences of length at least three and check whether any is a palindrome. That is impossible because even for $n = 50$, the number of subsequences is exponential. Another naive attempt would be to check all triples or all triples with gaps, but that misses longer palindromes.

There are also subtle cases that break greedy intuition. For example, in an array like $[1, 2, 3, 2, 1]$, the answer is clearly yes, but focusing only on adjacent duplicates or simple symmetry patterns would fail because the matching elements are separated.

The key hidden structure is that any valid palindrome subsequence of length at least three must contain either a repeated value forming the ends, or a pattern reducible to a simpler condition involving duplicates.

## Approaches

We start from the brute-force perspective. A subsequence palindrome of length at least three has a first and last element equal, and a middle part that is itself a palindrome. A direct approach would be to enumerate all subsequences, build each one, and check if it is a palindrome. This is exponential in $n$, roughly $O(2^n \cdot n)$, which is completely infeasible even for $n = 30$.

We can reduce the problem significantly by focusing on structure instead of construction. A palindrome subsequence of length at least three must fall into one of two patterns.

Either we have a value that appears at least three times, allowing us to pick it as the first and last element and also as the middle element, forming a subsequence like $[x, x, x]$, or we can form a longer symmetric structure using two different values where the outer pair matches and something exists between them.

The key observation is that if we ever have a value appearing at least three times, the answer is immediately yes. If not, every value appears at most twice, and the structure becomes constrained enough that we only need to check whether there exists a value that appears twice with at least one element in between its first and last occurrence. That gives a palindrome subsequence of the form $[x, y, x]$ where $x$ appears twice and $y$ lies between them.

This reduces the entire problem to frequency and positional checks, avoiding any subsequence enumeration.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force subsequences | $O(2^n \cdot n)$ | $O(n)$ | Too slow |
| Frequency + position check | $O(n)$ per test | $O(n)$ | Accepted |

## Algorithm Walkthrough

We process each test case independently.

1. We scan the array and store the positions of each value. This lets us reason about duplicates and spacing.
2. If any value appears at least three times, we immediately return "YES". This works because we can pick the first, second, and third occurrence to form a palindrome subsequence of length three.
3. If no value appears three times, we only have values appearing once or twice.
4. For every value that appears exactly twice, we check whether the two occurrences are not adjacent. If there is at least one index between them, we can pick those two equal elements as the ends of a subsequence.
5. We then check if there exists any element in between that we can use as the middle of the palindrome. Since any element works as a middle, the condition is simply that the two occurrences are separated by at least one index.
6. If any such pair exists, we return "YES".
7. If neither condition holds, we return "NO".

The key step is recognizing that once duplicates exist with separation, any intermediate element can serve as the center, guaranteeing a length-three palindrome subsequence.

### Why it works

Any palindrome subsequence of length at least three must have its first and last elements equal. So we are always looking for a repeated value that can serve as endpoints. If a value appears three or more times, we can trivially build a valid palindrome. If it appears exactly twice, those two occurrences define the only possible endpoints for that value. A valid middle element exists automatically because we are allowed to pick any element between them while preserving order. This structural restriction exhausts all possible constructions, so checking frequencies and gaps fully characterizes the answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))

        pos = {}
        for i, x in enumerate(a):
            pos.setdefault(x, []).append(i)

        ok = False

        for x, idxs in pos.items():
            if len(idxs) >= 3:
                ok = True
                break

        if ok:
            print("YES")
            continue

        for x, idxs in pos.items():
            if len(idxs) == 2:
                i, j = idxs
                if j - i > 1:
                    ok = True
                    break

        print("YES" if ok else "NO")

if __name__ == "__main__":
    solve()
```

The code first collects positions of each value so we can reason about repetition patterns. The first loop detects the trivial case of three occurrences of the same value. The second loop handles the case where exactly two occurrences exist and ensures they are not adjacent. The condition `j - i > 1` guarantees there is at least one element between them, which allows forming a length-three palindrome subsequence.

## Worked Examples

### Example 1

Input:

```
5
3
1 2 1
```

We track occurrences: 1 appears at positions [0, 2], 2 at [1]. No value appears three times. The value 1 appears twice and the gap between positions 0 and 2 is non-empty, so we can pick subsequence [1, 2, 1]. This confirms a valid palindrome.

| Value | Positions | Triple count | Gap check | Decision |
| --- | --- | --- | --- | --- |
| 1 | [0, 2] | 2 | gap exists | YES |

This shows how a single middle element enables a valid palindrome subsequence.

### Example 2

Input:

```
5
1 2 3 4 5
```

Every value appears once, so no repeated endpoints exist. Without repeated endpoints, no palindrome subsequence of length at least three can be formed.

| Value | Positions | Frequency | Decision |
| --- | --- | --- | --- |
| 1 | [0] | 1 | NO |
| 2 | [1] | 1 | NO |
| 3 | [2] | 1 | NO |
| 4 | [3] | 1 | NO |
| 5 | [4] | 1 | NO |

This confirms that repetition is necessary for any valid construction.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ per test | Each array is scanned once to build positions and then checked once |
| Space | $O(n)$ | Storage of index lists for each distinct value |

The total $n$ across all test cases is at most 5000, so this linear solution is easily fast enough under the constraints.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    t = int(input())
    out = []
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))

        pos = {}
        for i, x in enumerate(a):
            pos.setdefault(x, []).append(i)

        ok = False

        for x, idxs in pos.items():
            if len(idxs) >= 3:
                ok = True
                break

        if not ok:
            for x, idxs in pos.items():
                if len(idxs) == 2 and idxs[1] - idxs[0] > 1:
                    ok = True
                    break

        out.append("YES" if ok else "NO")

    return "\n".join(out)

# provided samples
assert run("""5
3
1 2 1
5
1 2 2 3 2
3
1 1 2
4
1 2 2 1
10
1 1 2 2 3 3 4 4 5 5
""") == """YES
YES
NO
YES
NO"""

# all equal
assert run("""1
5
7 7 7 7 7
""") == "YES"

# no repeats
assert run("""1
4
1 2 3 4
""") == "NO"

# separated pair
assert run("""1
4
1 2 1 3
""") == "YES"

# adjacent duplicates only
assert run("""1
4
1 1 2 3
""") == "NO"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all equal | YES | triple repetition shortcut |
| no repeats | NO | impossibility without duplicates |
| separated pair | YES | non-adjacent duplicate case |
| adjacent duplicates | NO | adjacency breaks length-3 construction |

## Edge Cases

One important edge case is when a value appears exactly twice but the occurrences are adjacent. For example, in `[1, 1, 2]`, there is no space to place a middle element between the two 1s, so no length-3 palindrome subsequence can be formed using that value.

Another case is when multiple values appear twice but all occurrences are adjacent pairs. For example `[1, 1, 2, 2, 3, 3]` has many duplicates, but none of them provide a gap, so the answer is still no. The algorithm correctly rejects this because every pair fails the separation condition.

A third case is when a value appears three times but is scattered, such as `[1, 2, 1, 3, 1]`. Even though the occurrences are not consecutive, selecting the first, third, and fifth occurrences still forms a valid palindrome subsequence, so the algorithm correctly accepts immediately on frequency alone.