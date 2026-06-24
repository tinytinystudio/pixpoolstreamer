# CODEX_CONTEXT.md

## Projeto

Este repositório é um projeto de exemplos de páginas web para anúncios digitais exibidos em telões e televisões na via pública.

As páginas devem funcionar como peças publicitárias em tela cheia, normalmente carregadas dentro do player por iframe.

## Onde criar exemplos

Todos os exemplos de anúncios devem ser criados dentro da pasta `pages/`.

Quando forem exemplos isolados ou modelos reutilizáveis, prefira a subpasta:

```text
pages/exemplos/
```

Exemplos existentes nessa pasta servem como referência de estrutura, principalmente:

```text
pages/exemplos/animado-produto.html
```

## Requisitos básicos para anúncios

- Cada anúncio deve ser uma página HTML independente, pronta para ocupar 100% do viewport.
- Use `html, body { width: 100%; height: 100%; margin: 0; overflow: hidden; }` ou equivalente.
- Todos os elementos visuais e textos importantes devem permanecer dentro da área visível do viewport.
- O layout deve escalar de acordo com a resolução do dispositivo usando `clamp()`, `min()`, `max()`, unidades relativas ao viewport e media queries.
- Evite valores absolutos que façam texto, preço, CTA ou produto saírem da tela em resoluções menores.
- Em anúncios para telões/TVs, priorize legibilidade à distância: textos curtos, alto contraste e hierarquia visual clara.
- Não dependa de rolagem. O anúncio deve ser consumido como uma tela única.
- Se houver animações, elas devem iniciar apenas quando o player enviar o evento `play`.

## Integração com o player

Os exemplos animados devem seguir o protocolo usado pelo player:

```js
const PROTOCOL = "iframeplayer.v1";
```

Fluxo esperado:

1. O player envia `init`.
2. O anúncio responde `ready`.
3. O player envia `play`.
4. O anúncio adiciona a classe ou estado de reprodução, inicia a animação e responde `started`.
5. O player pode enviar `stop`, e o anúncio deve parar ou resetar o estado animado.

Use os exemplos em `pages/exemplos/` como base para manter esse contrato consistente.

## Estilo recomendado

- Prefira HTML, CSS e JavaScript sem dependências externas para que os anúncios carreguem rápido e sejam fáceis de hospedar.
- Use assets locais quando necessário, dentro de `pages/exemplos/assets/`.
- Mantenha nomes de arquivos descritivos, em minúsculas e com hífens.
- Evite textos longos. O público verá a peça em movimento ou à distância.
- Teste mentalmente ou visualmente em proporções comuns: 16:9 horizontal, telas verticais e viewports baixos.
