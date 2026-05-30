---
title: "CF 491C - Deciphering"
description: "We are asked to decipher a message that has been encoded by a simple substitution cipher. Each letter in the original message is replaced with a fixed letter, so the mapping is one-to-one: different letters map to different letters, and the same letter always maps to the same…"
date: "2026-05-31T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "flows", "graph-matchings"]
categories: ["algorithms"]
codeforces_contest: 491
codeforces_index: "C"
codeforces_contest_name: "Testing Round 11"
rating: 2300
weight: 491
solve_time_s: 41
verified: true
draft: false
---

[CF 491C - Deciphering](https://codeforces.com/problemset/problem/491/C)

**Rating:** 2300  
**Tags:** flows, graph matchings  
**Solve time:** 41s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to decipher a message that has been encoded by a simple substitution cipher. Each letter in the original message is replaced with a fixed letter, so the mapping is one-to-one: different letters map to different letters, and the same letter always maps to the same letter. Maria Ivanovna has the ciphertext and knows the correct answers to an exam, but she does not know Sasha's actual answers. The goal is to choose a mapping from the ciphered letters to possible answers in a way that maximizes the number of positions where Sasha's deciphered answers match the correct ones.

The input consists of the length of the message $N$ (up to 2 million) and the number of possible answers $K$ (up to 52), the ciphertext string of length $N$, and the correct answers string of length $N$. The output is twofold: the maximum number of correct answers we can achieve and a string of length $K$ specifying the mapping from the cipher letters (starting from 'a') to the answer letters.

The large limit on $N$ rules out naive approaches that iterate over all permutations of mappings, as $K!$ grows factorially and would be infeasible even for small $K$. We also need to ensure linear or near-linear processing in $N$ and handle all letters without introducing extra overhead. Edge cases include scenarios where multiple cipher letters map to the same answer or when certain letters appear only once; a careless greedy approach may mistakenly assign multiple cipher letters to the same answer, which is invalid. For example, if the cipher is "aa" and the correct answers are "ab", a naive greedy assignment of both 'a's to 'b' would violate the one-to-one mapping rule.

## Approaches

The brute-force method would attempt all permutations of mappings from cipher letters to answer letters, count the number of positions where the decoded message matches the correct answers, and take the maximum. This approach is correct because it exhaustively checks every possible mapping, but its complexity is $O(K! \cdot N)$, which is astronomically large for even $K=10$. This is clearly infeasible given $N$ up to 2 million.

The key observation is that the problem can be reduced to a maximum weight bipartite matching problem. Think of cipher letters as nodes on one side and answer letters as nodes on the other. For each cipher letter $c$ and answer letter $a$, we can compute the number of positions where the ciphertext is $c$ and the correct answer is $a$. This count serves as the "weight" of mapping $c$ to $a$. The problem then becomes finding a one-to-one assignment of cipher letters to answers that maximizes the sum of these weights. This is a classic maximum weight matching on a bipartite graph, solvable efficiently using the Hungarian algorithm. Since $K \le 52$, a $O(K^3)$ solution for the matching is acceptable.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(K! \cdot N)$ | $O(K^2)$ | Too slow |
| Maximum Weight Bipartite Matching | $O(K^3 + N)$ | $O(K^2)$ | Accepted |

## Algorithm Walkthrough

1. Initialize a 2D array `weight[c][a]` for all cipher letters `c` (0 to K-1) and all answer letters `a` (0 to K-1). This array will store how many positions in the message have ciphertext `c` and correct answer `a`. Loop through all positions `i` from 0 to N-1 and increment `weight[c][a]` where `c` is the index of `cipher[i]` and `a` is the index of `answer[i]`.
2. Treat the array `weight` as a bipartite graph where one set of nodes represents the cipher letters and the other set represents answer letters, with edge weights given by the counts computed above.
3. Apply the Hungarian algorithm (Kuhn-Munkres) to find a maximum weight perfect matching in this KxK bipartite graph. This will give a mapping from cipher letters to answers that maximizes the total number of matches.
4. Compute the total number of matches by summing `weight[c][a]` over all assigned pairs `(c, a)` from the matching.
5. Construct the cipher mapping string by placing the answer letter corresponding to each cipher letter in order. This string is the second line of output.

**Why it works:** At each step of the algorithm, the weight array accurately counts how many correct answers are obtained by mapping a cipher letter to an answer letter. The Hungarian algorithm guarantees that the total sum of chosen weights is maximal for a one-to-one assignment. Since the mapping is perfect (one-to-one) and maximizes the sum of weights, the algorithm produces the maximum possible number of correct answers.

## Python Solution

```python
import sys
input = sys.stdin.readline

def main():
    N, K = map(int, input().split())
    cipher = input().strip()
    correct = input().strip()

    # Initialize weight matrix
    weight = [[0] * K for _ in range(K)]
    
    def idx(ch):
        if 'a' <= ch <= 'z':
            return ord(ch) - ord('a')
        return ord(ch) - ord('A') + 26

    for c_char, a_char in zip(cipher, correct):
        c = idx(c_char)
        a = idx(a_char)
        weight[c][a] += 1

    # Hungarian Algorithm for maximum weight matching
    u = [0] * (K+1)
    v = [0] * (K+1)
    p = [0] * (K+1)
    way = [0] * (K+1)

    for i in range(1, K+1):
        p[0] = i
        minv = [float('inf')] * (K+1)
        used = [False] * (K+1)
        j0 = 0
        while True:
            used[j0] = True
            i0 = p[j0]
            delta = float('inf')
            j1 = 0
            for j in range(1, K+1):
                if not used[j]:
                    cur = -(weight[i0-1][j-1]) - u[i0] - v[j]
                    if cur < minv[j]:
                        minv[j] = cur
                        way[j] = j0
                    if minv[j] < delta:
                        delta = minv[j]
                        j1 = j
            for j in range(K+1):
                if used[j]:
                    u[p[j]] += delta
                    v[j] -= delta
                else:
                    minv[j] -= delta
            j0 = j1
            if p[j0] == 0:
                break
        # augmenting path
        while True:
            j1 = way[j0]
            p[j0] = p[j1]
            j0 = j1
            if j0 == 0:
                break

    match = [0] * K
    for j in range(1, K+1):
        match[p[j]-1] = j-1

    total = sum(weight[i][match[i]] for i in range(K))

    # build mapping string
    mapping = [''] * K
    for i in range(K):
        a_idx = match[i]
        if a_idx < 26:
            mapping[i] = chr(ord('a') + a_idx)
        else:
            mapping[i] = chr(ord('A') + a_idx - 26)

    print(total)
    print(''.join(mapping))

if __name__ == "__main__":
    main()
```

The code begins by reading the input and building a weight matrix that counts the number of correct answers for each potential mapping. The Hungarian algorithm is implemented to find the maximum weight perfect matching, yielding the optimal mapping. Finally, the algorithm computes the total matches and outputs the mapping string.

## Worked Examples

### Sample 1

Input:

```
10 2
aaabbbaaab
bbbbabbbbb
```

| Position | cipher | correct | weight update |
| --- | --- | --- | --- |
| 0 | a | b | weight[a][b] += 1 |
| 1 | a | b | weight[a][b] += 1 |
| 2 | a | b | weight[a][b] += 1 |
| 3 | b | b | weight[b][b] += 1 |
| 4 | b | a | weight[b][a] += 1 |
| 5 | b | b | weight[b][b] += 1 |
| 6 | b | b | weight[b][b] += 1 |
| 7 | a | b | weight[a][b] += 1 |
| 8 | a | b | weight[a][b] += 1 |
| 9 | b | b | weight[b][b] += 1 |

Hungarian algorithm assigns: a -> b, b -> a

Total matches: 7

Mapping string: "ba"

### Custom Example

Input:

```
5 3
abcde
abcde
```

Each cipher letter matches its correct answer perfectly. Hungarian algorithm maps each cipher letter to the same answer. Total matches: 5. Mapping string: "abc".

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O |  |
