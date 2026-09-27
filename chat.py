import sys
import json
import urllib.request

API_URL = "http://127.0.0.1:8080/v1/chat/completions"

SYSTEM_PROMPT = {
    "role": "system",
    "content": "You are a helpful, concise, and technical AI assistant."
}

def stream_chat():
    messages = [SYSTEM_PROMPT]
    
    print("\n" + "="*50)
    print(" 🤖 MiniCPM 1B Local Chat Interface")
    print(" Type 'exit' or 'quit' to end | Type 'clear' to reset history")
    print("="*50 + "\n")

    while True:
        try:
            user_input = input("\nYou: ").strip()
            if not user_input:
                continue
            
            if user_input.lower() in ("exit", "quit"):
                print("\nGoodbye!")
                break
            
            if user_input.lower() == "clear":
                messages = [SYSTEM_PROMPT]
                print("\n[Conversation history cleared]")
                continue

            # Append user message
            messages.append({"role": "user", "content": user_input})

            payload = {
                "model": "MiniCPM5-1B",
                "messages": messages,
                "temperature": 0.7,
                "max_tokens": 1024,
                "stream": True  # Enable real-time token streaming
            }

            req = urllib.request.Request(
                API_URL,
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json"}
            )

            print("\nMiniCPM: ", end="", flush=True)
            assistant_reply = ""

            with urllib.request.urlopen(req) as response:
                for line in response:
                    line = line.decode("utf-8").strip()
                    if not line or not line.startswith("data: "):
                        continue
                    
                    data_str = line[6:]
                    if data_str == "[DONE]":
                        break
                    
                    try:
                        data = json.loads(data_str)
                        delta = data["choices"][0].get("delta", {})
                        chunk = delta.get("content")
                        
                        # Only print and add if chunk is an actual string, ignoring None
                        if chunk: 
                            print(chunk, end="", flush=True)
                            assistant_reply += chunk
                    except json.JSONDecodeError:
                        continue

            print()  # Newline after stream finishes
            messages.append({"role": "assistant", "content": assistant_reply})

        except KeyboardInterrupt:
            print("\n\nSession interrupted. Exiting...")
            break
        except Exception as e:
            print(f"\n[Error connecting to server: {e}]")
            print("Make sure your llama-server.exe is running on port 8080.")

if __name__ == "__main__":
    stream_chat()