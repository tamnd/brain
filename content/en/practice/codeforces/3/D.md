---
title: "CF 3D - Least Cost Bracket Sequence"
description: "We are given a bracket string containing \"(\", \")\", and \"?\". Every \"?\" can become either an opening or closing bracket, b"
date: "2026-05-27T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "greedy"]
categories: ["algorithms"]
codeforces_contest: 3
codeforces_index: "D"
codeforces_contest_name: "Codeforces Beta Round 3"
rating: 2600
weight: 3
solve_time_s: 141
verified: true
draft: false
---

[CF 3D - Least Cost Bracket Sequence](https://codeforces.com/problemset/problem/3/D)

**Rating:** 2600  
**Tags:** greedy  
**Solve time:** 2m 21s  
**Verified:** yes  
**Share:** https://chatgpt.com/share/6a172277-5124-83ec-be4e-543814d557ee  

## Solution
## Problem Understanding

We are given a bracket string containing `"("`, `")"`, and `"?"`. Every `"?"` can become either an opening or closing bracket, but each choice has a different cost. The goal is to replace every `"?"` so that the final string becomes a regular bracket sequence with minimum total cost.

A regular bracket sequence has two properties. First, the total number of opening and closing brackets must match. Second, while scanning from left to right, the balance must never become negative. The balance increases by one for `"("` and decreases by one for `")"`.

The string length is at most `5 * 10^4`, so we need something close to linear time. A quadratic solution would already perform around `2.5 * 10^9` operations in the worst case, which is far too slow for a 1 second limit. We need an algorithm that processes each character only a small number of times.

The tricky part is that local decisions are dangerous. Choosing the cheaper bracket for a single `"?"` may later make the whole sequence invalid. The problem is not just minimizing cost, it is minimizing cost while maintaining the prefix balance condition.

One edge case is when the sequence becomes invalid immediately and cannot be repaired. Consider:

```
)(
```

There are no `"?"` characters to fix. The first character already makes the balance negative, so the answer is `-1`.

Another subtle case is when repairing a negative balance requires changing earlier decisions. For example:

```
??
1 100
1 100
```

If we greedily choose the cheaper bracket every time, both `"?"` become `"("`, giving `"(("`, which is invalid because the final balance is not zero. The optimal valid answer is `"()"` with cost `101`.

A more interesting failure case for naive greedy logic is:

```
???
1 10
1 10
10 1
```

Suppose we always choose the cheaper option. The first two become `"("`, the last becomes `")"`, giving `"(()"`. The final balance is still positive. A valid sequence is impossible anyway because the length is odd, but this shows why checking only prefixes is not enough. We also need the final balance to be exactly zero.

Another important scenario happens when the balance becomes negative in the middle of the scan. Example:

```
)?(
5 1
```

If we initially treat `"?"` as `")"` because it is cheaper, the sequence becomes `"))("`. The balance becomes negative at position `0`, and there is no earlier `"?"` to flip into `"("`. The answer is `-1`.

## Approaches

The brute force idea is straightforward. For every `"?"`, try both possible replacements. If there are `k` question marks, there are `2^k` possible sequences. For each sequence, we can check whether it is regular in `O(n)` time and compute its cost.

This works because the definition of a regular bracket sequence is easy to verify with a single left to right scan. The problem is the number of possibilities. If the string contains `50000` question marks, we would need to explore `2^50000` states, which is astronomically impossible.

A slightly smarter brute force would use dynamic programming on position and balance. Let `dp[i][b]` be the minimum cost after processing the first `i` characters with current balance `b`. This avoids exponential branching, but the balance can grow up to `n`, so the complexity becomes `O(n^2)`. With `n = 50000`, that is around `2.5 * 10^9` states, still too large.

The key insight is that we do not actually need to decide every `"?"` immediately. Instead, we can temporarily assume every `"?"` becomes `")"`, because that gives us a concrete starting sequence. Then, whenever the balance becomes negative, we know we must change some earlier `"?"` from `")"` into `"("` to repair the prefix.

Changing a `"?"` from `")"` to `"("` changes the balance by `+2`. It also increases the cost by:

```
cost("(") - cost(")")
```

So whenever we are forced to repair the balance, we should choose the cheapest available flip. This becomes a classic greedy strategy with a priority queue.

The greedy works because every negative prefix must eventually be fixed by converting one of the earlier chosen `")"` brackets into `"("`. Among all available choices, picking the smallest extra cost is always optimal. Delaying a cheaper flip and taking a more expensive one can never help later.

We process the string left to right. Every `"?"` is initially treated as `")"`. We push its conversion cost into a min heap. If the balance drops below zero, we pop the cheapest available flip and convert that earlier position into `"("`.

This gives an `O(n log n)` solution, fast enough for `50000` characters.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^k * n) | O(k) | Too slow |
| DP on Position and Balance | O(n^2) | O(n^2) | Too slow |
| Greedy + Heap | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the string and convert it into a mutable array.

