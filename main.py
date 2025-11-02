from agents.task_agent import process_message
from db.database import init_db
import sys

def main():
    """Run the task reminder agent in interactive mode."""
    # Get username from command line or use default
    user = sys.argv[1] if len(sys.argv) > 1 else "local-user"
    
    # Initialize database
    try:
        init_db()
    except Exception as e:
        print(f"❌ Failed to initialize database: {e}")
        return
    
    # Welcome message
    print(f"Task Reminder Agent — User: {user}")
    print("Type 'exit' to quit, 'help' for commands\n")

    while True:
        try:
            # Get user input
            msg = input("You: ").strip()
            
            # Handle empty input
            if not msg:
                continue
            
            # Handle exit command
            if msg.lower() in ["exit", "quit", "q"]:
                print("👋 Goodbye!")
                break
            
            # Handle help command
            if msg.lower() == "help":
                print("Commands:")
                print("  • Type a task with time: 'remind me at 5pm to study'")
                print("  • exit/quit/q - Exit the program")
                continue
            
            # Process message
            reply = process_message(user, msg)
            print("Agent:", reply)
            
        except KeyboardInterrupt:
            print("\n\n👋 Interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            print("Please try again or type 'exit' to quit.")

if __name__ == "__main__":
    main()
