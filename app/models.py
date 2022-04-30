from app import database


class Symbol(database.Model):
    __table_args__ = {
        "mysql_engine": "InnoDB",
        "mysql_charset": "utf8"
    }
    __tablename__ = "symbol"
    id = database.Column(database.Integer, primary_key=True, unique=True, autoincrement=True)
    identifier = database.Column(database.VARCHAR(100))
    offset = database.Column(database.VARCHAR(100))
    lib_name = database.Column(database.VARCHAR(100), database.ForeignKey("lib.name", ondelete="CASCADE"))

    # relate_libs = database.relationship("Lib", backref="relate_symbols", lazy="dynamic")

    def __init__(self, identifier: str, offset: str, lib_name: str):
        self.identifier = identifier
        self.offset = offset
        self.lib_name = lib_name

    def __repr__(self):
        return f"<Database Object: Symbol {self.identifier}>"

    def toDict(self):
        return {
            "id": self.id,
            "identifier": self.identifier,
            "offset": self.offset,
            "lib_name": self.lib_name
        }


class Lib(database.Model):
    __table_args__ = {
        "mysql_engine": "InnoDB",
        "mysql_charset": "utf8"
    }
    __tablename__ = "lib"
    id = database.Column(database.Integer, primary_key=True, autoincrement=True)
    name = database.Column(database.VARCHAR(100), unique=True)
    distro = database.Column(database.VARCHAR(100), database.ForeignKey("distro.name", ondelete="CASCADE"))
    hash = database.Column(database.VARCHAR(64))
    so_url = database.Column(database.VARCHAR(200))
    base_url = database.Column(database.VARCHAR(200))

    def __init__(self, name: str, distro: str, hash: str, so_url: str, base_url: str):
        self.name = name
        self.distro = distro
        self.hash = hash
        self.so_url = so_url
        self.base_url = base_url

    def toDict(self):
        return {
            "id": self.id,
            "distro": self.distro,
            "hash": self.hash,
            "url": self.url
        }

    def __repr__(self):
        return f"<Database Object: Lib {self.name}>"


class Distro(database.Model):
    __table_args__ = {
        "mysql_engine": "InnoDB",
        "mysql_charset": "utf8"
    }
    __tablename__ = "distro"
    id = database.Column(database.Integer, primary_key=True, autoincrement=True)
    name = database.Column(database.VARCHAR(100), unique=True)

    def __init__(self, name: str):
        self.name = name

    def toDict(self):
        return {
            "id": self.id,
            "name": self.name
        }

    def __repr__(self):
        return f"<Database Object: Distro {self.name}>"


# sauce
# 报文分片
