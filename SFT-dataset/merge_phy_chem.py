import re
import json
import html

# Input files (replace with your own paths)
physics_path = "sft_formatted_maharashtra_physics.json"
chemistry_path = "sft_formatted_maharashtra_chemistry.json"
merged_output = "sft_formatted_maharashtra_phy_chem_final.json"


def normalize_equations(text: str) -> str:
    """Advanced normalization for readable math and symbols."""
    if not text:
        return ""

    text = html.unescape(text)

    replacements = {
        r"\\frac\{([^}]+)\}\{([^}]+)\}": r"(\1/\2)",
        r"rightArrow": "→",
        r"rightarrow": "→",
        r"Rightarrow": "⇒",
        r"leftArrow": "←",
        r"Leftarrow": "⇐",
        r"leftrightarrow": "↔",
        r"degreeC": "°C",
        r"degC": "°C",
        r"degree": "°",
        r"Delta": "Δ",
        r"Sigma": "Σ",
        r"sqrt": "√",
        r"times": "×",
        r"pi": "π",
        r"pm": "±",
        r"omega": "ω",
        r"theta": "θ",
        r"alpha": "α",
        r"beta": "β",
        r"gamma": "γ",
        r"tau": "τ",
        r"infty": "∞",
    }

    for pattern, repl in replacements.items():
        text = re.sub(pattern, repl, text)

    subscript_map = str.maketrans("0123456789+-=()", "₀₁₂₃₄₅₆₇₈₉₊₋₌₍₎")
    superscript_map = str.maketrans("0123456789+-=()", "⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁼⁽⁾")

    text = re.sub(r"_\{([0-9+\-=()]+)\}", lambda m: m.group(1).translate(subscript_map), text)
    text = re.sub(r"\^\{([0-9+\-=()]+)\}", lambda m: m.group(1).translate(superscript_map), text)

    text = re.sub(r"[{}]", "", text)
    text = text.replace("\\", "")
    text = re.sub(r"\s+", " ", text).strip()

    return text


def clean_and_merge(physics_path, chemistry_path, output_path):
    with open(physics_path, "r", encoding="utf-8") as f:
        physics_data = json.load(f)
    with open(chemistry_path, "r", encoding="utf-8") as f:
        chemistry_data = json.load(f)

    merged = []
    for dataset in [physics_data, chemistry_data]:
        for item in dataset:
            merged.append({
                "instruction": item["instruction"],
                "input": normalize_equations(item["input"]),
                "output": normalize_equations(item["output"])
            })

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(merged, f, indent=2, ensure_ascii=False)

    print(f"✅ Merged and cleaned file saved as {output_path}")


if __name__ == "__main__":
    clean_and_merge(physics_path, chemistry_path, merged_output)
