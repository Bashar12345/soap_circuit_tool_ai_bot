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
    print("processing.........")
    
    # Get conversation context
    context = conversation_context(user_id)
    sys_img_prompt = (
        f"""You are a marine engineering assistant specializing in diesel and steam engine components for maritime vessel propulsion systems.
        - Analyze the image and identify **only** diesel or steam engine components specific to ships.
        - Output a single-line component description in markdown code blocks, including type and specifications (if identifiable), e.g., `BOLT, HEX, 2 IN DIA X 6 5/8 IN LG`, `MOTOR, 440V, 92A, 56.5KW, 60HZ, IP 54, 3565 RPM`.
        - If the image is unrelated, respond with:
          ```
          This image is outside my expertise. Please upload an image of diesel or steam engine components.
          ```
        - **One-Shot Example**:
          **Image Input**: 
          The image shows a close-up of a person's hand holding a circular rubber or elastomeric seal or gasket. This component appears to be an oil seal or shaft seal, typically used to prevent the leakage of fluids along a rotating shaft. The numbers and letters embossed on the seal might be part numbers, manufacturer codes, or size specifications.
          **Output**:
          ```
          SEAL, RUBBER, OIL SEAL
          ```
        ### Conversation Context
        {context}
        """
    )

    sys_text_prompt = (
        f"""You are a marine engineering assistant specializing in diesel and steam engines for ship propulsion systems. All responses must be in **markdown format**, professional, and concise, avoiding unnecessary jargon. Use the conversation context to provide relevant, context-aware answers.

        - Engage in friendly, professional conversations.
        - Reference specific engine components (e.g., motors, bolts, bearings, O-rings) and explain their roles in propulsion systems.
        - Use standard description formats (e.g., `MOTOR, 440V, 92A, 56.5KW, 60HZ, 3 PHASE` or `BOLT, HEX, 2 IN DIA X 6 5/8 IN LG`).
        - If the query is outside your expertise, respond with:
          ```markdown
          This topic is outside my expertise. Please ask about diesel or steam engine propulsion systems.
          ```
        ### Conversation Context
        {context}
        """
    )

    # Case 1: No image_path provided, process only the question
    if not image_path or not os.path.exists(image_path):
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",  # Use a valid model
                messages=[
                    {"role": "system", "content": sys_text_prompt},
                    {"role": "user", "content": [{"type": "text", "text": question}]}
                ],
                max_tokens=100
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
                {"role": "system", "content": sys_img_prompt},
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
            max_tokens=30
        )
        # Save to conversation history
        message_saved = Conversation.objects.create(
            user_id=user_id,
            question=question,
            response=response.choices[0].message.content
        )
        if message_saved:
            print("ended the process")
        return response.choices[0].message.content
    except Exception as e:
        return f"Error processing image: {str(e)}"







    
def conversation_context(user_id=None, max_history=5):
    
    query = Conversation.objects.all()
    if user_id:
        query = query.filter(user_id=user_id)
    history = query.order_by('-timestamp')[:max_history][::-1] 
    # print(history)
    
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

