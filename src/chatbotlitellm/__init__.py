import os
import sys

def main() -> None:
    """Run the chatbot application using Chainlit."""
    # Get the directory of the current package
    package_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Change directory to the package directory
    os.chdir(package_dir)
    
    # Run the Chainlit app with the chatbot.py file
    os.system(f"chainlit run chatbot.py")

if __name__ == "__main__":
    main()