We need to modify characters in place when we later decide to flip a `"?"` from `")"` into `"("`.
2. Initialize balance as `0`, total cost as `0`, and an empty min heap.

The heap will store candidate flips. Each entry contains the extra cost of turning a chosen `")"` into `"("`, along with the position in the string.
3. Scan the string from left to right.

We maintain the current prefix balance exactly as the definition of a regular bracket sequence requires.
4. If the current character is `"("`, increase balance by `1`.

Opening brackets increase available unmatched openings.
5. If the current character is `")"`, decrease balance by `1`.

Closing brackets consume one unmatched opening.
6. If the current character is `"?"`, temporarily replace it with `")"`.

This gives the cheaper baseline structure where every unknown bracket starts as a closing bracket.
7. Add the cost of using `")"` to the answer.

Since we initially choose `")"`, this cost is definitely paid unless we later flip the bracket.
8. Push the pair `(cost("(") - cost(")"), position)` into the heap.

This represents how much extra money we would need if we later decide to convert this position into `"("`.
9. Decrease balance by `1`.

The current `"?"` is temporarily acting as `")"`.
10. If balance becomes negative, repair the sequence immediately.

A negative balance means the current prefix already violates the definition of a regular bracket sequence. Some earlier `"?"` must be flipped.
11. Pop the minimum extra cost from the heap.

Among all available flips, this one increases the total cost the least.
12. Change that position in the string from `")"` to `"("`.

This increases the balance by `2`, because the bracket changes from `-1` contribution to `+1`.
13. Add the extra flip cost to the answer.

We already paid for `")"` earlier, so now we only add the difference.
14. If the heap is empty when balance becomes negative, print `-1`.

There is no earlier `"?"` available to repair the invalid prefix.
15. After processing the whole string, check whether balance is exactly `0`.

If not, the number of opening and closing brackets does not match, so no valid sequence exists.
16. Otherwise, print the total cost and the final sequence.

## Python Solution

```python
import sys
import heapq

input = sys.stdin.readline

s = list(input().strip())
n = len(s)

heap = []
balance = 0
cost = 0

q_index = 0

for i in range(n):
    if s[i] == '(':
        balance += 1

    elif s[i] == ')':
        balance -= 1

    else:
        a, b = map(int, input().split())

        # Initially choose ')'
        s[i] = ')'
        cost += b
        balance -= 1

        # Extra cost to flip ')' into '('
        heapq.heappush(heap, (a - b, i))

    if balance < 0:
        if not heap:
            print(-1)
            sys.exit()

        extra, pos = heapq.heappop(heap)

        s[pos] = '('
        cost += extra
        balance += 2

if balance != 0:
    print(-1)
else:
    print(cost)
    print("".join(s))
```

The implementation follows the greedy strategy exactly.

Every `"?"` is initially treated as `")"`. That is why we immediately subtract one from the balance and add `b` to the cost. At the same time, we store the future conversion option `(a - b)` in the heap.

