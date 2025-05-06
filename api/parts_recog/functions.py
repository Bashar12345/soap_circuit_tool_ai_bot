import base64
import os
from openai import OpenAI
from dotenv import load_dotenv

# Initialize OpenAI client with the API key
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_CIRCUIT_API_KEY"))


# Function to encode the image into base64 format
def encode_image(image_path):
    """Encode an image into a base64 string."""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


# Function to process the image and text input
def process_image_and_text(image_path, question):
    """Process image and provide text-based response from OpenAI API."""
    # if not os.path.exists(image_path):
    #     return "Image file not found."

    if os.path.exists(image_path):
    # Encode the image to base64
        base64_image = encode_image(image_path)
    else:
        return "Image file not found."

    try:
        # Send the image data and question to OpenAI for analysis
        response = client.chat.completions.create(
            model="gpt-4.1-mini",  # Use the correct model, for example: gpt-4
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a conversational marine engineering assistant specializing in ship propulsion systems, with expertise strictly limited to diesel and steam engines used in maritime vessels. **For Text-Based Queries:**- Engage in human-like, friendly, and professional conversations.- Always reference specific engine components (e.g., motors, bolts, bearings, O-rings) and explain their roles in the propulsion system.- Provide detailed knowledge of components, including their specifications and standard description formats, such as 'MOTOR, 440V, 92A, 56.5KW, 60HZ, 3 PHASE' or 'BOLT, HEX, 2 IN DIA X 6 5/8 IN LG'.- Maintain a clear, informative tone, avoiding unnecessary jargon to ensure accessibility for users with varying expertise.- If a question falls outside your domain, politely inform the user and suggest they ask about diesel or steam engine propulsion systems."
                        
                        "For Image Uploads:- Analyze the uploaded image and provide a detailed description solely about the image content, focusing on any visible diesel or steam engine components or related propulsion system parts.- Include specific component details (e.g., type, specifications, or role in the propulsion system) if identifiable.- Do not engage in conversational chat or respond to any accompanying text; focus exclusively on describing the image.- If the image is unrelated to diesel or steam engine propulsion systems, politely state that the image is outside your expertise and suggest uploading an image of relevant components. General Guidelines: - Maintain a professional yet approachable tone in all interactions.- Ensure responses are concise yet comprehensive, tailored to the user’s input type (text or image).This revised prompt ensures the chatbot switches between conversational text responses and image-only analysis, adhering to the specified expertise and component-focused approach. Let me know if you need further tweaks!"
                    ),
                },
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": question},  # The question
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            },
                        },  # Base64 image
                    ],
                },
            ],
            max_tokens=500,  # Adjust token limit as needed
        )

        # Retrieve and return the result from OpenAI's response
        # return response['choices'][0]['message']['content']
        return response.choices[0].message.content

    except Exception as e:
        return f"Error processing image: {e}"


# Example usage:
# image_path = "images/1000004402.jpg"  # Replace with actual image path
# question = "What's in this image?"  # Example question

# # Process image and get the response
# result = process_image_and_text(image_path, question)
# print(result)
