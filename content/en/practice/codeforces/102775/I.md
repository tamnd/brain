---
title: "CF 102775I - \u041f\u0435\u0440\u0435\u043f\u043e\u043b\u043e\u0445 \u0432 \u041d\u0418\u0418\u0427\u0410\u0412\u041e"
description: "The task is to answer many independent queries about a mathematical function. For a value a, the function is the product $$f(a)=1^a cdot 2^{a-1}cdot 3^{a-2}cdots (a-1)^2cdot a^1$$ with the special value f(0)=1. Each query asks for this value modulo $10^9+7$."
date: "2026-07-27T20:42:20+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102775
codeforces_index: "I"
codeforces_contest_name: "ICPC Central Russia Regional Contest (CRRC 20), \u0427\u0435\u043c\u043f\u0438\u043e\u043d\u0430\u0442 \u0426\u0435\u043d\u0442\u0440\u0430\u043b\u044c\u043d\u043e\u0439 \u0420\u043e\u0441\u0441\u0438\u0438, \u043a\u0432\u0430\u043b\u0438\u0444\u0438\u043a\u0430\u0446\u0438\u043e\u043d\u043d\u044b\u0439 \u0440\u0430\u0443\u043d\u0434"
rating: 0
weight: 102775
solve_time_s: 55
verified: true
draft: false
---

