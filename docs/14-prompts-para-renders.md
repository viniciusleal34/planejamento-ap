# 🖼️ 14 — Prompts para Renders (IA)

[← Voltar ao README](../README.md) | [Anterior: Fornecedores](13-fornecedores-e-referencias.md) | [Próximo: Checklist →](15-checklist.md)

---

> **Objetivo**: gerar um conjunto completo de imagens conceituais do projeto (ambientes + detalhes + planta + iluminação + moodboard), com **consistência de estilo** e respeitando as decisões do planejamento.

Ferramentas sugeridas: **Midjourney**, **DALL·E**, **ChatGPT (imagem)**, **Leonardo AI**, **Stable Diffusion/SDXL**.

---

## ✅ Base do Projeto (use em todos os prompts)

Você pode copiar o bloco abaixo e colar no início de todos os prompts (ou manter mentalmente como “regra de consistência”).

```
PROJECT BASE (do not ignore): modern contemporary interior, clean, sophisticated, functional, minimalist. Brazilian compact apartment, 43.94 m². Layout: apartment entry opens into the kitchen; the kitchen is positioned BEHIND the sofa (not beside it); a balcony/varanda at the top connects both kitchen and living room with glass sliding doors. The sofa faces the TV wall panel, with its back toward the kitchen. Color palette: white and off-white base, light gray accents, small black accents, light oak / light wood. Materials: cement-look porcelain tile floor 60x60 (continuous), white matte MDF cabinetry, black matte metal details, black São Gabriel granite countertop in kitchen, matte black faucets and hardware. Lighting: warm 3000K, recessed spotlights and cove LED strip lighting; soft natural daylight. Architectural photography, photorealistic, realistic scale, tidy and uncluttered.
```

### Negative prompt (evitar)

```
NEGATIVE: clutter, messy cables, excessive decoration, colorful walls, strong patterns, glossy gold everywhere, heavy curtains, unrealistic proportions, fisheye distortion, people, readable text, watermark, logo, low resolution.
```

### Parâmetros rápidos (opcionais)

- **Midjourney**: `--ar 16:9 --style raw --v 6 --s 500` (wide) | `--ar 4:5` (vertical)
- **SDXL**: lente 24mm–28mm para wide, DOF leve, “photorealistic interior”

---

## 🏠 Pacote Completo de Imagens (shot list)

### 01 — Sala + Cozinha Integradas (vista geral)

```
PROJECT BASE. Wide-angle view (24mm) of the integrated living room + kitchen (approx. 12m² + 5m²). Black 180cm retractable sofa as focal point, facing a minimalist TV wall panel in light oak wood with black niches/shelves. The kitchen is positioned BEHIND the sofa (the sofa's back faces the kitchen area). A balcony/varanda with glass sliding doors is visible at the top, connecting both the living room and kitchen. Large rectangular decorative mirror with thin matte black frame reflecting daylight. Sheer white curtains. Kitchen with white flat-panel cabinets up to the ceiling, light wood accent strip, black granite countertop, white inverse refrigerator, black glass 4-burner cooktop. Continuous cement-look porcelain tile floor. Recessed ceiling with warm 3000K spots + subtle LED cove lighting. Photorealistic architectural photo, 8k.
NEGATIVE.
```

### 02 — Sala (ângulo do sofá para o painel de TV)

```
PROJECT BASE. Living room, camera positioned in the kitchen area looking toward the TV wall (as if standing where you enter the apartment). Show the back of the black 180cm sofa in the foreground, with the TV wall panel in light oak with black niches ahead. Balcony/varanda visible to the side with glass sliding doors. Emphasize the contrast: black sofa against white/off-white walls. Clean cable management, minimal decor. Warm 3000K lighting with soft cove LED glow and a few recessed spotlights. Cement-look porcelain floor. Photorealistic, 8k, realistic scale.
NEGATIVE.
```

### 03 — Sala (ângulo do painel para o sofá + espelho)

```
PROJECT BASE. Reverse angle: camera at the TV wall looking toward the black 180cm retractable sofa. Show the kitchen area fully visible behind the sofa (the apartment entry is through the kitchen). The balcony/varanda with glass sliding doors is visible at the top, connecting both living room and kitchen. Show the large mirror on the side wall with thin matte black frame reflecting natural light. Clean, airy, minimal decor, light oak accents. Warm 3000K lighting, recessed spots. Photorealistic, 8k.
NEGATIVE.
```

