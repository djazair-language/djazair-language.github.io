"""
Syntax highlighter for Djazair, C, and Shell code snippets.
"""
import re
import html

def highlight_djazair(code: str) -> str:
    """Highlight Djazair programming language code."""
    # Token specification ordered by precedence
    token_spec = [
        ('COMMENT_MULTI', r'#![\s\S]*?!#'),
        ('OUTPUT_COMMENT', r'#\s*=>[^\n]*'),
        ('COMMENT_SINGLE', r'#[^\n]*'),
        ('STRING_BACKTICK', r'`(?:\\.|[^`\\])*`'),
        ('STRING_DOUBLE', r'"(?:\\.|[^"\\])*"'),
        ('NUMBER', r'\b\d+(?:_\d+)*(?:\.\d+)?\b|\b0x[0-9a-fA-F]+\b'),
        ('KEYWORD', r'\b(?:let|fn|return|class|init|super|self|is|instanceof|try|catch|finally|throw|if|elif|else|match|case|default|while|do|for|in|to|break|continue|and|or|not|Null|True|False|use|import|as|end|new|async|await)\b'),
        ('BUILTIN', r'\b(?:print|input|type|str|num|bool|int|float|chr|ord|range|enumerate|zip|abs|round|exit|isNull|isString|isNumber|isInt|isFloat|isBool|isArray|isMap|isFunction|isClass|__native|hasNative|getFile|getDir|getLine)\b'),
        ('FN_CALL', r'\b[a-zA-Z_][a-zA-Z0-9_]*(?=\s*\()'),
        ('OP', r'[+\-*/%&|^~<>!=?:@]+|\.\.|\=\>'),
        ('IDENT', r'[a-zA-Z_][a-zA-Z0-9_]*'),
        ('SPACE', r'\s+'),
        ('OTHER', r'.')
    ]
    
    tok_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in token_spec)
    
    out = []
    for mo in re.finditer(tok_regex, code):
        kind = mo.lastgroup
        val = mo.group()
        esc_val = html.escape(val)
        
        if kind == 'COMMENT_MULTI' or kind == 'COMMENT_SINGLE':
            out.append(f'<span class="hl-comment">{esc_val}</span>')
        elif kind == 'OUTPUT_COMMENT':
            out.append(f'<span class="hl-output">{esc_val}</span>')
        elif kind in ('STRING_DOUBLE', 'STRING_BACKTICK'):
            # Highlight string interpolation ${...} inside strings
            interp_pattern = r'(\$\{)(.*?)(\})'
            def interp_replace(m):
                prefix = html.escape(m.group(1))
                inner = highlight_djazair(m.group(2))
                suffix = html.escape(m.group(3))
                return f'<span class="hl-interp">{prefix}</span>{inner}<span class="hl-interp">{suffix}</span>'
            
            # First escape string body
            highlighted_str = re.sub(interp_pattern, interp_replace, esc_val)
            out.append(f'<span class="hl-str">{highlighted_str}</span>')
        elif kind == 'KEYWORD':
            out.append(f'<span class="hl-kw">{esc_val}</span>')
        elif kind == 'BUILTIN':
            out.append(f'<span class="hl-builtin">{esc_val}</span>')
        elif kind == 'NUMBER':
            out.append(f'<span class="hl-num">{esc_val}</span>')
        elif kind == 'FN_CALL':
            out.append(f'<span class="hl-fn">{esc_val}</span>')
        elif kind == 'OP':
            out.append(f'<span class="hl-op">{esc_val}</span>')
        else:
            out.append(esc_val)
            
    return ''.join(out)

