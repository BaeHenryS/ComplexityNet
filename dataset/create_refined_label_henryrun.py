import time 
import jsonlines
import os
import openai
from openai import OpenAI
from dotenv import load_dotenv
import textwrap
import signal
import time
from contextlib import contextmanager

class TimeoutException(Exception): pass

@contextmanager
def time_limit(seconds):
    def signal_handler(signum, frame):
        raise TimeoutException("Timed out!")
    signal.signal(signal.SIGALRM, signal_handler)
    signal.alarm(seconds)
    try:
        yield
    finally:
        signal.alarm(0)


import bisect
import collections
import math
import heapq
import operator
import datetime
import itertools
import cmath
import sys
import re
import array
import copy
from collections import Counter


def getCodeFormat(code_input):
    # Make an OPENAI API Call to only return the function call and its inputs
    '''EXAMPLE:
    INPUT: class Pair(object): def __init__(self, a, b): self.a = a self.b = b def max_chain_length(arr, n): max = 0 mcl = [1 for i in range(n)] for i in range(1, n): for j in range(0, i): if (arr[i].a > arr[j].b and mcl[i] < mcl[j] + 1): mcl[i] = mcl[j] + 1 for i in range(n): if (max < mcl[i]): max = mcl[i] return max
    
    OUTPUT: Class Pair(object) def max_chain_length(arr, n)
    '''

    response = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=[
            {
                "role": "system",
                "content": "Return only the function definition, its inputs, and the output type from the code given by the user. Example: INPUT: class Pair(object): def __init__(self, a, b): self.a = a self.b = b def max_chain_length(arr, n): max = 0 mcl = [1 for i in range(n)] for i in range(1, n): for j in range(0, i): if (arr[i].a > arr[j].b and mcl[i] < mcl[j] + 1): mcl[i] = mcl[j] + 1 for i in range(n): if (max < mcl[i]): max = mcl[i] return max OUTPUT: Class Pair(object) def max_chain_length(arr, n) #-> int"
            },
            {
                "role": "user",
                "content": code_input
            }
        ],
        temperature=1,
        max_tokens=1024,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    
    responseText = response.choices[0].message.content

    # Remove the ```python and ``` from the response
    responseText = responseText.replace("```python", "")
    responseText = responseText.replace("```", "")

    responseText = textwrap.dedent(responseText)

    return responseText

def generateCode(modelType, userPrompt): 
    # Models: "gpt-4-1106-preview", "gpt-3.5-turbo-1106"
    response = client.chat.completions.create(
    model=modelType,
    messages=[
        {
            "role": "system",
            "content": "You are an expert in writing Python code. You will generate a Python Script that will complete the task outlined by the user. You will not provide any explanations, and only return the Python Script without the explanation of the code. The most IMPORTANT note is to have precise indents in your output. It is IMPORTANT to only include python code, and nothing else. Your response should start with ```python and end with ```"
        },
        {
            "role": "user",
            "content": userPrompt
        }
    ],
    temperature=1,
    max_tokens=2047,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
    )
    responseText = response.choices[0].message.content

    # Remove the ```python and ``` from the response
    responseText = responseText.replace("```python", "")
    responseText = responseText.replace("```", "")

    #Fix Spacing from responseTest so it can run on exec()
 



    return responseText



def checkCorrectness(output, obj):
    # Execute the code:
    try:
        exec(output)
    except Exception as e:
        # Continue to the next example and print the error
        print(f"Error: {e}")
        return False
    
    assertion_code = obj['test_list']

    success = True
    for assertion in assertion_code:
        try:
            exec(assertion)
            print("Code Passed Assertions")
        except Exception as e:
            # Continue to the next example and print the error
            print(f"Error: {e}")
            print("Code Failed Assertions")
            success = False

    return success
    
if __name__ == '__main__':
    # Create a text file storing progress   
    #max_loop = 974
    max_loop = 100
    # See how many rows are in mbpp_label_refined jsonl file
    with jsonlines.open('mbpp_label_refined_250.jsonl') as reader:
        i = sum(1 for _ in reader)
    # openai.api_key = os.getenv('OPENAI_API_KEY')
    load_dotenv()
    client = OpenAI(api_key= os.getenv('OPENAI_API_KEY'), )
    # client = OpenAI(api_key=openai.api_key)

    # GPT4 Model
    # Open JSONL File:
    with jsonlines.open('mbpp.jsonl') as reader: 
        # Loop through each example
        for count, obj in enumerate(reader):
            # Start from the last example that was run
            with jsonlines.open('mbpp_label_refined_250.jsonl') as reader:
                i = sum(1 for _ in reader)
            if count < i:
                continue
            print("Running Example: " + str(i))
            prompt = obj['text']
            code = obj['code']
            #print(obj['code'])
            # Call the getCodeFormat function to get the function call and its inputs
            #function_call = getCodeFormat(code)
            with time_limit(10):
                try:
                    function_call = getCodeFormat(code)
                except TimeoutError:
                    time.sleep(10)
                    try:
                        print("Timeout Error")
                        function_call = getCodeFormat(code)
                    except TimeoutError:
                        time.sleep(15)
                        try:
                            print("Timeout Error")
                            function_call = getCodeFormat(code)
                        except TimeoutError:
                            print("Timeout Error")
                            time.sleep(20)
                            function_call = getCodeFormat(code)


            print("Function Call")
            print(function_call)
            userPrompt =  prompt + " The name of the function should be "  + function_call + "\n\n"
            
            
            success_gpt3_5 = 0
            success_gpt4 = 0

            for _ in range(5):
                with time_limit(10):
                    try:
                        print("Running GPT-4")
                        responseText_gpt4 = generateCode("gpt-4-1106-preview", userPrompt)
                        print("Running GPT-3.5")
                        responseText_gpt3_5 = generateCode("gpt-3.5-turbo-1106", userPrompt)
                    except TimeoutError:
                        time.sleep(10)  # Wait for 10 seconds
                        try:
                            print("Timeout Error")
                            responseText_gpt4 = generateCode("gpt-4-1106-preview", userPrompt)
                            responseText_gpt3_5 = generateCode("gpt-3.5-turbo-1106", userPrompt)
                        except TimeoutError:
                            time.sleep(30)  # Wait for 1 minutes
                            try:
                                print("Timeout Error")
                                responseText_gpt4 = generateCode("gpt-4-1106-preview", userPrompt)
                                responseText_gpt3_5 = generateCode("gpt-3.5-turbo-1106", userPrompt)
                            except TimeoutError:
                                print("Timeout Error")
                                time.sleep(30)  # Wait for 4 minutes
                                responseText_gpt4 = generateCode("gpt-4-1106-preview", userPrompt)
                                responseText_gpt3_5 = generateCode("gpt-3.5-turbo-1106", userPrompt)

                # Check the correctness of the code 
                if checkCorrectness(responseText_gpt4, obj):
                    success_gpt4 += 1


                if checkCorrectness(responseText_gpt3_5, obj):
                    success_gpt3_5 += 1

                time.sleep(10)

            



        

            # Write to JSONL File
            obj["method2_gpt4_output"] = responseText_gpt4
            obj["method2_gpt3_5_output"] = responseText_gpt3_5
            obj["method2_gpt4_success"] = success_gpt4
            obj["method2_gpt3_5_success"] = success_gpt3_5

            with jsonlines.open('mbpp_label_refined_250.jsonl', mode='a') as writer:
                writer.write(obj)
            
            if i == max_loop:
                break
            
            
            time.sleep(5)


