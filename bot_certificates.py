import csv 
import smtplib
from email.message import EmailMessage
from PIL import Image, ImageDraw, ImageFont
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import os

TEMPLATE = "/Users/surajjaiswal/again certificates/ecelltemp.png"
OUTPUT = "cerificate_folder"
FONT_PATH = "System/Library/Fonts/Supplemental/Arial.ttf"
MAIL_USER = "unknown193837@gmail.com"
MAIL_PASS = "ycmfkzqlyqpoexgn"
os.makedirs(OUTPUT, exist_ok=True)
def gen_certificate(name): 
    img = Image.open(TEMPLATE).convert("RGB")
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(FONT_PATH, 80)
    bbox = draw.textbbox((0, 0), name, font=font)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]
    text_x = (img.width - w) / 2
    text_y = (img.height - h) / 2 + 120
    draw.text ((text_x, text_y), name, fill="black", font=font)
    output_path = f"{OUTPUT}/{name}.pdf"
    img.save(output_path, "PDF")
    return output_path
def send_email(name, email, pdf_path):
    msg = EmailMessage()
    msg["Subject"] = f"Your participation certificate - {name}"
    msg["From"] = MAIL_USER
    msg["TO"] = email
    msg.set_content(
        f"""
 Dear {name},

We are happy to congratulate 🎉 you for your enthusiastic involvement in our event.  Your participation, zeal, and dedication were crucial to the success of this event.

 This certificate serves as a tiny expression of gratitude for your commitment, time, and hard work.  We sincerely appreciate your commitment and the upbeat attitude you brought to the occasion.

 Again, I want to thank you for participating in this project.  We look forward to having you attend a lot more events in the future.

 I hope you keep growing and succeeding.

 Warm Regards,
 Suraj Jaiswal
 """  )
    with open(pdf_path, "rb") as f:
        msg.add_attachment(f.read(),
                           maintype="application",
                           subtype="pdf",
                           filename=os.path.basename(pdf_path))
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(MAIL_USER, MAIL_PASS)
            smtp.send_message(msg)
        print(f" 📩 Email sent to {email}")
    except Exception as e:
        print(f" ❌ Failed to send {email}: {e}")
def process_csv(csv_file):
    with open(csv_file, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            name = row["Name"].strip()
            email = row["Email"].strip()

            pdf_path = gen_certificate(name)
            send_email(name, email, pdf_path)
process_csv("certificate.csv")