---
title: "CF 105404B - Dividing"
description: "We are given several independent test cases. Each test case provides a list of positive integers. The task is to determine whether there exists at least one element in the list that can divide every element in the same list, including itself in a trivial way."
date: "2026-06-23T04:48:40+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105404
codeforces_index: "B"
codeforces_contest_name: "XXIV Spain Olympiad in Informatics, Online Qualifier 2"
rating: 0
weight: 105404
solve_time_s: 80
verified: false
draft: false
---

[CF 105404B - Dividing](https://codeforces.com/problemset/problem/105404/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 20s  
**Verified:** no  

## Solution
## Problem Understanding

We are given several independent test cases. Each test case provides a list of positive integers. The task is to determine whether there exists at least one element in the list that can divide every element in the same list, including itself in a trivial way.

In more concrete terms, for each array, we are searching for an index $i$ such that for every $j$, the value $a_i$ divides $a_j$ without remainder. If such an element exists, we answer "SI", otherwise we answer "NO".

The input size forces us to think carefully about per-test-case efficiency. There can be up to 100 test cases, and each test case may contain up to 10,000 numbers. A naive approach that checks divisibility pairs for each candidate element against all others would require checking up to $n^2$ relationships per test case, which in the worst case reaches $10^8$ divisibility checks. That is still borderline but can pass in optimized Python only if carefully implemented, though it is unnecessary.

A more subtle constraint comes from the value range: each number is up to $10^9$. This rules out any frequency array or direct indexing approaches. The structure is purely arithmetic.

One edge case that often breaks naive reasoning is repeated values. For example, in an array like `[4, 2, 4, 6, 8, 4]`, the value 4 appears multiple times and is a valid candidate, even though it does not divide 2 or 6 in all positions unless we carefully check all elements. Another edge case is when the smallest number is not the answer. For example `[2, 3, 6]` has 2 as a candidate but fails because 3 is not divisible by 2.

A second subtle failure mode is assuming the minimum element always works. For `[2, 3, 4]`, the minimum is 2, but 2 does not divide 3, so the correct answer is "NO".

Finally, arrays with many equal elements are tricky. If all numbers are the same, the answer is always "SI", since any element divides all others.

## Approaches

The brute-force approach is straightforward. For each element in the array, treat it as a candidate divisor and check whether it divides every other element. This requires two nested loops: one to select the candidate and one to verify divisibility across the array. Each check is constant time, so the complexity per test case is $O(n^2)$. With $n = 10^4$, this leads to $10^8$ operations per test case, which becomes too slow across multiple test cases.

The key observation is that a valid candidate must divide every element, including the maximum element. This immediately implies that the candidate must be less than or equal to every element it divides, so it must be the smallest value in the array. However, being the minimum alone is not sufficient in general reasoning unless we explicitly test divisibility.

This reduces the search space dramatically. Instead of testing every element, we only need to test the smallest value in the array. If this value divides every element, it is a valid answer. Otherwise, no other element can work, because any larger candidate would fail to divide the minimum itself.

This turns the problem into a single scan to find the minimum, followed by a second scan to verify divisibility.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. For each test case, read the array of integers. This separates independent scenarios so no state carries over between them.
2. Scan the array once to find the smallest element. This candidate is chosen because any valid divisor must be small enough to divide all elements.
3. Traverse the array again and check whether every element is divisible by this candidate.
4. If any element fails the divisibility check, immediately conclude that no valid element exists for this test case.
5. If all elements pass the check, output "SI", otherwise output "NO".

### Why it works

If a number divides every element in the array, it must in particular divide the minimum element. Since no number smaller than the minimum exists in the array, the only possible candidate that can survive all constraints is the minimum value itself. Any larger number cannot divide the minimum, so it cannot be valid. This creates a strict uniqueness property: at most one candidate needs to be checked, and its validity fully determines the answer.

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

        m = min(arr)

        ok = True
        for x in arr:
            if x % m != 0:
                ok = False
                break

        out.append("SI" if ok else "NO")

    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The solution begins by reading all test cases and processing them independently. For each case, it computes the minimum value using a single pass.

The second loop checks divisibility of every element by this minimum. The early break is important because it avoids unnecessary work once a counterexample is found, improving performance in worst-case inputs where failure occurs early.

A subtle point is that we do not need to test whether the minimum divides itself, since `x % m` is always zero when `x == m`. This avoids redundant logic and keeps the check uniform across all elements.

## Worked Examples

### Example 1

Input:

```
2
10 18
```

We compute the minimum as 10.

| Step | Current element | Minimum (m) | Divisible? | Status |
| --- | --- | --- | --- | --- |
| 1 | 10 | 10 | yes | continue |
| 2 | 18 | 10 | no | fail |

Since 18 is not divisible by 10, the result is "NO".

This confirms that even though the minimum is a natural candidate, it does not always satisfy the condition.

### Example 2

Input:

```
4 2 4 6 8 4
```

Minimum is 2.

| Step | Current element | Minimum (m) | Divisible? | Status |
| --- | --- | --- | --- | --- |
| 1 | 4 | 2 | yes | continue |
| 2 | 2 | 2 | yes | continue |
| 3 | 4 | 2 | yes | continue |
| 4 | 6 | 2 | yes | continue |
| 5 | 8 | 2 | yes | continue |
| 6 | 4 | 2 | yes | continue |

All values are divisible by 2, so the output is "SI".

This demonstrates the case where the minimum element correctly serves as the universal divisor.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | One pass to find minimum and one pass to verify divisibility |
| Space | O(1) extra | Only a few variables besides input storage |

The total work scales linearly with the number of elements across all test cases. With up to 10,000 elements per test case and 100 test cases, the solution performs at most about one million operations, which is comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys as _sys
    from types import SimpleNamespace

    # inline solution
    input = sys.stdin.readline
    t = int(input())
    res = []
    for _ in range(t):
        n = int(input())
        arr = list(map(int, input().split()))
        m = min(arr)
        ok = True
        for x in arr:
            if x % m != 0:
                ok = False
                break
        res.append("SI" if ok else "NO")
    return "\n".join(res)

# provided samples
assert run("""4
2
10 18
6
2 7 3 7 8 7
6
4 6 1 3 4 1
6
4 2 4 6 8 4
""") == """NO
NO
SI
SI"""

# custom cases
assert run("""1
3
5 10 20
""") == "SI"

assert run("""1
3
3 6 10
""") == "NO"

assert run("""1
4
7 7 7 7
""") == "SI"

assert run("""1
5
2 3 4 5 6
""") == "NO"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 5 10 20 | SI | minimum is valid divisor |
| 3 6 10 | NO | partial divisibility failure |
| 7 7 7 7 | SI | all-equal case |
| 2 3 4 5 6 | NO | no valid divisor exists |

## Edge Cases

One important edge case is when all elements are identical. For an input like `[7, 7, 7, 7]`, the minimum is 7 and every element is divisible by 7. The algorithm scans once, confirms divisibility for all elements, and outputs "SI". This verifies that repeated values do not require any special handling.

Another case is when the minimum appears only once and still fails as a divisor, such as `[2, 3, 4, 6]`. The algorithm selects 2 as candidate, but immediately fails on 3 since `3 % 2 != 0`. The early termination prevents unnecessary checks.

A third case is when a larger number might seem plausible, but cannot be correct because it cannot divide the minimum. For `[4, 2, 4, 6, 8, 4]`, any candidate other than 2 or 4 is impossible. The algorithm correctly settles on 2 and validates it against the full array, producing "SI".
