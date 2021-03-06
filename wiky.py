#!/usr/bin/env python2
"""
Wiky.py - Python library to converts Wiki MarkUp language to HTML.
          Based on Wiki.js by Tanin Na Nakorn
          
Copyright © 2013 Sandy Carter <bwrsandman@gmail.com>
This work is free. You can redistribute it and/or modify it under the
terms of the Do What The Fuck You Want To Public License, Version 2,
as published by Sam Hocevar. See the COPYING file for more details.
"""

import re

re_h2 = re.compile("^===[^=]+===$")
re_h3 = re.compile("^==[^=]+==$")
re_indent = re.compile("^:+")
re_hr = re.compile("^-{4}")
re_ul = re.compile("^\*+ ")
re_ol = re.compile("^#+ ")
re_ul_ol = re.compile("^(\*+|#+) ")
re_ul_li = re.compile("^(\*+|##+):? ")
re_ol_li = re.compile("^(\*\*+|#+):? ")
re_ul_ol_li = re.compile("^(\*+|#+):? ")
re_youtube = re.compile("^(https?://)?(www\.)?youtube.com/(watch\?(.*)v=|embed/)([^&]+)")
re_b_i = re.compile("'''''(([^']|([^']('{1,4})?[^']))+)'''''")
re_b = re.compile("'''(([^']|([^'](''?)?[^']))+)'''")
re_i = re.compile("''(([^']|([^']'?[^']))+)''")

class Wiky:
    def __init__(self, link_image=None):
        self.link_image = link_image

    def process(self, wikitext):
        lines = wikitext.split("\n")
        html = ""
        i = 0
        while i < len(lines):
            line = lines[i]
            if re_h2.match(line):
                html += "<h2>%s</h2>" % line[3:-3]
            elif re_h3.match(line):
                html += "<h3>%s</h3>" % line[2:-2]
            elif re_hr.match(line):
                html += "<hr/>"
            elif re_indent.match(line):
                start = i
                while i < len(lines) and re_indent.match(lines[i]):
                    i += 1
                i -= 1
                html += self.process_indent(lines[start: i + 1])
            elif re_ul.match(line):
                start = i
                while i < len(lines) and re_ul_li.match(lines[i]):
                    i += 1
                i -= 1
                html += self.process_bullet_point(lines[start: i + 1])
            elif re_ol.match(line):
                start = i
                while i < len(lines) and re_ol_li.match(lines[i]):
                    i += 1
                i -= 1
                html += self.process_bullet_point(lines[start: i + 1])
            else :
                html += self.process_normal(line)
            html += "<br/>\n"
            i += 1
        return html

    def process_indent(self, lines):
        html = "\n<dl>\n"
        i = 0
        while i < len(lines):
            line = lines[i]
            html += "<dd>"
            this_count = len(re_indent.match(line).group(0))
            html += self.process_normal(line[this_count:])

            nested_end = i
            j = i + 1
            while j < len(lines):
                nested_count = len(re_indent.match(lines[j]).group(0))
                if nested_count <= this_count:
                    break
                else:
                    nested_end = j
                j += 1

            if nested_end > i:
                html += self.process_indent(lines[i + 1: nested_end + 1])
                i = nested_end

            html += "</dd>\n"
            i += 1
        html += "</dl>\n"
        return html

    def process_bullet_point(self, lines):
        if not len(lines):
            return ""
        html = "<ul>" if lines[0][0] == "*" else "<ol>"
        html += '\n'
        i = 0
        while i < len(lines):
            line = lines[i]
            html += "<li>"
            this_count = len(re_ul_ol.match(line).group(1))
            html += self.process_normal(line[this_count+1:])

            # continue previous with #:
            nested_end = i
            j = i + 1
            while j < len(lines):
                nested_count = len(re_ul_ol_li.match(lines[j]).group(1))
                if nested_count < this_count:
                    break
                elif lines[j][nested_count] == ':':
                    html += "<br/>" + self.process_normal(lines[j][nested_count + 2:])
                    nested_end = j
                else:
                    break
                j += 1
            i = nested_end

            # nested bullet point
            nested_end = i
            j = i + 1
            while j < len(lines):
                nested_count = len(re_ul_ol_li.match(lines[j]).group(1))
                if nested_count <= this_count:
                    break
                else:
                    nested_end = j
                j += 1

            if nested_end > i:
                html += self.process_bullet_point(lines[i + 1: nested_end + 1])
                i = nested_end

            # continue previous with #:
            nested_end = i
            j = i + 1
            while j < len(lines):
                nested_count = len(re_ul_ol_li.match(lines[j]).group(1))
                if nested_count < this_count:
                    break
                elif lines[j][nested_count] == ':':
                    html += self.process_normal(lines[j][nested_count + 2:])
                    nested_end = j
                else:
                    break
                j += 1
            i = nested_end
            html += "</li>\n"
            i += 1
        html += "</ul>" if lines[0][0] == "*" else "</ol>"
        html += '\n'
        return html

    def process_url(self, txt):
        css = ('style="background: url(\"%s\") no-repeat scroll '
               'right center transparent;padding-right: 13px;"'
               % self.link_image) if self.link_image else ''
        try:
            index = txt.index(" ")
            url = txt[:index]
            label = txt[index + 1:]
        except ValueError:
            label = url = txt
        return """<a href="%s" %s>%s</a>""" % (url, css, label)

    @staticmethod
    def process_image(txt):
        try:
            index = txt.index(" ")
            url = txt[:index]
            label = txt[index + 1:]
        except ValueError:
            url = txt
            label = ""
        return '<img src="%s" alt="%s" />' % (url, label)

    @staticmethod
    def process_video(url):
        m = re_youtube.match(url)
        if not m:
            return "<b>%s is an invalid YouTube URL</b>" % url
        url = "http://www.youtube.com/embed/" + m.group(5)
        return '<iframe width="480" height="390" src="%s" frameborder="0" allowfullscreen=""></iframe>' % url

    def process_normal(self, wikitext):
        # Image
        while True:
            try:
                index = wikitext.index("[[File:")
                end_index = wikitext.index("]]", index + 7)
                wikitext = (wikitext[:index] +
                            self.process_image(wikitext[index + 7:end_index]) +
                            wikitext[end_index + 2:])
            except ValueError:
                break

        # Video
        while True:
            try:
                index = wikitext.index("[[Video:")
                end_index = wikitext.index("]]", index + 8)
                wikitext = (wikitext[:index] +
                            self.process_video(wikitext[index+8:end_index]) +
                            wikitext[end_index + 2:])
            except ValueError:
                break

        # URL
        for protocol in ["http","ftp","news"]:
            end_index = -1
            while True:
                try:
                    index = wikitext.index("[%s://" % protocol, end_index + 1)
                    end_index = wikitext.index("]", index + len(protocol) + 4)
                    wikitext = (wikitext[:index] +
                                self.process_url(wikitext[index+1:end_index]) +
                                wikitext[end_index+1:])
                except ValueError:
                    break

        # Bold, Italics, Emphasis
        wikitext = re_b_i.sub("<b><i>\g<1></i></b>", wikitext)
        wikitext = re_b.sub("<b>\g<1></b>", wikitext)
        wikitext = re_i.sub("<i>\g<1></i>", wikitext)

        return wikitext

if __name__ == "__main__":
    input_complete = open("input_complete").read()
    w = Wiky()
    print (w.process(input_complete))
