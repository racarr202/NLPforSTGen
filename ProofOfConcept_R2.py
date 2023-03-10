# python 3
# Richard Carr engineering applied AI proof of concept 
# Created 10/03/23

import os
import openai
from colorama import init, Fore, Style

openai.api_key = "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"

# Clear the terminal
os.system('cls' if os.name=='nt' else 'clear')

# Introduction to the user
print(Fore.GREEN + "Welcome to Richard Carr's structured text GPT-3 proof of concept application!\n" + Style.RESET_ALL)

print("This application is intended to showcase the the ability of OpenAI's GPT-3")
print("to generate structured text PLC code from ordinary english language.\n")



print("The model is trained to generate code for the following industrial scenarios:")
print("1. A conveyor that is started and stopped with a single pushbutton.")
print("2. A conveyor started and stopped with independent start/stop pushbuttons.")
print("3. A conveyor with two hand button press to run.\n")

# The user will input a his prompt now and the result stored in sUserPrompt
print("Please select one scenario and write in plain english what you want the code to do.")
print("Your answer will be put through three different natural language models, Base GPT-3, Codex followed by my personally fined tuned model (FTM).")
print("Note: You do not need to preface your prompt with anything like, \"Please write PLC code\" as this will be added for you.\n")
sUserPrompt = input(Fore.RED + "Enter your prompt:" + Style.RESET_ALL)

while True:

  # Make the prompt for the base model
  sBasePrompt = "Make structured text PLC code for the following input: " + sUserPrompt
  # First API call using base GPT model
  #try:
  response = openai.Completion.create(
    model="text-davinci-003",
    prompt=sBasePrompt,
    temperature=0.0,
    max_tokens=50,
    top_p=1,
    frequency_penalty=1,
    presence_penalty=0.5,
  )
  # display the text value within response
  print("\n\n\n")
  print(Fore.GREEN + "The prompt to base GPT-3 is:\n" + Style.RESET_ALL + sBasePrompt)
  print(Fore.GREEN + "The output from base GPT-3 is:" + Style.RESET_ALL)
  print(response["choices"][0]["text"].lstrip())
  """ except openai.Error.RateLimitError as e:
    print(f"An error occurred during the base GPT-3 API call: {e}")
    input("\n\nPress any key to exit the program...")  
    exit() """



  # Make the prompt for Codex
  sCodexPrompt = "// Structured text PLC code\n// " + sUserPrompt
    # Second API call using CODEX model
  #try:
  response = openai.Completion.create(
    model="code-davinci-002",
    prompt=sCodexPrompt,
    temperature=0.0,
    max_tokens=50,
    top_p=1,
    frequency_penalty=1.0,
    presence_penalty=0.5,
  )
  # display the text value within response
  print(Fore.GREEN + "\n\nThe prompt to Codex is:\n" + Style.RESET_ALL + sCodexPrompt)
  print(Fore.GREEN + "The output from Codex is:" + Style.RESET_ALL)
  print(response["choices"][0]["text"].lstrip())
  """ except openai.Error.RateLimitError as e:
    print(f"An error occurred during the base GPT-3 API call: {e}")
    input("\n\nPress any key to exit the program...")  
    exit() """


    # Third API call using my Fine Tuned Model with the prompt same as the base:
  #try:
  response = openai.Completion.create(
    model="curie:ft-engineering-applied-ai-2023-03-08-09-08-59",
    prompt=sBasePrompt,
    temperature=0.0,
    max_tokens=50,
    top_p=1,
    frequency_penalty=1.0,
    presence_penalty=0.5,
  )
  # display the text value within response
  print(Fore.GREEN + "\n\nThe prompt to my FTM is:\n" + Style.RESET_ALL + sBasePrompt)
  print(Fore.GREEN + "The output from my fine tuned model is:" + Style.RESET_ALL)
  print(response["choices"][0]["text"].lstrip())
  """ except openai.Error.RateLimitError as e:
    print(f"An error occurred during the base GPT-3 API call: {e}")
    input("\n\nPress any key to exit the program...")  
    exit() """

  print("\n\nWill any of the generated code work? If multiple will work which is more optimal?")
  answer = input("\nDo you want to try another scenario? (y/n): ")
  if answer.lower() == 'n':
    break
  
  print("\nThe three scenarios are:")
  print("1. A conveyor that is started and stopped with a single pushbutton.")
  print("2. A conveyor started and stopped with independent start/stop pushbuttons.")
  print("3. A conveyor with two hand button press to run.\n")

  sUserPrompt = input(Fore.RED + "Enter your prompt:" + Style.RESET_ALL)