import pypdf
from constants import DUMMY_PASSWORD, PDF_PATH
from password_generator import PasswordsGenerator
from datetime import datetime

passwords_tried = 1
password_generator = PasswordsGenerator(dummy_password=DUMMY_PASSWORD)
password = password_generator.setup_format_of_password()
def reading_pdf(*, password:str) -> str:
    global passwords_tried
    print(f"Trying {password=}", "attempt =", passwords_tried)
    try:
        pdf_reader = pypdf.PdfReader(stream=PDF_PATH, password=password)

        pdf_reader.pages
        return f"{password=}, {passwords_tried=}"
    except: 
        return False

time_before_execution = datetime.now()
while not reading_pdf(password=password):
    password=password_generator.gemerate_next_password()
    passwords_tried+=1
time_after_execution = datetime.now()
with open("password.txt", "w") as password_file:
    password_file.writelines(f"{time_before_execution=}", f"{time_after_execution=}")
    password_file.writelines(f"Total time taken={time_after_execution-time_before_execution}")
    password_file.writelines(f"{PDF_PATH=}")
    password_file.writelines(f"{password=}")