def highlight_c(code: str) -> str:
    """Highlight C / C++ code."""
    token_spec = [
        ('COMMENT', r'//[^\n]*|/\*[\s\S]*?\*/'),
        ('DIRECTIVE', r'#(?:include|define|undef|ifdef|ifndef|endif|pragma)\b[^\n]*'),
        ('STRING', r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\''),
        ('KEYWORD', r'\b(?:int|char|void|float|double|long|short|unsigned|signed|struct|enum|union|typedef|static|const|return|if|else|for|while|do|switch|case|default|break|continue|sizeof|NULL|true|false)\b'),
        ('NUMBER', r'\b\d+(?:\.\d+)?\b'),
        ('FN_CALL', r'\b[a-zA-Z_][a-zA-Z0-9_]*(?=\s*\()'),
        ('OP', r'[+\-*/%&|^~<>!=?:.]+'),
        ('SPACE', r'\s+'),
        ('OTHER', r'.')
    ]
    tok_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in token_spec)
    out = []
    for mo in re.finditer(tok_regex, code):
        kind = mo.lastgroup
        val = mo.group()
        esc_val = html.escape(val)
        if kind == 'COMMENT':
            out.append(f'<span class="hl-comment">{esc_val}</span>')
        elif kind == 'DIRECTIVE':
            out.append(f'<span class="hl-special">{esc_val}</span>')
        elif kind == 'STRING':
            out.append(f'<span class="hl-str">{esc_val}</span>')
        elif kind == 'KEYWORD':
            out.append(f'<span class="hl-kw">{esc_val}</span>')
        elif kind == 'NUMBER':
            out.append(f'<span class="hl-num">{esc_val}</span>')
        elif kind == 'FN_CALL':
            out.append(f'<span class="hl-fn">{esc_val}</span>')
        elif kind == 'OP':
            out.append(f'<span class="hl-op">{esc_val}</span>')
        else:
            out.append(esc_val)
    return ''.join(out)

def highlight_shell(code: str) -> str:
    """Highlight shell/bash/powershell commands."""
    token_spec = [
        ('COMMENT', r'#[^\n]*'),
        ('STRING', r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\''),
        ('CMD', r'^\s*[a-zA-Z0-9_.-]+'),
        ('FLAG', r'--?[a-zA-Z0-9_-]+'),
        ('SPACE', r'\s+'),
        ('OTHER', r'.')
    ]
    tok_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in token_spec)
    out = []
    for mo in re.finditer(tok_regex, code):
        kind = mo.lastgroup
        val = mo.group()
        esc_val = html.escape(val)
        if kind == 'COMMENT':
            out.append(f'<span class="hl-comment">{esc_val}</span>')
        elif kind == 'STRING':
            out.append(f'<span class="hl-str">{esc_val}</span>')
        elif kind == 'FLAG':
            out.append(f'<span class="hl-special">{esc_val}</span>')
        else:
            out.append(esc_val)
    return ''.join(out)

def process_code_blocks(html_content: str) -> str:
    """
    Find all <pre><code class="language-..."> blocks in HTML
    and replace them with highlighted code wrapped in .code-wrapper.
    """
    pattern = r'<pre><code class="language-([^"]+)">(.*?)</code></pre>'
    
    def repl(m):
        lang = m.group(1).lower()
        raw_code = m.group(2)
        # Unescape any preliminary escaping to get exact characters
        unescaped_code = html.unescape(raw_code).strip('\n')
        
        display_lang = lang
        if lang in ('dz', 'djazair'):
            highlighted = highlight_djazair(unescaped_code)
            display_lang = 'djazair'
        elif lang in ('c', 'cpp'):
            highlighted = highlight_c(unescaped_code)
            display_lang = 'c'
        elif lang in ('bash', 'sh', 'shell', 'powershell'):
            highlighted = highlight_shell(unescaped_code)
            display_lang = 'bash' if lang != 'powershell' else 'powershell'
        elif lang == 'json':
            highlighted = html.escape(unescaped_code)
            display_lang = 'json'
        else:
            highlighted = html.escape(unescaped_code)
            
        return f'''<div class="code-wrapper">
  <div class="code-header">
    <span class="code-lang">{display_lang}</span>
    <button class="copy-btn" aria-label="Copy code"><i class="fa-regular fa-copy"></i> Copy</button>
  </div>
  <pre><code>{highlighted}</code></pre>
</div>'''

    return re.sub(pattern, repl, html_content, flags=re.DOTALL)
