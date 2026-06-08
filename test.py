from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
pdfmetrics.registerFont(TTFont("DejaVu", font_path))

c = canvas.Canvas("pdfs/mathimatika.pdf")
c.setFont("DejaVu", 12)

lines = [
    "Μαθηματικη Αναλυση - Σημειωσεις",
    "",
    "Παραγωγος",
    "Η παραγωγος μιας συναρτησης f(x) οριζεται ως ο ρυθμος μεταβολης της.",
    "Συμβολιζεται ως f'(x) η df/dx.",
    "Παραδειγμα: αν f(x) = x^2 τοτε f'(x) = 2x.",
    "",
    "Κανονες Παραγωγισμου",
    "1. Παραγωγος σταθερας: αν f(x) = c τοτε f'(x) = 0",
    "2. Κανονας δυναμης: αν f(x) = x^n τοτε f'(x) = n * x^(n-1)",
    "3. Κανονας αθροισματος: (f+g)' = f' + g'",
    "4. Κανονας γινομενου: (f*g)' = f'*g + f*g'",
    "",
    "Ολοκληρωμα",
    "Το ολοκληρωμα ειναι η αντιστροφη πραξη του παραγωγισμου.",
    "Συμβολιζεται ως f(x)dx.",
    "Παραδειγμα: x^2 dx = x^3/3 + C",
    "",
    "Οριο Συναρτησης",
    "Το οριο της f(x) καθως το x τεινει στο a συμβολιζεται lim f(x) x->a.",
    "Παραδειγμα: lim (x^2) x->3 = 9",
]

y = 800
for line in lines:
    c.drawString(50, y, line)
    y -= 20

c.save()
print("✅ PDF δημιουργήθηκε: pdfs/mathimatika.pdf")
