#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
cache_reader.py — чтение кеша из указанной директории.

Программа получает путь к директории, рекурсивно находит в ней файлы
и выводит их содержимое в консоль: текст — как текст, бинарные данные —
в виде hex-превью.

Использование:
    python3 cache_reader.py ДИРЕКТОРИЯ [опции]

Примеры:
    python3 cache_reader.py /var/cache/myapp
    python3 cache_reader.py ~/.cache --pattern "*.db"
    python3 cache_reader.py /tmp/cache --list
    python3 cache_reader.py /tmp/cache --max-size 0        # читать файлы целиком
"""

import argparse
import fnmatch
import os
import sys
from datetime import datetime
from pathlib import Path

DEFAULT_MAX_SIZE = 64 * 1024  # превью по умолчанию: 64 КиБ


# ---------------------------------------------------------------------------
# Вспомогательные функции
# ---------------------------------------------------------------------------

def human_size(num: int) -> str:
    """Человекочитаемый размер: 1.5 КБ, 3.2 МБ и т.д."""
    if num < 1024:
        return f"{num} Б"
    value = float(num)
    for unit in ("КБ", "МБ", "ГБ", "ТБ"):
        value /= 1024.0
        if value < 1024:
            return f"{value:.1f} {unit}"
    return f"{value:.1f} ПБ"


def looks_like_text(data: bytes) -> bool:
    """Эвристика: похожи ли байты на текст."""
    if not data:
        return True
    if b"\x00" in data:
        return False
    textish = sum(1 for b in data if 32 <= b < 127 or b in (9, 10, 13) or b >= 128)
    return textish / len(data) >= 0.85


def decode_text(data: bytes) -> tuple[str, str]:
    """Декодировать байты в текст. Возвращает (текст, имя кодировки)."""
    if data.startswith((b"\xff\xfe", b"\xfe\xff")):
        try:
            return data.decode("utf-16"), "utf-16"
        except UnicodeDecodeError:
            pass
    try:
        return data.decode("utf-8"), "utf-8"
    except UnicodeDecodeError:
        pass
    # Возможно, UTF-8 обрезан посреди многобайтового символа (превью).
    # Если «битых» символов почти нет — восстанавливаем UTF-8.
    repaired = data.decode("utf-8", errors="replace")
    if repaired.count("\ufffd") <= 2:
        return repaired, "utf-8 (обрезано, восстановлено)"
    for enc in ("cp1251", "koi8-r", "latin-1"):
        try:
            return data.decode(enc), enc
        except UnicodeDecodeError:
            continue
    return data.decode("latin-1", errors="replace"), "latin-1"


def sanitize(line: str) -> str:
    """Убрать управляющие символы, чтобы не ломать вывод терминала."""
    out = []
    for ch in line:
        if ch == "\t":
            out.append("    ")
        elif ord(ch) >= 32:
            out.append(ch)
        else:
            out.append(f"\\x{ord(ch):02x}")
    return "".join(out)


def hexdump(data: bytes) -> str:
    """Классический hex-dump: смещение, hex-байты, ASCII-представление."""
    lines = []
    for off in range(0, len(data), 16):
        chunk = data[off:off + 16]
        hex_part = " ".join(f"{b:02x}" for b in chunk)
        ascii_part = "".join(chr(b) if 32 <= b < 127 else "." for b in chunk)
        lines.append(f"    {off:08x}  {hex_part:<47}  |{ascii_part}|")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Обход директории и чтение файлов
# ---------------------------------------------------------------------------

def iter_files(root: Path, pattern: str, recursive: bool):
    """Генератор путей к файлам, имена которых подходят под glob-шаблон."""
    def onerror(exc):
        print(f"  [!] не удалось войти в каталог: {exc}", file=sys.stderr)

    if recursive:
        for dirpath, dirnames, filenames in os.walk(root, followlinks=False,
                                                    onerror=onerror):
            dirnames.sort()
            for name in sorted(filenames):
                if fnmatch.fnmatch(name, pattern):
                    yield Path(dirpath) / name
    else:
        for p in sorted(root.iterdir()):
            if p.is_file() and fnmatch.fnmatch(p.name, pattern):
                yield p


def dump_file(path: Path, index: int, total: int,
              max_size: int, list_only: bool) -> int:
    """Прочитать один файл и напечатать его содержимое. Возвращает размер."""
    stat = path.stat()
    mtime = datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S")
    print(f"\n[{index}/{total}] {path}")
    print(f"    размер: {human_size(stat.st_size)} ({stat.st_size} Б) "
          f"| изменён: {mtime}")

    if list_only:
        return stat.st_size

    limit = stat.st_size if max_size <= 0 else min(max_size, stat.st_size)
    with path.open("rb") as f:
        data = f.read(limit)

    if looks_like_text(data):
        text, enc = decode_text(data)
        note = "" if limit == stat.st_size else (
            f" (показано первые {human_size(limit)})")
        print(f"    текст, кодировка {enc}{note}:")
        if text:
            for line in text.splitlines():
                print(f"    | {sanitize(line)}")
        else:
            print("    | (пустой файл)")
    else:
        note = "" if limit == stat.st_size else f", превью {human_size(limit)}"
        print(f"    бинарные данные{note}:")
        print(hexdump(data))

    return stat.st_size


# ---------------------------------------------------------------------------
# Точка входа
# ---------------------------------------------------------------------------

def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        prog="cache_reader.py",
        description="Читает файлы кеша из указанной директории "
                    "и выводит их содержимое в консоль.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Примеры:\n"
               "  python3 cache_reader.py /var/cache/myapp\n"
               "  python3 cache_reader.py ~/.cache -m '*.db'\n"
               "  python3 cache_reader.py /tmp/cache --list\n"
               "  python3 cache_reader.py /tmp/cache -n 0",
    )
    parser.add_argument("directory", metavar="ДИРЕКТОРИЯ",
                        help="путь к директории с кешем")
    parser.add_argument("-m", "--pattern", default="*", metavar="ШАБЛОН",
                        help="фильтр имён файлов (glob, по умолчанию '*')")
    parser.add_argument("-n", "--max-size", type=int, default=DEFAULT_MAX_SIZE,
                        metavar="БАЙТ",
                        help="сколько байт читать из каждого файла; "
                             "0 — целиком (по умолчанию 65536)")
    parser.add_argument("--flat", action="store_true",
                        help="не заходить в поддиректории")
    parser.add_argument("--list", action="store_true",
                        help="только перечислить файлы, не читая содержимое")
    args = parser.parse_args(argv)

    root = Path(args.directory).expanduser()
    if not root.exists():
        print(f"Ошибка: путь не существует: {root}", file=sys.stderr)
        return 2
    if not root.is_dir():
        print(f"Ошибка: это не директория: {root}", file=sys.stderr)
        return 2

    files = list(iter_files(root, args.pattern, recursive=not args.flat))
    print(f"Директория: {root}")
    print(f"Найдено файлов: {len(files)} (шаблон: {args.pattern!r})")
    if not files:
        return 0

    total_size = read_ok = errors = 0
    for i, path in enumerate(files, 1):
        try:
            total_size += dump_file(path, i, len(files),
                                    args.max_size, args.list)
            read_ok += 1
        except OSError as exc:
            errors += 1
            print(f"\n[{i}/{len(files)}] {path}", file=sys.stderr)
            print(f"    [!] ошибка чтения: {exc}", file=sys.stderr)

    print(f"\nИтого: {len(files)} файлов, общий размер "
          f"{human_size(total_size)}; прочитано {read_ok}, ошибок {errors}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
