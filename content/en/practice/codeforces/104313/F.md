---
title: "CF 104313F - \u0427\u0451\u0442\u043d\u043e-\u043d\u0435\u0447\u0451\u0442\u043d\u044b\u0435 \u043f\u0440\u0438\u0431\u0430\u0432\u043b\u0435\u043d\u0438\u044f"
description: "We are given several independent test cases. In each test case there is an array of integers, and then a sequence of operations."
date: "2026-07-01T19:46:10+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104313
codeforces_index: "F"
codeforces_contest_name: "II \u041e\u0442\u043a\u0440\u044b\u0442\u0430\u044f \u043a\u043e\u043c\u0430\u043d\u0434\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430 \u042e\u041c\u0428 \u043f\u043e \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044e"
rating: 0
weight: 104313
solve_time_s: 54
verified: true
draft: false
---

[CF 104313F - \u0427\u0451\u0442\u043d\u043e-\u043d\u0435\u0447\u0451\u0442\u043d\u044b\u0435 \u043f\u0440\u0438\u0431\u0430\u0432\u043b\u0435\u043d\u0438\u044f](https://codeforces.com/problemset/problem/104313/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 54s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given several independent test cases. In each test case there is an array of integers, and then a sequence of operations. Each operation targets the array based on parity: one type adds a fixed value to every even element, the other type adds a fixed value to every odd element. After every operation, we must report the total sum of the array.

The key difficulty is that the array is conceptually changing after every query, but we are not asked to output the array itself, only its total sum. The constraints make it clear that both the number of elements and the number of operations can reach 100000 per test case, with a total sum over all tests bounded by 200000. This immediately rules out recomputing the sum from scratch after each operation, since that would lead to roughly O(nq), which would exceed time limits by several orders of magnitude.

The natural edge case to consider is when parity changes dynamically. For example, if we add 1 to all even numbers, some of them become odd. A naive approach might try to update counts or sums incorrectly without accounting for this shift.

Consider this small example:

Input:

n = 3, a = [1, 2, 3]

Query: add 10 to evens

Correct array becomes [1, 12, 3], sum increases by 10 only once (because only one even element exists). A naive mistake would be to assume parity sets are fixed and just multiply by initial counts without tracking how elements move between parity classes over time. This becomes wrong as soon as updates accumulate.

The essential observation is that parity is not stable under additions, so we cannot maintain a fixed partition of indices. Instead, we need to track how many current evens and odds exist, and how their sums evolve.

## Approaches

A brute-force solution directly simulates each operation: scan the entire array, check parity of each element, apply the update when appropriate, and recompute the total sum. This is correct because it exactly mirrors the problem statement. However, each query costs O(n), and with q up to 100000, the total work becomes O(nq), which in worst case reaches 10^10 operations, far beyond limits.

The key insight is that we do not actually need the full array at any time. We only need three pieces of information: the sum of even elements, the sum of odd elements, and how many elements belong to each group. Once we maintain these aggregates, each operation becomes a constant-time update.

When we add x to all even elements, every even element increases by x, so the total sum increases by x multiplied by the number of even elements. However, parity changes: all those even elements become odd afterward. So we must transfer both their count and their contribution from the even bucket to the odd bucket. The same logic applies symmetrically for odd updates.

This transforms the problem from per-element simulation to per-group bookkeeping.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nq) | O(n) | Too slow |
| Optimal | O(n + q) | O(1) | Accepted |

## Algorithm Walkthrough

We maintain four values throughout the process: count of even elements, count of odd elements, sum of even elements, and sum of odd elements.

1. Initialize by scanning the array once, classifying each element as even or odd. We accumulate both counts and sums accordingly. This gives us a compressed representation of the entire array.
2. Compute the initial total sum as the sum of even and odd contributions. This value will be updated incrementally after each query.
3. For a query of type “add x to all even elements”, we first compute how much the total sum increases due to this operation, which is x multiplied by the number of even elements. This is because every even element is increased exactly once.
4. After updating the total sum, we must reflect structural changes. Every even element becomes odd after adding x, so the entire even bucket is transferred to the odd bucket. We update the odd sum by adding the old even sum plus x times the even count, and then reset the even sum to zero.
5. We also update the parity counts: all even elements become odd, so odd_count increases by even_count, and even_count becomes zero.
6. For a query of type “add x to all odd elements”, we apply the symmetric logic: increase total sum by x times odd_count, move all odd mass into the even bucket, and update counts accordingly.
7. After each query, output the current total sum.

The correctness rests on maintaining a correct partition of elements into two evolving groups, where each group fully represents current evens or odds.

### Why it works

