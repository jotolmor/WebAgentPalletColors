const form = document.getElementById("palette-form");
const paletteContainer = document.getElementById("palette");
const contrastText = document.getElementById("contrast");
const tokensEl = document.getElementById("tokens");
const colorWheel = document.getElementById("color-wheel");
const hueSlider = document.getElementById("hue");
const lightnessSlider = document.getElementById("lightness");
const alphaSlider = document.getElementById("alpha");
const addColorButton = document.getElementById("add-color");
const deleteColorButton = document.getElementById("delete-color");
const hueWheel = document.getElementById("hue-wheel");
const triadA = document.getElementById("triad-a");
const triadB = document.getElementById("triad-b");
const triadC = document.getElementById("triad-c");
const pageType = document.getElementById("page-type");
const pageRecommendation = document.getElementById("page-recommendation");
const aiPalettes = document.getElementById("ai-palettes");
const uiRecommendations = document.getElementById("ui-recommendations");
const layoutHtml = document.getElementById("layout-html");
const layoutBody = document.getElementById("layout-body");
const layoutNav = document.getElementById("layout-nav");
const layoutSlideshow = document.getElementById("layout-slideshow");
const layoutMain = document.getElementById("layout-main");
const layoutAside = document.getElementById("layout-aside");
const layoutFooter = document.getElementById("layout-footer");

let paletteState = [];
let selectedIndex = 0;
let baseHue = 210;

const toPayload = () => ({
  sentiment: form.sentiment.value,
  idea: form.idea.value,
  style: form.style.value || null,
  brand: form.brand.value || null,
  count: Number(form.count.value || 5),
  seed: form.seed.value ? Number(form.seed.value) : null,
});

const renderPalette = (data) => {
  paletteContainer.innerHTML = "";
  if (!data || data.error) {
    contrastText.textContent = data?.error
      ? `Error: ${data.error}`
      : "No se pudo generar la paleta.";
    return;
  }
  if (!data.palette || !data.contrast) {
    contrastText.textContent = "No se encontraron colores para mostrar.";
    return;
  }
  contrastText.textContent = `Contraste mínimo: ${data.contrast.min_ratio} — ${data.contrast.note}`;

  paletteState = data.palette.map((color) => ({ ...color }));
  baseHue = paletteState[0]?.hue ?? baseHue;
  paletteState.forEach((color, index) => {
    const swatch = document.createElement("div");
    swatch.className = "swatch";
    swatch.dataset.index = String(index);
    if (index === selectedIndex) {
      swatch.style.outline = "2px solid #6366f1";
    }

    const box = document.createElement("div");
    box.className = "color-box";
    box.style.background = color.formats.hex;

    const info = document.createElement("div");
    const textColor = getBestTextColor(color.formats.hex);
    const chipStyle = textColor === "#f8fafc" ? "#111827" : "#ffffff";
    info.innerHTML = `
      <strong>${color.name}</strong><br />
      <span class="meta">${color.formats.hex} · ${color.formats.rgb} · ${color.formats.hsl}</span>
      <div class="text-chip" style="background:${textColor}; color:${chipStyle}">
        Texto recomendado ${textColor}
      </div>
    `;

    swatch.appendChild(box);
    swatch.appendChild(info);
    paletteContainer.appendChild(swatch);
  });
  syncControlsWithSelection();
  renderRecommendations();
};

const renderAiPalettes = (data) => {
  aiPalettes.innerHTML = "";
  if (!data || !data.palettes) return;
  data.palettes.forEach((palette, index) => {
    const wrapper = document.createElement("div");
    wrapper.className = "mini-palette";
    const title = document.createElement("strong");
    title.textContent = `AI variante ${index + 1} (${palette.style || "base"})`;
    const row = document.createElement("div");
    row.className = "mini-row";
    palette.palette.slice(0, 5).forEach((color) => {
      const swatch = document.createElement("div");
      swatch.className = "mini-swatch";
      swatch.style.background = color.formats.hex;
      row.appendChild(swatch);
    });
    wrapper.appendChild(title);
    wrapper.appendChild(row);
    aiPalettes.appendChild(wrapper);
  });
};

