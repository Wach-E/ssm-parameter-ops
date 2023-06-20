single_string = 'PRIVATE_KEY=-----BEGIN OPENSSH PRIVATE KEY-----\nREDACTED\n-----END OPENSSH PRIVATE KEY-----'

multiline_string = single_string.replace('\\n', '\n')
print(multiline_string)