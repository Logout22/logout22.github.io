# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

# THINGS TO CONFIGURE
# ---------------------------------------------------------------------

AUTHOR = "Martin Unzner"
SITENAME = "Nebensinn blog"
SITESUBTITLE = ""
SITEURL = "https://logout22.github.io"
DEFAULT_LANG = "en"
DEFAULT_CATEGORY = "blog"


LANDING_PAGE_ABOUT = {
    "title": "Nebensinn blog",
    "details": """<p>Hi, I am Martin. On this blog I
 will post updates on technology
 that cannot be expressed as source code diffs.</p>""",
}


PROJECTS = [
    {
        "name": "ansible-role-ghost-backup",
        "url": "https://github.com/Logout22/ansible-role-ghost-backup",
        "description": "Ansible role to back up a Ghost blog",
    },
    {
        "name": "ansible-role-ghost-restore",
        "url": "https://github.com/Logout22/ansible-role-ghost-restore",
        "description": "Ansible role to restore a Ghost blog",
    },
    {
        "name": "shifting-alternator",
        "url": "https://codeberg.org/Logout/shifting-alternator",
        "description": "Test-driven Arduino project for my model rail set",
    },
    {
        "name": "rulsof",
        "url": "https://codeberg.org/Logout/rulsof",
        "description": "Rust wrapper library for the lsof utility",
    },
    {
        "name": "rulsof-c",
        "url": "https://codeberg.org/Logout/rulsof-c",
        "description": "C/C++ interface library for rulsof",
    },
    {
        "name": "ugame-tetris",
        "url": "https://github.com/Logout22/ugame-tetris",
        "description": "Tetris clone for the uGame10 (in development)",
    },
    {
        "name": "Linguafranka",
        "url": "https://github.com/Logout22/linguafranka-python",
        "description": "Proxy service querying multiple online dictionaries at once (in development)",
    },
]


LINKS = (("Nebensinn home page", "https://nebensinn.com"),)

SOCIAL = ()

# Extra files customization
EXTRA_PATH_METADATA = {}

EXTRA_TEMPLATES_PATHS = [
    "plugins/revealmd/templates",  # eg: "plugins/revealmd/templates"
]

STATIC_PATHS = ["images"]

# ONLY TOUCH IF YOU KNOW WHAT YOU'RE DOING!
# ---------------------------------------------------------------------

PATH = "content"

TIMEZONE = "Europe/Berlin"

# Put as draft content in the future
WITH_FUTURE_DATES = True

# Put full text in RSS feed
RSS_FEED_SUMMARY_ONLY = False

# Feed generation is usually not desired when developing

FEED_ALL_ATOM = "feeds/all.atom.xml"
FEED_ALL_RSS = "feeds/all.rss"

CATEGORY_FEED_ATOM = "feeds/{slug}.atom.xml"
CATEGORY_FEED_RSS = "feeds/{slug}.rss"
TRANSLATION_FEED_ATOM = "feeds/{lang}.atom.xml"
TRANSLATION_FEED_RSS = "feeds/{lang}.rss"
AUTHOR_FEED_ATOM = "feeds/{slug}.atom.xml"
AUTHOR_FEED_RSS = "feeds/{slug}.rss"
TAG_FEED_ATOM = "feeds/tag_{slug}.atom.xml"
TAG_FEED_RSS = "feeds/tag_{slug}.rss"

DISPLAY_PAGES_ON_MENU = True

CACHE_CONTENT = False
CACHE_PATH = ".cache"
LOAD_CONTENT_CACHE = False

# Plugins
PLUGIN_PATHS = ["plugins"]

PLUGINS = [
    "sitemap",
    "extract_toc",
    "tipue_search",
    "liquid_tags.img",
    "neighbors",
    "render_math",
    "related_posts",
    "share_post",
    "series",
    "assets",
    "post_stats",
    "revealmd",
    "photos",
]

# 'better_codeblock_line_numbering'
# 'better_figures_and_images'

THEME = "themes/elegant"

