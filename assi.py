from openai import OpenAI
import time


API_KEY = "sk-nV0FCo8hRmX7HiPp8k4UZ7sC3-6RF0VeSilCTYYi-MT3BlbkFJ8SovrV2BrKlmXVuY7vtfY0qDTesylGzriiSjPRpgMA"
client = OpenAI(api_key=API_KEY)

assistant = client.beta.assistants.create(
    name = "Chat-bot",
    instructions="You are a chat bot. Answer to the opponent like a friend.",
    tools = [{"type": "code_interpreter"}],
    model="gpt-4o"
)

thread = client.beta.threads.create()

from typing_extensions import override
from openai import AssistantEventHandler
 
# First, we create a EventHandler class to define
# how we want to handle the events in the response stream.
 
class EventHandler(AssistantEventHandler):    
  @override
  def on_text_created(self, text) -> None:
    print(f"\nassistant > ", end="", flush=True)
      
  @override
  def on_text_delta(self, delta, snapshot):
    print(delta.value, end="", flush=True)
      
  def on_tool_call_created(self, tool_call):
    print(f"\nassistant > {tool_call.type}\n", flush=True)
  
  def on_tool_call_delta(self, delta, snapshot):
    if delta.type == 'code_interpreter':
      if delta.code_interpreter.input:
        print(delta.code_interpreter.input, end="", flush=True)
      if delta.code_interpreter.outputs:
        print(f"\n\noutput >", flush=True)
        for output in delta.code_interpreter.outputs:
          if output.type == "logs":
            print(f"\n{output.logs}", flush=True)
 
# Then, we use the `stream` SDK helper 
# with the `EventHandler` class to create the Run 
# and stream the response.


def chat(talk):
  message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content=talk
  )

  with client.beta.threads.runs.stream(
    thread_id=thread.id,
    assistant_id=assistant.id,
    instructions="한국어로 친절하게 답변하시오.",
    event_handler=EventHandler(),
  ) as stream:
    stream.until_done()

  messages = client.beta.threads.messages.list(
    thread_id=thread.id,
  )
  return messages.data[0].content[0].text.value, len(messages.data)




#============================================================


# def chat(talk):
#   message = client.beta.threads.messages.create(
#     thread_id=thread.id,
#     role="user",
#     content=talk
#   )
#   run = client.beta.threads.runs.create(
#     thread_id=thread.id,
#     assistant_id=assistant.id,
#     instructions="Answer as a interviewee.",
#   )
#   run_status = client.beta.threads.runs.retrieve(
#     thread_id=thread.id,
#     run_id=run.id
#   ).status
  
#   time.sleep(1)

#   messages = client.beta.threads.messages.list(
#     thread_id=thread.id,
#   )
  
#   # 마지막 답변 : messages.data[0].content[0].text.value
#   # 전체 답변 객체 : messages
#   # hist = []
#   # for i in range(len(messages.data)-1, -1, -1):
#   #   hist.append(messages.data[i].content[0].text.value)
    
#   return messages.data[0].content[0].text.value