[CF 102775I - \u041f\u0435\u0440\u0435\u043f\u043e\u043b\u043e\u0445 \u0432 \u041d\u0418\u0418\u0427\u0410\u0412\u041e](https://codeforces.com/problemset/problem/102775/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 55s  
**Verified:** yes  

## Solution
## Problem Understanding

The task is to answer many independent queries about a mathematical function. For a value `a`, the function is the product

$$f(a)=1^a \cdot 2^{a-1}\cdot 3^{a-2}\cdots (a-1)^2\cdot a^1$$

with the special value `f(0)=1`. Each query asks for this value modulo $10^9+7$. The official statement gives the same definition and limits the queried values to $10^5$.

The input contains up to $10^5$ queries, and every queried `a` is also at most $10^5$. This immediately rules out recomputing the product from scratch for every query. A direct calculation for one query needs $O(a)$ multiplications, which would become about $10^{10}$ operations in the worst case. A 2 second time limit requires us to find a way to share work between queries.

The tricky cases are mostly around the boundaries. The first is `a = 0`, where the formula does not contain any factors at all, but the answer is explicitly defined as `1`. A solution that starts multiplying from `1` and assumes every query has at least one factor may mishandle this case.

For example:

```
Input
1
0
```

The correct output is:

```
1
```

A careless implementation that initializes the answer to `0` or tries to access the first factor of the product will fail.

Another edge case is `a = 1`. The product contains only one term:

$$f(1)=1^1=1$$

For example:

```
Input
1
1
```

The correct output is:

```
1
```

An implementation based on the recurrence must also handle this transition correctly, because it should multiply by `1!` and leave the value unchanged.

## Approaches

A straightforward approach is to evaluate every query independently. For a query `a`, we can loop through all numbers from `1` to `a` and multiply each number with its required power. This follows the definition directly, so it is correct. However, the largest possible query needs around $10^5$ factors, and doing this for $10^5$ queries gives roughly $10^{10}$ modular operations. That is far beyond what can fit in the time limit.

The key observation comes from comparing two consecutive values of the function. Instead of expanding the whole product every time, compare `f(a)` with `f(a-1)`:

$$f(a)=1^a\cdot2^{a-1}\cdots(a-1)^2\cdot a$$

and

$$f(a-1)=1^{a-1}\cdot2^{a-2}\cdots(a-1)^1$$

Every existing number from `1` to `a-1` gains exactly one extra copy in the exponent, and the new factor `a` appears once. The ratio becomes:

$$\frac{f(a)}{f(a-1)}=1\cdot2\cdot3\cdots a=a!$$

So the recurrence is:

$$f(a)=f(a-1)\cdot a!$$

This changes the problem completely. We only need to precompute factorials and then build the sequence of answers once. After that, every query is answered by a single array lookup.

The brute-force works because the definition directly describes the value, but it repeats almost the same work for neighboring queries. The observation that consecutive answers differ only by a factorial lets us replace repeated products with a prefix computation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(sum of all queried values) | O(1) | Too slow |
| Optimal | O(max(a) + n) | O(max(a)) | Accepted |

## Algorithm Walkthrough

1. Read all queries first and find the largest requested value. We need this maximum because all values up to it can be prepared in advance, while smaller queries can reuse the same precomputed answers.
2. Compute factorials from `1` to the maximum value. Let `fact[i]` store $i!$ modulo $10^9+7$. These values represent the multiplier needed to move from `f(i-1)` to `f(i)`.
3. Build the answer array. Start with `f(0)=1`. For every `i` from `1` to the maximum value, multiply the previous answer by `fact[i]`. The resulting value is `f(i)` because every transition applies exactly one factorial.
4. For every input query `a`, output the precomputed value stored at index `a`. No additional mathematical work is needed because all possible values have already been generated.

Why it works:

The invariant during preprocessing is that after processing index `i`, the stored value is exactly $f(i)$. Initially, this is true because the stored value is $f(0)=1$. When moving from `i-1` to `i`, we multiply by `i!`, and the derived recurrence proves that this produces exactly `f(i)`. Since every query asks for one of these already verified states, the returned value is always correct.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10 ** 9 + 7

def solve():
    n = int(input())
    queries = [int(input()) for _ in range(n)]

    mx = max(queries)

    fact = [1] * (mx + 1)
    for i in range(1, mx + 1):
        fact[i] = fact[i - 1] * i % MOD

    ans = [1] * (mx + 1)
    for i in range(1, mx + 1):
        ans[i] = ans[i - 1] * fact[i] % MOD

    print("\n".join(str(ans[x]) for x in queries))

if __name__ == "__main__":
    solve()
```

The input is stored before processing because the largest query determines how far preprocessing must go. Without knowing that maximum, we would either waste memory or need to extend the arrays dynamically.

The `fact` array stores ordinary factorial values modulo the required prime. The second loop constructs the actual function values using the recurrence $f(i)=f(i-1)\cdot i!$. Keeping these two arrays separate avoids recomputing factorials repeatedly.

The initialization of `ans[0]` as `1` handles the special definition of `f(0)`. The loop starts from `1`, so there is no off-by-one issue with the empty product. Python integers do not overflow, but every multiplication is reduced modulo `MOD` to keep values small and match the required output.

## Worked Examples

Consider the input:

```
3
3
4
5
```

The preprocessing behaves as follows.

| i | factorial i! | f(i) |
| --- | --- | --- |
| 0 | 1 | 1 |
| 1 | 1 | 1 |
| 2 | 2 | 2 |
| 3 | 6 | 12 |
| 4 | 24 | 288 |
| 5 | 120 | 34560 |

The outputs are:

```
12
288
34560
```

This trace shows the recurrence in action. Moving from one row to the next only requires multiplying by the next factorial, rather than rebuilding the entire original expression.

A second example focuses on the boundary:

```
4
0
1
2
3
```

| i | factorial i! | f(i) |
| --- | --- | --- |
| 0 | 1 | 1 |
| 1 | 1 | 1 |
| 2 | 2 | 2 |
| 3 | 6 | 12 |

The output is:

```
1
1
2
12
```

This confirms that the empty product case and the first few recurrence transitions are handled correctly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(max(a) + n) | We compute all values once up to the largest query and then answer each query in constant time. |
| Space | O(max(a)) | The factorial and answer arrays each contain at most `100001` values. |

The maximum value of `a` is only $10^5$, so the preprocessing requires a small number of operations. The memory usage is also comfortably within the limit because the arrays store only a few hundred thousand integers.

## Test Cases

```python
import sys
import io

MOD = 10 ** 9 + 7

def solution(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)

    n = int(sys.stdin.readline())
    queries = [int(sys.stdin.readline()) for _ in range(n)]

    mx = max(queries)

    fact = [1] * (mx + 1)
    for i in range(1, mx + 1):
        fact[i] = fact[i - 1] * i % MOD

    ans = [1] * (mx + 1)
    for i in range(1, mx + 1):
        ans[i] = ans[i - 1] * fact[i] % MOD

    res = "\n".join(str(ans[x]) for x in queries)

    sys.stdin = old_stdin
    return res

assert solution("""3
3
4
5
""") == """12
288
34560""", "sample"

assert solution("""1
0
""") == "1", "zero case"

assert solution("""5
1
1
1
1
1
""") == """1
1
1
1
1""", "all equal values"

assert solution("""4
0
1
2
3
""") == """1
1
2
12""", "small boundary values"

assert solution("""2
99999
100000
""").count("\n") == 1, "maximum size queries"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `3, 3, 4, 5` | `12, 288, 34560` | Original sample progression and recurrence |
| `1, 0` | `1` | Explicit `f(0)` definition |
| Five queries with value `1` | Five ones | Repeated queries and smallest positive value |
| `0, 1, 2, 3` | `1, 1, 2, 12` | Transition boundaries |
| Queries `99999` and `100000` | Two valid answers | Maximum preprocessing range |

## Edge Cases

For `a = 0`, the algorithm creates the answer array with `ans[0]=1` before applying any transitions. On the input

```
1
0
```

the maximum requested value is zero, so no factorials are computed and the stored answer remains `1`. The output is correct because the function is defined separately for this case.

For `a = 1`, the algorithm computes `fact[1]=1` and then updates:

$$ans[1]=ans[0]\cdot fact[1]=1\cdot1=1$$

For the input

```
1
1
```

the answer is:

```
1
```

The transition does not accidentally introduce an extra factor because multiplying by `1!` leaves the previous value unchanged.

For many identical large queries, preprocessing still happens only once. For example:

```
3
100000
100000
100000
```

The algorithm builds `f(100000)` a single time and performs three array accesses afterward. This avoids the repeated work that makes the direct formula too slow.
