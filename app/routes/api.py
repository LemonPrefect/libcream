import json
from json import JSONDecodeError
from flask import Blueprint, request
from sqlalchemy import or_, and_
from sqlalchemy.exc import SQLAlchemyError

from app import database
from app.models import Distro, Symbol, Lib

api = Blueprint("api", __name__)


@api.route("/libs", methods=["POST"])
def search_lib():
    """
    Search lib using symbols.
    :return: libs matched
    """
    try:
        args = json.loads(request.get_data(as_text=True))
    except JSONDecodeError as error:
        return json.dumps({
            "status": 1,
            "msg": f"at json parse: JSON parse error.\n{error}"
        })

    symbols = args.get("symbols", {})
    try:
        libs = database.session.query(
            Symbol.lib_name,
            Lib.distro,
            database.func.count("*")
        ).join(
            Lib, Lib.name == Symbol.lib_name
        ).filter(
            or_(*[and_(Symbol.identifier == key, Symbol.offset.like(f"%{symbols[key]}"))
                  for key in symbols])
        ).group_by(
            Symbol.lib_name
        ).order_by(
            database.func.count("*").desc()
        ).limit(50)
    except SQLAlchemyError as error:
        return json.dumps({
            "status": 1,
            "msg": f"at database query: Database query error.\n{error}"
        })
    """
    select lib_name, lib.distro, count(*) as times
    from symbol left join lib on lib.name = symbol.lib_name
    where (identifier = 'puts' and offset like('%ca0'))
    or (identifier = 'a64l' and offset like('%ad0'))
    or (identifier = 'abs' and offset like('%b50'))
    group by lib_name
    """
    if not libs:
        return json.dumps([])
    return json.dumps([{
        "distro": lib[1],
        "name": lib[0],
        "match": lib[2]
    } for lib in libs])


@api.route("/libs", methods=["GET"])
def libs():
    """
    Query all libs' name with limit and offset in specific distro.
    :return: json of info
    """
    distro_name = request.args.get("distro", type=str, default="")
    offset = request.args.get("offset", type=int, default=0)
    limit = request.args.get("limit", type=int, default=50)

    try:
        lib_names = database.session.query(Lib.name).filter(
            (Lib.distro == distro_name) if distro_name != "" else True
        ).limit(limit).offset(offset).all()
    except SQLAlchemyError as error:
        return json.dumps({
            "status": 1,
            "msg": f"at database query: Database query error.\n{error}"
        })
    if not lib_names:
        return json.dumps([])
    return json.dumps({"distro": distro_name, "libs": [lib_name[0] for lib_name in lib_names]})


@api.route("/lib/<lib_name>", methods=["GET"])
def lib(lib_name: str):
    """
    Query all info of a lib includes symbols and urls.
    :param lib_name: lib name
    :return: json of info
    """
    try:
        lib = database.session.query(Lib).filter(Lib.name == lib_name).first()
        symbols = database.session.query(Symbol.identifier, Symbol.offset).filter(Symbol.lib_name == lib_name).all()
    except SQLAlchemyError as error:
        return json.dumps({
            "status": 1,
            "msg": f"at database query: Database query error.\n{error}"
        })
    if not lib:
        return json.dumps([])

    return json.dumps({
        "distro": lib.distro,
        "name": lib.name,
        "hash": lib.hash,
        "base_url": lib.base_url,
        "so_url": lib.so_url,
        "symbols": {
            symbol[0]: symbol[1] for symbol in symbols
        }})


@api.route("/distro", methods=["GET"])
def distros():
    """
    Query all distros' name.
    :return: json of info
    """
    try:
        distro_names = database.session.query(Distro.name).all()
    except SQLAlchemyError as error:
        return json.dumps({
            "status": 1,
            "msg": f"at database query: Database query error.\n{error}"
        })
    if not distro_names:
        return json.dumps([])
    return json.dumps({"distros": [distro_name[0] for distro_name in distro_names]})


@api.route("/distro/<distro>", methods=["GET"])
def distro(distro_name: str):
    """
    Query all info of a distro includes libs.
    :param distro_name: distro name
    :return: json of info
    """
    try:
        libs = database.session.query(Lib).filter(Lib.distro == distro_name).all()
    except SQLAlchemyError as error:
        return json.dumps({
            "status": 1,
            "msg": f"at database query: Database query error.\n{error}"
        })
    if not libs:
        return json.dumps([])
    return json.dumps({
        "name": distro_name,
        "libs": [lib.name for lib in libs]
    })
