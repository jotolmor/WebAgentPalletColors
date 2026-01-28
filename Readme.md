# Web Palette Colors LLM Agent

Este repositorio incluye una aplicación/agent que genera paletas de color para diseñadores web a partir de un sentimiento o una idea. La salida entrega los formatos más usados (RGB, RGBA, HEX, HSL, HSLA), métricas de contraste y sugerencias para mejorar la propuesta.

## ¿Qué hace el agente?

- Traduce un sentimiento (por ejemplo, `calma`, `energia`, `confianza`, `creatividad`, `naturaleza`, `lujo`) a una paleta cromática con soporte de sinónimos.
- Permite aplicar estilos (`minimalista`, `brutalista`, `retro`, `futurista`) para ajustar saturación y luminosidad.
- Genera 5 colores con variaciones sutiles basadas en rangos de saturación y luminosidad.
- Devuelve la paleta en formatos RGB, RGBA, HEX, HSL y HSLA.
- Calcula contraste mínimo y añade sugerencias de accesibilidad y consistencia visual.

## Uso rápido

```bash
python3 palette_agent.py "calma" "app de meditación minimalista" --count 5 --seed 42 --style minimalista --brand "Logo azul"
```

Comparador A/B rápido:

```bash
python3 palette_agent.py "calma" "landing de bienestar" --count 5 --seed 42 --ab minimalista futurista
```

## Ejecutar la app web (FastAPI)

```bash
pip install -r requirements.txt
uvicorn app:app --reload
```

Luego abre `http://localhost:8000` para generar paletas, guardar presets automáticamente y exportar tokens.

Los presets se guardan en `data/presets.json`.

## API rápida

Generar paleta:

```bash
curl -X POST http://localhost:8000/api/palette \\
  -H \"Content-Type: application/json\" \\
  -d '{\"sentiment\":\"calma\",\"idea\":\"landing de bienestar\",\"count\":5,\"style\":\"minimalista\"}'
```

Exportar tokens:

```bash
curl -X POST http://localhost:8000/api/export \\
  -H \"Content-Type: application/json\" \\
  -d '{\"sentiment\":\"calma\",\"idea\":\"landing de bienestar\",\"format\":\"css\"}'
```

Listar presets guardados:

```bash
curl http://localhost:8000/api/presets
```

## Salida esperada (extracto)

```json
{
  "sentiment": "calma",
  "idea": "app de meditación minimalista",
  "profile": "calma",
  "notes": "Paleta suave, ideal para interfaces relajantes.",
  "palette": [
    {
      "name": "Color 1",
      "hue": 194,
      "saturation": 29,
      "lightness": 78,
      "formats": {
        "rgb": "rgb(161, 196, 210)",
        "rgba": "rgba(161, 196, 210, 0.88)",
        "hex": "#A1C4D2",
        "hsl": "hsl(194, 29%, 73%)",
        "hsla": "hsla(194, 29%, 73%, 0.88)"
      }
    }
  ],
  "contrast": {
    "min_ratio": 4.72,
    "note": "Contraste general adecuado para texto estándar."
  },
  "brand_hint": "Logo azul",
  "style": "minimalista",
  "suggestions": [
    "Ajusta el contraste según WCAG para textos y fondos.",
    "Define un color dominante, dos secundarios y dos de acento.",
    "Verifica la paleta en modo oscuro si la interfaz lo requiere.",
    "Testea accesibilidad con simuladores de daltonismo."
  ]
}
```

## Ideas para mejorar el LLM

- Añadir un módulo de análisis semántico para detectar sinónimos del sentimiento.
- Permitir estilos adicionales (minimalista, brutalista, retro, futurista).
- Integrar evaluación automática de contraste y sugerencias de ajustes.
- Exportar directamente a tokens de diseño (JSON/Style Dictionary).
- Generar paletas adaptadas a dispositivos (mobile/desktop) con contraste dinámico.
- Incluir reglas de armonía cromática (análoga, complementaria, triádica).
- Soportar identificación de marca (logo) para derivar paletas coherentes.
- Sugerir tipografías complementarias basadas en la emoción.

## Extensiones sugeridas

Si integras este script en la app, puedes:

1. Usar el sentimiento como `system prompt` o `tool call`.
2. Guardar las paletas más usadas como presets.
3. Añadir una capa de feedback del usuario para refinar futuras paletas.
4. Permitir guardar y versionar paletas para futuras campañas.
5. Ofrecer variaciones de accesibilidad (alto contraste, baja saturación).
6. Exportar tokens a CSS variables o configuraciones de Tailwind/Figma para acelerar implementación.
7. Mostrar métricas de accesibilidad en la interfaz (AA/AAA) junto con sugerencias accionables.
8. Insertar bibliotecas de marca con presets reutilizables por proyecto.

## Recomendaciones adicionales para la aplicación

- Incluir un comparador A/B de paletas para evaluar estilos y variantes rápidamente.
- Mostrar métricas de accesibilidad en la interfaz (AA/AAA) junto con sugerencias accionables.
- Guardar las paletas más usadas como presets para reutilizarlas rápidamente.
- Permitir guardar paletas creadas para reutilizarlas en proyectos futuros.
- Incorporar bibliotecas de marca con presets reutilizables por proyecto.
