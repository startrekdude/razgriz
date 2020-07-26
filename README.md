# Razgriz

### An encrypted paper vault for 2FA recovery codes

Razgriz is a cryptographically secure encrypted paper vault designed for 2FA recovery codes. It uses a custom checksummed variant of [Base36](https://en.wikipedia.org/wiki/Base36) to fit more data on a page and make it easy for users to decrypt secrets—without having to transcribe long hexadecimal codes. The encryption key is derived using [Argon2](https://en.wikipedia.org/wiki/Argon2), and secrets are protected with [ChaCha20](https://en.wikipedia.org/wiki/Salsa20#ChaCha_variant).

## Usage

```shell
> python -m razgriz encrypt
Razgriz Encryption Mode
Select Argon2 Parameters
Rounds [8] ? 32
Memory Cost (MiB) [1000] ? 3072
Password?
Confirm?
(Key: 23589839ef5ba4e51d12a312bf9ac35fb4d98f390b5f6ebfaba7e5217a01360f)
Section Name? Google
Secret? example
Secret?
Section Name?
Razgriz Vault - time cost 32, memory cost 3145728

Google
1. 3W6RD-22FMV-69SHW-6WQNO-AH79T-FODYM

> python -m razgriz decrypt
Razgriz Decryption Mode
Password?
Confirm?
Please enter the vault parameters exactly as shown.
Time cost? 32
Memory cost? 3145728
Cipher? 3W6RD-22FMV-69SHW-6WQNO-AH79T-F0DYM
Checksum error in 'F0DY'
Cipher? 3W6RD-22FMV-69SHW-6WQNO-AH79T-FODYM
example
```

(Note: in encryption mode, only the vault is printed to stdout to allow for easy piping)

## Download

Please see the releases section for prebuilt Python 3 wheels.

## License

[GNU General Public License, version 3](https://choosealicense.com/licenses/gpl-3.0/)

## Name

[Isn't this a bop?](https://www.youtube.com/watch?v=mjY6awCr2_c)

## Limitations

Due to the short nonces used by Razgriz, security cannot be guaranteed if more than ~13,000 secrets are encrypted with the same key and Argon2 parameters. Given the intended use case of Razgriz, this should be easily avoidable.

