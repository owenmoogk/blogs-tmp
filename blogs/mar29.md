---
title: Pretending to Hack GitHub, and some Git Security Notes
date: Mar 29, 2024
tags: ["reflection", "tech"]
---

## Pretending to Hack GitHub, and some Git Security Notes

This week, I pulled a good prank on a friend of mine by pretending to hack into his GitHub (the only mistake I made was not saving it for April Fools). GitHub has some interesting procedures when assigning users to a commit because it’s based on Git architecture. Anybody can make a commit as any user, just by changing the user.name and user.email configuration.

Then, provided you have permission to push and pull from the repo, you can do so with commits made by anyone. This allowed me to push to our company’s *private* repo under his name, and accuse him of hacking! To reveal that it was me all along, I then pushed another commit under Notch’s (the creator of Minecraft) GitHub account.

![The commit tree, entirely made by me.](https://cdn-images-1.medium.com/max/2000/1*EMPjtlk_QVAgldZ2Jv6gUQ.png)

This has some interesting implications, as one can commit as anyone whom they have the associated email address for (which people generally make public), and it’s unable to be detected. That is, unless one consistently signs their commits, verifying that it was their GitHub account that pushed it.

At first, I was very confused as to why this is, but it does make sense given that you have to push the commits of others in forks and branches. However, I am now going to be a lot more cautious about commits that don't have the *verified *tag attached to them. Also, I will definitely look a lot more closely into signing commits.

As a sidenote, this was used to ‘troll’ GitHub when they took down youtube-dl, with people pretending to commit as Nat Friedman: [https://gist.github.com/lrvick/02088ee5466ca51116bdaf1e709ddd7c](https://gist.github.com/lrvick/02088ee5466ca51116bdaf1e709ddd7c).

The moral of the story: don’t trust a GitHub commit was authored by the person that it claims.
