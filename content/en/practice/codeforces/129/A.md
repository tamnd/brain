---
title: "CF 129A - Cookies"
description: "We are given several bags of cookies, where each bag contains some number of cookies. Olga wants to steal exactly one bag. After removing that bag, the total number of cookies left behind must be even so the two sisters can split them equally."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 129
codeforces_index: "A"
codeforces_contest_name: "Codeforces Beta Round 94 (Div. 2 Only)"
rating: 900
weight: 129
solve_time_s: 104
verified: true
draft: false
---

[CF 129A - Cookies](https://codeforces.com/problemset/problem/129/A)

**Rating:** 900  
**Tags:** implementation  
**Solve time:** 1m 44s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given several bags of cookies, where each bag contains some number of cookies. Olga wants to steal exactly one bag. After removing that bag, the total number of cookies left behind must be even so the two sisters can split them equally.

The task is to count how many bags Olga can choose so that the remaining total is even.

The input consists of the number of bags and the number of cookies in each bag. The output is a single integer, the number of valid bags that can be removed.

The constraints are very small. There are at most 100 bags, and each bag contains at most 100 cookies. Even a quadratic solution would run instantly, since at worst we would only perform around 10,000 operations. That means we can focus entirely on clarity and correctness instead of optimization tricks.

The tricky part is understanding how parity behaves after removing one bag. A careless implementation may recompute sums incorrectly or misunderstand when an even total remains even.

Consider this example:

```
1
1
```

The total number of cookies is 1. If Olga removes the only bag, the remaining total becomes 0, which is even. The correct answer is:

```
1
```

A buggy solution might forget that zero is even and incorrectly print 0.

Another easy place to make mistakes is parity logic. Consider:

```
3
1 2 3
```

The total sum is 6, which is even. Removing a bag with an even number keeps the remaining sum even, while removing an odd bag makes it odd. Here only the bag containing 2 works, so the answer is:

```
1
```

If someone only counts odd bags or only checks the original total parity without reasoning carefully, they may get the wrong result.

A final edge case is when every bag has the same parity. For example:

```
4
2 2 2 2
```

The total sum is 8. Removing any bag leaves 6, which is even. The answer is 4. An implementation that accidentally checks the parity of the removed bag instead of the remaining sum can silently fail here.

## Approaches

The most direct solution is brute force. We first compute the total number of cookies. Then, for every bag, we imagine removing it and check whether the remaining total is even.

For bag `i`, the remaining total is:

```
total_sum - a[i]
```

If that value is divisible by 2, then this bag is a valid choice.

This approach is already fast enough. With at most 100 bags, we perform at most 100 checks after computing the sum once.

There is also a useful parity observation behind the problem. The parity of the remaining total depends only on the parity of the total sum and the removed bag.

If the total sum is even, then removing an even bag keeps the result even, while removing an odd bag makes it odd.

If the total sum is odd, then removing an odd bag makes the remaining total even.

So the problem can also be viewed as counting bags whose parity matches the parity of the total sum.

The brute-force version works because every candidate bag can be checked independently. The parity observation explains why those checks are so simple.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n) | O(1) | Accepted |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of bags and the array of cookie counts.
2. Compute the total number of cookies across all bags.
3. Initialize an answer counter to 0.
4. Iterate through every bag.
5. For the current bag, compute the remaining total after removing it:

```
remaining = total_sum - current_bag
```
6. Check whether `remaining` is even.

If `remaining % 2 == 0`, increment the answer.
7. After processing all bags, print the answer.

### Why it works

For every bag, the algorithm directly computes the number of cookies left after removing that bag. A bag is counted exactly when the remaining total is even, which matches the problem requirement precisely.

Since every possible bag is checked once and the parity test is mathematically correct, the algorithm cannot miss a valid answer or count an invalid one.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
a = list(map(int, input().split()))

total = sum(a)

answer = 0

for x in a:
    if (total - x) % 2 == 0:
        answer += 1

print(answer)
```

The solution begins by reading the number of bags and the cookie counts. The total sum is computed once at the beginning so we do not repeatedly recompute it for every bag.

The loop checks each bag independently. For a bag containing `x` cookies, removing it leaves `total - x` cookies behind. If this remaining amount is divisible by 2, the bag contributes one valid choice.

The implementation stays simple because the constraints are tiny. There are no overflow concerns in Python, and no special handling is needed for zero because `0 % 2 == 0` naturally works.

One subtle point is the order of operations. We must subtract the current bag before checking parity. Checking only the parity of the bag itself would not always be correct unless we separately reason about the parity of the total sum.

## Worked Examples

### Example 1

Input:

```
1
1
```

Total sum is 1.

| Current Bag | Remaining Total | Even? | Answer |
| --- | --- | --- | --- |
| 1 | 0 | Yes | 1 |

The final answer is:

```
1
```

This example confirms that removing the only bag is valid because zero is even.

### Example 2

Input:

```
4
1 2 3 4
```

The total sum is 10.

| Current Bag | Remaining Total | Even? | Answer |
| --- | --- | --- | --- |
| 1 | 9 | No | 0 |
| 2 | 8 | Yes | 1 |
| 3 | 7 | No | 1 |
| 4 | 6 | Yes | 2 |

The final answer is:

```
2
```

This trace shows the parity behavior clearly. Since the total sum is even, removing even bags keeps the remaining total even.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | We compute the sum once and scan the array once |
| Space | O(1) | Only a few integer variables are used |

With at most 100 bags, the algorithm easily fits within the time and memory limits. Even much slower approaches would pass, but the linear scan is both simple and optimal.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline

    n = int(input())
    a = list(map(int, input().split()))

    total = sum(a)

    ans = 0

    for x in a:
        if (total - x) % 2 == 0:
            ans += 1

    print(ans)

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    return sys.stdout.getvalue().strip()

# provided sample
assert run("1\n1\n") == "1", "sample 1"

# minimum size, even remaining becomes zero
assert run("1\n7\n") == "1", "single bag"

# all even values
assert run("4\n2 2 2 2\n") == "4", "all bags valid"

# mixed parity
assert run("4\n1 2 3 4\n") == "2", "only even bags work"

# no valid choices
assert run("2\n2 2\n") == "0", "removing any bag leaves odd total"

# larger case
assert run("5\n2 2 2 2 99\n") == "1", "only odd bag works"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 7` | `1` | Zero remaining cookies are treated as even |
| `4 / 2 2 2 2` | `4` | Every bag can be removed |
| `4 / 1 2 3 4` | `2` | Mixed parity handling |
| `2 / 2 2` | `0` | No valid removals |
| `5 / 2 2 2 2 99` | `1` | Only one bag satisfies the condition |

## Edge Cases

Consider the smallest possible input:

```
1
1
```

The total sum is 1. Removing the only bag leaves:

```
1 - 1 = 0
```

Since 0 is even, the algorithm increments the answer and prints 1. This confirms that empty remaining cookies are handled correctly.

Now consider a case where every bag is even:

```
4
2 2 2 2
```

The total sum is 8. Removing any bag leaves 6, which is even.

The algorithm checks all four bags:

```
8 - 2 = 6
```

every time, so the answer becomes 4.

Finally, consider a case where only one bag works:

```
5
2 2 2 2 99
```

The total sum is 107, which is odd.

Removing any even bag leaves 105, still odd.

Removing the bag with 99 leaves:

```
107 - 99 = 8
```

which is even.

The algorithm correctly counts exactly one valid choice.
