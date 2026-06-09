---
title: "CF 1895D - XOR Construction"
description: "We are given the XOR values between consecutive elements of an unknown permutation. Let the required permutation be $b$. For every adjacent pair, we know $$bi oplus b{i+1} = ai.$$ The array $b$ must contain every integer from $0$ to $n-1$ exactly once."
date: "2026-06-08T21:46:38+07:00"
tags: ["codeforces", "competitive-programming", "bitmasks", "constructive-algorithms", "data-structures", "math", "string-suffix-structures", "trees"]
categories: ["algorithms"]
codeforces_contest: 1895
codeforces_index: "D"
codeforces_contest_name: "Educational Codeforces Round 157 (Rated for Div. 2)"
rating: 1900
weight: 1895
solve_time_s: 169
verified: true
draft: false
---

[CF 1895D - XOR Construction](https://codeforces.com/problemset/problem/1895/D)

**Rating:** 1900  
**Tags:** bitmasks, constructive algorithms, data structures, math, string suffix structures, trees  
**Solve time:** 2m 49s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given the XOR values between consecutive elements of an unknown permutation.

Let the required permutation be $b$. For every adjacent pair, we know

$$b_i \oplus b_{i+1} = a_i.$$

The array $b$ must contain every integer from $0$ to $n-1$ exactly once. The input guarantees that at least one such permutation exists.

The first observation is that once $b_1$ is fixed, every other element becomes determined. From

$$b_2 = b_1 \oplus a_1,$$

and then

$$b_3 = b_2 \oplus a_2,$$

and so on. The entire array is a function of a single unknown starting value.

The constraint $n \le 2 \cdot 10^5$ immediately rules out anything quadratic. An $O(n^2)$ verification process would require around $4 \cdot 10^{10}$ operations in the worst case, which is far beyond the time limit. We should expect an $O(n)$ or $O(n \log n)$ solution.

The tricky part is finding the correct value of $b_1$. A naive implementation might try every possible starting value and check whether the resulting sequence is a permutation. That works conceptually but becomes too slow.

Several edge cases are easy to mishandle.

Consider:

```
n = 2
a = [1]
```

The valid permutation is either $[0,1]$ or $[1,0]$. A solution that assumes $b_1=0$ without verification would fail whenever the true starting value is different.

Consider:

```
n = 4
a = [2,1,2]
```

If we choose $b_1=0$, we obtain

```
0 2 3 1
```

which is valid. But in many inputs, choosing $0$ creates duplicate values. The fact that the generated numbers stay inside a small range does not imply they form a permutation.

Another subtle case appears when XOR prefixes repeat:

```
prefixes = [0, 5, 2, 5]
```

A careless argument might conclude that duplicates are unavoidable. In reality, shifting every prefix by a suitable XOR value changes all numbers simultaneously, and duplicates depend on the chosen starting value. The correct solution must reason about the whole set of values, not individual positions.

## Approaches

The brute-force idea follows directly from the observation that fixing $b_1$ determines the entire permutation.

Define prefix XORs:

$$p_1 = 0,$$

and

$$p_i = a_1 \oplus a_2 \oplus \cdots \oplus a_{i-1}.$$

Then every element satisfies

$$b_i = b_1 \oplus p_i.$$

If we try every possible value of $b_1$ from $0$ to $n-1$, we can generate all $n$ values and check whether they form exactly the set $\{0,1,\dots,n-1\}$.

The reasoning is correct because every valid permutation must arise from one of those starting values. The problem is complexity. There are $n$ candidates for $b_1$, and each verification costs $O(n)$, leading to $O(n^2)$.

The key observation is that the input is guaranteed to have a solution. Instead of testing all possible starts, we can derive the correct one directly.

Let

$$p_1,p_2,\dots,p_n$$

be the prefix XOR values with $p_1=0$.

Since

$$b_i=b_1\oplus p_i,$$

the set

$$\{b_1\oplus p_i\}$$

must equal exactly

$$\{0,1,\dots,n-1\}.$$

Now focus on the binary trie interpretation.

For a candidate value $x$, the largest number among

$$x \oplus p_i$$

can be found efficiently with a trie. If the resulting set is exactly $[0,n-1]$, then every value must be below $n$. Hence

$$\max_i (x \oplus p_i) < n.$$

Because a solution is guaranteed to exist, the correct starting value is precisely the value $x$ for which the maximum XOR with any prefix becomes $n-1$.

The original Codeforces solution inserts all prefix XORs into a binary trie and finds the value $x$ whose maximum XOR against the set equals $n-1$. That value becomes $b_1$. Once $b_1$ is known, reconstructing the entire permutation is immediate.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^2)$ | $O(n)$ | Too slow |
| Optimal | $O(n \log V)$ | $O(n \log V)$ | Accepted |

Here $V$ is the maximum possible XOR value, which is below $2^{18}$ for this problem.

## Algorithm Walkthrough

1. Compute prefix XORs.

Let $p_1=0$. For each position, append the cumulative XOR of all previous $a$-values.
2. Insert all prefix XORs into a binary trie.

The trie allows us to answer maximum-XOR queries in $O(\log V)$.
3. For every value $x$ from $0$ to $n-1$, query the trie for

$$\max_i (x \oplus p_i).$$

This is the standard maximum XOR query.
4. Find the unique value $x$ whose maximum XOR equals $n-1$.

Because the final permutation must contain every number from $0$ to $n-1$, the largest generated value is exactly $n-1$. The guaranteed existence of a solution implies that the correct starting value satisfies this condition.
5. Set $b_1=x$.
6. Reconstruct the permutation using

$$b_i = x \oplus p_i.$$
7. Output the resulting sequence.

### Why it works

The prefix XOR representation gives

