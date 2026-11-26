"""3 AM commit message entry for make.fun.

Writes a single commit message — pushed at 3 AM by a developer who fixed
a bug by deleting the code that caused it — to $MAKEFUN_OUTPUT_DIR/entry.txt
for the bounty "The 3AM Commit Message". Only the Python standard library
is used.
"""

import os
import sys

COMMIT = "commit 3am: fixed the bug by deleting the code that caused it. tests pass. i am afraid to ask why. merging anyway"

MAX_CHARS = 139  # sealed gate in the kit's RULES.txt: 1 to 139 characters


def check_commit(text):
    """Return the commit message once it passes the sealed gate, else raise.

    The gate takes UTF-8 text of 1 to 139 characters, not only white space,
    on a single line with no trailing newline. A bad message is refused
    here, loudly, instead of shipping an entry the judge never sees.
    """
    if not isinstance(text, str):
        raise TypeError("commit message must be text")
    stripped = text.strip()
    if not stripped:
        raise ValueError("commit message must not be blank")
    if stripped != text:
        raise ValueError("commit message has leading or trailing space")
    if len(stripped) > MAX_CHARS:
        raise ValueError(
            "commit message is %d characters, over the %d limit"
            % (len(stripped), MAX_CHARS)
        )
    if "\n" in stripped or "\r" in stripped:
        raise ValueError("commit message must be a single line")
    return stripped


def describe_commit(text):
    """Summarise the commit message for the run log: characters vs bytes.

    The gate measures characters, while the file holds bytes; the two
    counts are reported side by side so a multi-byte character can never
    silently push the file past the gate the scorer reads.
    """
    encoded = text.encode("utf-8")
    for char in text:
        if ord(char) < 32:
            raise ValueError("commit message holds a control character: U+%04X" % ord(char))
    return "%d characters, %d UTF-8 bytes" % (len(text), len(encoded))


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if not out_dir:
        print("MAKEFUN_OUTPUT_DIR is not set", file=sys.stderr)
        return 1
    message = check_commit(COMMIT)
    summary = describe_commit(message)
    target = os.path.join(out_dir, "entry.txt")
    os.makedirs(out_dir, exist_ok=True)
    with open(target, "w", encoding="utf-8") as handle:
        handle.write(message)
    print("wrote %s (%s)" % (target, summary))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
