from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import os

def generate_pdf(story_title, story_content, illustrations, output_dir="./backend/static/pdfs"):
    """
    Generates a PDF containing the story text and illustrations.

    Args:
        story_title (str): The title of the story.
        story_content (str): The content of the story.
        illustrations (list): A list of file paths to illustration images.
        output_dir (str): Directory to save the generated PDF.

    Returns:
        str: File path of the generated PDF.
    """
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Clean title for filename
    pdf_filename = f"{story_title.replace(' ', '_').lower()}.pdf"
    pdf_filepath = os.path.join(output_dir, pdf_filename)

    # Create a new PDF canvas
    pdf = canvas.Canvas(pdf_filepath, pagesize=letter)
    width, height = letter

    # Add title to the first page
    pdf.setFont("Helvetica-Bold", 20)
    pdf.drawCentredString(width / 2.0, height - 50, story_title)

    # Add illustrations and text
    y_position = height - 100  # Start below the title
    pdf.setFont("Helvetica", 12)

    # Add illustrations
    for illustration in illustrations:
        if y_position < 200:  # Check if there's enough space on the page
            pdf.showPage()  # Create a new page if needed
            y_position = height - 50

        try:
            img = ImageReader(illustration)
            img_width, img_height = img.getSize()
            aspect_ratio = img_width / img_height

            # Resize image to fit within a fixed width (400px)
            img_display_width = 400
            img_display_height = img_display_width / aspect_ratio

            pdf.drawImage(
                img,
                x=(width - img_display_width) / 2.0,
                y=y_position - img_display_height,
                width=img_display_width,
                height=img_display_height,
            )
            y_position -= img_display_height + 20  # Move cursor down after image
        except Exception as e:
            print(f"Error adding illustration {illustration}: {e}")

    # Add story content
    lines = story_content.split("\n")
    for line in lines:
        if y_position < 50:  # Check if there's enough space on the page
            pdf.showPage()  # Create a new page if needed
            y_position = height - 50

        pdf.drawString(50, y_position, line.strip())
        y_position -= 15  # Move cursor down after each line

    # Save the PDF file
    pdf.save()
    return pdf_filepath

# Example usage
if __name__ == "__main__":
    title = "Harry Potter and the Monster"
    content = "Once upon a time...\nHarry met a monster in the forest.\nThey became friends and lived happily ever after."
    images = ["./backend/static/images/generated_image_1.png", "./backend/static/images/generated_image_2.png"]
    
    pdf_path = generate_pdf(title, content, images)
    print(f"PDF generated at: {pdf_path}")
