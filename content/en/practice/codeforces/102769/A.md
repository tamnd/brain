---
title: "CF 102769A - A Greeting from Qinhuangdao"
description: "We have a container holding red and blue balls. The number of red balls is r, and the number of blue balls is b. Two balls are picked uniformly at random without replacement, meaning every pair of balls has the same chance of being chosen."
date: "2026-07-28T23:17:52+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102769
codeforces_index: "A"
codeforces_contest_name: "2020 China Collegiate Programming Contest Qinhuangdao Site"
rating: 0
weight: 102769
solve_time_s: 55
verified: false
draft: false
---

[CF 102769A - A Greeting from Qinhuangdao](https://codeforces.com/problemset/problem/102769/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 55s  
**Verified:** no  

## Solution
## Problem Understanding

We have a container holding red and blue balls. The number of red balls is `r`, and the number of blue balls is `b`. Two balls are picked uniformly at random without replacement, meaning every pair of balls has the same chance of being chosen. The task is to find the probability that both chosen balls are red and print it as a simplified fraction.

The key part is translating the random experiment into counting. The total number of possible pairs comes from choosing any two balls out of all available balls. Since there are `r + b` balls, the total number of outcomes is:

$$\binom{r+b}{2}$$

The successful outcomes are the pairs containing only red balls. There are `r` red balls, so the number of successful pairs is:

$$\binom{r}{2}$$

The answer is the ratio between these two quantities:

$$\frac{\binom{r}{2}}{\binom{r+b}{2}}$$

The constraints are small, with at most 10 test cases and each color count not exceeding 100. This means even direct arithmetic is enough. There is no need for advanced algorithms or large data structures. The main challenge is handling the probability calculation correctly and reducing the fraction.

A careless solution can fail by treating the two draws as independent. For example, with input:

```
2 1
```

There are three balls, two red and one blue. The probability of getting two red balls is not:

$$\frac{2}{3} \times \frac{2}{3}$$

because after selecting one red ball, the number of remaining red balls changes. The correct calculation is:

$$\frac{\binom{2}{2}}{\binom{3}{2}}=\frac{1}{3}$$

Another common mistake is forgetting that the answer must be reduced. For:

```
8 8
```

the raw fraction is:

$$\frac{\binom{8}{2}}{\binom{16}{2}}=\frac{28}{120}$$

which must become:

$$\frac{7}{30}$$

Printing `28/120` would be mathematically equivalent but rejected.

## Approaches

The straightforward approach is to count all possible pairs and all successful pairs, then simplify the resulting fraction. The brute-force version would literally enumerate every pair of balls, checking whether both selected balls are red. This is correct because every possible selection is considered exactly once.

However, this interpretation is unnecessary. If there are up to 200 balls, enumerating all pairs means checking around:

$$\binom{200}{2}=19900$$

pairs for a single case. With these constraints it would still pass, but it ignores the mathematical structure of the problem. If the same idea were extended to much larger inputs, the pair enumeration would quickly become the bottleneck.

The useful observation is that the balls are identical except for their colors. We do not care which specific red ball was chosen, only how many ways exist to choose two red balls. Combinations give this count immediately.

The brute-force method works because every pair is independent and easy to classify, but the problem only asks for the number of pairs, not the pairs themselves. The observation that combinations already represent the number of possible selections reduces the entire problem to computing two values and simplifying their ratio.

The fraction reduction is necessary because the output requires an irreducible fraction. Computing the greatest common divisor of the numerator and denominator gives the exact amount by which both values should be divided.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O((r+b)^2) | O(1) | Works for given limits, but unnecessary |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Compute the number of successful selections. Two red balls can be chosen from `r` red balls in:

$$\frac{r(r-1)}{2}$$

ways. This is the numerator of the probability because every successful outcome contains exactly two red balls.

1. Compute the total number of possible selections. Two balls can be chosen from all `r+b` balls in:

$$\frac{(r+b)(r+b-1)}{2}$$

ways. This is the denominator because every possible pair has equal probability.

1. Find the greatest common divisor of the numerator and denominator. Dividing both values by this number produces the unique irreducible representation of the same probability.
2. Output the reduced numerator and denominator in the required case format.

Why it works:

The probability of an event is the number of favorable outcomes divided by the number of all outcomes when every outcome is equally likely. Every possible pair of balls has the same probability of being selected, so counting pairs is enough. The numerator counts exactly the pairs containing two red balls, while the denominator counts every possible pair. Reducing the fraction does not change its value, so the produced fraction represents the required probability in the required format.
