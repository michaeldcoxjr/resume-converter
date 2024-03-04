from src.Convert.GoogleGeminiWrapper import GoogleGenimiWrapper
from src.Output.Resume import Resume
from src.Output.Formatter.Jake import JakesFormatter
from src.Parse.ParserController import ParserController;
from latex import build_pdf

def get_text(file):
    parsed = ParserController.get_one().parse(file)
    return parsed

def format_text_to_json(text, app):
    return GoogleGenimiWrapper.get_one().format_text(text, app)

def json_to_tex(json):
    return Resume(json, JakesFormatter()).output()

def compile_tex(tex_content):
    pdf = build_pdf(tex_content, builder='pdflatex')
    return bytes(pdf)

def log_tex(tex):
    with open('output.tex', 'w') as f:
        f.write(tex)

def convert_resume_handler(file, app):
    text = get_text(file)
    json = format_text_to_json(text, app)
    tex = json_to_tex(json)
    log_tex(tex) 

    pdf = compile_tex(tex)

    return tex.encode(), pdf

