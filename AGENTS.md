# Documentação do ChatClean: instruções

- Site Mintlify: páginas MDX com frontmatter YAML (`title`, `description`, `icon`); a navegação e o `openapi` ficam no `docs.json`.
- Idioma único: português do Brasil. Rótulos de tela em **negrito**, exatamente como aparecem no app (fonte: `app/javascript/dashboard/i18n/locale/pt_BR/*.json` do repositório do sistema, branch `main`).
- O código do sistema (repositório `dev-chatclean/chatclean_sistem`, branch `main`, que é o que roda em produção) é a fonte da verdade. Toda afirmação sobre comportamento precisa bater com ele. O que não estiver na `main` não entra.
- A produção roda sem a pasta `enterprise/`. Não documente telas que só existem nela: Captain, SLA, Auditoria, Funções personalizadas, Cobrança, Chamadas de voz, Fluxo de conversa, Atribuição de agentes e Monitores.
- O ChatClean é só SaaS: não há self-hosting nem instruções de instalação.
- Sem prints de tela (ainda). Sem linguagem de marketing nem emoji. Frases curtas, voz ativa, tratamento por "você".
- Links internos sempre a partir da raiz e sem extensão (`/atendimento/conversas`).

## URLs

| Serviço | URL |
| --- | --- |
| App | `https://chat.chatclean.com.br` |
| API REST | `https://chat.chatclean.com.br/api/v1` |
| Documentação | `https://docs.chatclean.com.br` |
| Suporte | `contato@chatclean.com.br` |

## API

`openapi.json` gera as páginas de endpoint. Ele vem do `swagger/swagger.json` do sistema, só com a API da aplicação e a API do cliente, com o servidor trocado para `https://chat.chatclean.com.br`. As descrições dos endpoints ainda estão em inglês. Para regenerar: `python3 scripts/build_openapi.py <caminho do swagger.json>`.
