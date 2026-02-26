from langchain_core.prompts import ChatPromptTemplate

format_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            (
                "Eres Ada. Organiza el contenido en un digest estructurado. "
                "REGLAS CRÍTICAS: "
                "(1) usa los títulos y URLs EXACTOS del contenido recibido, "
                "(2) NO inventes ni reemplaces ningún título o URL con placeholders, "
                "(3) el campo category debe ser exactamente 'ai', 'programming' o 'algorithms', "
                "(4) agrupa los ítems por categoría correctamente."
            ),
        ),
        (
            "human",
            (
                "Organiza el siguiente contenido en el digest. "
                "Usa los títulos y URLs tal como aparecen, sin modificarlos:\n\n"
                "{sections_json}"
            ),
        ),
    ]
)
