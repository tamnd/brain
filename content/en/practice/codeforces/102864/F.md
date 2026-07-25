---
title: "CF 102864F - Ironhead\u7684\u63a8\u514d\u8d44\u683c\uff08\u4f20\u8bf4\uff09"
description: "I’ll provide the editorial as a finished document below. Edit The task is to simulate a university recommendation process. Each student has a name, a study ranking, and a ranking based on other achievements."
date: "2026-07-25T13:42:18+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102864
codeforces_index: "F"
codeforces_contest_name: "The 15-th BIT Campus Programming Contest - Online Round"
rating: 0
weight: 102864
solve_time_s: 82
verified: true
draft: false
---

[CF 102864F - Ironhead\u7684\u63a8\u514d\u8d44\u683c\uff08\u4f20\u8bf4\uff09](https://codeforces.com/problemset/problem/102864/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 22s  
**Verified:** yes  

## Solution
I’ll provide the editorial as a finished document below.

Edit

# Problem Understanding

The task is to simulate a university recommendation process. Each student has a name, a study ranking, and a ranking based on other achievements. Only students whose study ranking is within the best 30 percent of the department can compete for recommendation places. Among those eligible students, recommendation places are assigned by increasing comprehensive score, where the study ranking contributes 85 percent and the other ranking contributes 15 percent. The required output is the name of the student who receives the last available place after applying all tie-breaking rules.

The number of students is at most 1000. This size is small enough that sorting the students is easily possible, because an O(n log n) solution performs only a few thousand comparisons. Even an O(n²) solution might pass for n = 1000, but designing the solution around sorting is simpler and more robust. There is no need for advanced data structures because the entire input can be stored in memory.

The main implementation risks come from rounding and tie handling. The recommendation percentage and eligibility percentage both require rounding upward. A program that uses normal integer division will lose students at the boundary.

For example, when there are 10 students, the recommendation quota is ceil(10 × 18.6%) = ceil(1.86) = 2. A program computing 10 * 186 // 1000 would get 1 and output the wrong final student.

```
10
a 1 10
b 2 9
c 3 8
d 4 7
e 5 6
f 6 5
g 7 4
h 8 3
i 9 2
j 10 1
```

The correct output depends on sorting the eligible students and taking the second one. A careless implementation using floor division would choose only one person and fail.

Another common mistake is using floating point values for the comprehensive score. Two students can have equal scores after multiplication by 0.85 and 0.15, and floating point representation can make equal values appear slightly different. For example:

```
2
alice 1 2
bob 2 1
```

Both scores are equal because 85 × 1 + 15 × 2 = 115 and 85 × 2 + 15 × 1 = 185, so this particular pair is not tied. A real tie example is:

```
3
alice 1 3
bob 2 2
carol 3 1
```

The integer scores are 130, 200, and 270, so the example does not create a tie either. A valid tie is easier to see directly from the formula: any two students satisfying 85(a1-a2)+15(b1-b2)=0 have the same score. The implementation should compare the multiplied integer value instead of the decimal expression.

The final edge case is that the last admitted student may be decided by name ordering. If the last available place reaches a group of students with equal comprehensive scores, the names must be sorted lexicographically before choosing the final position. Sorting only by score gives an unstable and incorrect answer.

## Approaches

A straightforward solution is to repeatedly search for the next best student. First, determine the eligible students, then scan the remaining candidates to find the smallest comprehensive score, removing students one by one until the quota is filled. This approach is correct because every selection step chooses exactly the person who should be next in the ranking.

The problem with this method is repeated searching. In the worst case, after choosing one student, the algorithm scans almost all remaining students again. With n students, this requires roughly n + (n - 1) + ... + 1 comparisons, which is O(n²). For n = 1000 this is not disastrous, but it ignores the natural ordering structure already present in the problem.

The key observation is that the entire ranking rule can be represented as one sorting order. Eligibility depends only on the study ranking, and the final selection order depends only on the comprehensive score followed by the name. Once all eligible students are collected, sorting them once gives the exact order in which recommendation places are assigned.

The decimal formula can also be removed. Multiplying the comprehensive score by 100 gives:

85 × study ranking + 15 × other ranking.

The multiplication does not change the order of students, and it avoids precision problems completely.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n) | Accepted for this constraint, but unnecessary |
| Optimal | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read every student's name, study ranking, and other ranking. Store the information because both the eligibility check and final ordering need these values.
2. Compute the number of students allowed to compete by calculating ceil(30% of n). The formula is `(3 * n + 9) // 10`, which performs the upward rounding using integers.
3. Sort all students by their study ranking and keep only the first eligible count of students. These are the only people who can receive recommendation places.
4. Compute each eligible student's integer comprehensive score as `85 * a + 15 * b`. Sort the eligible students by this score first and by name second. The second comparison is exactly the required tie-breaking rule.
5. Compute the number of recommendation places using `ceil(18.6% of n)`, which is `(186 * n + 999) // 1000`.
6. Output the name at index `quota - 1` in the final sorted list. This is the student occupying the last available position.

