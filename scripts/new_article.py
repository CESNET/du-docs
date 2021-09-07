#!/usr/bin/env python3

import argparse

parser = argparse.ArgumentParser(description="Script to create an empty article")
parser.add_argument('name', metavar='Name', type=str, help='Article name')
parser.add_argument('--file', dest='file', type=str, default=None, help='File name of the article (optional) (do not include .md)')

args = parser.parse_args()

if(args.file == None):
    args.file = args.name.lower().replace(' ', '-')

args.file = args.file.replace('.md', '')

lines = [
        "---\n",
        "layout: article\n",
        "title: {}\n".format(args.name),
        "permalink: /docs/{}.html\n".format(args.file),
        "key: {}\n".format(args.file),
        "aside:\n",
        "  toc: true\n",
        "sidebar:\n",
        "  nav: docs\n",
        "---\n",
        ]


with open("{}.md".format(args.file), "w") as article:
    article.writelines(lines)