### 04 — Detalhe: painel de TV + LED + nichos pretos

```
PROJECT BASE. Close-up detail shot of the TV wall panel: light oak MDF, matte black niches/shelves, subtle warm 3000K LED backlighting behind the TV/panel. Minimal objects, clean lines, no clutter. Photorealistic, macro detail, 8k.
NEGATIVE.
```

### 04B — Detalhe: painel ripado (parede destaque)

```
PROJECT BASE. Close-up / mid shot of a light oak MDF fluted slat wall panel (painel ripado) from floor to ceiling used as a feature wall in the living room or corridor. Clean vertical lines, warm 3000K grazing light, minimalist styling, cement-look porcelain floor. Photorealistic architectural detail, 8k.
NEGATIVE.
```

### 04C — Detalhe: sanca de gesso com LED indireto (sala)

```
PROJECT BASE. Upward-looking interior detail shot of the living room ceiling: gypsum cove (sanca) with hidden warm 3000K LED strip creating soft indirect light, plus a few recessed spotlights. Clean modern ceiling lines, no chandeliers, no clutter. Photorealistic, 8k.
NEGATIVE.
```

### 05 — Cozinha (vista frontal funcional)

```
PROJECT BASE. Compact modern kitchen wide shot (24–28mm). White matte MDF cabinets up to the ceiling, light wood detail strip, hidden handles or black aluminum profile. Black São Gabriel granite countertop with undermount stainless sink and matte black single-lever faucet. White inverse refrigerator. Black glass cooktop. Under-cabinet warm 3000K LED strip lighting. Cement-look porcelain floor. Photorealistic architectural photo, 8k.
NEGATIVE.
```

### 06 — Detalhe: bancada granito + cuba inox + torneira preta

```
PROJECT BASE. Close-up on kitchen countertop: black São Gabriel granite, undermount stainless sink, matte black faucet, clean backsplash, warm under-cabinet LED. Minimal accessories. Photorealistic macro, 8k.
NEGATIVE.
```

### 07 — Lavanderia (compacta e organizada)

```
PROJECT BASE. Compact laundry area (~2.5m²) wide shot. White Samsung washer-dryer on the floor against the back wall. White upper cabinet (up to ceiling) above the machine + 2–3 open niches for cleaning products. Compact 40x40 utility sink/tank with simple faucet. Retractable wall clothes rack. Cement-look porcelain tile floor continuous. Warm 3000K spot lighting. Very organized, practical, minimal.
NEGATIVE.
```

### 08 — Quarto 1 (casal, ~9m²) — vista geral

```
PROJECT BASE. Compact master bedroom (~9m²), wide-angle (24–28mm). Double bed 160x200 centered on the back wall, light wood headboard or light gray upholstered headboard. Two small nightstands (light wood or white). Full-wall wardrobe with sliding doors and large mirror panels in white matte MDF. Sheer white curtains, warm 3000K lighting, clean and calm. Cement-look porcelain floor. Photorealistic, 8k.
NEGATIVE.
```

### 09 — Quarto 1 — detalhe do guarda-roupa com espelho (amplitude)

```
PROJECT BASE. Bedroom wardrobe detail: white matte sliding wardrobe doors with large mirror panels reflecting daylight and making the room feel bigger. Minimal, tidy. Warm 3000K lighting. Photorealistic, 8k.
NEGATIVE.
```

### 10 — Quarto 2 (solteiro + escritório, ~7m²) — vista geral com 2 notebooks

```
PROJECT BASE. Compact second bedroom/home office (~7m²), wide-angle (24–28mm). One single bed 88x188 with neutral bedding. Sliding wardrobe with mirror panel in white MDF. A long desk (160x60 ideal) placed under the window or on a free wall, designed for TWO laptops (personal + work): two laptops on stands, one compact external keyboard and mouse, optional single external monitor, cable management tray. Ergonomic office chair. Warm 3000K lighting, very organized, minimal. Cement-look porcelain floor. Photorealistic, 8k.
NEGATIVE.
```