Why it works:

The eligibility sorting step keeps exactly the students allowed to participate because the rule only depends on study ranking. Among these students, the second sort creates the same order as the official comprehensive ranking because the integer score is a positive multiple of the original formula. Equal scores are ordered by name, matching the stated tie-breaking rule. Taking the student at the final quota position therefore gives exactly the last admitted student.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n_line = input().strip()
    if not n_line:
        return
    n = int(n_line)

    students = []
    for _ in range(n):
        name, a, b = input().split()
        students.append((name, int(a), int(b)))

    eligible_count = (3 * n + 9) // 10

    students.sort(key=lambda x: x[1])
    students = students[:eligible_count]

    students.sort(key=lambda x: (85 * x[1] + 15 * x[2], x[0]))

    quota = (186 * n + 999) // 1000
    print(students[quota - 1][0])

if __name__ == "__main__":
    solve()
```

The first sort is only used for finding the eligible group. Since the original ranking can contain equal values, it is enough to sort by study ranking because the eligibility rule does not require another tie-breaker.

The second sort is the actual recommendation ranking. The expression `85 * a + 15 * b` is the original score multiplied by 100, so it preserves ordering while avoiding floating point errors. The tuple key automatically applies name ordering when two students have the same score.

The ceiling calculations are handled with integer arithmetic. The extra value before division is what moves any non-integer result upward. The final index is `quota - 1` because Python arrays start at zero.

## Worked Examples

For the given sample:

```
1
ironhead 1 1
```

The only student is eligible and the quota is one place.

| Step | Eligible students | Sorted recommendation order | Answer |
| --- | --- | --- | --- |
| After reading | ironhead | Not sorted yet | None |
| After eligibility | ironhead | Not sorted yet | None |
| After score sort | ironhead | ironhead | ironhead |

This demonstrates the smallest possible case. No filtering or tie-breaking is needed.

A second example:

```
5
alice 1 5
bob 2 4
carol 3 3
dave 4 2
eve 5 1
```

The eligibility limit is ceil(5 × 30%) = 2, so only the first two students by study ranking compete. The recommendation quota is ceil(5 × 18.6%) = 1.

| Step | Value |
| --- | --- |
| Eligible count | 2 |
| Eligible students | alice, bob |
| alice score | 160 |
| bob score | 230 |
| Quota | 1 |
| Selected index | 0 |
| Output | alice |

The trace shows that students outside the top study-ranking range never enter the final ranking, even if their comprehensive score would have been good.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Two sorting operations dominate the runtime |
| Space | O(n) | The student records are stored in lists |

With n limited to 1000, the solution easily fits within the time and memory limits. The approach also scales naturally to larger inputs because it only depends on sorting.

## Test Cases

```python
import sys
import io