const renderRecommendations = () => {
  if (!paletteState.length || !uiRecommendations) return;
  const sorted = [...paletteState].sort((a, b) => a.lightness - b.lightness);
  const darkest = sorted[0];
  const lightest = sorted[sorted.length - 1];
  const accent = sorted[Math.floor(sorted.length / 2)];
  const hover = sorted[Math.max(0, sorted.length - 2)];
  uiRecommendations.innerHTML = `
    <p class="meta">Usa estas combinaciones para una UI coherente y creativa:</p>
    <ul class="meta">
      <li><strong>HTML fondo:</strong> ${lightest.formats.hex}</li>
      <li><strong>Body fondo:</strong> ${sorted[sorted.length - 2].formats.hex}</li>
      <li><strong>Encabezado:</strong> ${accent.formats.hex}</li>
      <li><strong>Menú navegación:</strong> ${darkest.formats.hex}</li>
      <li><strong>Botones:</strong> ${accent.formats.hex}</li>
      <li><strong>Botones hover:</strong> ${hover.formats.hex}</li>
      <li><strong>Footer:</strong> ${darkest.formats.hex}</li>
    </ul>
  `;
  renderLayoutPreview({
    html: lightest.formats.hex,
    body: sorted[sorted.length - 2].formats.hex,
    nav: darkest.formats.hex,
    slideshow: accent.formats.hex,
    main: accent.formats.hex,
    aside: hover.formats.hex,
    footer: darkest.formats.hex,
  });
};

const setLayoutBlock = (element, hex) => {
  if (!element) return;
  element.style.background = hex;
  element.style.color = getBestTextColor(hex);
  element.textContent = `${element.dataset.label || element.textContent} ${hex}`;
};

const renderLayoutPreview = ({ html, body, nav, slideshow, main, aside, footer }) => {
  setLayoutBlock(layoutHtml, html);
  setLayoutBlock(layoutBody, body);
  setLayoutBlock(layoutNav, nav);
  setLayoutBlock(layoutSlideshow, slideshow);
  setLayoutBlock(layoutMain, main);
  setLayoutBlock(layoutAside, aside);
  setLayoutBlock(layoutFooter, footer);
};

const hexToHsl = (hex) => {
  const clean = hex.replace("#", "");
  const r = parseInt(clean.substring(0, 2), 16) / 255;
  const g = parseInt(clean.substring(2, 4), 16) / 255;
  const b = parseInt(clean.substring(4, 6), 16) / 255;
  const max = Math.max(r, g, b);
  const min = Math.min(r, g, b);
  let h = 0;
  let s = 0;
  const l = (max + min) / 2;
  if (max !== min) {
    const d = max - min;
    s = l > 0.5 ? d / (2 - max - min) : d / (max + min);
    switch (max) {
      case r:
        h = (g - b) / d + (g < b ? 6 : 0);
        break;
      case g:
        h = (b - r) / d + 2;
        break;
      default:
        h = (r - g) / d + 4;
    }
    h *= 60;
  }
  return { h: Math.round(h), s: Math.round(s * 100), l: Math.round(l * 100) };
};

const hslToHex = (h, s, l) => {
  const sat = s / 100;
  const light = l / 100;
  const c = (1 - Math.abs(2 * light - 1)) * sat;
  const x = c * (1 - Math.abs(((h / 60) % 2) - 1));
  const m = light - c / 2;
  let r1 = 0;
  let g1 = 0;
  let b1 = 0;
  if (h < 60) {
    r1 = c;
    g1 = x;
  } else if (h < 120) {
    r1 = x;
    g1 = c;
  } else if (h < 180) {
    g1 = c;
    b1 = x;
  } else if (h < 240) {
    g1 = x;
    b1 = c;
  } else if (h < 300) {
    r1 = x;
    b1 = c;
  } else {
    r1 = c;
    b1 = x;
  }
  const toHex = (value) => Math.round((value + m) * 255).toString(16).padStart(2, "0");
  return `#${toHex(r1)}${toHex(g1)}${toHex(b1)}`;
};

