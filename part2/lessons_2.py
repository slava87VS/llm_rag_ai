from langchain_core.prompts import PromptTemplate

template_str = "Привет, {% if formal %}уважаемый{% else %}дорогой{% endif %} {{ name }}!"
prompt = PromptTemplate(
    template=template_str,
    input_variables=["name", "formal"],
    template_format="jinja2"
)

print(prompt.format_prompt(name="Иван", formal=True).to_string())
# Вывод: "Привет, уважаемый Иван!"
