import base64

file = "Keyractor.py"
out_file = "output.py"

fIn = open(file, 'r')
fOut = open(out_file, 'w')

b = base64.b64encode(bytes(str(fIn.read()), 'utf-8'))  # bytes
base64_str = b.decode('utf-8')  # convert bytes to string

fOut.write("import base64\n")
fOut.write(f"data = \"{base64_str}\"\n")
fOut.write("code = base64.b64decode(data).decode('utf-8')\n")
fOut.write("exec(code)\n")
fOut.write("if __name__ == \"__main__\":\n")
fOut.write("    print('test')\n")
fOut.close()

