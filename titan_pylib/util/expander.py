# user settings --------------------------------------------------
# `./titan_pylib` がある絶対パス
LIB_PATH = (
    "/mnt/c/Users/titan/source/Library_py/",
    "C:\\Users\\titan\\source\\Library_py\\",
    "/home/titan/source/Library_py/",
)
#  ----------------------------------------------------------------

from logging import getLogger, basicConfig
import shutil
import pyperclip
import ast
import argparse
import re
import black
import os

LIB = "titan_pylib"

logger = getLogger(__name__)


def init_clipboard():
    for command in ["wl-clipboard", "xclip", "xsel"]:
        if shutil.which(command):
            pyperclip.set_clipboard(command)
            break


class Expander:
    """titan_pylib の expander"""

    def __init__(self, input_path: str, verbose: bool) -> None:
        """
        Args:
            input_path (str): 入力ファイルのパス
        """
        self.verbose: bool = verbose
        self.input_path: str = input_path
        self.seen_path: set[str] = set()
        self.added_modules: set[str] = set()
        self.need_modules: set[str] = set()
        self.outputs: list[str] = []

    def _finalize(self, formatter: bool) -> str:
        """self.outputsの最終処理をしたコードを返す"""
        code = "".join(self.outputs)
        if formatter:
            if self.verbose:
                logger.info("set formatter.")
            code = black.format_str(code, mode=black.FileMode())
        try:
            ast.parse(code)
        except SyntaxError as e:
            logger.critical(f"Syntax Error in _finalize()\n{e}")
            exit(1)
        return code

    def _get_path(self, path: str, is_titan_pylib: bool) -> str:
        """pathをスラッシュ表記にする"""
        if is_titan_pylib:
            for lib_path in LIB_PATH:
                new_path = lib_path + path.replace(".", "/") + ".py"
                if os.path.exists(new_path):
                    path = new_path
                    break
            else:
                logger.critical(f'File "{path}" not found.')
                exit(1)
        return path

    def _find_imported_modules(self, path: str, is_titan_pylib: bool) -> None:
        """fromで始まるモジュールを列挙し、need_modulesに格納する
        (pathファイルの中で必要なモジュールの列挙)
        """
        with open(self._get_path(path, is_titan_pylib), "r", encoding="utf-8") as f:
            tree = ast.parse(f.read())
        for node in ast.walk(tree):
            if not isinstance(node, ast.ImportFrom):
                continue
            module_name = node.module if node.module else ""
            if not module_name.startswith(LIB):
                continue
            for alias in node.names:
                if alias.name not in self.added_modules:
                    self.need_modules.add(alias.name)
                    if self.verbose:
                        logger.info(f"[SEARCH] {path} {alias.name}")

    def _find_classes(self, path: str, is_titan_pylib: bool) -> None:
        """classで始まるモジュールを列挙し、added_modulesに格納する
        (pathファイルは今見ている)
        """
        with open(self._get_path(path, is_titan_pylib), "r", encoding="utf-8") as f:
            tree = ast.parse(f.read())
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                self.added_modules.add(node.name)
                if self.verbose:
                    logger.info(f"[ FIND ] {path} {node.name}")

    def _find_defs(self, path: str, is_titan_pylib: bool) -> None:
        """defで始まる関数を列挙し、added_modulesに格納する
        (pathファイルは今見ている)
        """
        with open(self._get_path(path, is_titan_pylib), "r", encoding="utf-8") as f:
            linenum: int = 0
            for line in f:
                if not line.startswith("def"):
                    continue
                pattern = r"def\s+(.*?)\("
                matches = re.search(pattern, line)
                if matches:
                    defs = matches.group(1)
                    if self.verbose:
                        logger.info(f"[ FIND ] {path} {defs}()")
                    self.added_modules.add(defs)
                else:
                    logger.critical(
                        f"may be SyntaxError?\nfile: {path},\nlinenum: {linenum},\nline: {line}"
                    )
                    exit(1)

    def _get_code(self, path: str, is_titan_pylib: bool) -> None:
        """pathファイルを展開してoutputsに格納する"""

        # メモ化
        if self._get_path(path, is_titan_pylib) in self.seen_path:
            return
        self.seen_path.add(self._get_path(path, is_titan_pylib))

        # 今見ているファイルに必要なモジュール検出
        self._find_imported_modules(path, is_titan_pylib)

        # 今見ているファイルから取得できるモジュール検出
        self._find_classes(path, is_titan_pylib)
        self._find_defs(path, is_titan_pylib)

        # 1行ずつ見ていく
        linenum: int = 0
        with open(self._get_path(path, is_titan_pylib), "r", encoding="utf-8") as f:
            it = iter(f)
            while True:
                try:
                    line = next(it)
                    linenum += 1
                except StopIteration:
                    break

                if not line.startswith(f"from {LIB}"):
                    self.outputs.append(line)
                    continue

                pattern = r"from\s+(.*?)\s+import"
                matches = re.search(pattern, line)
                if matches:
                    module = matches.group(1)
                else:
                    logger.critical(
                        f"may be SyntaxError?\nfile: {path},\nlinenum: {linenum},\nline: {line}"
                    )
                    exit(1)
                if "(" in line:
                    while ")" not in line:
                        self.outputs.append(f"# {line}")
                        try:
                            line = next(it)
                            linenum += 1
                        except StopIteration:
                            break
                self.outputs.append(f"# {line}")
                self._get_code(module, True)

    def expand(self, output_fiepath: str, formatter: bool) -> None:
        """コードを展開してoutput_fiepathに書き出す"""
        self.outputs = []
        self._get_code(self.input_path, False)
        if self.need_modules - self.added_modules:
            if self.verbose:
                for cname in self.need_modules - self.added_modules:
                    logger.error(f"  {cname}")
            logger.critical("class not found.")
            exit(1)
        output_code = self._finalize(formatter)
        if output_fiepath in ["clip"]:
            output_fiepath = "clipboard"
            pyperclip.copy(output_code)
        else:
            with open(output_fiepath, "w", encoding="utf-8") as f:
                f.write(output_code)
        if self.verbose:
            logger.info("The process completed successfully.")
            logger.info(f"Output file: {output_fiepath} .")


if __name__ == "__main__":
    basicConfig(
        format="%(asctime)s [%(levelname)s] : %(message)s",
        datefmt="%H:%M:%S",
        level=os.getenv("LOG_LEVEL", "INFO"),
    )
    init_clipboard()

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "input_path",
    )
    parser.add_argument(
        "-o",
        "--output_path",
        default="clip",
        action="store",
    )
    parser.add_argument(
        "-f",
        "--formatter",
        required=False,
        action="store_true",
        default=False,
        help="do format. default is `False`.",
    )
    args = parser.parse_args()

    expander = Expander(args.input_path, True)
    expander.expand(args.output_path, args.formatter)
