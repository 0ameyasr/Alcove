""" 
test.py

This is a dummy file that serves its purpose in action testing & implementation
of new features in the project.

"""
import markdown2
import re

def clean_message(message):
  message = re.sub(r'\\(.)', r'\1', message)
  message = message.replace('\\"', '"')
  message = message.replace('\\n', '\n')
  message = re.sub(r'\s+', ' ', message).strip()
  return message


msg = """

parts {
  text: "For a 3D Snake game in Python, you\'ll likely need:\n\n*   **Pygame:** While primarily 2D, it can be used with some 3D techniques, though less ideal.\n*   **PyOpenGL:** A robust option for direct OpenGL interaction in Python.\n*   **Panda3D:** A more full-featured 3D game engine that simplifies development.\n*   **Ursina Engine:** A relatively beginner-friendly 3D game engine.\n\n\nConsider your experience level when choosing. Pygame might be sufficient for a simple 3D effect, but Panda3D or Ursina will provide a better 3D experience with less manual coding.  PyOpenGL gives you the most control but requires a deeper understanding of OpenGL.\n"
}
role: "model"

"""
latest_message = f"**Ace**: "+msg.replace("text: ","").replace("parts {","").replace("}","").replace("role: \"model\"","").strip() + "~"
print(latest_message)

print(markdown2.markdown(latest_message))