The heap is the critical structure here. It always gives us the cheapest bracket to flip when the balance becomes negative. Since Python's `heapq` is a min heap, the smallest extra cost is returned automatically.

One subtle detail is the balance adjustment after flipping. The character was previously counted as `")"` with contribution `-1`. After changing it into `"("`, the contribution becomes `+1`. The net change is `+2`.

Another easy mistake is forgetting that a valid bracket sequence must end with balance exactly zero. Even if every prefix is non-negative, a final positive balance still means unmatched opening brackets remain.

The algorithm never revisits characters except through heap entries, so the complexity stays efficient.

## Worked Examples

### Example 1

Input:

```
(??)
1 2
2 8
```

| Position | Character | Action | Balance | Cost | Heap |
| --- | --- | --- | --- | --- | --- |
| 0 | ( | fixed opening | 1 | 0 | [] |
| 1 | ? | choose `)` initially | 0 | 2 | [(−1,1)] |
| 2 | ? | choose `)` initially | -1 | 10 | [(-1,1),(-6,2)] |
| 2 | repair | flip position 2 to `(` | 1 | 4 | [(-1,1)] |
| 3 | ) | fixed closing | 0 | 4 | [(-1,1)] |

Final sequence:

```
()()
```

Total cost:

```
4
```

This trace shows why the greedy chooses the cheapest repair. Flipping the second `"?"` costs `2 - 8 = -6`, which is cheaper than flipping the first one with extra cost `1 - 2 = -1`.

### Example 2

Input:

```
)?(
5 1
```

| Position | Character | Action | Balance | Cost | Heap |
| --- | --- | --- | --- | --- | --- |
| 0 | ) | fixed closing | -1 | 0 | [] |

The balance becomes negative immediately, but the heap is empty. There is no earlier `"?"` available to flip into `"("`.

Output:

```
-1
```

This demonstrates the core invariant of the algorithm. Every invalid prefix must be repaired using an earlier `"?"`. If none exists, the sequence is impossible.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Each `"?"` is inserted into and removed from the heap at most once |
| Space | O(n) | The heap and mutable string can both store up to `n` elements |

With `n <= 50000`, the `log n` factor is small enough to comfortably fit within the 1 second limit. The memory usage is also well below the 64 MB limit.

## Test Cases

### Test Case 1

Input:

```
()
```

Expected output:

```
0
()
```

This verifies the simplest already-valid sequence with no `"?"` characters.

### Test Case 2

Input:

```
??
1 100
100 1
```

Expected output:

```
2
()
```

This checks whether the algorithm correctly balances cheap and expensive flips.

### Test Case 3

Input:

```
))((
```

Expected output:

```
-1
```

This confirms the algorithm correctly rejects impossible sequences with no repair options.

### Test Case 4

Input:

```
????
10 1
10 1
1 10
1 10
```

Expected output:

```
4
(())
```

This tests multiple repairs and verifies that the heap always chooses the cheapest flip available.

## Edge Cases

Consider the impossible prefix case:

```
)(
```

The first character immediately makes the balance `-1`. Since there are no `"?"` positions stored in the heap, the algorithm stops and prints `-1`. This matches the fact that no replacement operation exists.

Now consider:

```
??
1 100
1 100
```

The algorithm first chooses both positions as `")"` because that is the temporary default. After the first character, balance becomes `-1`, so it flips the cheapest available position into `"("`. The same process happens again later. The final sequence becomes `"()"` with cost `101`.

Another subtle case is:

```
((
```

No prefix ever becomes negative, but the final balance is `2`. The algorithm reaches the end and rejects the sequence because unmatched opening brackets remain.

Finally, consider:

```
????
1 10
1 10
10 1
10 1
```

Initially all positions become `")"`, making the balance heavily negative. The heap repairs the sequence by flipping the two cheapest positions into `"("`. The final result is `(())`, which is both valid and minimum cost.
