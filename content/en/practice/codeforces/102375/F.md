---
title: "CF 102375F - \u041f\u0440\u0430\u0432\u0438\u043b\u044c\u043d\u044b\u0439 \u043f\u043e\u0434\u043c\u043d\u043e\u0433\u043e\u0443\u0433\u043e\u043b\u044c\u043d\u0438\u043a"
description: "We have a regular polygon with (N) vertices, and we want to keep as few of those vertices as possible while making the selected vertices themselves the vertices of another regular polygon. Suppose we choose (k) vertices."
date: "2026-08-15T07:04:17+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102375
codeforces_index: "F"
codeforces_contest_name: "\u041a\u0432\u0430\u043b\u0438\u0444\u0438\u043a\u0430\u0446\u0438\u043e\u043d\u043d\u044b\u0439 \u0440\u0430\u0443\u043d\u0434 \u0427\u0435\u043c\u043f\u0438\u043e\u043d\u0430\u0442\u0430 \u0421\u0435\u0432\u0435\u0440\u043e-\u0417\u0430\u043f\u0430\u0434\u0430 \u0420\u043e\u0441\u0441\u0438\u0438 \u0438 \u041c\u043e\u0441\u043a\u0432\u044b ICPC 2019"
rating: 0
weight: 102375
solve_time_s: 128
verified: false
draft: false
---

[CF 102375F - \u041f\u0440\u0430\u0432\u0438\u043b\u044c\u043d\u044b\u0439 \u043f\u043e\u0434\u043c\u043d\u043e\u0433\u043e\u0443\u0433\u043e\u043b\u044c\u043d\u0438\u043a](https://codeforces.com/problemset/problem/102375/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 8s  
**Verified:** no  

## Solution
## Problem Understanding

We have a regular polygon with (N) vertices, and we want to keep as few of those vertices as possible while making the selected vertices themselves the vertices of another regular polygon.

Suppose we choose (k) vertices. Since all original vertices lie on the same circle and are equally spaced by an angle of (2\pi/N), the selected vertices form a regular (k)-gon exactly when we can take every (N/k)-th original vertex. That is possible precisely when (k) divides (N).

So the problem reduces to finding the smallest divisor of (N) that is at least (3). If (N) is prime, there is no proper divisor at least (3), so the answer is (N) itself.

The value of (N) can reach (10^{12}). An algorithm that scans all possible polygon sizes up to (N) could perform almost (10^{12}) iterations, which is far beyond what is practical. We need to exploit the divisor structure of (N), rather than examine every possible number.

There are two small cases that easily expose mistakes. For (N=5), the answer is (5), because (5) is prime and there is no triangle or other smaller regular polygon among its vertices. For (N=8), the answer is (4), not (8), because every second vertex forms a square. A careless solution that only searches for odd divisors would miss (4). Another useful example is (N=10), where the answer is (5). The divisor (2) is too small to represent a polygon, so the first usable divisor is (5).

## Approaches

A direct approach is to try every possible number (k) of selected vertices, starting from (3), and test whether (k) divides (N). The first successful value is exactly the answer because a regular (k)-gon can be formed precisely for divisors (k) of (N). In the worst case, when (N) is prime, we test every value from (3) through (N), which is (N-2) divisibility checks. For (N=10^{12}-11), that is essentially one trillion iterations, so this approach is unusable.

The key observation is the standard divisor property that every composite number (N) has a divisor not exceeding (\sqrt N). Suppose the smallest usable divisor (d\ge3) is larger than (\sqrt N). Its complementary divisor (N/d) would then be smaller than (\sqrt N). Since (d) is at least (3), the complementary divisor is also a divisor of (N), and if it is at least (3), it would be an even smaller usable answer. The only possible complementary divisor below (3) is (1) or (2), and those cases mean that the relevant factor (d) is (N) or (N/2). In either situation, checking all divisors up to (\sqrt N) still gives us the answer when combined with the direct test of each candidate divisor.

In fact, we can simply test every integer (d) from (3) through (\lfloor\sqrt N\rfloor). The first divisor encountered is the answer. If no such divisor exists, (N) is prime, except for the possibility that the smallest divisor is (2). But (2) itself cannot be the answer, so we must keep searching for a usable divisor. A loop through all integers handles this naturally. For an even prime-like case such as (N=2p), the loop eventually reaches (p), provided (p\le\sqrt N), and if (p>\sqrt N), then (N) is actually handled by recognizing that its only proper divisor is (2), so the answer is (p=N/2). Thus the cleanest implementation explicitly handles the factor (2), then searches odd divisors.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(N)) | (O(1)) | Too slow |
| Optimal | (O(\sqrt N)) | (O(1)) | Accepted |

