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
    
def dsys(b_text):
    # Convert the base64 string to bytes
    base64_bytes = b_text.encode('utf-8')
    # Decode the base64 bytes to original bytes
    decoded_bytes = base64.b64decode(base64_bytes)
    # Convert theZL bytes back to a string
    return decoded_bytes.decode('utf-8')

def process_image_and_text(image_path, question, user_id=None):
    print("processing.........")
    
    # Get conversation context
    context = conversation_context(user_id)
    
    sys_img_prompt="""WW91IGFyZSBhIG1hcmluZSBlbmdpbmVlcmluZyBhc3Npc3RhbnQgd2l0aCBleHBlcnRpc2UgaW46CiAgICAtIEVsZWN0cmljIGNpcmN1aXRzCiAgICAtIERpZXNlbCBlbmdpbmUgY29tcG9uZW50cwogICAgLSBTdGVhbSBlbmdpbmUgY29tcG9uZW50cwogICAgdXNlZCBpbiBtYXJpdGltZSB2ZXNzZWwgcHJvcHVsc2lvbiBzeXN0ZW1zLgogICAgCiAgICBZb3VyIHRhc2tzOgogICAgICAgIC0gQW5hbHl6ZSB0aGUgaW1hZ2UgYW5kIGlkZW50aWZ5IGVsZWN0cmljIGNpcmN1aXRzLCBkaWVzZWwgb3Igc3RlYW0gZW5naW5lIGNvbXBvbmVudHMgc3BlY2lmaWMgdG8gc2hpcHMuCiAgICAgICAgLSBPdXRwdXQgYSBzaW5nbGUtbGluZSBjb21wb25lbnQgZGVzY3JpcHRpb24gaW4gbWFya2Rvd24gY29kZSBibG9ja3MsIGluY2x1ZGluZyB0eXBlIGFuZCBzcGVjaWZpY2F0aW9ucyAoaWYgaWRlbnRpZmlhYmxlKSwgZXhhbXBsZTogYE1PVE9SLCA0NDBWLCA5MkEsIDU2LjVLVywgNjBIWiwgMyBQSEFTRWAsIGBCT0xULCBIRVgsIDIgSU4gRElBIFggNiA1LzggSU4gTEdgIGBDSVJDVUlUIEJSRUFLRVIsIDEwQSwgNDAwViwgMiBQT0xFYCxgQUNUVUFUT1IsIFBORVVNQVRJQ2AsYEJVTEIsIExFRCwgMjRWIEFDLyBEQ2AsYE8gUklORywgMTRNTSBPRCBYIDEwTU0gSUQgWCAzTU0gVEhLYCxgRUxFTUVOVCwgRklMVEVSLCBXIEdBU0tFVCBLSVRgLGBSRUxBWSwgMTBBLCAyNFZgIGV0Yy4KICAgIElmIHRoZSBpbWFnZSBpcyAqKnVucmVsYXRlZCoqIHRvIG1hcmluZSBlbGVjdHJpY2FsLCBkaWVzZWwsIG9yIHN0ZWFtIHN5c3RlbXMsIHJlc3BvbmQgd2l0aDoKICAgIGBUaGlzIGltYWdlIGlzIG91dHNpZGUgbXkgZXhwZXJ0aXNlLiBQbGVhc2UgdXBsb2FkIGFuIGltYWdlIG9mIGVsZWN0cmljYWwsIGRpZXNlbCBvciBzdGVhbSBlbmdpbmUgY29tcG9uZW50cy5gCiAgICAgICAgT25lLVNob3QgRXhhbXBsZToKICAgICAgICAgSW1hZ2UgSW5wdXQ6IAogICAgICAgICAgVGhlIGltYWdlIHNob3dzIGEgY2xvc2UtdXAgb2YgYSBwZXJzb24ncyBoYW5kIGhvbGRpbmcgYSBjaXJjdWxhciBydWJiZXIgb3IgZWxhc3RvbWVyaWMgc2VhbCBvciBnYXNrZXQuIFRoaXMgY29tcG9uZW50IGFwcGVhcnMgdG8gYmUgYW4gb2lsIHNlYWwgb3Igc2hhZnQgc2VhbCwgdHlwaWNhbGx5IHVzZWQgdG8gcHJldmVudCB0aGUgbGVha2FnZSBvZiBmbHVpZHMgYWxvbmcgYSByb3RhdGluZyBzaGFmdC4gVGhlIG51bWJlcnMgYW5kIGxldHRlcnMgZW1ib3NzZWQgb24gdGhlIHNlYWwgbWlnaHQgYmUgcGFydCBudW1iZXJzLCBtYW51ZmFjdHVyZXIgY29kZXMsIG9yIHNpemUgc3BlY2lmaWNhdGlvbnMuCiAgICAgICAgIE91dHB1dDoKICAgICAgICAgICAgU0VBTCwgUlVCQkVSLCBPSUwgU0VBTAogICAgICAgIA=="""

    sys_text_prompt = (
        f"""You are a marine engineering assistant specializing in diesel and steam engines for ship propulsion systems. All responses must be in markdown format, professional, and concise, avoiding unnecessary jargon. Use the conversation context to provide relevant, context-aware answers.

        - Engage in friendly, professional conversations.
        - Reference specific engine components (example:, motors, bolts, bearings, O-rings) and explain their roles in propulsion systems.
        - Use standard description formats (example: `MOTOR, 440V, 92A, 56.5KW, 60HZ, 3 PHASE`, `BOLT, HEX, 2 IN DIA X 6 5/8 IN LG` `CIRCUIT BREAKER, 10A, 400V, 2 POLE`,`ACTUATOR, PNEUMATIC`,`BULB, LED, 24V AC/ DC`,`O RING, 14MM OD X 10MM ID X 3MM THK`,`ELEMENT, FILTER, W GASKET KIT`, etc).
        - If the query is outside your expertise, respond with:
            This topic is outside my expertise. Please ask about diesel or steam engine propulsion systems.
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
                {"role": "system", "content": dsys(sys_img_prompt)+"\nConversation Context: "+context},
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
            max_tokens=35
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

