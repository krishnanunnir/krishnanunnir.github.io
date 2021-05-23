---
layout: post
title: Why you should use tmux on remote machines!
description: how to run process in background in remote machine
comments: true
---

Imagine you have a setup with multiple monitors, you will try to organise your applications on different monitors based on their usage type, maybe you have all entertainment apps in one monitor and all the work related apps in another monitor.

Now imagine if you remove the other monitors, and you just have a single monitor, in order to maintain a separation of ideas, you start using virtual workspaces in your machine - in a way replicating multiple monitors.

Now imagine if we are further restricted to a machine with just the terminal app. Here we will create multiple instances to replicate separation of ideas.

We will go one more step - you are further restricted to just one terminal console, as in the case of a remote session accessed via ssh. What would be the flow to abstract and separate out ideas as we have done in earlier tweets.

Say hello to tmux - tmux is to terminal what virtual workspace is to monitor. This is a gross generalisation which doesn’t do justice to the true power of tmux in a remote session.

tmux has three levels of hierarchies - sessions, windows and panes. Continuing with the earlier analogy, we can think of sessions as monitors, windows as the different applications running on it and panes as different subprocess of an application like tabs in a browser.

Why should you use this in a remote session?
1. You can create, control and access a number of terminals from a single screen.
2. One of its biggest advantage in remote session is tmux's ability to be detachable. Imagine you are running a long process like downloading a large file, in a normal terminal you would have to run this process synchronously, blocking any other activity.  
Tmux being detachable allows it to run processes in the background asynchronously and once it is done, we can reattach tmux back allowing us to start from where we left off. The use of this feature is immense when the processs' you execute are time consuming.
3. There is a keyboard shortcut for everything - copying, scrolling, detach, if you want to avoid the switch between mouse and keyboard then tmux is a good option.

You would be able to see why these features would mean a lot in remote ssh. If you are in a job which is remote access intensive - tmux is not an option, it is a necessity. Once you use tmux to its strengths - going back will be hard.