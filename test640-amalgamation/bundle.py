import argparse
import os.path
import re


RE_LOCAL_INCLUDE = re.compile('#include "(.+?)"')


def main():
    run(**parse_args())


def parse_args():
    parser = argparse.ArgumentParser()
    arg = parser.add_argument
    arg("--pre", type=str, default=None, help="Pre-guard fragment for output")
    arg("--guard", type=str, default=None, help="Guard name for output")
    arg("paths", type=str, nargs="+", help="Header files to merge")
    return vars(parser.parse_args())


def run(paths, pre, guard):
    headers = {path: Header(path) for path in paths}

    for header in headers.values():
        header.resolve_depends(headers)

    if pre:
        with open(pre) as file:
            print(file.read())

    if guard:
        print(f"#ifndef {guard}")
        print(f"#define {guard}")

    merge(headers.values())

    if guard:
        print("")
        print("#endif")


def merge(headers, resolved=set()):
    for header in headers:
        if header in resolved:
            continue

        if header.depends:
            merge(header.depends)

        print(header.make_output())
        resolved.add(header)


class Header:
    def __init__(self, path):
        self._path = path
        self._code_lines = None
        self._depend_paths = None

        if path is None:
            return

        lines = load_code_lines(path)

        rel_depends = extract_local_includes(lines)
        basedir = os.path.dirname(path)
        depends = [os.path.normpath(os.path.join(basedir, dep)) for dep in rel_depends]

        self._path = path
        self._code_lines = lines
        self._depend_paths = depends

    @property
    def path(self):
        return self._path

    def resolve_depends(self, headers):
        self.depends = [headers[path] for path in self._depend_paths]

    def make_output(self):
        header = [
            "",
            "//--------------------------------------------------------------------------",
            "",
        ]
        return "\n".join(header + remove_local_includes(self._code_lines))


def remove_local_includes(lines):
    output = []
    for line in lines:
        if RE_LOCAL_INCLUDE.match(line):
            trim = rindex_if(output, len) + 1
            output = output[:trim]
        else:
            output.append(line)
    return output


def extract_local_includes(lines):
    depends = []
    for line in lines:
        match = RE_LOCAL_INCLUDE.match(line)
        if match:
            depends.append(match.group(1))
    return depends


def load_code_lines(path):
    with open(path) as file:
        lines = [line.rstrip() for line in file]

    beg = index_if(lines, lambda s: s.startswith("#define")) + 1
    end = rindex_if(lines, lambda s: s.startswith("#endif"))

    return strip_empty(lines[beg:end])


def strip_empty(texts):
    beg = index_if(texts, len)
    end = rindex_if(texts, len) + 1
    return texts[beg:end]


def index_if(texts, pred):
    for i, text in enumerate(texts):
        if pred(text):
            return i
    return None


def rindex_if(texts, pred):
    for i, text in enumerate(texts[::-1]):
        if pred(text):
            return len(texts) - i - 1
    return None


if __name__ == "__main__":
    main()
