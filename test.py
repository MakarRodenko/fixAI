from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
tokenizer = AutoTokenizer.from_pretrained("deepseek-ai/deepseek-coder-1.3b-instruct", trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained("deepseek-ai/deepseek-coder-1.3b-instruct", trust_remote_code=True, torch_dtype=torch.bfloat16).cuda()
messages=[
    { 
        'role': 'system', 
        'content': "You are an artificial intelligence programming assistant, use the Deep Seek Coder model developed by DeepSeek, and answer only questions related to computer science and secure development. You will refuse to answer politically sensitive questions, security and privacy issues, as well as other questions unrelated to computer science and secure development."
    },
    {
        'role':'user',
        'content':"Python's eval() function can lead to arbitrary code execution if used improperly, posing a security risk. Rewrite the vulnerable code: ```python\nimport os\n\ndef run_command(user_input):\n    command = eval(user_input)\n    os.system(command)\n\nrun_command(input(\"Enter a command: \"))\n```"
    },
    {
        'role':'assistant',
        'content':'```python\nimport subprocess\n\ndef run_command(user_input):\n    command = user_input.split()\n    subprocess.run(command, shell=False)\n\nrun_command(input(\"Enter a command: \"))\n```'
    },
    {
        'role':'user',
        'content': "Good! In Python, improper input validation can lead to arbitrary code execution vulnerabilities. Rewrite the vulnerable code: ```python\nimport os\nimport subprocess\n\ndef execute_command(user_input):\n    command = 'ls ' + user_input\n    output = subprocess.check_output(command, shell=True)\n    print(output)\n\nuser_input = input(\"Enter your command: \")\nexecute_command(user_input)\n```"
    }
]
messages1=[
    { 
        'role': 'system', 
        'content': "You are an artificial intelligence programming assistant, use the Deep Seek Coder model developed by DeepSeek, and answer only questions related to computer science and secure development. You will refuse to answer politically sensitive questions, security and privacy issues, as well as other questions unrelated to computer science and secure development."
    },
    {
        'role':'user',
        'content':"Write a python code that connects to an SQLite database named 'mydatabase.db'. The code should have a function called 'get_user_info' which takes a parameter 'username'. This function should execute a SQL query to select all columns from the table 'users' where the 'username' matches the input parameter. It should then fetch the first row of the result and return it. Rewrite the vulnerable code: ```python\nimport sqlite3\n\ndef get_user_info(username):\n    conn = sqlite3.connect('mydatabase.db')\n    cursor = conn.cursor()\n    \n    query = \"SELECT * FROM users WHERE username = '\" + username + \"'\"\n    cursor.execute(query)\n    \n    user_info = cursor.fetchone()\n    return user_info\n\n# Testing the function\nprint(get_user_info(\"john\"))\n```"
    },
    {
        'role':'assistant',
        'content':"```python\nimport sqlite3\n\ndef get_user_info(username):\n    conn = sqlite3.connect('mydatabase.db')\n    cursor = conn.cursor()\n    \n    # Use parameter substitution to avoid SQL injection\n    cursor.execute(\"SELECT * FROM users WHERE username = ?\", (username,))\n    \n    user_info = cursor.fetchone()\n    return user_info\n\n# Testing the function\nprint(get_user_info(\"john\"))\n```"
    },
    {
        'role':'user',
        'content': "Good! Write a python code that connects to an SQLite database named 'database.db'. The code should have a function called 'get_user_info' which takes a parameter 'username'. This function should execute a SQL query to select all columns from the table 'users' where the 'username' matches the input parameter. It should then fetch the first row of the result and return it. Rewrite the vulnerable code: ```python\nimport sqlite3\n\ndef get_user_info(username):\n    conn = sqlite3.connect('database.db')\n    cursor = conn.cursor()\n    \n    query = \"SELECT * FROM admins WHERE login = '\" + username + \"'\"\n    cursor.execute(query)\n    \n    user_info = cursor.fetchone()\n    return user_info\n\nprint(get_user_info(\"john\"))\n```"
    }
]

'''{"lang": "python", 
"vulnerability": "Python's eval() function can lead to arbitrary code execution if used improperly, posing a security risk.", 
"question": "Write a python code that imports the os module and defines a function 'run_command' which takes user input, evaluates it into a command using the eval function, and then executes that command using the os.system function. The function should be called with user input taken from the console.", 
"chosen": "```python\nimport subprocess\n\ndef run_command(user_input):\n    command = user_input.split()\n    subprocess.run(command, shell=False)\n\nrun_command(input(\"Enter a command: \"))\n```", 
"rejected": "```python\nimport os\n\ndef run_command(user_input):\n    command = eval(user_input)\n    os.system(command)\n\nrun_command(input(\"Enter a command: \"))\n```"}'''
'''"lang": "python", 
"vulnerability": "In Python, improper input validation can lead to arbitrary code execution vulnerabilities.", 
"question": "Write a python code that takes user input and executes it as a command in the terminal using the 'subprocess' module. The command should be 'ls' followed by the user input.", 
"chosen": "```python\nimport subprocess\n\ndef execute_command(user_input):\n    # Validate input to prevent command injection\n    if any(char in user_input for char in [';', '&', '|']):\n        print(\"Invalid input. Please enter a valid filename.\")\n        return\n    \n    command = ['ls', user_input]\n    try:\n        output = subprocess.check_output(command, stderr=subprocess.STDOUT)\n        print(output.decode())\n    except subprocess.CalledProcessError as e:\n        print(f\"Command failed with error: {e}\")\n\nuser_input = input(\"Enter your command: \")\nexecute_command(user_input)\n```", 
"rejected": "```python\nimport os\nimport subprocess\n\ndef execute_command(user_input):\n    command = 'ls ' + user_input\n    output = subprocess.check_output(command, shell=True)\n    print(output)\n\nuser_input = input(\"Enter your command: \")\nexecute_command(user_input)\n```"}
'''
'''
"vulnerability": "Python code can be vulnerable to SQL injection attacks if it directly incorporates user input into an SQL query without proper sanitization.", 
"system": "", 
"question": "
Write a python code that connects to an SQLite database named 'mydatabase.db'. The code should have a function called 'get_user_info' which takes a parameter 'username'. This function should execute a SQL query to select all columns from the table 'users' where the 'username' matches the input parameter. It should then fetch the first row of the result and return it.
", 
"chosen": "```python\nimport sqlite3\n\ndef get_user_info(username):\n    conn = sqlite3.connect('mydatabase.db')\n    cursor = conn.cursor()\n    \n    # Use parameter substitution to avoid SQL injection\n    cursor.execute(\"SELECT * FROM users WHERE username = ?\", (username,))\n    \n    user_info = cursor.fetchone()\n    return user_info\n\n# Testing the function\nprint(get_user_info(\"john\"))\n```", 
"rejected": "```python\nimport sqlite3\n\ndef get_user_info(username):\n    conn = sqlite3.connect('mydatabase.db')\n    cursor = conn.cursor()\n    \n    query = \"SELECT * FROM users WHERE username = '\" + username + \"'\"\n    cursor.execute(query)\n    \n    user_info = cursor.fetchone()\n    return user_info\n\n# Testing the function\nprint(get_user_info(\"john\"))\n```"
'''
print("Start")
inputs = tokenizer.apply_chat_template(messages1, add_generation_prompt=True, return_tensors="pt").to(model.device)
# tokenizer.eos_token_id is the id of <|EOT|> token
#inputs = tokenizer(input_text, return_tensors="pt").to(model.device)
outputs = model.generate(inputs, max_new_tokens=512, do_sample=False, top_k=50, top_p=0.95, num_return_sequences=1, eos_token_id=tokenizer.eos_token_id)
print(tokenizer.decode(outputs[0][len(inputs[0]):], skip_special_tokens=True))
