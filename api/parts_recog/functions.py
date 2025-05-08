import base64
import os
from openai import OpenAI
from dotenv import load_dotenv
from api.models import Conversation

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_CIRCUIT_API_KEY"))

def encode_image(image_path):
    """Encode an image into a base64 string."""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

def process_image_and_text(image_path, question, user_id=None):
    """Process image (if provided) and provide text-based response from OpenAI API."""
    
    # Get conversation context
    context = conversation_context(user_id)
    system_prompt = (
"""You are a conversational marine engineering assistant specializing in ship propulsion systems, with expertise strictly limited to diesel and steam engines used in maritime vessels. For Text-Based Queries: Engage in human-like, friendly, and professional conversations. Reference specific engine components (e.g., motors, bolts, bearings, O-rings) and explain their roles in the propulsion system. Maintain a clear, informative tone, avoiding unnecessary jargon. If a question falls outside your domain, politely inform the user and suggest they ask about diesel or steam engine propulsion systems. Conversation Context: {context}  
For Image Uploads: Analyze the uploaded image and provide a detailed description solely about the image content, focusing on any visible diesel or steam engine components or related propulsion system parts.
Include specific component details (e.g., type, specifications, or role in the propulsion system) if identifiable. Do not engage in conversational chat or respond to any accompanying text; focus exclusively on describing the image.  
If the image is unrelated, politely state that the image is outside your expertise and suggest uploading an image of relevant components.
Image Iutput:
 The image shows a close-up of a person's hand holding a circular rubber or elastomeric seal or gasket. This component appears to be an oil seal or shaft seal, typically used to prevent the leakage of fluids along a rotating shaft. The numbers and letters embossed on the seal might be part numbers, manufacturer codes, or size specifications. 
Output:
seal, rubber

EXAMPLES OF PART WRITE UPS IN UNIFORM FOR MEMORY
BOLT, HEX, 2 IN DIA X 6 5/8 IN LG
BOLT, TYPE OF BOLT, DIA OF BOLT X LENGH OF BOLT AND THREAD PER IN
ACTUATOR, ROTARY, WITH BUTTERFLY VALVE
MOTOR, 440V, 92A, 56.5KW, 60HZ, IP 54, 3565 RPM
""")

    # Case 1: No image_path provided, process only the question
    if not image_path or not os.path.exists(image_path):
        try:
            response = client.chat.completions.create(
                model="gpt-4o",  # Use a valid model
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": [{"type": "text", "text": question}]}
                ],
                max_tokens=500
            )
            
            # Save to conversation history
            Conversation.objects.create(
                user_id=user_id,
                question=question,
                response=response.choices[0].message.content
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error processing text query: {str(e)}"

    # Case 2: Image_path provided, process both image and question
    try:
        base64_image = encode_image(image_path)
        response = client.chat.completions.create(
            model="gpt-4o",  # Use a valid model
            messages=[
                {"role": "system", "content": system_prompt},
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": question},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=500
        )
        # Save to conversation history
        Conversation.objects.create(
            user_id=user_id,
            question=question,
            response=response.choices[0].message.content
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error processing image: {str(e)}"







    
def conversation_context(user_id=None, max_history=5):
    
    query = Conversation.objects.all()
    if user_id:
        query = query.filter(user_id=user_id)
    history = query.order_by('-timestamp')[:max_history][::-1] 
    
    if not history:
        return "No prior conversation history available."
    
    # Format history for summarization
    history_text = "\n".join(
        f"User: {entry.question}\nAssistant: {entry.response}" for entry in history
    )
    
    # Summarize the conversation using OpenAI
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a summarization assistant. Summarize the following conversation history concisely, "
                        "focusing on key topics and questions related to marine engineering and ship propulsion systems. "
                        "Keep the summary under 100 words and avoid including irrelevant details."
                    )
                },
                {
                    "role": "user",
                    "content": history_text
                }
            ],
            max_tokens=150
        )
        context = response.choices[0].message.content.strip()
        return context
    except Exception as e:
        return f"Error summarizing conversation: {str(e)}"














# Example usage:
# image_path = "images/1000004402.jpg"  # Replace with actual image path
# question = "What's in this image?"  # Example question

# # Process image and get the response
# result = process_image_and_text(image_path, question)
# print(result)

