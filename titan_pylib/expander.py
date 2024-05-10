# user settings --------------------------------------------------
# LIB_PATH = "/mnt/c/Users/titan/source/Library_py"
LIB_PATH = "C:\\Users\\titan\\source\\Library_py\\"
#  ----------------------------------------------------------------

from logging import getLogger, basicConfig
import sys
import pyperclip
import ast
import re
import black
from os import getenv

LIB = "titan_pylib"

logger = getLogger(__name__)


class Expander:
    """titan_pylib の expander"""

    def __init__(self, input_path: str) -> None:
        self.input_path = input_path
        self.seen_path = set()
        self.added_modules = set()
        self.need_modules = set()
        self.outputs: list[str] = []

    def _finalize(self) -> str:
        """self.outputsの最終処理をしたコードを返す
        - black-formatをかける
        """
        code = black.format_str("".join(self.outputs), mode=black.FileMode())
        try:
            ast.parse(code)
        except SyntaxError as e:
            logger.critical(f"Syntax Error in _finalize()\n{e}")
            exit(1)
        return code

    def _get_path(self, path: str, is_titan_pylib: bool) -> str:
        """pathをスラッシュ表記にする"""
        if is_titan_pylib:
            path = LIB_PATH + path.replace(".", "/") + ".py"
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

    def _find_classes(self, path: str, is_titan_pylib: bool) -> None:
        """classで始まるモジュールを列挙し、added_modulesに格納する
        (pathファイルは今見ている)
        """
        with open(self._get_path(path, is_titan_pylib), "r", encoding="utf-8") as f:
            tree = ast.parse(f.read())
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                self.added_modules.add(node.name)
                logger.info(f"{path} {node.name}")

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
                    logger.info(f"{path} {defs}")
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

    def expand(self, output_fiepath: str) -> None:
        """コードを展開してoutput_fiepathに書き出す"""
        self.outputs = []
        self._get_code(self.input_path, False)
        if self.need_modules - self.added_modules:
            for cname in self.need_modules - self.added_modules:
                logger.error(f"  {cname}")
            raise ImportError("class not found.")
        output_code = self._finalize()
        if output_fiepath in ["clip"]:
            output_fiepath = "clipboard"
            pyperclip.copy(output_code)
        else:
            with open(output_fiepath, "w", encoding="utf-8") as f:
                f.write(output_code)
        logger.info("The process completed successfully.")
        logger.info(f"Output file: {output_fiepath} .")


if __name__ == "__main__":
    basicConfig(
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%H:%M:%S",
        level=getenv("LOG_LEVEL", "INFO"),
    )
    input_path = sys.argv[1]
    output_filepath = sys.argv[2] if len(sys.argv) == 3 else "clip"
    expander = Expander(input_path)
    expander.expand(output_filepath)
