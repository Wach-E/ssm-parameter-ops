multiline_string = '''PRIVATE_KEY=-----BEGIN OPENSSH PRIVATE KEY-----
REDACTED
-----END OPENSSH PRIVATE KEY-----'''
single_line_string = multiline_string.replace('\n', '\\n')
print(single_line_string)