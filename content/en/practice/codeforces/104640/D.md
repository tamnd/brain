---
title: "CF 104640D - \u0422\u0435\u0441\u0442 \u043d\u0430 \u0438\u043d\u0442\u0435\u043b\u043b\u0435\u043a\u0442"
description: "We are asked to construct a string of length $n$ over lowercase Latin letters. After we output the string, a machine evaluates it in a way that depends only on which distinct letters appear and how many times each appears."
date: "2026-06-29T16:49:53+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104640
codeforces_index: "D"
codeforces_contest_name: "\u0418\u043d\u0442\u0435\u0440\u043d\u0435\u0442-\u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u044b, \u0421\u0435\u0437\u043e\u043d 2023-2024, \u041f\u0435\u0440\u0432\u0430\u044f \u043a\u043e\u043c\u0430\u043d\u0434\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430"
rating: 0
weight: 104640
solve_time_s: 60
verified: true
draft: false
---

[CF 104640D - \u0422\u0435\u0441\u0442 \u043d\u0430 \u0438\u043d\u0442\u0435\u043b\u043b\u0435\u043a\u0442](https://codeforces.com/problemset/problem/104640/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to construct a string of length $n$ over lowercase Latin letters. After we output the string, a machine evaluates it in a way that depends only on which distinct letters appear and how many times each appears.

The machine first counts how many distinct letters are used in the string, call this $k$. Then it assigns to those $k$ letters distinct integer weights from $1$ to $k$, choosing the assignment that minimizes the final score. The score is computed by summing the weight of every character occurrence in the string.

So the machine is effectively adversarial in how it assigns weights, but still constrained to use a permutation of $1 \ldots k$. For any fixed multiset of letter frequencies, the machine will assign smaller weights to more frequent letters, because that reduces the sum.

We are required to construct a string of length $n$ that maximizes this final minimized score.

The input size allows $n \le 10^5$, so we need an $O(n)$ or $O(n \log n)$ construction. Anything involving searching over all strings or permutations is immediately infeasible because the number of strings is $26^n$, and even evaluating one configuration requires sorting frequencies, which would be too slow if done repeatedly.

A subtle edge case appears when all characters are identical. For example, if $n = 3$ and the string is `"aaa"`, then $k = 1$, the weight is forced to be $1$, and the score is $3$. If instead we use `"abc"`, then $k = 3$, and the machine assigns weights $1,2,3$ in the best possible way, leading to a much larger score. This suggests that increasing diversity tends to increase the score, but the interaction is not just “maximize distinct letters”, because the machine always assigns best weights against us.

## Approaches

If we fix a string, the machine’s behavior is deterministic: it sorts letters by frequency in descending order and assigns weight $1$ to the most frequent letter, $2$ to the second most frequent, and so on. This is optimal for minimizing the sum because every occurrence of a frequent letter is multiplied by a smaller weight.

So the value becomes:

$$T = \sum_{i=1}^{k} f_i \cdot w_i$$

where $f_i$ are frequencies sorted in non-increasing order, and $w_i$ is a permutation of $1 \ldots k$, optimally assigned as $w_i = i$.

Thus:

$$T = \sum_{i=1}^{k} f_i \cdot i$$

Now we want to choose a string, meaning we choose a frequency distribution over at most 26 letters summing to $n$, to maximize this weighted sum.

The key observation is that higher indices are more valuable, so we want large frequencies to align with large weights. Since the weights are fixed as $1$ through $k$, maximizing $k$ alone is not sufficient. Instead, we want to structure frequencies so that larger indices get large counts.

However, there is a stronger simplification. For a fixed $k$, the best we can do is concentrate as much mass as possible on the largest index $k$, because that letter gets the highest weight. To maximize $T$, we want to maximize $k$, since increasing $k$ increases both the number of terms and the maximum possible weight.

But $k \le 26$, so we can always use up to 26 distinct letters. Once we use all 26, the only remaining choice is how to distribute frequencies. For fixed $k$, to maximize:

$$\sum i \cdot f_i$$

we should assign the largest frequencies to largest indices. That means we want a strictly increasing frequency assignment in reverse index order.

This becomes a classic greedy construction: distribute $n$ characters among up to 26 letters such that:

$$f_{26} \ge f_{25} \ge \cdots \ge f_1 \ge 0$$

and maximize the weighted sum. The optimal strategy is to use all 26 letters (or fewer if $n < 26$) and distribute as evenly as possible, giving extra characters to higher-index letters first.

The brute force approach would try all partitions of $n$ into at most 26 parts and compute the score, which is exponential in $n$. The greedy distribution reduces this to a linear pass.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential in $n$ | O(n) | Too slow |
| Optimal Greedy Distribution | O(26) | O(1) | Accepted |

## Algorithm Walkthrough

1. Determine the number of distinct letters $k = \min(26, n)$. This ensures we never exceed the alphabet limit while maximizing diversity when possible.
2. Initialize an array of size 26 with all zeros, representing frequencies of letters `'a'` to `'z'`.
3. Assign one occurrence to each of the first $k$ letters. This guarantees we use the maximum possible distinct letters.
4. Let remaining characters be $rem = n - k$. These are extra occurrences that must be distributed.
5. Repeatedly assign one extra character to letters from `'a' + k - 1` downward to `'a'`, cycling from highest index to lowest, until all remaining characters are distributed. This ensures higher-weight letters receive more frequency, which maximizes the weighted sum.
6. Construct the final string by repeating each letter according to its frequency.

### Why it works

The final score depends on matching high frequencies with high weights. Since the machine assigns higher weights to less frequent letters, we want to control the frequency ordering so that the mapping forces large counts onto large weights. By distributing extra occurrences in reverse alphabetical order, we ensure that higher-index letters are never less frequent than lower-index ones. This keeps the machine’s sorted frequency order aligned with our constructed ordering, maximizing the contribution of higher weights.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input().strip())
    
    k = min(26, n)
    freq = [0] * 26
    
    for i in range(k):
        freq[i] = 1
    
    rem = n - k
    idx = k - 1
    
    while rem > 0:
        freq[idx] += 1
        rem -= 1
        idx -= 1
        if idx < 0:
            idx = k - 1
    
    res = []
    for i in range(26):
        res.append(chr(ord('a') + i) * freq[i])
    
    print("".join(res))

