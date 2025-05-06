from openai import OpenAI
import os,re , requests
from dotenv import load_dotenv
from django.conf import settings

# import openai
from PIL import Image, ImageOps, ImageDraw, ImageFont
from io import BytesIO
#openai==0.28.0

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_TEMPLATE_GENERATOR_API_KEY"))  # Load your OpenAI API key from environment variables


def generate_image(prompt):
    try:
        # Use the correct method for image generation
        response = client.images.generate(
            model="dall-e-3",  # Ensure this model is available in your OpenAI account
            prompt=prompt,
            n=1,
            size="1024x1024"
        )
        image_url = response.data[0].url
        image_data = requests.get(image_url).content
        

        local_image_path = f"gen_i_{prompt[:10].replace(' ', '_')}.png"
                # Save the image in the media directory
        os.makedirs(settings.MEDIA_ROOT, exist_ok=True)  # Ensure the media directory exists
        local_image_path = os.path.join(settings.MEDIA_ROOT, f"generated_image_{prompt[:10].replace(' ', '_')}.png")
        with open(local_image_path, "wb") as file:
            file.write(image_data)

        # Construct the publicly accessible URL
        public_image_url = f"{settings.MEDIA_URL}{os.path.basename(local_image_path)}"
        print(f"Image saved locally at: {local_image_path}")
        print(f"Publicly accessible URL: {public_image_url}")
        return public_image_url
   
        # with open(local_image_path, "wb") as file:
        #     file.write(image_data)
        # print(f"Image saved locally at: {local_image_path}")
        # return local_image_path

    
    except Exception as e:
        print(f"Error generating image: {e}")
        return None



def generate_template_content(user_input, template_structure=None):
    # Construct the prompt for OpenAI
    template_prompt = f"""
You are a content and design assistant. Based on the user input, generate content following the given structure and suggest design elements for a visually appealing landing poster (suitable for PowerPoint or HTML). Create the topic from the user input.
    
    Args:
        user_input (str): The prompt provided by the user, potentially containing a template topic.

**Template Structure:**
    Title: [topic]
    Description: A brief overview of [topic], including its population and key features.
    Key Points:
    - Point 1 about [topic].
    - Point 2 about [topic].
    - Point 3 about [topic].
    - Point 4 about [topic].
    - Point 5 about [topic].
    Image Descriptions:
    - Image 1: A detailed description of a notable landmark in [topic], including specific visual elements.
    - Image 2: A detailed description of another notable feature in [topic].
    - Image 3: A detailed description of a cultural or historical site in [topic].
    - Image 4: A detailed description of a natural or scenic attraction in [topic].
    - Image 5: A detailed description of a unique or iconic element in [topic].
    Design_Recommendations:
    - Background Color: Suggest a background color that reflects the theme of [topic] (provide hex code).
    - Title Font: Suggest a font family, size, and color for the title (e.g., font-family, font-size in pt or px, hex color).
    - Description Font: Suggest a font family, size, and color for the description.
    - Key Points Font: Suggest a font family, size, and color for the key points.
    - Image Placement: Suggest where to place the images on the poster (e.g., "Image 1 at top-left, Image 2 at bottom-right").
    - Additional Styling: Suggest any additional styling (e.g., borders, shadows, text alignment).
    
    **User Input:**
    {user_input}

    Generate the content and design recommendations according to the above structure. Ensure all sections, especially Image Descriptions and Design Recommendations, contain specific and vivid details relevant to [topic]. For design elements, choose colors and fonts that match the vibe of [topic].
    """

    # Call OpenAI ChatCompletion API to generate content
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful content generation assistant.",
            },
            {"role": "user", "content": template_prompt},
        ],
        temperature=0.7,
    )

    # Extract and return the generated content
    # Step 4: Extract the generated content
    generated_content = response.choices[0].message.content.strip()

    # Step 5: Extract Image Descriptions from the generated content
    image_descriptions = []
    # Use regex to find the Image Descriptions section
    image_section_match = re.search(r'\*\*Image Descriptions:\*\*\n(.*?)(?=\n\n|\Z)', generated_content, re.DOTALL)
    if image_section_match:
        image_section = image_section_match.group(1)
        # Extract each image description (lines starting with "- Image")
        descriptions = re.findall(r'- Image \d+: (.*?)(?=\n|$)', image_section)
        image_descriptions.extend(descriptions)


    image_results = []
    for description in image_descriptions:
        image_result = generate_image(description)
        image_results.append(image_result)
        
    design_recommendations = {}
    design_section_match = re.search(r'\*\*Design_Recommendations:\*\*\n(.*?)(?=\n\n|\Z)', generated_content, re.DOTALL)
    if design_section_match:
        design_section = design_section_match.group(1)
        # Extract each design recommendation
        background_color = re.search(r'- Background Color: (.*?)(?=\n|$)', design_section)
        title_font = re.search(r'- Title Font: (.*?)(?=\n|$)', design_section)
        description_font = re.search(r'- Description Font: (.*?)(?=\n|$)', design_section)
        key_points_font = re.search(r'- Key Points Font: (.*?)(?=\n|$)', design_section)
        image_placement = re.search(r'- Image Placement: (.*?)(?=\n|$)', design_section)
        additional_styling = re.search(r'- Additional Styling: (.*?)(?=\n|$)', design_section)

        design_recommendations = {
            "background_color": background_color.group(1) if background_color else "Not specified",
            "title_font": title_font.group(1) if title_font else "Not specified",
            "description_font": description_font.group(1) if description_font else "Not specified",
            "key_points_font": key_points_font.group(1) if key_points_font else "Not specified",
            "image_placement": image_placement.group(1) if image_placement else "Not specified",
            "additional_styling": additional_styling.group(1) if additional_styling else "Not specified"
        }

    # Step 7: Return the generated content and image generation results
    return {
        "content": generated_content,
        "image_results": image_results,
        "design_recommendations": design_recommendations
    }

# Example usage
# if __name__ == "__main__":
#     # Example user input
#     user_input = "Tell me about San Antonio"

#     # Generate content and images
#     result = generate_template_content(user_input)
    
#     # Print the generated content
#     print("Generated Content:")
#     print(result["content"])
#     print("\nImage Generation Results:")
#     for image_result in result["image_results"]:
#         print(image_result)