# the Razgriz crypto routines
# see each method for details

from os import urandom

from argon2.low_level import hash_secret_raw, Type
from Crypto.Cipher import ChaCha20

def derive_key(pwd, time_cost, memory_cost):
	"Derive an encryption key using Argon2id"
	
	# we don't use a salt here - why?
	# we're using this to derive an encryption key, not to hash passwords
	# rainbow tables are not a concern
	pwd = pwd.encode("utf8")
	return hash_secret_raw(pwd, b"\x00" * 16, time_cost, memory_cost, 8, 32, Type.ID, version=19)

def generate_nonce():
	"Generate a nonce suitable for use with ChaCha20"
	return urandom(8)

def encrypt(pt, key, nonce):
	"Encrypt a message using ChaCha20 with the given key and nonce"
	pt = pt.encode("utf8")
	enc = ChaCha20.new(key=key, nonce=nonce)
	return enc.encrypt(pt)

def decrypt(ct, key, nonce):
	"Decrypt a message using ChaCha20 with the given key and nonce"
	enc = ChaCha20.new(key=key, nonce=nonce)
	pt = enc.decrypt(ct).decode("utf8")
	return pt