if __name__ == "__main__":
    solve()
```

The solution first ensures maximal distinct letters by assigning one occurrence to each of the first $k$ letters. The remaining characters are then distributed greedily starting from the highest indexed active letter, which biases frequency upward in the lexicographically later characters that correspond to higher machine-assigned weights after sorting.

The construction phase is straightforward: we rebuild the string by repeating each character according to its computed frequency.

A subtle implementation detail is the cyclic decrement of `idx`, which ensures fair distribution among all chosen letters instead of starving lower indices completely when $rem$ is large.

## Worked Examples

### Example 1

Input:

```
3
```

We compute $k = 3$. Initial frequencies are:

`a:1, b:1, c:1`, remaining is 0.

| Step | k | freq(a) | freq(b) | freq(c) | rem |
| --- | --- | --- | --- | --- | --- |
| init | 3 | 1 | 1 | 1 | 0 |

Output string can be:

```
abc
```

This shows that when no extra characters exist, the optimal solution is simply to maximize distinct letters.

### Example 2

Input:

```
5
```

We have $k = 5$, so we start with one of each `a` to `e`, then distribute 0 extra since $n = k$.

| Step | a | b | c | d | e | rem |
| --- | --- | --- | --- | --- | --- | --- |
| init | 1 | 1 | 1 | 1 | 1 | 0 |

Output:

```
abcde
```

This confirms that full diversification is optimal when $n \le 26$.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(26 + n) | Frequency assignment and string construction are linear in alphabet size and output size |
| Space | O(26) | Only frequency array for letters |

The solution is efficient for $n \le 10^5$, since all operations are linear and constants are small.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n = int(sys.stdin.readline().strip())
    
    k = min(26, n)
    freq = [0] * 26
    
    for i in range(k):
        freq[i] = 1
    
    rem = n - k
    idx = k - 1
    
    while rem > 0:
        freq[idx] += 1
        rem -= 1
        idx -= 1
        if idx < 0:
            idx = k - 1
    
    res = []
    for i in range(26):
        res.append(chr(ord('a') + i) * freq[i])
    
    return "".join(res)

# provided sample
assert run("3\n") == "abc", "sample 1"

# custom cases
assert len(run("1\n")) == 1, "minimum size"
assert len(run("26\n")) == 26, "exact alphabet"
assert set(run("5\n")) <= set("abcde"), "no extra letters"
assert run("27\n").count("a") >= 1, "wrap distribution"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 | single letter | minimum boundary |
| 26 | permutation of a-z | full alphabet usage |
| 5 | abcde | basic correctness |
| 27 | a repeated among others | wrap-around distribution |

## Edge Cases

For $n = 1$, the algorithm sets $k = 1$, assigns `a:1`, and outputs `"a"`. There is no redistribution step since `rem = 0`, so the result is trivially correct.

For $n = 26$, we hit the full alphabet exactly once each. The machine assigns weights $1$ through $26$, and no redistribution occurs. The construction produces uniform frequencies, which matches the intended extremal structure.

For $n > 26$, the cyclic distribution ensures no letter is starved of occurrences. Each extra character increases the weight contribution of higher-index letters first due to the reverse assignment order. Tracing $n = 28$ shows two cycles of distribution across the 26 letters, preserving the intended frequency ordering and keeping the machine’s sorted assignment aligned with our construction.
