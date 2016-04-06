#!/usr/bin/env python

from flask import Flask, request, render_template

from datetime import datetime, timedelta
from jinja2 import Environment, FileSystemLoader
import markdown2

import os

app = Flask(__name__)

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
jenv = Environment(loader=FileSystemLoader(THIS_DIR), trim_blocks=True)

@app.route('/')
def index():
    """
    The landing page.
    """

    try:
        path = 'index.md'
        html = markdown2.markdown_path(path, extras=["metadata"])

        metadata = html.metadata
        if 'template' in metadata.keys():
            template = metadata['template']
        else:
            template = 'templates/index.html'

        render_data = metadata.copy()
        render_data[u'body'] = html

        rendered = jenv.get_template(template).render(render_data)
        return rendered

    except IOError as e:
        return render_template('404.html'), 404

@app.route('/<category>', methods=['GET', 'POST'])
def category(category):
    """
    Categories of items.

    Essentially a 'directory listing' page. 

    Returns to the items to the 'index'.

    """

    try:

        # First do the items
        items = []
        for filename in os.listdir(category):
            if 'index.md' in filename: 
                continue
            item = markdown2.markdown_path(category + '/' + filename, extras=["metadata"])
            item.metadata['slug'] = filename.split('/')[-1].replace('.md', '')
            items.append(item)

        # Then do the index
        path = category + '/index.md'
        html = markdown2.markdown_path(path, extras=["metadata"])

        metadata = html.metadata
        if 'template' in metadata.keys():
            template = metadata['template']
        else:
            template = 'templates/category.html'

        render_data = metadata.copy()
        render_data[u'body'] = html
        render_data[u'items'] = items
        render_data[u'category'] = category

        rendered = jenv.get_template(template).render(render_data)
        return rendered

    except IOError as e:
        print e
        return render_template('404.html'), 404

@app.route('/<category>/<item_slug>', methods=['GET', 'POST'])
def item(category, item_slug):
    """
    A single specific item.

    """

    try:
        path = category + '/' + item_slug + '.md'
        html = markdown2.markdown_path(path, extras=["metadata"])

        metadata = html.metadata
        if 'template' in metadata.keys():
            template = metadata['template']
        else:
            template = 'templates/item.html'

        render_data = metadata.copy()
        render_data[u'body'] = html
        render_data[u'category'] = category
        render_data[u'item_slug'] = item_slug

        rendered = jenv.get_template(template).render(render_data)
        return rendered

    except IOError as e:
        return render_template('404.html'), 404

# We only need this for local development.
if __name__ == '__main__':
    app.debug = True
    app.run()
