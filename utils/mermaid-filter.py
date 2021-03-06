#!/usr/bin/env python

import os
import sys
import subprocess

from pathlib import Path

from pandocfilters import toJSONFilter, Para, Image
from pandocfilters import get_filename4code, get_caption, get_extension

MERMAID_BIN = os.environ.get('MERMAID_BIN', 'mmdc')
OUT_FOLDER = os.environ.get("OUTPUT_FOLDER", "") + "/"
Path(OUT_FOLDER + "mermaid-images").mkdir(parents=True, exist_ok=True)

def mermaid(key, value, format_, _):
    if key == 'CodeBlock':
        [[ident, classes, keyvals], code] = value

        if "mermaid" in classes:
            caption, typef, keyvals = get_caption(keyvals)

            filename = get_filename4code("mermaid", code)
            filetype = get_extension(format_, "png", html="svg", latex="png")

            filename_ = OUT_FOLDER + filename
            src = filename_ + '.mmd'
            dest = filename_ + '.' + filetype

            if not os.path.isfile(dest):
                txt = code.encode(sys.getfilesystemencoding())
                with open(src, "wb") as f:
                    f.write(txt)

                subprocess.check_call([MERMAID_BIN, "-i", src, "-o", dest])
                sys.stderr.write('Created image ' + dest + '\n')

            return Para([Image([ident, [], keyvals], caption, [filename + ".png", typef])])


def main():
    toJSONFilter(mermaid)


if __name__ == "__main__":
    main()

