import os
import sys
import base64
import requests

# Add the current directory to sys.path so we can import 'app'
sys.path.append(os.getcwd())

from app.agents.graph import conversation_graph

def generate_visuals():
    try:
        # 1. Get the mermaid string from the compiled graph
        mermaid_text = conversation_graph.get_graph().draw_mermaid()
        
        # 2. Save the .mmd file
        with open("graph_diagram.mmd", "w") as f:
            f.write(mermaid_text)
        print("Successfully saved Mermaid code to 'graph_diagram.mmd'")

        # 3. Generate PNG using mermaid.ink
        print("Generating PNG image via mermaid.ink...")
        
        # Base64 encode the mermaid string
        base64_string = base64.b64encode(mermaid_text.encode('ascii')).decode('ascii')
        url = f"https://mermaid.ink/img/{base64_string}"
        
        response = requests.get(url)
        if response.status_code == 200:
            with open("graph_diagram.png", "wb") as f:
                f.write(response.content)
            print("Successfully saved graph image to 'graph_diagram.png'")
        else:
            print(f"Failed to generate PNG. HTTP Status: {response.status_code}")
            
        print("\nYou can now open 'graph_diagram.png' to see the full visualization!")
        
    except Exception as e:
        print(f"Error generating visuals: {e}")

if __name__ == "__main__":
    generate_visuals()
