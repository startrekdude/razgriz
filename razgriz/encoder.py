# The Razgriz encoder
# Quite useful for paper-based vaults
# Easy to read, reasonably compact
# Identifies transcription errors precisely

B36_ALPHABET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"

class ChecksumError(ValueError):
	"Represents a checksum validation error"
	def __init__(self, message):
		super(ChecksumError, self).__init__(message)
		self.message = message

def b36encode(num):
	"Encodes a number into base36"
	s = ""
	while num:
		num, d = divmod(num, 36)
		s = B36_ALPHABET[d] + s
	return s

def chunkify(s, x):
	"Yields x-character chunks of s until it's completely consumed"
	i = 0
	while i < len(s):
		yield s[i:i+x]
		i += x

def checkdigit(s):
	"Calculates a checkdigit over s - s should be in base36"
	
	# very simple checksumming algorithm, still prevents switching characters
	x = 0
	for i, c in enumerate(s):
		x += ((i + 1) * B36_ALPHABET.index(c))
		x %= 36
	return B36_ALPHABET[x]

def make_checksum(s):
	"Makes checksums for a base36 encoded string"
	return "-".join(chunk + checkdigit(chunk) for chunk in chunkify(s, 4))

def encode(b):
	"Encode a value for storage in a Razgriz vault"
	b = b"\x01" + b # to prevent leading zero bytes from being stripped
	num = int.from_bytes(b, "big", signed=False)
	return make_checksum(b36encode(num))

def validate_checksum(s):
	"""
	Validates checksums, throwing a ChecksumError as required
	Returns the value without checksums
	"""
	parts = s.split("-")
	result = ""
	for part in parts:
		*part, check = part
		if checkdigit(part) != check:
			raise ChecksumError("Checksum error in '{}'".format("".join(part)))
		result += "".join(part)
	return result

def decode(s):
	"Decode a value from a Razgriz vault"
	s = validate_checksum(s)
	x = int(s, 36)
	return x.to_bytes((x.bit_length() + 7) // 8, "big", signed=False)[1:]