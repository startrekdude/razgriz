# Razgriz vault creation and decryption routines
# Encoding a crypto logic goes elsewhere,
# as does user input

import razgriz.crypto as crypto
import razgriz.encoder as encoder

def linewrap(s, length=72):
	"""
	Tries to minimize the amount of paper used by a vault by
	putting short lines into two columns
	"""
	lines = s.split("\n")
	result = ""
	i = 0
	
	# Operate (usually) two lines at a time
	while i < len(lines):
		# special case last line
		if i == len(lines)-1:
			result += lines[i] + "\n"
			break
		
		current = lines[i]
		next = lines[i+1]
		if len(current) + 1 < length // 2 and len(next) < length // 2:
			# preserve empty lines
			if current == "":
				result += "\n"
				i += 1
				continue
			result += current + (" " * (length // 2 - len(current)))
			result += next + "\n"
			i += 2
		else:
			result += current + "\n"
			i += 1
	return result

class Razgriz:
	"The Razgriz vault creator"
	def __init__(self):
		self.time_cost = None
		self.memory_cost = None
		self.key = None
		self.count = 0
		self.result = ""
		self.header = ""
	
	def derive_key(self, pwd):
		"Derive a key - first step, also outputs vault header"
		self.header = "Razgriz Vault - time cost {}, memory cost {}\n".format(self.time_cost, self.memory_cost)
		self.key = crypto.derive_key(pwd, self.time_cost, self.memory_cost)
	
	def start_section(self, name):
		"Begin a new section-resets the counter"
		self.count = 0
		self.result += "\n{}\n".format(name)
	
	def add_secret(self, secret):
		"Add a secret to the vault, in the current section"
		self.count += 1
		
		# Encrypt and encode the secret, using a random nonce
		nonce = crypto.generate_nonce()
		ct = crypto.encrypt(secret, self.key, nonce)
		ct = nonce + ct
		coded = encoder.encode(ct)
		
		self.result += "{}. {}\n".format(self.count, coded)
	
	def finish(self):
		"Finish creating the vault and return it as a string"
		return self.header + linewrap(self.result)

class RazgrizDecryptor:
	"Decrypts secrets from a Razgriz vault created with the same key"
	def __init__(self, pwd, time_cost, memory_cost):
		self.key = crypto.derive_key(pwd, time_cost, memory_cost)
	def decrypt(self, secret):
		"Decrypt a single secret"
		ct = encoder.decode(secret)
		nonce = ct[:8]
		ct = ct[8:]
		return crypto.decrypt(ct, self.key, nonce)