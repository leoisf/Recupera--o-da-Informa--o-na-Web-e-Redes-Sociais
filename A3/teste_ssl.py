import sys
import ssl

print("Python:", sys.executable)
print("OpenSSL:", ssl.OPENSSL_VERSION)
print("Verify paths:", ssl.get_default_verify_paths())

try:
    import truststore
    truststore.inject_into_ssl()
    print("truststore: OK")
except Exception as e:
    print("truststore: FALHOU ->", e)