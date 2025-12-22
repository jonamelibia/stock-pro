import os
import re

def patch_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()
    
    original_content = content
    
    # 1. Add correct imports if missing
    if "from typing import" in content:
        if "Union" not in content:
            content = content.replace("from typing import", "from typing import Union, Optional, ")
        else:
             content = content.replace("from typing import", "from typing import Optional, ")
    else:
        content = "from typing import Union, Optional\n" + content

    # 2. Replace "Type | None" -> "Optional[Type]"
    # Regex: ([\w\[\].]+)\s*\|\s*None
    # This captures word characters, brackets, dots (for qualified names)
    content = re.sub(r'([\w\[\].]+)\s*\|\s*None', r'Optional[\1]', content)
    content = re.sub(r'None\s*\|\s*([\w\[\].]+)', r'Optional[\1]', content)

    # 3. Replace "TypeA | TypeB" -> "Union[TypeA, TypeB]"
    # This is harder to do perfectly with regex for nested stuff, but let's try a simple version
    # matching fairly simple types.
    # We define a "Type" as alphanumeric + . + [ + ]
    type_pattern = r'([\w\[\].]+)'
    # We iterate multiple times to handle chains like A | B | C -> Union[A, B, C] would require recursion or iterative parsing.
    # For now, let's just handle simple binary unions not involving None (already handled).
    
    # A | B -> Union[A, B]
    # We loop until no changes
    for _ in range(5):
        new_content = re.sub(r'([\w\[\].]+)\s*\|\s*([\w\[\].]+)', r'Union[\1, \2]', content)
        if new_content == content:
            break
        content = new_content

    if content != original_content:
        print(f"Patching {filepath}")
        with open(filepath, 'w') as f:
            f.write(content)

def walk_and_patch(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                patch_file(os.path.join(root, file))

if __name__ == "__main__":
    walk_and_patch("chronos-forecasting/src/chronos")
