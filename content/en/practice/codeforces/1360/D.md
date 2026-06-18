---
problem: 1360D
contest_id: 1360
problem_index: D
name: "Buying Shovels"
contest_name: "Codeforces Round 644 (Div. 3)"
rating: 1300
tags: ["math", "number theory"]
answer: passed_samples
verified: true
solve_time_s: 307
date: 2026-06-14
model: gpt-5-3-mini
samples_passed: 1
samples_total: 1
share_url: https://chatgpt.com/share/6a2e3e41-0410-83ec-a5d4-0c1d78bc83af
---

# CF 1360D - Buying Shovels

**Rating:** 1300  
**Tags:** math, number theory  
**Model:** gpt-5-3-mini  
**Solve time:** 5m 7s  
**Verified:** yes (1/1 samples)  
**Share:** https://chatgpt.com/share/6a2e3e41-0410-83ec-a5d4-0c1d78bc83af  

---

## Solution

## Problem Understanding

Polycarp wants to obtain exactly $n$ shovels, but he cannot mix different package sizes. The shop offers packages of size $1$ through $k$, and once he chooses a package size $i$, every purchase must be that same size. The task is to choose the best package size and then buy as few packages as possible so that the total number of shovels is exactly $n$.

In other words, for each valid package size $i$, we are allowed to represent $n$ as a sum of identical terms $i + i + \dots + i$. This is only possible if $i$ divides $n$, and in that case the number of packages is $n / i$. The goal is to minimize this value over all $i \le k$ that divide $n$.

The constraints allow up to $10^9$ for both $n$ and $k$, with up to 100 test cases. This rules out any approach that iterates over all package sizes up to $k$ per test case, since that would require up to $10^11$ operations in the worst case.

A naive mistake comes from trying all $i$ from $1$ to $k$. For example, if $n = 10^9$ and $k = 10^9$, iterating over all candidates is impossible in time limits.

Another subtle edge case appears when $k \ge n$. In that situation, choosing $i = n$ is allowed and gives answer $1$. A careless approach that only checks divisors of $n$ but ignores the upper bound constraint may miss this shortcut.

## Approaches

The brute-force idea is straightforward: try every package size $i$ from $1$ to $k$, check whether $i$ divides $n$, and compute $n / i$. The answer is the minimum among all valid choices. This is correct because it explicitly evaluates every allowed configuration.

However, this approach performs $O(k)$ checks per test case. With $k$ up to $10^9$, this becomes infeasible even for a single test case.

The key observation is that we do not need to search all values of $i$. The best answer corresponds to making $i$ as large as possible while still dividing $n$, since the answer is $n / i$. Therefore, we want the largest divisor of $n$ that does not exceed $k$.

If $k \ge n$, we can directly pick $i = n$, giving answer $1$. Otherwise, we restrict ourselves to divisors of $n$ that are at most $k$. The largest such divisor is either a large divisor found near $\sqrt{n}$ or a divisor paired with a small complement.

We can iterate over all divisors of $n$ up to $\sqrt{n}$, which is efficient because any divisor pair $(d, n/d)$ contains one small and one large value. We track the largest valid divisor not exceeding $k$, and compute $n$ divided by it.

This reduces the problem from scanning all candidates up to $k$ to scanning only up to $\sqrt{n}$.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(k)$ per test | $O(1)$ | Too slow |
| Optimal | $O(\sqrt{n})$ per test | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. If $k \ge n$, immediately return $1$, because choosing package size $n$ is valid and uses a single package. This is the global minimum possible answer.
2. Otherwise, initialize the answer as $n$, corresponding to the worst valid choice $i = 1$.
3. Iterate over all integers $d$ from $1$ to $\lfloor \sqrt{n} \rfloor$. Each $d$ represents a potential divisor candidate.
4. If $d$ divides $n$, consider both $d$ and $n / d$ as valid package sizes.
5. For each valid divisor candidate $i$, check if $i \le k$. If so, update the answer as $\min(\text{answer}, n / i)$. This step is justified because choosing package size $i$ leads to exactly $n / i$ packages.
6. After checking all divisor pairs, output the best answer found.

### Why it works