# elegant
TYPOGRIFY = True
RECENT_ARTICLE_SUMMARY = True
RESPONSIVE_IMAGES = True

MARKDOWN = {
    "extension_configs": {
        "markdown.extensions.codehilite": {"css_class": "highlight", "linenums": True},
        "markdown.extensions.extra": {},
        "markdown.extensions.toc": {"permalink": "true"},
        "markdown.extensions.meta": {},
        "markdown.extensions.admonition": {},
    },
    "output_format": "html5",
}

DIRECT_TEMPLATES = ("index", "tags", "categories", "archives", "search", "404")

# Elegant Labels
SOCIAL_PROFILE_LABEL = "Stay in Touch"
RELATED_POSTS_LABEL = "Keep Reading"
SHARE_POST_INTRO = "Like this post? Share on:"
COMMENTS_INTRO = ""

FILENAME_METADATA = r"(?P<date>\d{4}-\d{2}-\d{2})_(?P<slug>.*)"
USE_FOLDER_AS_CATEGORY = False

SEARCH_BOX = False

# URL Settings to be compatible with octopress
ARTICLE_URL = "blog/{date:%Y}/{date:%m}/{date:%d}/{slug}/"
ARTICLE_SAVE_AS = "blog/{date:%Y}/{date:%m}/{date:%d}/{slug}/index.html"

ARTICLE_LANG_URL = "blog/{date:%Y}/{date:%m}/{date:%d}/{slug}-{lang}/"
ARTICLE_LANG_SAVE_AS = "blog/{date:%Y}/{date:%m}/{date:%d}/{slug}-{lang}/index.html"

YEAR_ARCHIVE_URL = "blog/archive/{date:%Y}/"
YEAR_ARCHIVE_SAVE_AS = "blog/archive/{date:%Y}/index.html"

MONTH_ARCHIVE_URL = "blog/archive/{date:%Y}/{date:%m}/"
MONTH_ARCHIVE_SAVE_AS = "blog/archive/{date:%Y}/{date:%m}/index.html"

CATEGORY_URL = "blog/category/{slug}/"
CATEGORY_SAVE_AS = "blog/category/{slug}/index.html"

TAG_URL = "blog/tag/{slug}/"
TAG_SAVE_AS = "blog/tag/{slug}/index.html"

PAGE_URL = "{slug}/"
PAGE_SAVE_AS = "{slug}/index.html"

AUTHOR_SAVE_AS = ""
AUTHORS_SAVE_AS = ""

ARCHIVES_URL = "blog/archives/"
ARCHIVES_SAVE_AS = "blog/archives/index.html"

CATEGORIES_URL = "blog/categories/"
CATEGORIES_SAVE_AS = "blog/categories/index.html"

TAGS_URL = "blog/tags/"
TAGS_SAVE_AS = "blog/tags/index.html"

TAGS_URL = "tags"
TAGS_SAVE_AS = "tags/index.html"
AUTHORS_URL = "authors"
AUTHORS_SAVE_AS = "authors/index.html"
CATEGORIES_URL = "categories"
CATEGORIES_SAVE_AS = "categories/index.html"
ARCHIVES_URL = "archives"
ARCHIVES_SAVE_AS = "archives/index.html"

DEFAULT_PAGINATION = 5
DEFAULT_ORPHANS = 0

PAGINATION_PATTERNS = (
    (1, "{base_name}/", "{base_name}/index.html"),
    (2, "{base_name}/page/{number}/", "{base_name}/page/{number}/index.html"),
)


# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True

# sitemap
SITEMAP = {
    "format": "xml",
    "priorities": {"articles": 0.5, "indexes": 0.5, "pages": 0.5},
    "changefreqs": {"articles": "monthly", "indexes": "daily", "pages": "monthly"},
}

SITE_UPDATED = datetime.date.today()

# use those if you want pelican standard pages to appear in your menu
MENU_INTERNAL_PAGES = (
    ("Tags", TAGS_URL, TAGS_SAVE_AS),
    ("Archives", ARCHIVES_URL, ARCHIVES_SAVE_AS),
)
