#!/usr/bin/env python

def camel_case(text: str | None) -> str | None:
    if text is None or len(text) == 0:
        return text

    return text[0:1].upper() + text[1:]


def right_pad(text: str | None, length: int) -> str:
    if text is None:
        text = ''

    return text.ljust(length)