A slightly cleaner way to formulate the optimal search is to find the smallest divisor of (N) that is at least (3). We can first handle powers of (2) through the candidate (4), then search odd divisors. However, there is an even simpler implementation: test (d=3,4,5,\ldots) up to (\sqrt N), and if none divides (N), determine the remaining case from the factor (2). The implementation below uses this direct formulation.

## Algorithm Walkthrough

1. Read (N). We are looking for the smallest divisor of (N) that is at least (3).
2. If (N) is divisible by (4), immediately return (4). A square is the smallest possible polygon after a triangle, and divisibility by (4) means every (N/4)-th vertex forms one.
3. Starting from (d=3), test every integer (d) while (d^2\le N). If (d\mid N), return (d). Searching in increasing order guarantees that the first divisor found is the smallest possible answer.
4. If no divisor from (3) through (\sqrt N) exists, distinguish the remaining cases. If (N) is even, its only proper divisor that can be smaller than (\sqrt N) is (2), so (N=2p) for some odd prime (p), and the smallest usable divisor is (p=N/2). If (N) is odd, the absence of a divisor up to (\sqrt N) means that (N) is prime, so the answer is (N).

The reason the search only needs to reach (\sqrt N) is that divisors come in pairs (d) and (N/d). If a composite number has a divisor larger than (\sqrt N), its paired divisor is smaller than (\sqrt N). Thus a missing divisor below (\sqrt N) tells us exactly what the remaining factorization can look like.

### Why it works

Let (k) be the number of selected vertices. The selected vertices form a regular (k)-gon exactly when their positions around the original polygon are equally spaced. The spacing must be (N/k) original edges, so (N/k) must be an integer. Hence valid polygon sizes are exactly the divisors of (N) that are at least (3).

