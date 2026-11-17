"""Gera openapi.json a partir do swagger/swagger.json do sistema.

Mantém só a API da aplicação e a API do cliente, troca o servidor para a
produção do ChatClean e o nome do produto nas descrições.
Uso: python3 scripts/build_openapi.py <caminho do swagger.json>
"""
import json
import re
import sys

KEEP_GROUPS = {'Application', 'Client'}
DROP_TAGS = {'Audit Logs'}  # tela só do Enterprise, fora da produção
SERVER = 'https://chat.chatclean.com.br'


REPLACEMENTS = [
    (' Available in Chatwoot `v4.19.0` and later.', ''),
    (' in Chatwoot `v4.19.0` and later', ''),
    ('https://www.chatwoot.com/hc/user-guide/articles/1677839703-how-to-create-an-api-channel-inbox',
     'https://docs.chatclean.com.br/canais/api'),
    ('app.chatwoot.com', 'chat.chatclean.com.br'),
    ('https://www.chatwoot.com', 'https://www.exemplo.com.br'),
    ('chatwoot.help', 'ajuda.exemplo.com.br'),
    ('chatwoot.com', 'exemplo.com.br'),
]


def rebrand(value):
    if isinstance(value, str):
        for old, new in REPLACEMENTS:
            value = value.replace(old, new)
        return re.sub(r'(?<![_a-z])[Cc]hatwoot(?![_a-z])', 'ChatClean', value)
    if isinstance(value, list):
        return [rebrand(item) for item in value]
    if isinstance(value, dict):
        return {key: rebrand(item) for key, item in value.items()}
    return value


def main(source):
    spec = json.load(open(source))
    groups = [g for g in spec.get('x-tagGroups', []) if g['name'] in KEEP_GROUPS]
    tags = {tag for group in groups for tag in group['tags']} - DROP_TAGS
    for group in groups:
        group['tags'] = [tag for tag in group['tags'] if tag in tags]

    paths = {}
    for path, operations in spec['paths'].items():
        kept = {}
        for method, operation in operations.items():
            if not isinstance(operation, dict) or 'tags' not in operation:
                kept[method] = operation
            elif operation['tags'][0] in tags:
                kept[method] = operation
        if any(isinstance(op, dict) and 'tags' in op for op in kept.values()):
            paths[path] = kept

    platform = {'platformAppBearerAuth', 'platformAppApiKey'}
    for name in platform:
        spec['components']['securitySchemes'].pop(name, None)
    for operations in paths.values():
        for operation in operations.values():
            if isinstance(operation, dict) and 'security' in operation:
                operation['security'] = [s for s in operation['security'] if not platform & set(s)]
    spec['paths'] = paths
    spec['x-tagGroups'] = groups
    spec['tags'] = [tag for tag in spec.get('tags', []) if tag['name'] in tags]
    spec['servers'] = [{'url': SERVER}]
    spec['info'] = {
        'title': 'ChatClean API',
        'description': 'API REST do ChatClean.',
        'version': spec['info']['version'],
        'contact': {'email': 'contato@chatclean.com.br'},
    }
    spec = rebrand(spec)
    with open('openapi.json', 'w') as out:
        json.dump(spec, out, ensure_ascii=False, indent=2)
    print(f'{len(paths)} caminhos, {len(tags)} tags')


if __name__ == '__main__':
    main(sys.argv[1])