$$b_i=b_1\oplus p_i.$$

Thus every valid permutation is obtained by XOR-shifting the entire prefix set by a single value.

Suppose $x=b_1$. Since the resulting numbers are exactly $\{0,\dots,n-1\}$, their maximum equals $n-1$. Hence

$$\max_i(x\oplus p_i)=n-1.$$

For any other candidate, the shifted set cannot equal the desired permutation, so the maximum-XOR value differs. The trie allows us to identify the correct shift efficiently. After recovering $b_1$, every remaining element follows from the defining XOR relations, so the reconstructed array is exactly the required permutation.

## Python Solution

```python
import sys
input = sys.stdin.readline

class TrieNode:
    __slots__ = ("ch",)

    def __init__(self):
        self.ch = [-1, -1]

trie = [TrieNode()]

def add(x):
    node = 0
    for bit in range(20, -1, -1):
        b = (x >> bit) & 1
        if trie[node].ch[b] == -1:
            trie[node].ch[b] = len(trie)
            trie.append(TrieNode())
        node = trie[node].ch[b]

def max_xor(x):
    node = 0
    ans = 0
    for bit in range(20, -1, -1):
        b = (x >> bit) & 1
        want = b ^ 1
        if trie[node].ch[want] != -1:
            ans |= 1 << bit
            node = trie[node].ch[want]
        else:
            node = trie[node].ch[b]
    return ans

def solve():
    n = int(input())
    a = list(map(int, input().split()))

    pref = [0]
    cur = 0
    for x in a:
        cur ^= x
        pref.append(cur)

    for x in pref:
        add(x)

    start = 0
    for x in range(n):
        if max_xor(x) == n - 1:
            start = x
            break

    ans = [start ^ p for p in pref]
    print(*ans)

solve()
```

The first part builds the prefix XOR array. The relation

$$b_i=b_1\oplus p_i$$

is the central structural fact of the problem, so everything after that operates on the prefix values.

The trie stores all prefixes. Each level corresponds to one bit. A maximum-XOR query greedily follows the opposite bit whenever possible, which is the standard proof for maximum XOR in a binary trie.

The loop over all candidates $x \in [0,n-1]$ searches for the starting value whose maximum XOR against the prefix set equals $n-1$. The problem guarantee ensures such a value exists.

Finally, the answer is reconstructed directly as $x \oplus p_i$. No additional verification is necessary.

The implementation uses 21 bits, which comfortably covers all values in the problem. XOR operations never overflow in Python, so there are no integer-size concerns.

## Worked Examples

### Example 1

Input:

```
4
2 1 2
```

Prefix XORs:

| Step | Current a | Prefix XOR |
| --- | --- | --- |
| Start | - | 0 |
| 1 | 2 | 2 |
| 2 | 1 | 3 |
| 3 | 2 | 1 |

So:

```
pref = [0, 2, 3, 1]
```

Candidate search:

| x | max(x XOR pref[i]) |
| --- | --- |
| 0 | 3 |
| 1 | 3 |
| 2 | 2 |
| 3 | 3 |

The first valid choice is $x=0$.

Reconstruction:

| i | pref[i] | b[i] = 0 XOR pref[i] |
| --- | --- | --- |
| 1 | 0 | 0 |
| 2 | 2 | 2 |
| 3 | 3 | 3 |
| 4 | 1 | 1 |

Output:

```
0 2 3 1
```

This trace demonstrates the core idea that the entire permutation is simply a shifted version of the prefix XOR set.

### Example 2

Input:

```
2
1
```

Prefix XORs:

| Step | Prefix XOR |
| --- | --- |
| Start | 0 |
| After a[1] | 1 |

So:

```
pref = [0, 1]
```

Candidate search:

| x | max(x XOR pref[i]) |
| --- | --- |
| 0 | 1 |
| 1 | 1 |

Choose $x=0$.

Reconstruction:

| i | pref[i] | Result |
| --- | --- | --- |
| 1 | 0 | 0 |
| 2 | 1 | 1 |

Output:

```
0 1
```

This example shows the smallest possible input and confirms that the reconstruction formula works even when only one XOR constraint exists.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \log V)$ | Each prefix insertion and each query traverses all trie levels |
| Space | $O(n \log V)$ | Trie nodes created while storing all prefixes |

For this problem, $V$ is below $2^{21}$, so $\log V$ is effectively a small constant. With $n \le 2 \cdot 10^5$, the solution easily fits within the time and memory limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def solve():
    class TrieNode:
        __slots__ = ("ch",)

        def __init__(self):
            self.ch = [-1, -1]

    trie = [TrieNode()]

    def add(x):
        node = 0
        for bit in range(20, -1, -1):
            b = (x >> bit) & 1
            if trie[node].ch[b] == -1:
                trie[node].ch[b] = len(trie)
                trie.append(TrieNode())
            node = trie[node].ch[b]

    def max_xor(x):
        node = 0
        ans = 0
        for bit in range(20, -1, -1):
            b = (x >> bit) & 1
            want = b ^ 1
            if trie[node].ch[want] != -1:
                ans |= 1 << bit
                node = trie[node].ch[want]
            else:
                node = trie[node].ch[b]
        return ans

    n = int(input())
    a = list(map(int, input().split()))

    pref = [0]
    cur = 0
    for x in a:
        cur ^= x
        pref.append(cur)

    for x in pref:
        add(x)

    start = 0
    for x in range(n):
        if max_xor(x) == n - 1:
            start = x
            break

    ans = [start ^ p for p in pref]
    print(*ans)

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out

    global input
    input = sys.stdin.readline

    solve()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return out.getvalue().strip()

# provided sample
assert run("4\n2 1 2\n") == "0 2 3 1"

# minimum size
assert run
```
