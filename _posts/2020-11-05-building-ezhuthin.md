---
layout: post
title: Building ezhuth.in!
description: Learnings from building a Malaylam social media website.
comments: true
---

For the past few months I have been working on building [ezhuth.in](ezhuth.in). Here are the lessons learned in the process.



I have been working on this website for some time on and off. I feel satisfied enough to release it, but I wouldn't call it done yet. Lots of things to be done. If you are free do have a look.

I implemented this with Django, for the backend and pure HTML, CSS for the front-end. I am using Gunicorn, along with Nginx as a reverse proxy. I have hosted this on an ubuntu node in digital ocean and used domain names from namecheap.com.

Things I learned by building the website.

1. How hard it is to make something bigger than a side project - the amount of time I spend to fix bugs that I would introduce with each feature was huge. Writing unit tests for your code is a good idea to prevent this - but I just put it off for some reason.

2. Hosting a website in production - the server that comes along with Django is pretty weak to do the kind of stuff when you want to scale your products, I went with Gunicorn as I have heard good things about it. I used Nginx as a reverse proxy - which sort of means like I use it to serve static files. I also learned to connect domain names to IP and such. I also used certbot to enable https on the server. Also, I learned to put our sensitive info as environment variables that are loaded using python packages like dotenv.

3. Reading code - I looked up a lot of code of Django projects on Github in order to have a look at better ways to implement the features - I learned some of the abstractions that are commonly used like ContentType and also things like signals which is not covered in an average tutorial. If you do have time please do look at this [repo](https://github.com/django/django-contrib-comments) - this is an official Django repo for adding comments in your codebase. It is very insightful and well written.

4. Learned a bit of frond-end - I learned how to use pure HTML and CSS to design a responsive website. I was never confident enough about my front end skills. The hard truth of the matter is, a website needs to look good to get attention, also a ton of people will want to use it from mobile, so it should look good on mobile. After building the current front end and looking at the older front end I could see how far I have come with the designing. I found this [blog](https://github.com/django/django-contrib-comments) very helpful in improving my design skills.

I would love to hear your opinions and suggestions to improve the website. Thanks a lot!
