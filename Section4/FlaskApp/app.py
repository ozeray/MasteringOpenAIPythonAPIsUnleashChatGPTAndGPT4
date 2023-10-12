import openai
from flask import Flask, render_template, request
from dotenv import dotenv_values
import json

config = dotenv_values(".env")
openai.api_key = config["OPEN_API_KEY"]


app = Flask(__name__,
            template_folder='templates',
            static_url_path='/',
            static_folder='static'
            )


def get_colors(text):
    prompt = f"""
    You are a color palette generating assistant that responds to text prompts for color palettes. You should generate color palettes that fit the theme, mood, or instructions in the prompt. The palettes should be between 2 and 8 colors.

    Q: Convert the following description of a color palette into a list of colors: The Mediterranean Sea
    A: ["#006699", "#66CCCC", "#F0E68C", "#008000", "#F08080"]

    Q: Convert the following description of a color palette into a list of colors: sage, nature, earth
    A: ["#EDF1D6", "#9DC08B", "#609966", "#40513B"]

    Desired Format: a JSON array of hexadecimal color codes
    Q: Convert the following description of a color palette into a list of colors: {text}
    A:
    """

    response = openai.Completion.create(
        prompt=prompt,
        model="text-davinci-003",
        max_tokens=200,
    )

    return json.loads(response["choices"][0]["text"])


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/palette", methods=['POST'])
def prompt_to_palette():
    query = request.form.get('query')
    app.logger.info(f'Request received: {query}')
    colors = get_colors(query)
    return {'colors': colors}


if __name__ == "__main__":
    app.run(debug=True)
