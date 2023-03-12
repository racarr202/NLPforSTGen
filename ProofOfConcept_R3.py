# python 3
# Richard Carr engineering applied AI proof of concept 
# Created 10/03/23

import os
import openai
from flask import Flask, render_template, request, session

#Enter the open AI api key
openai.api_key = "SET API HERE!"
# This function takes a string sPrompt and sModel as arguments and returns either error or the response from GPT-3 
def sGetGPTReply(sPrompt, sModel):
  # print stuff to the terminal just for debug purposes
  print("Prompt sent: \n" + sPrompt + "\nTo model:" + sModel)
  try:
    response = openai.Completion.create(
      model=sModel,
      prompt=sPrompt,
      temperature=0.0,
      max_tokens=50,
      top_p=1,
      frequency_penalty=1,
      presence_penalty=0.5,
    )
    # print stuff to the terminal just for debug purposes
    print("Reply recieved:\n" + response["choices"][0]["text"].lstrip())
    return response["choices"][0]["text"].lstrip()
  except openai.Error as e:
    return f"An error occurred during the API call: {e}"
  

app = Flask(__name__)
app.secret_key = "SekRetKey"

@app.route('/', methods=['GET'])
def index():

  sUserPrompt = request.args.get('userPrompt','')
  
  # Only render the table with the Open AI responses if the user prompt exists in the GET data
  if sUserPrompt != '':
    # If user prompt hasn't changed and all cached data is there dont bother re-doing the API calls...
    if (
      sUserPrompt == session.get('lastUserPrompt', None)
      and session.get('prompt1', '') != ''
      and session.get('prompt2', '') != ''
      and session.get('prompt3', '') != ''
      and session.get('model1Output', '') != ''
      and session.get('model2Output', '') != ''
      and session.get('model3Output', '') != ''
      ):
        # ...just return the result cached in session data
        prompt1 = session.get('prompt1', '')
        prompt2 = session.get('prompt2', '')
        prompt3 = session.get('prompt3', '')
        model1Output = session.get('model1Output', '')
        model2Output = session.get('model2Output', '')
        model3Output = session.get('model3Output', '')
    # User prompt has changed or a re-gen is requested, run the Open AI requests
    else:
        # Set the prompts appropriate prefix
        sBasePrompt = "Make structured text PLC code for the following prompt: " + sUserPrompt
        sCodexPrompt = "// Structured text PLC code\n// " + sUserPrompt

        # Run the API requests
        model1Output = sGetGPTReply(sBasePrompt, "text-davinci-003").strip()
        model2Output = sGetGPTReply(sCodexPrompt, "code-cushman-001").strip()
        model3Output = sGetGPTReply(sBasePrompt, "curie:ft-engineering-applied-ai-2023-03-08-09-08-59").strip()

        # Cache the results and the user prompt in session data so that the API requests wont run on page refreshes
        session['lastUserPrompt'] = sUserPrompt
        session['model1Output'] = model1Output
        session['model2Output'] = model2Output
        session['model3Output'] = model3Output
        prompt1 = sBasePrompt
        prompt2 = sCodexPrompt
        prompt3 = sBasePrompt
        session['prompt1'] = prompt1
        session['prompt2'] = prompt2
        session['prompt3'] = prompt3

    return render_template('index.html', model1Output=model1Output, model2Output=model2Output, model3Output=model3Output, prompt1=prompt1, prompt2=prompt2, prompt3=prompt3)
  else:
    # If no user prompt make sure the variables are cleared before rendering
    prompt1 = None
    prompt2 = None
    prompt3 = None
    model1Output = None
    model2Output = None
    model3Output = None

    # Render without the table showing the API responses
    return render_template('index.html')

if __name__ == '__main__':
  app.run(host='127.0.0.1', debug=True, use_reloader=True, port=5000)