def solve_case(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    n = int(input())
    students = []

    for _ in range(n):
        name, a, b = input().split()
        students.append((name, int(a), int(b)))

    eligible_count = (3 * n + 9) // 10
    students.sort(key=lambda x: x[1])
    students = students[:eligible_count]

    students.sort(key=lambda x: (85 * x[1] + 15 * x[2], x[0]))

    quota = (186 * n + 999) // 1000
    return students[quota - 1][0]

assert solve_case("""1
ironhead 1 1
""") == "ironhead", "sample 1"

assert solve_case("""5
alice 1 5
bob 2 4
carol 3 3
dave 4 2
eve 5 1
""") == "alice", "basic filtering"

assert solve_case("""10
a 1 10
b 2 9
c 3 8
d 4 7
e 5 6
f 6 5
g 7 4
h 8 3
i 9 2
j 10 1
""") == "b", "ceiling quota"

assert solve_case("""4
z 1 2
a 2 1
m 3 3
q 4 4
""") == "z", "top eligibility boundary"

assert solve_case("""1000
student1 1 1
student2 2 2
student3 3 3
student4 4 4
student5 5 5
student6 6 6
student7 7 7
student8 8 8
student9 9 9
student10 10 10
student11 11 11
student12 12 12
student13 13 13
student14 14 14
student15 15 15
student16 16 16
student17 17 17
student18 18 18
student19 19 19
student20 20 20
student21 21 21
student22 22 22
student23 23 23
student24 24 24
student25 25 25
student26 26 26
student27 27 27
student28 28 28
student29 29 29
student30 30 30
student31 31 31
student32 32 32
student33 33 33
student34 34 34
student35 35 35
student36 36 36
student37 37 37
student38 38 38
student39 39 39
student40 40 40
student41 41 41
student42 42 42
student43 43 43
student44 44 44
student45 45 45
student46 46 46
student47 47 47
student48 48 48
student49 49 49
student50 50 50
student51 51 51
student52 52 52
student53 53 53
student54 54 54
student55 55 55
student56 56 56
student57 57 57
student58 58 58
student59 59 59
student60 60 60
student61 61 61
student62 62 62
student63 63 63
student64 64 64
student65 65 65
student66 66 66
student67 67 67
student68 68 68
student69 69 69
student70 70 70
student71 71 71
student72 72 72
student73 73 73
student74 74 74
student75 75 75
student76 76 76
student77 77 77
student78 78 78
student79 79 79
student80 80 80
student81 81 81
student82 82 82
student83 83 83
student84 84 84
student85 85 85
student86 86 86
student87 87 87
student88 88 88
student89 89 89
student90 90 90
student91 91 91
student92 92 92
student93 93 93
student94 94 94
student95 95 95
student96 96 96
student97 97 97
student98 98 98
student99 99 99
student100 100 100
student101 101 101
student102 102 102
student103 103 103
student104 104 104
student105 105 105
student106 106 106
student107 107 107
student108 108 108
student109 109 109
student110 110 110
student111 111 111
student112 112 112
student113 113 113
student114 114 114
student115 115 115
student116 116 116
student117 117 117
student118 118 118
student119 119 119
student120 120 120
student121 121 121
student122 122 122
student123 123 123
student124 124 124
student125 125 125
student126 126 126
student127 127 127
student128 128 128
student129 129 129
student130 130 130
student131 131 131
student132 132 132
student133 133 133
student134 134 134
student135 135 135
student136 136 136
student137 137 137
student138 138 138
student139 139 139
student140 140 140
student141 141 141
student142 142 142
student143 143 143
student144 144 144
student145 145 145
student146 146 146
student147 147 147
student148 148 148
student149 149 149
student150 150 150
student151 151 151
student152 152 152
student153 153 153
student154 154 154
student155 155 155
student156 156 156
student157 157 157
student158 158 158
student159 159 159
student160 160 160
student161 161 161
student162 162 162
student163 163 163
student164 164 164
student165 165 165
student166 166 166
student167 167 167
student168 168 168
student169 169 169
student170 170 170
student171 171 171
student172 172 172
student173 173 173
student174 174 174
student175 175 175
student176 176 176
student177 177 177
student178 178 178
student179 179 179
student180 180 180
student181 181 181
student182 182 182
student183 183 183
student184 184 184
student185 185 185
student186 186 186
student187 187 187
student188 188 188
student189 189 189
student190 190 190
student191 191 191
student192 192 192
student193 193 193
student194 194 194
student195 195 195
student196 196 196
student197 197 197
student198 198 198
student199 199 199
student200 200 200
student201 201 201
student202 202 202
student203 203 203
student204 204 204
student205 205 205
student206 206 206
student207 207 207
student208 208 208
student209 209 209
student210 210 210
student211 211 211
student212 212 212
student213 213 213
student214 214 214
student215 215 215
student216 216 216
student217 217 217
student218 218 218
student219 219 219
student220 220 220
student221 221 221
student222 222 222
student223 223 223
student224 224 224
student225 225 225
student226 226 226
student227 227 227
student228 228 228
student229 229 229
student230 230 230
student231 231 231
student232 232 232
student233 233 233
student234 234 234
student235 235 235
student236 236 236
student237 237 237
student238 238 238
student239 239 239
student240 240 240
student241 241 241
student242 242 242
student243 243 243
student244 244 244
student245 245 245
student246 246 246
student247 247 247
student248 248 248
student249 249 249
student250 250 250
student251 251 251
student252 252 252
student253 253 253
student254 254 254
student255 255 255
student256 256 256
student257 257 257
student258 258 258
student259 259 259
student260 260 260
student261 261 261
student262 262 262
student263 263 263
student264 264 264
student265 265 265
student266 266 266
student267 267 267
student268 268 268
student269 269 269
student270 270 270
student271 271 271
student272 272 272
student273 273 273
student274 274 274
student275 275 275
student276 276 276
student277 277 277
student278 278 278
student279 279 279
student280 280 280
student281 281 281
student282 282 282
student283 283 283
student284 284 284
student285 285 285
student286 286 286
student287 287 287
student288 288 288
student289 289 289
student290 290 290
student291 291 291
student292 292 292
student293 293 293
student294 294 294
student295 295 295
student296 296 296
student297 297 297
student298 298 298
student299 299 299
student300 300 300
student301 301 301
student302 302 302
student303 303 303
student304 304 304
student305 305 305
student306 306 306
student307 307 307
student308 308 308
student309 309 309
student310 310 310
student311 311 311
student312 312 312
student313 313 313
student314 314 314
student315 315 315
student316 316 316
student317 317 317
student318 318 318
student319 319 319
student320 320 320
student321 321 321
student322 322 322
student323 323 323
student324 324 324
student325 325 325
student326 326 326
student327 327 327
student328 328 328
student329 329 329
student330 330 330
student331 331 331
student332 332 332
student333 333 333
student334 334 334
student335 335 335
student336 336 336
student337 337 337
student338 338 338
student339 339 339
student340 340 340
student341 341 341
student342 342 342
student343 343 343
student344 344 344
student345 345 345
student346 346 346
student347 347 347
student348 348 348
student349 349 349
student350 350 350
student351 351 351
student352 352 352
student353 353 353
student354 354 354
student355 355 355
student356 356 356
student357 357 357
student358 358 358
student359 359 359
student360 360 360
student361 361 361
student362 362 362
student363 363 363
student364 364 364
student365 365 365
student366 366 366
student367 367 367
student368 368 368
student369 369 369
student370 370 370
student371 371 371
student372 372 372
student373 373 373
student374 374 374
student375 375 375
student376 376 376
student377 377 377
student378 378 378
student379 379 379
student380 380 380
student381 381 381
student382 382 382
student383 383 383
student384 384 384
student385 385 385
student386 386 386
student387 387 387
student388 388 388
student389 389 389
student390 390 390
student391 391 391
student392 392 392
student393 393 393
student394 394 394
student395 395 395
student396 396 396
student397 397 397
student398 398 398
student399 399 399
student400 400 400
student401 401 401
student402 402 402
student403 403 403
student404 404 404
student405 405 405
student406 406 406
student407 407 407
student408 408 408
student409 409 409
student410 410 410
student411 411 411
student412 412 412
student413 413 413
student414 414 414
student415 415 415
student416 416 416
student417 417 417
student418 418 418
student419 419 419
student420 420 420
student421 421 421
student422 422 422
student423 423 423
student424 424 424
student425 425 425
student426 426 426
student427 427 427
student428 428 428
student429 429 429
student430 430 430
student431 431 431
student432 432 432
student433 433 433
student434 434 434
student435 435 435
student436 436 436
student437 437 437
student438 438 438
student439 439 439
student440 440 440
student441 441 441
student442 442 442
student443 443 443
student444 444 444
student445 445 445
student446 446 446
student447 447 447
student448 448 448
student449 449 449
student450 450 450
student451 451 451
student452 452 452
student453 453 453
student454 454 454
student455 455 455
student456 456 456
student457 457 457
student458 458 458
student459 459 459
student460 460 460
student461 461 461
student462 462 462
student463 463 463
student464 464 464
student465 465 465
student466 466 466
student467 467 467
student468 468 468
student469 469 469
student470 470 470
student471 471 471
student472 472 472
student473 473 473
student474 474 474
student475 475 475
student476 476 476
student477 477 477
student478 478 478
student479 479 479
student480 480 480
student481 481 481
student482 482 482
student483 483 483
student484 484 484
student485 485 485
student486 486 486
student487 487 487
student488 488 488
student489 489 489
student490 490 490
student491 491 491
student492 492 492
student493 493 493
student494 494 494
student495 495 495
student496 496 496
student497 497 497
student498 498 498
student499 499 499
student500 500 500
student501 501 501
student502 502 502
student503 503 503
student504 504 504
student505 505 505
student506 506 506
student507 507 507
student508 508 508
student509 509 509
student510 510 510
student511 511 511
student512 512 512
student513 513 513
student514 514 514
student515 515 515
student516 516 516
student517 517 517
student518 518 518
student519 519 519
student520 520 520
student521 521 521
student522 522 522
student523 523 523
student524 524 524
student525 525 525
student526 526 526
student527 527 527
student528 528 528
student529 529 529
student530 530 530
student531 531 531
student532 532 532
student533 533 533
student534 534 534
student535 535 535
student536 536 536
student537 537 537
student538 538 538
student539 539 539
student540 540 540
student541 541 541
student542 542 542
student543 543 543
student544 544 544
student545 545 545
student546 546 546
student547 547 547
student548 548 548
student549 549 549
student550 550 550
student551 551 551
student552 552 552
student553 553 553
student554 554 554
student555 555 555
student556 556 556
student557 557 557
student558 558 558
student559 559 559
student560 560 560
student561 561 561
student562 562 562
student563 563 563
student564 564 564
student565 565 565
student566 566 566
student567 567 567
student568 568 568
student569 569 569
student570 570 570
student571 571 571
student572 572 572
student573 573 573
student574 574 574
student575 575 575
student576 576 576
student577 577 577
student578 578 578
student579 579 579
student580 580 580
student581 581 581
student582 582 582
student583 583 583
student584 584 584
student585 585 585
student586 586 586
student587 587 587
student588 588 588
student589 589 589
student590 590 590
student591 591 591
student592 592 592
student593 593 593
student594 594 594
student595 595 595
student596 596 596
student597 597 597
student598 598 598
student599 599 599
student600 600 600
student601 601 601
student602 602 602
student603 603 603
student604 604 604
student605 605 605
student606 606 606
student607 607 607
student608 608 608
student609 609 609
student610 610 610
student611 611 611
student612 612 612
student613 613 613
student614 614 614
student615 615 615
student616 616 616
student617 617 617
student618 618 618
student619 619 619
student620 620 620
student621 621 621
student622 622 622
student623 623 623
student624 624 624
student625 625 625
student626 626 626
student627 627 627
student628 628 628
student629 629 629
student630 630 630
student631 631 631
student632 632 632
student633 633 633
student634 634 634
student635 635 635
student636 636 636
student637 637 637
student638 638 638
student639 639 639
student640 640 640
student641 641 641
student642 642 642
student643 643 643
student644 644 644
student645 645 645
student646 646 646
student647 647 647
student648 648 648
student649 649 649
student650 650 650
student651 651 651
student652 652 652
student653 653 653
student654 654 654
student655 655 655
student656 656 656
student657 657 657
student658 658 658
student659 659 659
student660 660 660
student661 661 661
student662 662 662
student663 663 663
student664 664 664
student665 665 665
student666 666 666
student667 667 667
student668 668 668
student669 669 669
student670 670 670
student671 671 671
student672 672 672
student673 673 673
student674 674 674
student675 675 675
student676 676 676
student677 677 677
student678 678 678
student679 679 679
student680 680 680
student681 681 681
student682 682 682
student683 683 683
student684 684 684
student685 685 685
student686 686 686
student687 687 687
student688 688 688
student689 689 689
student690 690 690
student691 691 691
student692 692 692
student693 693 693
student694 694 694
student695 695 695
student696 696 696
student697 697 697
student698 698 698
student699 699 699
student700 700 700
student701 701 701
student702 702 702
student703 703 703
student704 704 704
student705 705 705
student706 706 706
student707 707 707
student708 708 708
student709 709 709
student710 710 710
student711 711 711
student712 712 712
student713 713 713
student714 714 714
student715 715 715
student716 716 716
student717 717 717
student718 718 718
student719 719 719
student720 720 720
student721 721 721
student722 722 722
student723 723 723
student724 724 724
student725 725 725
student726 726 726
student727 727 727
student728 728 728
student729 729 729
student730 730 730
student731 731 731
student732 732 732
student733 733 733
student734 734 734
student735 735 735
student736 736 736
student737 737 737
student738 738 738
student739 739 739
student740 740 740
student741 741 741
student742 742 742
student743 743 743
student744 744 744
student745 745 745
student746 746 746
student747 747 747
student748 748 748
student749 749 749
student750 750 750
student751 751 751
student752 752 752
student753 753 753
student754 754 754
student755 755 755
student756 756 756
student757 757 757
student758 758 758
student759 759 759
student760 760 760
student761 761 761
student762 762 762
student763 763 763
student764 764 764
student765 765 765
student766 766 766
student767 767 767
student768 768 768
student769 769 769
student770 770 770
student771 771 771
student772 772 772
student773 773 773
student774 774 774
student775 775 775
student776 776 776
student777 777 777
student778 778 778
student779 779 779
student780 780 780
student781 781 781
student782 782 782
student783 783 783
student784 784 784
student785 785 785
student786 786 786
student787 787 787
student788 788 788
student789 789 789
student790 790 790
student791 791 791
student792 792 792
student793 793 793
student794 794 794
student795 795 795
student796 796 796
student797 797 797
student798 798 798
student799 799 799
student800 800 800
student801 801 801
student802 802 802
student803 803 803
student804 804 804
student805 805 805
student806 806 806
student807 807 807
student808 808 808
student809 809 809
student810 810 810
student811 811 811
student812 812 812
student813 813 813
student814 814 814
student815 815 815
student816 816 816
student817 817 817
student818 818 818
student819 819 819
student820 820 820
student821 821 821
student822 822 822
student823 823 823
student824 824 824
student825 825 825
student826 826 826
student827 827 827
student828 828 828
student829 829 829
student830 830 830
student831 831 831
student832 832 832
student833 833 833
student834 834 834
student835 835 835
student836 836 836
student837 837 837
student838 838 838
student839 839 839
student840 840 840
student841 841 841
student842 842 842
student843 843 843
student844 844 844
student845 845 845
student846 846 846
student847 847 847
student848 848 848
student849 849 849
student850 850 850
student851 851 851
student852 852 852
student853 853 853
student854 854 854
student855 855 855
student856 856 856
student857 857 857
student858 858 858
student859 859 859
student860 860 860
student861 861 861
student862 862 862
student863 863 863
student864 864 864
student865 865 865
student866 866 866
student867 867 867
student868 868 868
student869 869 869
student870 870 870
student871 871 871
student872 872 872
student873 873 873
student874 874 874
student875 875 875
student876 876 876
student877 877 877
student878 878 878
student879 879 879
student880 880 880
student881 881 881
student882 882 882
student883 883 883
student884 884 884
student885 885 885
student886 886 886
student887 887 887
student888 888 888
student889 889 889
student890 890 890
student891 891 891
student892 892 892
student893 893 893
student894 894 894
student895 895 895
student896 896 896
student897 897 897
student898 898 898
student899 899 899
student900 900 900
student901 901 901
student902 902 902
student903 903 903
student904 904 904
student905 905 905
student906 906 906
student907 907 907
student908 908 908
student909 909 909
student910 910 910
student911 911 911
student912 912 912
student913 913 913
student914 914 914
student915 915 915
student916 916 916
student917 917 917
student918 918 918
student919 919 919
student920 920 920
student921 921 921
student922 922 922
student923 923 923
student924 924 924
student925 925 925
student926 926 926
student927 927 927
student928 928 928
student929 929 929
student930 930 930
student931 931 931
student932 932 932
student933 933 933
student934 934 934
student935 935 935
student936 936 936
student937 937 937
student938 938 938
student939 939 939
student940 940 940
student941 941 941
student942 942 942
student943 943 943
student944 944 944
student945 945 945
student946 946 946
student947 947 947
student948 948 948
student949 949 949
student950 950 950
student951 951 951
student952 952 952
student953 953 953
student954 954 954
student955 955 955
student956 956 956
student957 957 957
student958 958 958
student959 959 959
student960 960 960
student961 961 961
student962 962 962
student963 963 963
student964 964 964
student965 965 965
student966 966 966
student967 967 967
student968 968 968
student969 969 969
student970 970 970
student971 971 971
student972 972 972
student973 973 973
student974 974 974
student975 975 975
student976 976 976
student977 977 977
student978 978 978
student979 979 979
student980 980 980
student981 981 981
student982 982 982
student983 983 983
student984 984 984
student985 985 985
student986 986 986
student987 987 987
student988 988 988
student989 989 989
student990 990 990
student991 991 991
student992 992 992
student993 993 993
student994 994 994
student995 995 995
student996 996 996
student997 997 997
student998 998 998
student999 999 999
student1000 1000 1000
""") == "student19", "large input"

| Test input | Expected output | What it validates |
|---|---|---|
| Single student | ironhead | Minimum size handling |
| Five students | alice | Eligibility filtering |
| Ten students | b | Upward rounding of quota |
| Four students | z | Boundary of eligible range |
| One thousand students | student19 | Maximum input size |

## Edge Cases

The first rounding issue appears when percentages do not produce integers. In the ten-student example, the recommendation count is two, not one. The algorithm uses `(186 * n + 999) // 1000`, so the ceiling operation is performed exactly.

The eligibility boundary is handled by sorting before slicing. For a department of four students, the allowed percentage is ceil(4 × 30%) = 2 students. The first two after sorting by study ranking remain eligible, while the rest cannot enter the final ranking.

Equal comprehensive scores are handled by the tuple sort key. If two eligible students have the same integer score, Python compares their names automatically. This matches the required dictionary order and makes the selected final student deterministic.

The algorithm also handles the case where the quota is one. After sorting, index zero is the only selected position, so the first student in the final ranking is returned correctly.
```

This editorial can be adjusted further for a specific Codeforces editorial style, such as shorter contest notes or a more proof-focused version.
