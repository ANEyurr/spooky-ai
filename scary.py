
import tkinter as tk
from tkinter import filedialog, ttk
from gtts import gTTS
import openai


openai.api_key = "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"
# ... (rest of your code remains the same)



from pydub import AudioSegment
from pydub.playback import play

def play_audio(file_path):
    song = AudioSegment.from_mp3(file_path)
    play(song)

def speak_story():
    story = output_text.get("1.0", tk.END).strip()
    if not story:
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, "No story to speak!")
        return play_audio()

    selected_voice = voice_var.get()
    language_mapping = {
        "English (US)": "en",
        "English (UK)": "en-uk",
        "Spanish": "es",
        "French": "fr",
        "German": "de",
    }

    language = language_mapping.get(selected_voice, "en")

    tts = gTTS(text=story, lang=language)
    audio_file = "story.mp3"
    tts.save(audio_file)

    # Play the audio after saving
    play_audio(audio_file)

    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, f"Story has been spoken and saved as {audio_file}")

# Ensure play_audio is defined before you call speak_story or any other function that requires it.



def generate_story(name, age, fav_candy, traits, fun_fact, location, notes):
    prompt = (
        f"Create an extremely horrifying story about a character named {name}, who is {age} years old, "
        f"whose favorite Halloween candy is {fav_candy}. "
        f"{name} is known for being {traits}. "
        f"One fun fact about {name} is that {fun_fact}. "
        f"The story takes place in {location}. "
        f"{notes} "
    )

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message['content']
    except Exception as e:
        return f"Error: {str(e)}"

def on_button_click():
    name = name_entry.get()
    age = age_entry.get()
    fav_candy = candy_entry.get()
    traits = traits_entry.get()
    fun_fact = fact_entry.get()
    location = location_entry.get()
    notes = notes_text.get("1.0", tk.END).strip()  # Get multi-line notes

    if not all([name, age, fav_candy, traits, fun_fact, location]):
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, "Please fill in all fields.")
        return

    # Generate the story using the OpenAI API
    story = generate_story(name, age, fav_candy, traits, fun_fact, location, notes)
    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, story)

def download_story():
    story = output_text.get("1.0", tk.END).strip()  # Get the story text
    if not story:
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, "No story to download!")
        return
    
    # Ask for a file location to save the story
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", 
                                               filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if file_path:
        with open(file_path, 'w') as file:
            file.write(story)



root = tk.Tk()
root.title("Horror Story Creator")
root.geometry("600x800")
root.configure(bg="#2E2E2E")

# Create a canvas and a scrollbar
canvas = tk.Canvas(root, bg="#2E2E2E", width=600, height=800)
scrollbar = ttk.Scrollbar(root, orient="vertical", command=canvas.yview)
scrollbar.pack(side="right", fill="y")
canvas.pack(side="left", fill="both", expand=True)
canvas.configure(yscrollcommand=scrollbar.set)

# Create a frame inside the canvas
frame = tk.Frame(canvas, bg="#2E2E2E")
canvas.create_window((0, 0), window=frame, anchor="nw")

# Configure scrolling region
def configure_scroll(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

frame.bind("<Configure>", configure_scroll)

# Add widgets to the frame instead of root
tk.Label(frame, text="Character Name:", bg="#2E2E2E", fg="white", font=("Times New Roman", 12)).pack(pady=5)
name_entry = tk.Entry(frame, width=30, font=("Times New Roman", 12))
name_entry.pack(pady=5)

tk.Label(frame, text="Age:", bg="#2E2E2E", fg="white", font=("Times New Roman", 12)).pack(pady=5)
age_entry = tk.Entry(frame, width=30, font=("Times New Roman", 12))
age_entry.pack(pady=5)

tk.Label(frame, text="Favorite Halloween Candy:", bg="#2E2E2E", fg="white", font=("Times New Roman", 12)).pack(pady=5)
candy_entry = tk.Entry(frame, width=30, font=("Times New Roman", 12))
candy_entry.pack(pady=5)

tk.Label(frame, text="Traits (e.g., Brave, Mischievous):", bg="#2E2E2E", fg="white", font=("Times New Roman", 12)).pack(pady=5)
traits_entry = tk.Entry(frame, width=30, font=("Times New Roman", 12))
traits_entry.pack(pady=5)

tk.Label(frame, text="Fun Fact:", bg="#2E2E2E", fg="white", font=("Times New Roman", 12)).pack(pady=5)
fact_entry = tk.Entry(frame, width=30, font=("Times New Roman", 12))
fact_entry.pack(pady=5)

tk.Label(frame, text="Story Location:", bg="#2E2E2E", fg="white", font=("Times New Roman", 12)).pack(pady=5)
location_entry = tk.Entry(frame, width=30, font=("Times New Roman", 12))
location_entry.pack(pady=5)

tk.Label(frame, text="Additional Notes (optional):", bg="#2E2E2E", fg="white", font=("Times New Roman", 12)).pack(pady=5)
notes_text = tk.Text(frame, height=5, width=50, bg="#FFFFFF", fg="#000000", font=("Times New Roman", 10))
notes_text.pack(pady=5)

button = tk.Button(frame, text="Generate Spooky Story", command=on_button_click, bg="#FF5733", fg="white", font=("Times New Roman", 12))
button.pack(pady=10)

output_text = tk.Text(frame, wrap="word", width=70, height=15, bg="#FFFFFF", fg="#000000", font=("Times New Roman", 10))
output_text.pack(pady=20)

voice_var = tk.StringVar(frame)
voice_var.set("English (US)")
voice_options = ["English (US)", "English (UK)", "Spanish", "French", "German"]
voice_menu = tk.OptionMenu(frame, voice_var, *voice_options)
voice_menu.config(bg="#FFFFFF", fg="#000000", font=("Times New Roman", 12))
tk.Label(frame, text="Select Voice:", bg="#2E2E2E", fg="white", font=("Times New Roman", 12)).pack(pady=5)
voice_menu.pack(pady=5)

speak_button = tk.Button(frame, text="Speak Story", command=speak_story, bg="#FF5733", fg="white", font=("Times New Roman", 12))
speak_button.pack(pady=10)

download_button = tk.Button(frame, text="Download Story.txt", command=download_story, bg="#FF5733", fg="white", font=("Times New Roman", 12))
download_button.pack(pady=10)

root.mainloop()
