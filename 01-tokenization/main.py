import tiktoken
# encoder - with pre-defined model
enc = tiktoken.encoding_for_model("gpt-4o")

# take input text
text = "Hello, I am Om Vishwakarma"
# convertion into token
tokens = enc.encode(text)

print("Tokens :", tokens)

# detokenization
Tokens = tokens 
decoded = enc.decode(Tokens)
print("Decoded text : ", decoded)


