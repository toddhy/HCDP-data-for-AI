from google import genai

client = genai.Client()

user_prompt = input("Enter your prompt: ")

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=user_prompt
)
print(response.text)