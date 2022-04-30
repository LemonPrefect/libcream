import hashlib
from pathlib import Path

from sqlalchemy import and_

from app import database
from app.config import LIBC_DIR
from app.models import Distro, Lib, Symbol


def init():
    database.drop_all()
    database.create_all()
    libcs = _libcs()
    for libc in libcs:
        _add_lib(libc)


def update():
    libcs = _libcs()
    for libc in libcs:
        distro = _distro(libc)
        lib_name = libc.split("/")[-1][:-1]
        if len(database.session.query(Lib).filter(and_(Lib.name == lib_name, Lib.distro == distro)).all()) == 0:
            _add_lib(libc)


def _add_lib(libc: str) -> bool:
    distro = _distro(libc)
    symbol = _symbols(libc)
    base_url = _base_url(libc)
    lib_name = libc.split("/")[-1][:-1]

    if len(database.session.query(Distro).filter(Distro.name == distro).all()) == 0:
        database.session.add(Distro(name=distro))

    database.session.add(Lib(
        name=lib_name,
        distro=distro,
        hash=None if _so(libc) is None else hashlib.sha1(_so(libc)).hexdigest(),
        so_url=f"{lib_name}.so",
        base_url=base_url
    ))
    for key in symbol:
        database.session.add(Symbol(
            identifier=key,
            offset=symbol[key],
            lib_name=lib_name
        ))
    database.session.commit()
    return True


def _symbols(libc: str) -> dict:
    return {
        _[0]: _[1]
        for _ in [
            symbol.split(" ")
            for symbol in
            open(f"{libc}symbols", "r").read().strip().split("\n")
        ]
    }


def _base_url(libc: str) -> str:
    return open(f"{libc}url", "r").read().strip()


def _distro(libc: str) -> str:
    return open(f"{libc}info", "r").read().strip()


def _libcs() -> list:
    libc_dir = Path(LIBC_DIR)
    return [
        libc_dir.joinpath(file.name[:-4]).as_posix()
        for file in libc_dir.resolve().glob("*.info")
    ]


def _so(libc: str):
    try:
        return open(f"{libc}so", "rb")
    except FileNotFoundError:
        return None
