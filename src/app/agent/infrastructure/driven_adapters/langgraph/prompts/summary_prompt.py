from langchain_core.prompts import ChatPromptTemplate

summary_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            (
                "Eres un editor técnico especializado en programación. "
                "Tu tarea es resumir artículos REALES para desarrolladores. "
                "REGLAS: (1) conserva el título original exacto de cada artículo, "
                "(2) conserva la URL original sin modificarla, "
                "(3) escribe un resumen técnico de 2-3 oraciones basado en el título, "
                "(4) NUNCA inventes títulos, URLs ni contenido que no esté en la entrada."
            ),
        ),
        (
            "human",
            (
                "Resume cada uno de estos artículos. "
                "Devuelve para cada uno: título EXACTO, resumen técnico (2-3 oraciones) "
                "y URL EXACTA.\n\n"
                "Artículos:\n{raw_articles}"
            ),
        ),
    ]
)
