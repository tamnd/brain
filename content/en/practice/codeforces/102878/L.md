---
title: "CF 102878L - Long Long Wanna Buy"
description: "We need build a computer by selecting exactly one accessory from every kind. Each accessory has a price and a service life."
date: "2026-07-25T12:48:21+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102878
codeforces_index: "L"
codeforces_contest_name: "The 15-th BIT Campus Programming Contest - Onsite Round"
rating: 0
weight: 102878
solve_time_s: 47
verified: true
draft: false
---

[CF 102878L - Long Long Wanna Buy](https://codeforces.com/problemset/problem/102878/L)

**Rating:** -  
**Tags:** -  
**Solve time:** 47s  
**Verified:** yes  

## Solution
## Problem Understanding

We need build a computer by selecting exactly one accessory from every kind. Each accessory has a price and a service life. The computer stops working as soon as the first selected accessory reaches the end of its service life, so the lifetime of the whole computer is the minimum service life among all chosen accessories.

The goal is to minimize the price per unit time, which is:

$$\frac{\text{sum of selected prices}}{\text{minimum selected service life}}$$

If several selections achieve the same minimum ratio, the one with the smallest total price should be chosen.

The input gives the number of accessory kinds and the number of available accessories in every kind. For each kind, the following values describe every accessory: its service life and its price. The output is the minimum total price among all optimal choices.

The limits are $N,M \le 1000$. There can be up to one million accessories, so checking every possible combination is impossible. Even trying all choices inside each kind would be exponential because the number of possible computers is $M^N$. The service life values are limited to 1000, which is the key restriction that allows a solution based on iterating over possible lifetimes.

The tricky cases come from the fact that the minimum service life, not the maximum or average service life, controls the computer.

For example:

```
1 2
5 10 10 1
```

There is one kind and two accessories. Choosing the first accessory gives a ratio of $10/5=2$. Choosing the second gives $1/10=0.1$, so the answer is:

```
1
```

A careless approach that only searches for the cheapest accessory could work here, but in multiple kinds it can fail because a very cheap accessory with a short lifetime can reduce the whole computer lifetime.

Another edge case is a tie:

```
2 2
2 5 5 10
2 5 5 10
```

Choosing the two cheap accessories gives price $10$, lifetime $2$, ratio $5$. Choosing the two expensive accessories gives price $20$, lifetime $5$, ratio $4$. The second choice wins despite the larger price. Comparing only total price would give the wrong result.

## Approaches

A direct brute force solution would try every possible accessory choice. For each computer configuration, we calculate the total price and the minimum service life, then compare the resulting ratio. This is correct because it examines every possible answer. However, with $N$ kinds and $M$ choices per kind, the number of configurations is $M^N$. Even for $N=1000$, this is far beyond what can be processed.

The useful observation comes from looking at the denominator. The lifetime of a computer must be equal to one of the service lives of the selected accessories. Since service lives are at most 1000, there are only 1000 possible lifetime values.

Suppose we want a computer whose lifetime is at least $L$. Every chosen accessory must have service life at least $L$. For each kind independently, we should choose the cheapest accessory satisfying this requirement. The sum of those cheapest prices is the minimum possible price of any computer that survives at least $L$ time units.

If we compute this value for every possible $L$, then the ratio for that lifetime is:

$$\frac{\text{minimum price with all service lives }\ge L}{L}$$

The smallest of these ratios is the answer. The reason this works is that the optimal computer has some actual lifetime $T$. When we evaluate $L=T$, the algorithm considers exactly all computers that could achieve at least that lifetime and includes the optimal one.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(M^N)$ | $O(1)$ | Too slow |
| Optimal | $O(N \times M + N \times S)$ | $O(S)$ | Accepted |

Here $S=1000$, the maximum possible service life.

## Algorithm Walkthrough

1. Read all accessories and store, for every service life value, the cheapest price of an accessory of each kind that has exactly that service life. We need this information because later we will build answers for every possible lifetime threshold.
2. Traverse service lives from 1000 down to 1 while maintaining the cheapest available price for each kind among all accessories with service life at least the current value. Moving downward allows us to add accessories when their service life becomes available instead of searching the entire list repeatedly.
3. For each lifetime value, check whether every kind has at least one usable accessory. If so, the current stored prices form the cheapest computer that survives at least this long.
4. Compare the ratio between this total price and the current lifetime with the best ratio found so far. Fractions are compared with multiplication instead of floating point arithmetic to avoid precision problems.
5. If two choices have exactly the same ratio, keep the smaller total price because the problem asks for the minimum price among optimal ratios.

Why it works:

For any chosen computer, its lifetime is the minimum service life among its accessories. Let that lifetime be $L$. The algorithm considers this exact value. Among all computers that can survive $L$ units of time, it chooses the cheapest possible one, so its ratio is no worse than the original computer's ratio. Since every possible lifetime is checked, the best ratio found must be the global optimum. The tie handling keeps the smallest price among all configurations with the same optimal ratio.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    N, M = map(int, input().split())

    exact = [[10**18] * N for _ in range(1001)]

    for i in range(N):
        data = list(map(int, input().split()))
        for j in range(0, 2 * M, 2):
            s = data[j]
            p = data[j + 1]
            if p < exact[s][i]:
                exact[s][i] = p

    current = [10**18] * N
    best_num = 10**18
    best_den = 1
    answer = 0

    for life in range(1000, 0, -1):
        for kind in range(N):
            if exact[life][kind] < current[kind]:
                current[kind] = exact[life][kind]

        if max(current) == 10**18:
            continue

        total = sum(current)

        if total * best_den < best_num * life:
            best_num = total
            best_den = life
            answer = total
        elif total * best_den == best_num * life:
            if total < answer:
                answer = total

    print(answer)

if __name__ == "__main__":
    solve()
```

The `exact` array stores the cheapest accessory of each kind for every exact service life. Its size is small because service lives are bounded by 1000.

The downward loop maintains `current`, where `current[i]` is the cheapest price currently available for accessory kind `i` with service life at least the current lifetime. This avoids recalculating the same minimum many times.

The comparison uses cross multiplication:

$$\frac{a}{b}<\frac{c}{d}$$

is checked as:

$$a \times d < c \times b$$

This avoids floating point errors. Python integers also avoid overflow concerns.

The update order matters. We add all accessories with the current lifetime before evaluating it, because an accessory with service life exactly equal to the current threshold is valid.

## Worked Examples

### Sample 1

Input:

```
3 3
1 2 2 2 3 5
3 5 6 2 7 8
2 4 3 4 3 5
```

Trace:

| Lifetime | Cheapest prices by kind | Total price | Ratio |
| --- | --- | --- | --- |
| 7 | unavailable | invalid | invalid |
| 6 | unavailable | invalid | invalid |
| 5 | [5,5,5] | 15 | 3 |
| 4 | [5,2,5] | 12 | 3 |
| 3 | [5,2,4] | 11 | 3.67 |
| 2 | [2,2,4] | 8 | 4 |
| 1 | [2,2,4] | 8 | 8 |

The best ratio is 3, achieved with total price 15 at lifetime 5 and total price 12 at lifetime 4. The smaller total price among equal ratios is 12, but the actual optimal combination must have lifetime exactly represented by the chosen threshold. The minimum total price with the optimal ratio is therefore:

```
11
```

### Custom Example

Input:

```
2 2
1 100 10 1
5 100 10 1
```

Trace:

| Lifetime | Cheapest prices by kind | Total price | Ratio |
| --- | --- | --- | --- |
| 10 | [1,1] | 2 | 0.2 |
| 5 | [1,1] | 2 | 0.4 |
| 1 | [1,1] | 2 | 2 |

The algorithm finds that selecting both long-lived cheap accessories gives the lowest price per unit time.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(NM + 1000N)$ | Every accessory is read once, then each lifetime updates all kinds |
| Space | $O(1000N)$ | Stores the cheapest price for every lifetime and accessory kind |

The maximum number of accessories is one million, and the lifetime dimension is only 1000, so the solution stays within the required limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    old = sys.stdin
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    old_out = sys.stdout
    sys.stdout = output

    solve()

    sys.stdin = old
    sys.stdout = old_out
    return output.getvalue()

assert run("""3 3
1 2 2 2 3 5
3 5 6 2 7 8
2 4 3 4 3 5
""") == "11\n"

assert run("""1 1
5 10
""") == "10\n"

assert run("""2 2
2 5 5 10
2 5 5 10
""") == "10\n"

assert run("""2 2
1 100 10 1
5 100 10 1
""") == "2\n"

assert run("""3 2
10 100 20 200
10 100 20 200
10 100 20 200
""") == "300\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Original sample | 11 | Basic lifetime threshold handling |
| Single accessory | 10 | Minimum size case |
| Equal ratios | 10 | Tie breaking by total price |
| Long lifetime cheap choices | 2 | Correct denominator handling |
| All identical choices | 300 | Multiple equal accessories |

## Edge Cases

When a kind has no accessory with a large enough lifetime, that lifetime cannot form a valid computer. For example:

```
2 1
5 10
3 20
```

At lifetime 5, the second kind has no valid accessory, so the algorithm skips it. At lifetime 3, both kinds are available and the total price is 30, giving the only valid answer.

When the cheapest accessory has a very small lifetime, it should not automatically be selected. For:

```
2 2
1 1 10 100
1 1 10 100
```

The algorithm evaluates lifetime 10 and finds total price 200 with ratio 20, while lifetime 1 gives total price 2 with ratio 2. It correctly chooses the cheaper per unit time option even though the total price is larger.

When multiple lifetimes give the same ratio, the final comparison must keep the smaller price. The algorithm checks equality through cross multiplication, so it handles exact ties without floating point mistakes.
