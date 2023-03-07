# Report of Observations

## Drift

**Machine with rate 1:**
* Logical clock time received from server: this is the clock time sent in the most recent message to this machine by another (most likely faster) machine.
* Updated logical clock value: this is the machine's logical clock value after it takes a message off the queue.

Takeaway: this machine processes messages much slower than it receives them. 
```
Logical clock time received from server: 434
Updated logical clock value to now be 346
Logical clock time received from server: 449
Logical clock time received from server: 451
Updated logical clock value to now be 347
Logical clock time received from server: 453
Updated logical clock value to now be 348
Updated logical clock value to now be 352
Logical clock time received from server: 465
Updated logical clock value to now be 357
Logical clock time received from server: 470
Updated logical clock value to now be 358
Logical clock time received from server: 475
Updated logical clock value to now be 364
Logical clock time received from server: 477
Updated logical clock value to now be 365
Logical clock time received from server: 483
Updated logical clock value to now be 372
Logical clock time received from server: 484
Updated logical clock value to now be 373
Logical clock time received from server: 492
Logical clock time received from server: 492
Updated logical clock value to now be 374
Updated logical clock value to now be 386
Logical clock time received from server: 500
Logical clock time received from server: 506
Updated logical clock value to now be 391
Logical clock time received from server: 507
Updated logical clock value to now be 392
Logical clock time received from server: 513
Updated logical clock value to now be 393
Updated logical clock value to now be 407
Updated logical clock value to now be 413
Updated logical clock value to now be 414
Logical clock time received from server: 532
Updated logical clock value to now be 417
Updated logical clock value to now be 418
Updated logical clock value to now be 419
Logical clock time received from server: 550
Updated logical clock value to now be 420
Logical clock time received from server: 551
Logical clock time received from server: 552
Updated logical clock value to now be 423
Updated logical clock value to now be 424
Logical clock time received from server: 563
Updated logical clock value to now be 436
Updated logical clock value to now be 437
Updated logical clock value to now be 441
Logical clock time received from server: 576
Logical clock time received from server: 570
Updated logical clock value to now be 442
Logical clock time received from server: 573
Logical clock time received from server: 585
Logical clock time received from server: 575
Updated logical clock value to now be 443
Logical clock time received from server: 577
Updated logical clock value to now be 450
Logical clock time received from server: 579
Logical clock time received from server: 592
Logical clock time received from server: 581
Updated logical clock value to now be 452
Updated logical clock value to now be 454
Logical clock time received from server: 601
```

**Machine with rate 5:**

Takeaway: this machine processes messages much slower than it receives them. 

```
Logical clock time received from server: 500
Updated logical clock value to now be 504
Logical clock time received from server: 519
Updated logical clock value to now be 524
Logical clock time received from server: 532
Updated logical clock value to now be 535
Logical clock time received from server: 534
Updated logical clock value to now be 539
Logical clock time received from server: 537
Updated logical clock value to now be 544
Logical clock time received from server: 553
Updated logical clock value to now be 557
Logical clock time received from server: 561
Updated logical clock value to now be 563
Logical clock time received from server: 563
Updated logical clock value to now be 567
Logical clock time received from server: 565
Updated logical clock value to now be 570
Logical clock time received from server: 570
Updated logical clock value to now be 578
Logical clock time received from server: 575
Updated logical clock value to now be 587
Logical clock time received from server: 578
Updated logical clock value to now be 592
Logical clock time received from server: 581
Updated logical clock value to now be 597
```