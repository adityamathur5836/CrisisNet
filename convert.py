import re

def html_to_jsx(html):
    # Convert typical HTML to JSX
    jsx = html.replace('class="', 'className="')
    # Self-close img tags without closing slash
    jsx = re.sub(r'(<img[^>]+)(?<!/)>', r'\1 />', jsx)
    # Self-close input tags
    jsx = re.sub(r'(<input[^>]+)(?<!/)>', r'\1 />', jsx)
    # Self-close svg attributes if needed (not standard here but ok)
    # Convert HTML comments to JSX comments
    jsx = re.sub(r'<!--(.*?)-->', r'{/* \1 */}', jsx, flags=re.DOTALL)
    # Fix inline styles (very basic, specifically the ones we have)
    jsx = jsx.replace('style="font-variation-settings: \'FILL\' 1;"', "style={{ fontVariationSettings: \"'FILL' 1\" }}")
    # Fix data attributes if necessary, Data attributes are supported in React.
    return jsx

def extract_main_and_save(file_in, file_out, component_name):
    with open(file_in, 'r') as f:
        content = f.read()

    # match everything inside <main ...> ... </main>
    match = re.search(r'<main[^>]*>(.*?)</main>', content, re.DOTALL)
    if not match:
        print(f"Main tag not found in {file_in}")
        return

    main_content = match.group(1)
    jsx_content = html_to_jsx(main_content)

    final_code = f"""import React from 'react';

const {component_name} = () => {{
  return (
    <>
      {jsx_content}
    </>
  );
}};

export default {component_name};
"""
    with open(file_out, 'w') as f:
        f.write(final_code)

if __name__ == "__main__":
    extract_main_and_save('frontend_backup/index.html', 'frontend/src/pages/Home.jsx', 'Home')
    extract_main_and_save('frontend_backup/agents.html', 'frontend/src/pages/Agents.jsx', 'Agents')
    extract_main_and_save('frontend_backup/zones.html', 'frontend/src/pages/Zones.jsx', 'Zones')
    print("React pages generated successfully.")