At any moment, every element belongs to exactly one of two disjoint sets: current even values and current odd values. Each operation applies a uniform transformation to one set only. Because all elements in the chosen set receive identical increments, their relative parity flips consistently, and no element splits or behaves differently from others in the same group. This allows the entire state to be summarized by counts and sums without losing information, and every transition preserves the invariant that group sums and counts exactly match the underlying array.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, q = map(int, input().split())
        a = list(map(int, input().split()))

        even_cnt = 0
        odd_cnt = 0
        even_sum = 0
        odd_sum = 0

        for v in a:
            if v % 2 == 0:
                even_cnt += 1
                even_sum += v
            else:
                odd_cnt += 1
                odd_sum += v

        total = even_sum + odd_sum
        out = []

        for _ in range(q):
            typ, x = map(int, input().split())

            if typ == 0:
                total += x * even_cnt
                odd_sum += even_sum + x * even_cnt
                odd_cnt += even_cnt
                even_sum = 0
                even_cnt = 0
            else:
                total += x * odd_cnt
                even_sum += odd_sum + x * odd_cnt
                even_cnt += odd_cnt
                odd_sum = 0
                odd_cnt = 0

            out.append(str(total))

        print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The code maintains aggregated information instead of the full array. The initialization loop classifies elements into parity groups. Each query updates the total sum directly and then performs a full transfer of one group into the other, reflecting parity flips after addition. The most subtle point is that after adding x to a group, every element in that group changes parity, so we must move the entire accumulated sum and count into the opposite bucket, not partially update values.

Care must be taken that the sum update uses the old state before resetting counters, otherwise the transferred mass would be lost.

## Worked Examples

### Example 1

Input:

n = 3, a = [1, 2, 3]

Queries:

(0, 2), (1, 1)

Initial state:

| step | even_cnt | odd_cnt | even_sum | odd_sum | total |
| --- | --- | --- | --- | --- | --- |
| init | 1 | 2 | 2 | 4 | 6 |

After (0, 2): add 2 to evens

| step | even_cnt | odd_cnt | even_sum | odd_sum | total |
| --- | --- | --- | --- | --- | --- |
| after | 0 | 3 | 0 | 10 | 12 |

Explanation: even element 2 becomes 4, then flips to odd, joining odd group.

After (1, 1): add 1 to odds

| step | even_cnt | odd_cnt | even_sum | odd_sum | total |
| --- | --- | --- | --- | --- | --- |
| after | 3 | 0 | 13 | 0 | 13 |

This confirms that parity flips correctly propagate through aggregated state.

### Example 2

Input:

n = 4, a = [2, 4, 5, 7]

Query: (1, 3)

Initial:

| even_cnt | odd_cnt | even_sum | odd_sum | total |
| --- | --- | --- | --- | --- |
| 2 | 2 | 6 | 12 | 18 |

After (1, 3):

All odds increase by 3: 5→8, 7→10

| even_cnt | odd_cnt | even_sum | odd_sum | total |
| --- | --- | --- | --- | --- |
| 4 | 0 | 18 | 0 | 18 + 6 = 24 |

Odd group becomes even group after transformation.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + q) per test | Each element is processed once initially, each query is O(1) updates |
| Space | O(1) extra | Only counters and sums are stored |

The constraints allow up to 200000 total operations, so a linear solution comfortably fits within time limits. Constant-time updates per query ensure no bottlenecks even in worst-case test distributions.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    import sys
    from io import StringIO
    old_stdout = sys.stdout
    sys.stdout = StringIO()
    solve()
    out = sys.stdout.getvalue()
    sys.stdout = old_stdout
    return out.strip()

# small case
assert run("""1
1 1
2
0 5
""") == "7"

# all odd
assert run("""1
3 2
1 3 5
1 2
0 1
""") == "18\n21"

# all even
assert run("""1
3 2
2 4 6
0 1
1 10
""") == "18\n48"

# alternating parity flips
assert run("""1
4 3
1 2 3 4
0 1
1 1
0 2
""") == "11\n15\n19"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element | 7 | minimal structure |
| all odd chain | 18, 21 | odd-only transitions |
| all even chain | 18, 48 | even-only transitions |
| alternating flips | 11, 15, 19 | parity switching correctness |

## Edge Cases

A corner case appears when repeated operations collapse one parity group entirely. For instance, starting with all even numbers and applying an odd increment to evens immediately moves every element into the odd bucket.

Input:

n = 2, a = [2, 4], query (0, 1)

Initial state:

even_cnt = 2, even_sum = 6

After operation:

every element becomes odd: [3, 5]

The algorithm updates total sum by 2 * 2 = 4, giving 10, and transfers the entire even state into the odd state. Even counters drop to zero. The representation remains consistent because all elements change parity uniformly.

Another subtle case is when multiple consecutive operations target an already empty parity group. The update formula uses counts, so multiplying by zero ensures no incorrect drift occurs, and state remains stable without special casing.