### 11 — Quarto 2 — detalhe do setup duplo (organização + cabos)

```
PROJECT BASE. Close-up detail of the dual-laptop workspace: two laptops (personal + work), one vertical stand for the idle laptop, one USB-C hub or simple KVM switch, tidy cable management channel, minimalist desk surface, warm 3000K ambient light. No brand logos, no readable text on screens. Photorealistic macro, 8k.
NEGATIVE.
```

### 12 — Banheiro (~3,5m²) — vista geral (perfil preto + metais pretos)

```
PROJECT BASE. Compact modern bathroom (~3.5m²), wide-angle (24–28mm). Tempered glass shower enclosure with matte black aluminum profile. Shower wall with cement-look or light gray porcelain tile. Vanity with black granite countertop (or gray porcelain), white basin (support or semi-recessed), matte black faucet. Large mirror spanning the width of the countertop, clean edges (optionally with subtle LED backlight). Matte black accessories. Warm 3000K ambient lighting (optional neutral 4000K at mirror). Photorealistic, 8k.
NEGATIVE.
```

### 13 — Banheiro — detalhe do box + metais pretos

```
PROJECT BASE. Close-up on shower enclosure: matte black frame profile, clean glass, matte black shower fixtures, light gray cement-look porcelain tiles, minimal spa-like look. Photorealistic macro, 8k.
NEGATIVE.
```

### 14 — Varanda (~3,5m²) — vista geral aconchegante

```
PROJECT BASE. Small balcony/varanda (~3.5m²) that connects BOTH the living room AND the kitchen through glass sliding doors. Same cement-look porcelain tile floor continuing from the interior (or subtle deck tiles as an optional variant). Small round bistro table (Ø60cm) with two chairs in matte black metal. 2–3 potted plants (snake plant, succulents, peace lily). Warm 3000K matte black wall sconce. Show the connection to both spaces. Cozy, minimal, clean. Photorealistic wide-angle, 8k.
NEGATIVE.
```

---

## 📐 Entregáveis Visuais do Planejamento (extras úteis)

### 15 — Moodboard / Material board (paleta + materiais)

```
Create a clean interior design moodboard (no readable text): white/off-white paint swatches, light gray cement-look porcelain tile sample (60x60), light oak wood texture, matte black metal accents, black São Gabriel granite sample, sheer white curtain fabric. Modern contemporary, minimalist, high-end look, evenly lit, top-down flat lay, photorealistic.
NEGATIVE.
```

### 16 — Planta humanizada (layout com mobiliário)

```
Generate a humanized floor plan for a 43.94m² Brazilian apartment, top-down 2D/3D hybrid. Keep original layout: open-plan living + kitchen, 2 bedrooms, bathroom, balcony, laundry, circulation hall. Place furniture: living room with black 180cm retractable sofa facing TV panel; kitchen with L/straight counter and white inverse refrigerator; bedroom 1 with 160x200 bed and mirrored wardrobe; bedroom 2 with single bed + long desk for two laptops and mirrored wardrobe; bathroom with vanity + shower box; balcony with Ø60 bistro table + 2 chairs + plants; laundry with white washer-dryer + upper cabinet + compact sink. Same material palette: white/off-white, light oak, light gray, small black accents. No labels, no readable text, clean linework.
NEGATIVE.
```

### 17 — Plano de iluminação (forro refletido)

```
Create a clean reflected ceiling plan (RCP) for the same 43.94m² apartment: show recessed spotlights positions per room, warm 3000K. Add cove LED strip lighting in living room and corridor. Minimal technical drawing style, monochrome linework, no readable text, no dimensions, high clarity.
NEGATIVE.
```

---

## 💡 Dicas para sair com imagens “de projeto”

- Gere primeiro a **imagem 01**; depois peça “match this style”/“use the same materials and palette” para todas as outras.
- Se a ferramenta começar a inventar objetos, acrescente: “**strictly follow the described items only**”.
- Para telas de notebook/TV: peça “**blank screens, no text**”.

---

[← Voltar ao README](../README.md) | [Anterior: Fornecedores](13-fornecedores-e-referencias.md) | [Próximo: Checklist →](15-checklist.md)