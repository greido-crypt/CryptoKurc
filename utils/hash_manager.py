import hashlib
from pydantic import BaseModel


class HashResponse(BaseModel):
    sha256: str
    sha512: str


class HashManager:
    @staticmethod
    def get_hashes(data: bytes) -> HashResponse:
        sha256_hash = hashlib.sha256(data).hexdigest()
        sha512_hash = hashlib.sha512(data).hexdigest()
        return HashResponse(sha256=sha256_hash, sha512=sha512_hash)
