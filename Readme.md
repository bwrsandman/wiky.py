Wiky.py - a python script to convert Wiki Markup language to HTML based on Wiki.js.
=======================

(It is buggy, please use with care)

Wiky.py is a python script javascript library that converts Wiki Markup language to HTML based on Wiki.js.


How to use it
-------------------
Import wiki in python. Wiki.py has only one function, which is `wiky.process(wikitext)`.


Supported Syntax
-------------------
* `== Heading ==`
* `=== Subheading ===`
* `[http://www.url.com Name of URLs]`
* `[[File:http://www.url.com/image.png Alternative Text]]`
* `--------------------` (Horizontal line)
* `:` (Indentation)
* `#` Ordered bullet point
* `*` Unordered bullet point



Contributors
-------------------

Sandy Carter (Wiki.py)

Tanin Na Nakorn (Wiki.js)

Tanun Niyomjit (Designer)

Dav Glass [davglass]


Options
-------

It only supports one option at the moment: `link-image`

Setting this to `false` will tell `wiky.py` to not imbed CSS into the markup for link icons.

License
---------

Do What The Fuck You Want To Public License (http://www.wtfpl.net)

0. You just DO WHAT THE FUCK YOU WANT TO.