The algorithm examines these possible divisors in increasing order up to (\sqrt N). If it finds one, no smaller valid divisor can have been skipped. If none is found, every proper divisor smaller than (\sqrt N) is either (1) or (2). For odd (N), that means (N) is prime. For even (N), it means the only proper divisor is (2), so (N=2p), and (p=N/2) is the smallest divisor that can represent a polygon. The returned value is therefore always the minimum valid number of vertices.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())

    if n % 4 == 0:
        print(4)
        return

    d = 3
    while d * d <= n:
        if n % d == 0:
            print(d)
            return
        d += 2

    if n % 2 == 0:
        print(n // 2)
    else:
        print(n)

solve()
```

The first check for divisibility by (4) handles the smallest possible even polygon size. If (4\mid N), no answer smaller than (4) can exist because (3\nmid N), so (4) is immediately optimal.

After that, the loop checks only odd candidates starting at (3). Even candidates other than (4) cannot be the smallest answer. If (8\mid N), for example, (4) was already returned. If (N) is divisible by an even number greater than (4), it is also divisible by (4), so that case was already handled.

The condition `d * d <= n` is the integer form of (d\le\sqrt N). Python integers have arbitrary precision, so there is no overflow concern even when (N=10^{12}).

If the loop finishes, there is no odd divisor of (N) between (3) and (\sqrt N). For odd (N), this means (N) is prime, giving answer (N). For even (N), the factor (2) is the only small factor, so (N=2p), and the smallest valid divisor is (p=N/2).

The loop increments by (2) because every even candidate has already been covered by the special (4) case. This roughly halves the number of iterations without changing the logic.

## Worked Examples

For (N=5), the execution is short.

| (N) | (d) | (d^2\le N) | (N\bmod d) | Action |
| --- | --- | --- | --- | --- |
| 5 | 3 | No |  | Stop loop |
| 5 |  |  |  | (N) is odd, output 5 |

The search never reaches a divisor because (5) is prime. The answer is consequently the whole pentagon, with all (5) vertices selected.

For (N=21), we get the following trace.

| (N) | (d) | (d^2\le N) | (21\bmod d) | Action |
| --- | --- | --- | --- | --- |
| 21 | 3 | Yes | 0 | Output 3 |

The first candidate (3) already divides (21). Selecting every seventh vertex gives three equally spaced vertices, so the answer is (3).

A useful additional trace is (N=10).

| (N) | (d) | (d^2\le N) | (10\bmod d) | Action |
| --- | --- | --- | --- | --- |
| 10 | 3 | Yes | 1 | Continue |
| 10 | 5 | No after loop condition |  | Loop stops |
| 10 |  |  |  | (N) is even, output (10/2=5) |

Here (2) divides (10), but two vertices do not form a polygon. The next valid divisor is (5), and the final even-number branch recovers exactly that value.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(\sqrt N)) | At most about (\sqrt N/2) odd candidates are tested |
| Space | (O(1)) | Only (N) and the current divisor are stored |

For (N\le10^{12}), (\sqrt N\le10^6). The algorithm therefore performs at most roughly half a million divisibility checks, which is easily practical. The memory usage remains constant regardless of the size of (N).

## Test Cases

```python
import sys
import io

def solve_value(n: int) -> int:
    if n % 4 == 0:
        return 4

    d = 3
    while d * d <= n:
        if n % d == 0:
            return d
        d += 2

    if n % 2 == 0:
        return n // 2

    return n

def run(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)
    try:
        n = int(sys.stdin.readline())
        return str(solve_value(n))
    finally:
        sys.stdin = old_stdin

# Provided samples
assert run("5\n") == "5", "sample 1"
assert run("21\n") == "3", "sample 2"

# Minimum-size input
assert run("3\n") == "3", "minimum N"

# Smallest composite case
assert run("4\n") == "4", "square"

# Even number with no divisor 3 or 4
assert run("10\n") == "5", "2 * prime"

# Maximum-size boundary
assert run("1000000000000\n") == "4", "maximum N"

# Large odd prime
assert run("999999999989\n") == "999999999989", "large prime"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `3` | `3` | Minimum allowed polygon size |
| `4` | `4` | Smallest composite value and the special square case |
| `10` | `5` | Even value where (2) is unusable and (N/2) is the answer |
| `1000000000000` | `4` | Maximum input boundary and early return |
| `999999999989` | `999999999989` | Large prime requiring the full (\sqrt N) search |

## Edge Cases

For (N=3), the loop starts at (d=3), but the condition (3^2\le3) is already false. Since (N) is odd, the algorithm returns (N=3). This is correct because a triangle is already the smallest possible regular polygon.

For (N=5), the same reasoning returns (5). A careless implementation that assumes every regular polygon contains a triangle among its vertices would incorrectly return (3), but three vertices of a regular pentagon are not equally spaced.

For (N=8), the initial (N\bmod4=0) check returns (4). The four vertices obtained by taking every second vertex form a square. A solution that only checks odd divisors could incorrectly conclude that (8) is the answer.

For (N=10), (4) does not divide (N), and the loop checks (3), which is not a divisor. The loop stops because (5^2>10). Since (N) is even, the remaining factor is (10/2=5), which is the correct answer. This catches the common mistake of treating (2) as a possible answer.

For (N=21), the first candidate (d=3) divides (21), so the algorithm immediately returns (3). The three selected vertices are separated by (21/3=7) original edges, giving equal angular gaps.

For the maximum input (N=10^{12}), the number is divisible by (4), so the algorithm returns (4) immediately without entering the divisor loop. More generally, even when the maximum-sized value is chosen to be prime, the loop has to test only odd numbers up to (10^6), which is still within the intended complexity.
