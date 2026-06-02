---
title: "CF 176A - Trading Business"
description: "We have several planets. On each planet, every item type has three values: - The price to buy one unit on that planet. - The price at which that planet buys one unit from us. - The number of units available for purchase."
date: "2026-06-02T17:04:00+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "sortings"]
categories: ["algorithms"]
codeforces_contest: 176
codeforces_index: "A"
codeforces_contest_name: "Croc Champ 2012 - Round 2"
rating: 1200
weight: 176
solve_time_s: 48
verified: false
draft: false
---

[CF 176A - Trading Business](https://codeforces.com/problemset/problem/176/A)

**Rating:** 1200  
**Tags:** greedy, sortings  
**Solve time:** 48s  
**Verified:** no  

## Solution
## Problem Understanding

We have several planets. On each planet, every item type has three values:

- The price to buy one unit on that planet.
- The price at which that planet buys one unit from us.
- The number of units available for purchase.

Qwerty chooses exactly one planet where all purchases are made and exactly one planet where all sales are made. The buying and selling happen only once. He may buy any subset of available items, subject to the ship capacity limit `k`.

If an item of type `j` is bought on planet `A` and sold on planet `B`, the profit from one unit is:

`profit = sell_price[B][j] - buy_price[A][j]`

The goal is to maximize total profit.

The first observation is that the actual amount of money required for buying does not matter. The loan has no interest, so only net profit matters. We only care about which items generate positive profit and how many of them we can carry.

The constraints are surprisingly small. There are at most 10 planets and at most 100 item types. The cargo capacity is at most 100. A solution that examines every ordered pair of planets is completely reasonable because there are at most `10 * 10 = 100` such pairs.

The capacity bound of 100 is the most important number. It suggests that algorithms proportional to `k`, `mk`, or even `nmk` are easily affordable. On the other hand, trying all subsets of item types would be impossible because `m` can reach 100.

A subtle point is that items are divisible only into integer units. If one profitable trade allows buying 50 copies and another allows buying 30 copies, we cannot simply take both entirely when `k = 60`. We must choose the best individual units.

Another easy mistake is assuming we should only consider different planets for buying and selling. The statement does not forbid using the same planet for both actions. Such a choice simply produces non-positive profit because every selling price is strictly smaller than the corresponding buying price, but the algorithm should still handle it naturally.

Consider:

```
2 1 1
A
10 5 1
B
20 15 1
```

Buying on A and selling on B yields profit `15 - 10 = 5`, so the answer is 5.

A careless solution that compares only total prices or only item types could miss this profitable trade.

Another edge case occurs when every possible transaction loses money:

```
2 1 10
A
```
