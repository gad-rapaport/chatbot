from api_client import get_bot_response

def start_chat():
    print("\n--- My Chatbot is Ready! (type 'exit' to quit) ---")
    
    while True:
        try:
            user_input = input("You: ")
            
            if user_input.lower() in ['exit', 'quit', 'bye']:
                print("Bot: Goodbye!")
                break
            
            # Get response from API
            response = get_bot_response(user_input)
            
            print(f"Bot: {response}\n")
            
        except KeyboardInterrupt:
            print("\nBot: Goodbye!")
            break

if __name__ == "__main__":
    start_chat()