const getBestTextColor = (hex) => {
  const [r, g, b] = hexToRgb(hex).map((value) => value / 255);
  const luminance = 0.2126 * r + 0.7152 * g + 0.0722 * b;
  return luminance > 0.6 ? "#0f172a" : "#f8fafc";
};

const updateSelectedColor = (hex, alpha) => {
  if (!paletteState[selectedIndex]) return;
  const hsl = hexToHsl(hex);
  paletteState[selectedIndex].formats.hex = hex.toUpperCase();
  paletteState[selectedIndex].formats.rgb = `rgb(${hexToRgb(hex).join(", ")})`;
  paletteState[selectedIndex].formats.hsl = `hsl(${hsl.h}, ${hsl.s}%, ${hsl.l}%)`;
  paletteState[selectedIndex].formats.rgba = `rgba(${hexToRgb(hex).join(", ")}, ${alpha})`;
  paletteState[selectedIndex].formats.hsla = `hsla(${hsl.h}, ${hsl.s}%, ${hsl.l}%, ${alpha})`;
  paletteState[selectedIndex].hue = hsl.h;
  paletteState[selectedIndex].saturation = hsl.s;
  paletteState[selectedIndex].lightness = hsl.l;
  renderPalette({ palette: paletteState, contrast: { min_ratio: "-", note: "Personalizado" } });
};

const hexToRgb = (hex) => {
  const clean = hex.replace("#", "");
  return [
    parseInt(clean.substring(0, 2), 16),
    parseInt(clean.substring(2, 4), 16),
    parseInt(clean.substring(4, 6), 16),
  ];
};

const updateTriad = (hex) => {
  const hsl = hexToHsl(hex);
  const triad1 = hslToHex((hsl.h + 120) % 360, hsl.s, hsl.l);
  const triad2 = hslToHex((hsl.h + 240) % 360, hsl.s, hsl.l);
  triadA.style.background = hex;
  triadB.style.background = triad1;
  triadC.style.background = triad2;
};

const syncControlsWithSelection = () => {
  const selected = paletteState[selectedIndex];
  if (!selected) return;
  const hex = selected.formats.hex;
  colorWheel.value = hex;
  hueSlider.value = selected.hue;
  lightnessSlider.value = selected.lightness;
  alphaSlider.value = selected.formats.rgba?.split(", ").pop()?.replace(")", "") || 0.85;
  updateTriad(hex);
};

const fetchPalette = async () => {
  const response = await fetch("/api/palette", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(toPayload()),
  });
  const data = await response.json();
  if (!response.ok) {
    return { error: data.detail || "No se pudo generar la paleta." };
  }
  return data;
};

const fetchTokens = async () => {
  const payload = toPayload();
  payload.format = form.format.value;
  const response = await fetch("/api/export", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  const data = await response.json();
  if (!response.ok) {
    return { error: data.detail || data.error || "No se pudo exportar." };
  }
  return data;
};

const fetchAiPalettes = async () => {
  const response = await fetch("/api/ai-palettes", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(toPayload()),
  });
  return response.json();
};

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const palette = await fetchPalette();
  renderPalette(palette);
  const ai = await fetchAiPalettes();
  renderAiPalettes(ai);
  const tokens = await fetchTokens();
  if (tokens.error) {
    tokensEl.textContent = tokens.error;
    return;
  }
  tokensEl.textContent =
    typeof tokens.content === "string"
      ? tokens.content
      : JSON.stringify(tokens.content, null, 2);
});

paletteContainer.addEventListener("click", (event) => {
  const swatch = event.target.closest(".swatch");
  if (!swatch) return;
  selectedIndex = Number(swatch.dataset.index);
  syncControlsWithSelection();
  renderPalette({ palette: paletteState, contrast: { min_ratio: "-", note: "Personalizado" } });
});

