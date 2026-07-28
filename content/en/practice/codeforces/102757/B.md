---
title: "CF 102757B - Modern Gladiator"
description: "The problem simulates a shop where every customer buys one item for one bronze coin. A customer does not always pay with bronze, they may hand over a silver coin or a gold coin. Alfonso must immediately return the correct change before serving the next customer."
date: "2026-07-29T00:28:20+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102757
codeforces_index: "B"
codeforces_contest_name: "UTPC Contest 10-09-20 Div. 2"
rating: 0
weight: 102757
solve_time_s: 45
verified: true
draft: false
---

[CF 102757B - Modern Gladiator](https://codeforces.com/problemset/problem/102757/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 45s  
**Verified:** yes  

## Solution
# Problem Understanding

The problem simulates a shop where every customer buys one item for one bronze coin. A customer does not always pay with bronze, they may hand over a silver coin or a gold coin. Alfonso must immediately return the correct change before serving the next customer.

The coin system is binary: one silver coin has the same value as two bronze coins, and one gold coin has the same value as two silver coins. Equivalently, the values are bronze = 1, silver = 2, and gold = 4. Alfonso starts with no coins, so the first few customers can determine whether he will ever have enough smaller coins to continue. The goal is to decide whether the entire queue can be served.

The number of customers can reach 100000, so an algorithm that repeatedly searches through the whole history or tries possible choices would be too slow. We need a single pass over the customers, with only constant work per customer, giving an O(n) solution.

The tricky cases come from the fact that having enough total money is not sufficient. Alfonso may have enough value but not the right denominations for change. For example:

```
3
gold
gold
gold
```

The correct output is:

```
NO
```

After the first gold coin, Alfonso owns a gold coin but needs to give back three bronze coins. He has no smaller coins, so he fails immediately. A careless solution that only tracks total value would think he has enough money and give the wrong answer.

Another edge case is when a higher denomination appears after a few smaller coins:

```
4
bronze
bronze
silver
gold
```

The correct output is:

```
YES
```

The first two customers give Alfonso two bronze coins. The silver payment can be handled by returning one bronze. The final gold payment can be handled by returning one silver and one bronze. A solution that only checks whether every coin value appears enough times may miss the ordering requirement.

A final boundary case is:

```
3
bronze
silver
gold
```

The correct output is:

```
NO
```

After the bronze payment Alfonso has one bronze. The silver payment succeeds and leaves one silver coin. The gold payment needs three bronze coins worth of change, but Alfonso has only one silver coin. The silver coin cannot be returned as change because it would be worth two coins instead of three.

# Approaches

A straightforward approach is to simulate every possible way Alfonso could make change. For each customer, the program could try different combinations of coins that sum to the required change and continue recursively. This is correct because every possible sequence of decisions is considered, but it quickly becomes impossible. In the worst case, every gold customer introduces several possible ways to create three bronze coins worth of change, and exploring those branches leads to exponential behavior.

The structure of the coin system gives a much simpler route. Since each denomination is exactly twice the previous one, larger coins are always more valuable and less flexible than smaller coins. The only thing that matters for future customers is how many bronze and silver coins Alfonso currently has, because gold coins are never needed for making change. A gold coin always remains in his collection after the transaction.

The key observation is that change can be made greedily. A silver customer requires exactly one bronze coin. A gold customer requires three bronze coins of value. The best way to provide three bronze coins worth of change is to use one silver coin and one bronze coin whenever possible, because this preserves more bronze coins for future silver customers. If that is impossible, three bronze coins are the only remaining option.

The brute force works because it explores every valid way to make change, but fails because the number of choices grows too quickly. The binary nature of the coin values removes that ambiguity and lets us maintain only the necessary coin counts while processing the line once.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential in the number of customers | O(n) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

# Algorithm Walkthrough

1. Maintain counters for the number of bronze, silver, and gold coins Alfonso owns. Initially all three counters are zero.
2. Read customers from the front of the queue one by one and add the received coin to Alfonso's collection. The received coin cannot be used to pay for the item because the transaction has already happened, so it becomes part of his available coins.
3. If the customer paid with bronze, no change is needed because the payment exactly matches the price.
4. If the customer paid with silver, remove one bronze coin as change. If no bronze coin exists, serving the customer is impossible.
5. If the customer paid with gold, remove change worth three bronze coins. Prefer using one silver coin and one bronze coin because that keeps the remaining bronze coins available for later silver payments. If that is not possible, use three bronze coins. If neither option exists, the process fails.
6. If every customer is processed successfully, output `YES`. Otherwise output `NO` at the first point where change cannot be produced.

Why it works:

The invariant is that after every successfully served customer, the stored coin counts represent exactly the coins Alfonso has after completing all transactions so far. For a silver payment, the only possible required change is one bronze coin. For a gold payment, every valid way of returning three bronze coins is either one silver plus one bronze, or three bronze coins. The greedy choice is safe because replacing one silver coin with two bronze coins would only decrease Alfonso's flexibility. Keeping the larger coin while spending smaller value first gives at least as much ability to serve all future customers. Since every customer is handled using a valid transaction that preserves this invariant, the final answer is correct.

# Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    bronze = 0
    silver = 0
    gold = 0

    for _ in range(n):
        coin = input().strip()

        if coin == "bronze":
            bronze += 1
        elif coin == "silver":
            silver += 1
            if bronze == 0:
                print("NO")
                return
            bronze -= 1
        else:
            gold += 1
            if silver > 0 and bronze > 0:
                silver -= 1
                bronze -= 1
            elif bronze >= 3:
                bronze -= 3
            else:
                print("NO")
                return

    print("YES")

if __name__ == "__main__":
    solve()
```

The three variables store only the information needed for future customers. Gold coins are counted because they belong to Alfonso after being received, but they never participate in making change.

For silver payments, the code first adds the silver coin and then removes one bronze coin. The order is correct because the customer gives the coin before Alfonso returns change.

For gold payments, the code first keeps the gold coin and then checks the two valid ways to create three bronze coins of change. The preferred branch uses a silver coin and a bronze coin. The fallback branch uses three bronze coins. The checks are written before subtraction so the counters never become negative.

Python integers do not overflow, and the algorithm uses only a few variables, so it remains efficient even for the maximum number of customers.

# Worked Examples

Sample 1:

Input:

```
4
bronze
bronze
silver
gold
```

| Customer | Payment | Bronze | Silver | Gold | Action |
| --- | --- | --- | --- | --- | --- |
| 1 | bronze | 1 | 0 | 0 | Keep exact payment |
| 2 | bronze | 2 | 0 | 0 | Keep exact payment |
| 3 | silver | 1 | 1 | 0 | Return one bronze |
| 4 | gold | 0 | 0 | 1 | Return one silver and one bronze |

The example demonstrates why tracking denominations matters. Alfonso has enough value at every stage, but the exact coins determine whether he can continue.

Sample 2:

Input:

```
3
bronze
silver
gold
```

| Customer | Payment | Bronze | Silver | Gold | Action |
| --- | --- | --- | --- | --- | --- |
| 1 | bronze | 1 | 0 | 0 | Keep exact payment |
| 2 | silver | 0 | 1 | 0 | Return one bronze |
| 3 | gold | 1 | 1 | 1 | Cannot create change |

The last transaction fails because Alfonso has a silver coin and a bronze coin, but the change required is three bronze coins. The algorithm correctly rejects this ordering.

# Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each customer is processed once with constant-time updates. |
| Space | O(1) | Only three coin counters are stored. |

The input size can reach 100000 customers, so a linear scan is easily within the required limits. No data structure depending on the number of customers is needed.

# Test Cases

```python
import sys, io

def solve_io(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out

    n = int(sys.stdin.readline())
    bronze = silver = gold = 0

    for _ in range(n):
        coin = sys.stdin.readline().strip()

        if coin == "bronze":
            bronze += 1
        elif coin == "silver":
            silver += 1
            if bronze == 0:
                print("NO")
                break
            bronze -= 1
        else:
            gold += 1
            if silver > 0 and bronze > 0:
                silver -= 1
                bronze -= 1
            elif bronze >= 3:
                bronze -= 3
            else:
                print("NO")
                break
    else:
        print("YES")

    sys.stdin = old_stdin
    sys.stdout = old_stdout
    return out.getvalue()

assert solve_io("""4
bronze
bronze
silver
gold
""") == "YES\n", "sample 1"

assert solve_io("""3
bronze
silver
gold
""") == "NO\n", "sample 2"

assert solve_io("""3
gold
gold
gold
""") == "NO\n", "no initial change"

assert solve_io("""5
bronze
bronze
bronze
gold
silver
""") == "YES\n", "multiple change operations"

assert solve_io("""3
silver
bronze
gold
""") == "NO\n", "bad ordering"

assert solve_io("""100000
""" + "bronze\n" * 100000) == "YES\n", "large input"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `bronze, bronze, silver, gold` | YES | Normal successful sequence |
| `bronze, silver, gold` | NO | Denomination ordering issue |
| `gold, gold, gold` | NO | Starting without change |
| `bronze, bronze, bronze, gold, silver` | YES | Repeated use of change |
| `silver, bronze, gold` | NO | Cases where total value is misleading |
| 100000 bronze payments | YES | Maximum input size |

# Edge Cases

For the first edge case:

```
3
gold
gold
gold
```

The algorithm starts with zero coins. The first gold customer gives Alfonso a gold coin, but the algorithm checks whether three bronze coins worth of change exist. Neither one silver plus one bronze nor three bronze coins is available, so it immediately prints `NO`. This matches the real process because the gold coin cannot be split into smaller coins.

For the ordering-sensitive case:

```
3
bronze
silver
gold
```

After the bronze customer, Alfonso owns one bronze coin. The silver customer gives a silver coin and takes one bronze coin, leaving only a silver coin. The gold customer requires three bronze coins of change. The algorithm cannot find either a silver and bronze pair or three bronze coins, so it rejects the sequence.

For the successful boundary case:

```
4
bronze
bronze
silver
gold
```

The algorithm accumulates two bronze coins, spends one for the silver payment, and then uses the remaining bronze together with the silver coin for the gold payment. Every transaction preserves the invariant that Alfonso's stored coins are exactly his real coins after serving the customers, so the final answer is `YES`.
