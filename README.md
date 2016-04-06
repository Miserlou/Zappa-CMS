# Zappa-CMS

A tiny, Zappa-powered serverless CMS for busy hackers.

No websever, no database, just Markdown and metadata.

It's not dissimilar to [Pico](http://picocms.org/) or [Pelican](http://blog.getpelican.com/), but slightly more flexible because it's based on Flask, not static files.

## Usage

For each category, just create a folder and put files in it.

Each file should follow this format:

```markdown
---
title: The Title
author: Your Name
date-created: 01-01-2016
format: markdown
---

# Title title title 

**Body** body body body.

```

To see your site locally, run

    $ ./zappa_cms.py

And to deploy it:

    $ zappa deploy production