colorWheel.addEventListener("input", () => {
  const newHue = hexToHsl(colorWheel.value).h;
  const delta = newHue - baseHue;
  paletteState = paletteState.map((color) => {
    const nextHue = (color.hue + delta + 360) % 360;
    const nextHex = hslToHex(nextHue, color.saturation, color.lightness);
    return {
      ...color,
      hue: nextHue,
      formats: {
        ...color.formats,
        hex: nextHex.toUpperCase(),
        rgb: `rgb(${hexToRgb(nextHex).join(", ")})`,
        hsl: `hsl(${nextHue}, ${color.saturation}%, ${color.lightness}%)`,
      },
    };
  });
  baseHue = newHue;
  renderPalette({ palette: paletteState, contrast: { min_ratio: "-", note: "Personalizado" } });
});

hueSlider.addEventListener("input", () => {
  const hex = hslToHex(Number(hueSlider.value), 60, Number(lightnessSlider.value));
  updateSelectedColor(hex, alphaSlider.value);
});

lightnessSlider.addEventListener("input", () => {
  const hex = hslToHex(Number(hueSlider.value), 60, Number(lightnessSlider.value));
  updateSelectedColor(hex, alphaSlider.value);
});

alphaSlider.addEventListener("input", () => {
  updateSelectedColor(colorWheel.value, alphaSlider.value);
});

addColorButton.addEventListener("click", () => {
  const hex = colorWheel.value;
  const hsl = hexToHsl(hex);
  paletteState.push({
    name: `Color ${paletteState.length + 1}`,
    hue: hsl.h,
    saturation: hsl.s,
    lightness: hsl.l,
    formats: {
      hex: hex.toUpperCase(),
      rgb: `rgb(${hexToRgb(hex).join(", ")})`,
      rgba: `rgba(${hexToRgb(hex).join(", ")}, ${alphaSlider.value})`,
      hsl: `hsl(${hsl.h}, ${hsl.s}%, ${hsl.l}%)`,
      hsla: `hsla(${hsl.h}, ${hsl.s}%, ${hsl.l}%, ${alphaSlider.value})`,
    },
  });
  selectedIndex = paletteState.length - 1;
  renderPalette({ palette: paletteState, contrast: { min_ratio: "-", note: "Personalizado" } });
});

deleteColorButton.addEventListener("click", () => {
  if (paletteState.length <= 1) return;
  paletteState.splice(selectedIndex, 1);
  selectedIndex = Math.max(0, selectedIndex - 1);
  renderPalette({ palette: paletteState, contrast: { min_ratio: "-", note: "Personalizado" } });
});

hueWheel.addEventListener("click", (event) => {
  const rect = hueWheel.getBoundingClientRect();
  const x = event.clientX - rect.left - rect.width / 2;
  const y = event.clientY - rect.top - rect.height / 2;
  const angle = (Math.atan2(y, x) * 180) / Math.PI;
  const hue = (angle + 360 + 90) % 360;
  hueSlider.value = Math.round(hue);
  const hex = hslToHex(Number(hueSlider.value), 60, Number(lightnessSlider.value));
  updateSelectedColor(hex, alphaSlider.value);
});

pageType.addEventListener("change", () => {
  const map = {
    landing: {
      sentiment: "energia",
      style: "futurista",
      recommendation: "Usa colores vibrantes con alto contraste para captar atención.",
    },
    ecommerce: {
      sentiment: "confianza",
      style: "minimalista",
      recommendation: "Mantén tonos claros y confiables para facilitar la compra.",
    },
    portfolio: {
      sentiment: "creatividad",
      style: "retro",
      recommendation: "Combina acentos llamativos para destacar proyectos.",
    },
    dashboard: {
      sentiment: "confianza",
      style: "minimalista",
      recommendation: "Prioriza legibilidad y fondos neutros.",
    },
  };
  const selection = map[pageType.value];
  if (selection) {
    form.sentiment.value = selection.sentiment;
    form.style.value = selection.style;
    pageRecommendation.textContent = selection.recommendation;
  } else {
    pageRecommendation.textContent = "";
  }
});
