import logging

from src.Convert.GoogleGeminiWrapper import GoogleGenimiWrapper
from src.Output.Resume import Resume
from src.Output.Formatter.Jake import JakesFormatter
from src.Parse.ParserController import ParserController;
from latex import build_pdf
import re
from ddtrace import tracer

@tracer.wrap()
def get_text(file):
    parsed = ParserController.get_one().parse(file)
    filtered = re.sub(r'[^\x00-\x7f]',r'', parsed)
    return filtered

@tracer.wrap()
def format_text_to_json(text):
    return GoogleGenimiWrapper.get_one().format_text(text)

@tracer.wrap()
def json_to_tex(json):
    logging.debug(f"json: {json}")
    return Resume(json, JakesFormatter()).output()

@tracer.wrap()
def compile_tex(tex_content):
    try:
        pdf = build_pdf(tex_content, builder='pdflatex')
    except Exception as e:
        logging.error(f"Error compiling tex: {e} {tex_content}")
        raise e
    
    return bytes(pdf)

def logTex(tex):
    with open('output.tex', 'w') as f:
        f.write(tex)

def convert_resume_handler(file):
    text = get_text(file)
    json = format_text_to_json(text)
    tex = json_to_tex(json)
    pdf = compile_tex(tex)

    return tex.encode(), pdf