Every valid solution corresponds to choosing a divisor $i$ of $n$ with $i \le k$. The algorithm enumerates all divisors of $n$, so it never misses any feasible choice. For each candidate, it computes the exact number of packages required. Since the objective is minimizing $n / i$, maximizing $i$ under the constraint $i \mid n$ and $i \le k$, the best candidate is guaranteed to be among the enumerated divisors. This ensures correctness without needing to scan non-divisors or values above $\sqrt{n}$.

## Python Solution

```python
import sys
input = sys.stdin.readline
import math

def solve():
    t = int(input())
    for _ in range(t):
        n, k = map(int, input().split())

        if k >= n:
            print(1)
            continue

        ans = n

        r = int(math.isqrt(n))
        for d in range(1, r + 1):
            if n % d == 0:
                if d <= k:
                    ans = min(ans, n // d)
                other = n // d
                if other <= k:
                    ans = min(ans, n // other)

        print(ans)

if __name__ == "__main__":
    solve()
```

The solution first handles the trivial optimal case where a single package is possible. The divisor loop ensures all candidate package sizes are checked without exceeding $\sqrt{n}$ complexity. Each divisor pair is processed carefully, checking both elements because only one may be within the limit $k$.

A common implementation pitfall is forgetting to check both $d$ and $n/d$, which would miss valid large divisors. Another is not handling the $k \ge n$ shortcut, which otherwise still works but may waste time or complicate logic unnecessarily.

## Worked Examples

### Example 1: $n = 8, k = 7$

We check divisors of 8.

| d | d divides n | d ≤ k | n/d | n/d ≤ k | best ans |
| --- | --- | --- | --- | --- | --- |
| 1 | yes | yes | 8 | yes | 1 |
| 2 | yes | yes | 4 | yes | 1 |
| 3 | no | - | - | - | 1 |
| 4 | yes | yes | 2 | yes | 1 |

The algorithm finds that package size 4 gives $8 / 4 = 2$, which is optimal among valid options. The table confirms that multiple valid divisors exist, but the smallest number of packages comes from the largest valid divisor.

### Example 2: $n = 6, k = 10$

Since $k \ge n$, we immediately return 1.

| Step | Condition | Action |
| --- | --- | --- |
| Check k ≥ n | 10 ≥ 6 | return 1 |

This demonstrates the shortcut case where the optimal package size is the whole $n$.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(t \sqrt{n})$ | each test checks divisors up to $\sqrt{n}$ |
| Space | $O(1)$ | only constant variables used |

With $t \le 100$ and $n \le 10^9$, $\sqrt{n}$ is about $3 \times 10^4$, so the total operations stay comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output

    import math

    t = int(input())
    for _ in range(t):
        n, k = map(int, input().split())

        if k >= n:
            print(1)
            continue

        ans = n
        r = int(math.isqrt(n))
        for d in range(1, r + 1):
            if n % d == 0:
                if d <= k:
                    ans = min(ans, n // d)
                other = n // d
                if other <= k:
                    ans = min(ans, n // other)

        print(ans)

    return output.getvalue()

# provided samples
assert run("5\n8 7\n8 1\n6 10\n999999733 999999732\n999999733 999999733\n") == "2\n8\n1\n999999733\n1\n"

# custom cases
assert run("1\n1 1\n") == "1\n"
assert run("1\n10 3\n") == "5\n"
assert run("1\n12 12\n") == "1\n"
assert run("1\n100 7\n") == "4\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 1 | 1 | smallest boundary case |
| 10 3 | 5 | restricted divisor choice |
| 12 12 | 1 | k ≥ n shortcut |
| 100 7 | 4 | multiple divisor candidates |

## Edge Cases

When $n = 1$, the only possible package size is 1, so the answer is always 1 regardless of $k$. The algorithm immediately handles this because $k \ge n$ or because the divisor loop includes $d = 1$, producing answer $1 / 1 = 1$.

When $k \ge n$, such as $n = 50, k = 100$, the algorithm triggers the early return. This avoids unnecessary divisor computation and directly produces the optimal single-package solution.

When $n$ is prime and $k < n$, such as $n = 999999733, k = 10$, the only divisor not exceeding $k$ is 1. The loop finds no larger valid divisor, so the answer remains $n$, which corresponds to buying $n$ packages of size 1.