# The Razgriz command line program
# Designed-for-paper encrypted vault for 2FA backup keys

# Everything here outputs to stderr, the idea being you
# can pipe *just the actual vault* to clip, or maybe a lpr, etc

from getpass import getpass
from sys import argv as args, stderr

from .encoder import ChecksumError
from .frontend import Razgriz, RazgrizDecryptor

def user_password():
	"Get a password from the user, forcing confirmation"
	while True:
		if (pwd := getpass("Password? ")) == getpass("Confirm? "):
			return pwd

def user_int(prompt, default=None):
	"""
	Reads an integer value from the user, allowing the user to retry
	until they enter a valid integer
	Optionally, allows a default value (this should be reflected in the prompt!)
	"""
	while True:
		print(prompt, file=stderr, end="")
		s = input()
		if s == "" and default: return default
		try:
			return int(s)
		except ValueError: continue

def encrypt():
	"Walks the user through creating a Razgriz vault"
	print("Razgriz Encryption Mode", file=stderr)
	r = Razgriz()
	
	# The Argon2 parameters
	print("Select Argon2 Parameters", file=stderr)
	r.time_cost = user_int("Rounds [8] ? ", 8)
	r.memory_cost = user_int("Memory Cost (MiB) [1000] ? ", 100) * 1024
	
	# Key
	r.derive_key(user_password())
	print("(Key: {})".format(r.key.hex()), file=stderr)
	
	# Allow sections - put multiple services in one vault
	while True:
		print("Section Name? ", file=stderr, end="")
		section_name = input()
		if section_name == "": break
		
		r.start_section(section_name)
		while True:
			print("Secret? ", file=stderr, end="")
			secret = input()
			if secret == "": break
			r.add_secret(secret)
	
	# this, and only this, goes to stdout - for easy piping
	print(r.finish())

def decrypt():
	"Walk the user through unlocking secrets stored in a Razgriz vault"
	print("Razgriz Decryption Mode", file=stderr)
	pwd = user_password()
	
	# Read back parameters
	print("Please enter the vault parameters exactly as shown.", file=stderr)
	time_cost = user_int("Time cost? ")
	memory_cost = user_int("Memory cost? ")
	
	r = RazgrizDecryptor(pwd, time_cost, memory_cost)
	
	# NOTE: the checksum error identifies fairly precisely the location
	# of the error
	while (s := input("Cipher? ")):
		try:
			print(r.decrypt(s))
		except ChecksumError as e:
			print(e.message)

def main():
	"Entry point. Reads args and dispatches the right action"
	if len(args) < 2:
		print("Usage: razgriz <decrypt|encrypt>", file=stderr)
		exit(-1)
	action = args[1]
	if action == "encrypt":
		encrypt()
	elif action == "decrypt":
		decrypt()
	else:
		print("Unknown action: '{}'".format(action), file=stderr)

if __name__ == "__main__":
	main()