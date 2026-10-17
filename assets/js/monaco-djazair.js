/**
 * Djazair Language Definition for Monaco Editor
 * Aligned with the official Djazair IDE (djazair-ide) grammar and theme.
 */

(function (root, factory) {
    'use strict';
    var api = factory();
    if (typeof root !== 'undefined') {
        root.MonacoDjazair = api;
    }
    if (typeof window !== 'undefined') {
        window.MonacoDjazair = api;
    }
    if (typeof define === 'function' && define.amd) {
        try {
            define('monaco-djazair', [], function () { return api; });
        } catch (_) {}
    }
    if (typeof root !== 'undefined' && typeof root.monaco !== 'undefined') {
        try { api.setup(root.monaco); } catch (_) {}
    }
})(typeof self !== 'undefined' ? self : this, function () {
    'use strict';

    const DJAZAIR_KEYWORDS = [
        'fn', 'let', 'class', 'new', 'end', 'use', 'import', 'as',
        'if', 'elif', 'else', 'for', 'while', 'do',
        'match', 'case', 'default',
        'try', 'catch', 'finally', 'throw',
        'return', 'break', 'continue',
        'super', 'self', 'init',
        'async', 'await',
        'is', 'instanceof',
        'and', 'or', 'not', 'in'
    ];

    const DJAZAIR_CONSTANTS = ['True', 'False', 'Null'];

    const DJAZAIR_TYPES = ['Number', 'String', 'Bool', 'Map', 'Array', 'Function', 'NullType'];

    const DJAZAIR_STDLIB = [
        'assert', 'bytes', 'collections', 'crypto', 'datetime', 'dir',
        'env', 'file', 'http', 'json', 'lang', 'math', 'net', 'os',
        'path', 'process', 'random', 'regex', 'thread', 'uuid'
    ];

    const DJAZAIR_OPERATORS = [
        '++', '--', '**', '//', '..', '->', '=>',
        '+=', '-=', '*=', '/=', '%=', '**=', '//=', '&=', '|=', '^=', '<<=', '>>=',
        '==', '!=', '<=', '>=', '&&', '||', '<<', '>>',
        '+', '-', '*', '/', '%', '<', '>', '=', '!', '&', '|', '^', '~', ':', '.'
    ];

    const DJAZAIR_CONFIGURATION = {
        comments: {
            lineComment: '#',
            blockComment: ['#*', '*#']
        },
        brackets: [
            ['{', '}'],
            ['[', ']'],
            ['(', ')']
        ],
        autoClosingPairs: [
            { open: '{', close: '}' },
            { open: '[', close: ']' },
            { open: '(', close: ')' },
            { open: '"', close: '"', notIn: ['string'] },
            { open: '`', close: '`', notIn: ['string'] }
        ],
        surroundingPairs: [
            { open: '{', close: '}' },
            { open: '[', close: ']' },
            { open: '(', close: ')' },
            { open: '"', close: '"' },
            { open: '`', close: '`' }
        ],
        wordPattern: /[a-zA-Z0-9_\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF]+/,
        indentationRules: {
            increaseIndentPattern: /^\s*(fn|class|if|elif|else|while|do|for|match|case|default|try|catch|finally)\b.*$/,
            decreaseIndentPattern: /^\s*(end|else|elif|catch|finally|default)\b.*$/
        },
        onEnterRules: [
            {
                beforeText: /^\s*(fn|class|if|while|for|match|try|do)\b.*$/,
                afterText: /^\s*end\b/,
                action: { indentAction: 1 /* Indent */ }
            },
            {
                beforeText: /^\s*(fn|class|if|while|for|match|try|do)\b.*$/,
                action: { indentAction: 1 /* Indent */, appendText: 'end' }
            }
        ]
    };

    const DJAZAIR_MONARCH = {
        keywords: DJAZAIR_KEYWORDS,
        constants: DJAZAIR_CONSTANTS,
        stdlib: DJAZAIR_STDLIB,
        typeKeywords: DJAZAIR_TYPES,
        operators: DJAZAIR_OPERATORS,

        tokenizer: {
            root: [
                // Multi-line block comments (#* ... *#)
                [/#\*/, 'comment', '@comment'],
                // Doc line comments (### ...)
                [/###.*$/, 'comment.doc'],
                // Single-line comments (# ...)
                [/#.*$/, 'comment'],

                // Strings
                [/"/, { token: 'string.quote', next: '@dstring' }],
                [/`/, { token: 'string.quote', next: '@btstring' }],

                // Numbers: hex, binary, octal, decimal with underscores
                [/0[xX][\da-fA-F][\da-fA-F_]*/, 'number'],
                [/0[bB][01][01_]*/, 'number'],
                [/0[oO][0-7][0-7_]*/, 'number'],
                [/\d[\d_]*(\.[\d_]*)?([eE][+-]?\d[\d_]*)?/, 'number'],
                [/\.[\d_]+([eE][+-]?\d[\d_]*)?/, 'number'],

                // Range operator
                [/\.\./, 'operator'],

                // Functions (Identifiers followed by '(')
                [/[a-zA-Z_\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF][\w\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF]*(?=\s*\()/, {
                    cases: {
                        '@keywords': 'keyword',
                        '@default': 'function'
                    }
                }],

                // Identifiers and keywords (supporting ASCII and Arabic unicode characters)
                [/[a-zA-Z_\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF][\w\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF]*/, {
                    cases: {
                        '@keywords': 'keyword',
                        '@constants': 'constant.language',
                        '@stdlib': 'type',
                        '@typeKeywords': 'type',
                        '@default': 'identifier'
                    }
                }],

                // Operators
                [/[+\-*/%&|^~<>=!.:]+/, {
                    cases: {
                        '@operators': 'operator',
                        '@default': ''
                    }
                }],

                // Brackets
                [/[{}()\[\]]/, '@brackets']
            ],

            comment: [
                [/[^#*]+/, 'comment'],
                [/#\*/, 'comment', '@push'],
                [/\*#/, 'comment', '@pop'],
                [/[#*]/, 'comment']
            ],

            dstring: [
                [/[^"$\\\n]+/, 'string'],
                [/\\./, 'string.escape'],
                [/\$\{/, { token: 'string.interpolation', next: '@interpolation' }],
                [/"/, { token: 'string.quote', next: '@pop' }],
                [/./, 'string']
            ],

            btstring: [
                [/[^`$\\]+/, 'string'],
                [/\\./, 'string.escape'],
                [/\$\{/, { token: 'string.interpolation', next: '@interpolation' }],
                [/`/, { token: 'string.quote', next: '@pop' }],
                [/./, 'string']
            ],

            interpolation: [
                [/[^}]+/, 'string.expression'],
                [/}/, { token: 'string.interpolation', next: '@pop' }]
            ]
        }
    };

    const DJAZAIR_THEME = {
        base: 'vs-dark',
        inherit: true,
        rules: [
            { token: 'keyword', foreground: '00e5ff', fontStyle: 'bold' },
            { token: 'constant.language', foreground: 'ffeac0', fontStyle: 'bold' },
            { token: 'type', foreground: 'c792ea', fontStyle: 'bold' },
            { token: 'string', foreground: 'c3e88d' },
            { token: 'string.quote', foreground: 'c3e88d' },
            { token: 'string.escape', foreground: 'f78c6c' },
            { token: 'string.interpolation', foreground: 'ffcb6b' },
            { token: 'string.expression', foreground: 'e2e2e6' },
            { token: 'comment', foreground: '546e7a', fontStyle: 'italic' },
            { token: 'comment.doc', foreground: '546e7a', fontStyle: 'italic' },
            { token: 'number', foreground: 'f78c6c' },
            { token: 'operator', foreground: '89ddff' },
            { token: 'function', foreground: '82aaff', fontStyle: 'bold' },
            { token: 'identifier', foreground: 'e2e2e6' }
        ],
        colors: {
            'editor.background': '#0b101e',
            'editor.foreground': '#e2e2e6',
            'editor.lineHighlightBackground': '#131c31',
            'editorCursor.foreground': '#00e5ff',
            'editorLineNumber.foreground': '#546e7a',
            'editorLineNumber.activeForeground': '#00e5ff',
            'editor.selectionBackground': '#00e5ff22',
            'editor.inactiveSelectionBackground': '#00e5ff11'
        }
    };

    function setup(monaco) {
        if (!monaco || !monaco.languages) return;

        try {
            const existing = monaco.languages.getLanguages();
            const exists = existing && existing.some(function (l) { return l.id === 'djazair'; });
            if (!exists) {
                monaco.languages.register({ id: 'djazair', extensions: ['.dz', '.djazair'] });
            }
            monaco.languages.setLanguageConfiguration('djazair', DJAZAIR_CONFIGURATION);
            monaco.languages.setMonarchTokensProvider('djazair', DJAZAIR_MONARCH);

            monaco.editor.defineTheme('djazair-theme', DJAZAIR_THEME);
            monaco.editor.defineTheme('djazair-dark', DJAZAIR_THEME);
            monaco.editor.setTheme('djazair-theme');
        } catch (err) {
            console.warn('Monaco Djazair setup warning:', err);
        }
    }

    return {
        KEYWORDS: DJAZAIR_KEYWORDS,
        CONSTANTS: DJAZAIR_CONSTANTS,
        TYPES: DJAZAIR_TYPES,
        STDLIB: DJAZAIR_STDLIB,
        OPERATORS: DJAZAIR_OPERATORS,
        CONFIGURATION: DJAZAIR_CONFIGURATION,
        MONARCH: DJAZAIR_MONARCH,
        THEME: DJAZAIR_THEME,
        setup: setup
    };
});
