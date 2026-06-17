import anywidget
import traitlets
from pydantic import BaseModel, ConfigDict

from core import Settings

_ESM = """
function render({ model, el }) {
  el.innerHTML = `
    <div class="bayes-anywidget">
      <div class="bayes-controls"></div>
      <div class="bayes-posterior"></div>
      <svg class="bayes-chart" viewBox="0 0 520 240" preserveAspectRatio="xMidYMid meet"></svg>
    </div>
  `;
  const controls = el.querySelector(".bayes-controls");
  const posteriorBox = el.querySelector(".bayes-posterior");
  const svg = el.querySelector(".bayes-chart");

  const sliders = [
    { key: "prevalence",  label: "Prevalencia",   min: 0.001, max: 0.5,   step: 0.001 },
    { key: "sensitivity", label: "Sensibilidad",  min: 0.5,   max: 0.999, step: 0.001 },
    { key: "specificity", label: "Especificidad", min: 0.5,   max: 0.999, step: 0.001 },
  ];

  const valueLabels = {};
  for (const { key, label, min, max, step } of sliders) {
    const row = document.createElement("label");
    row.className = "bayes-row";
    const text = document.createElement("span");
    text.className = "bayes-label";
    text.textContent = label;
    const slider = document.createElement("input");
    slider.type = "range";
    slider.min = min;
    slider.max = max;
    slider.step = step;
    slider.value = model.get(key);
    const valueLabel = document.createElement("span");
    valueLabel.className = "bayes-value";
    valueLabel.textContent = Number(slider.value).toFixed(3);
    valueLabels[key] = valueLabel;
    slider.addEventListener("input", () => {
      const numeric = parseFloat(slider.value);
      model.set(key, numeric);
      model.save_changes();
      valueLabel.textContent = numeric.toFixed(3);
      redraw();
    });
    row.appendChild(text);
    row.appendChild(slider);
    row.appendChild(valueLabel);
    controls.appendChild(row);
  }

  function bayesPosterior(prevalence, sensitivity, specificity) {
    const truePositiveRate  = sensitivity * prevalence;
    const falsePositiveRate = (1 - specificity) * (1 - prevalence);
    const evidence = truePositiveRate + falsePositiveRate;
    return evidence === 0 ? 0 : truePositiveRate / evidence;
  }

  function bar(svgEl, x, label, prior, posterior) {
    const maxHeight = 150;
    const baseY = 190;
    const groupWidth = 160;
    const barWidth = 60;
    const priorX = x + groupWidth / 2 - barWidth - 4;
    const postX = x + groupWidth / 2 + 4;
    const priorH = prior * maxHeight;
    const postH = posterior * maxHeight;

    for (const [bx, bh, color] of [
      [priorX, priorH, "#1f77b4"],
      [postX,  postH,  "#ff7f0e"],
    ]) {
      const rect = document.createElementNS("http://www.w3.org/2000/svg", "rect");
      rect.setAttribute("x", bx);
      rect.setAttribute("y", baseY - bh);
      rect.setAttribute("width", barWidth);
      rect.setAttribute("height", bh);
      rect.setAttribute("fill", color);
      rect.setAttribute("opacity", "0.85");
      svgEl.appendChild(rect);
    }

    const caption = document.createElementNS("http://www.w3.org/2000/svg", "text");
    caption.setAttribute("x", x + groupWidth / 2);
    caption.setAttribute("y", 215);
    caption.setAttribute("text-anchor", "middle");
    caption.setAttribute("font-size", "12");
    caption.setAttribute("fill", "#333");
    caption.textContent = label;
    svgEl.appendChild(caption);

    const priorLabel = document.createElementNS("http://www.w3.org/2000/svg", "text");
    priorLabel.setAttribute("x", priorX + barWidth / 2);
    priorLabel.setAttribute("y", baseY - priorH - 6);
    priorLabel.setAttribute("text-anchor", "middle");
    priorLabel.setAttribute("font-size", "11");
    priorLabel.setAttribute("fill", "#1f77b4");
    priorLabel.textContent = prior.toFixed(3);
    svgEl.appendChild(priorLabel);

    const postLabel = document.createElementNS("http://www.w3.org/2000/svg", "text");
    postLabel.setAttribute("x", postX + barWidth / 2);
    postLabel.setAttribute("y", baseY - postH - 6);
    postLabel.setAttribute("text-anchor", "middle");
    postLabel.setAttribute("font-size", "11");
    postLabel.setAttribute("fill", "#ff7f0e");
    postLabel.textContent = posterior.toFixed(3);
    svgEl.appendChild(postLabel);
  }

  function redraw() {
    const prev = model.get("prevalence");
    const sens = model.get("sensitivity");
    const spec = model.get("specificity");
    const posteriorSick    = bayesPosterior(prev, sens, spec);
    const posteriorHealthy = 1 - posteriorSick;
    const priorHealthy     = 1 - prev;

    posteriorBox.innerHTML =
      `<b>P(Enfermo \u2223 Test positivo)</b> = ${posteriorSick.toFixed(4)}`;

    svg.innerHTML = "";
    const axis = document.createElementNS("http://www.w3.org/2000/svg", "line");
    axis.setAttribute("x1", 30);
    axis.setAttribute("x2", 510);
    axis.setAttribute("y1", 190);
    axis.setAttribute("y2", 190);
    axis.setAttribute("stroke", "#999");
    svg.appendChild(axis);

    const legend = document.createElementNS("http://www.w3.org/2000/svg", "text");
    legend.setAttribute("x", 30);
    legend.setAttribute("y", 20);
    legend.setAttribute("font-size", "12");
    legend.setAttribute("fill", "#333");
    legend.textContent = "azul: previa  \u2022  naranja: posterior";
    svg.appendChild(legend);

    bar(svg, 60,  "Enfermo", prev, posteriorSick);
    bar(svg, 300, "Sano",    priorHealthy, posteriorHealthy);
  }

  for (const { key } of sliders) {
    model.on(`change:${key}`, () => {
      valueLabels[key].textContent = Number(model.get(key)).toFixed(3);
      redraw();
    });
  }
  redraw();
}
export default { render };
"""

_CSS = """
.bayes-anywidget {
  font-family: Inter, system-ui, sans-serif;
  padding: 12px 14px;
  border: 1px solid #e0e0e0;
  border-radius: 6px;
  background: #fafafa;
  max-width: 560px;
}
.bayes-anywidget .bayes-row {
  display: grid;
  grid-template-columns: 130px 1fr 60px;
  align-items: center;
  gap: 10px;
  margin-bottom: 6px;
  font-size: 13px;
}
.bayes-anywidget .bayes-row input[type="range"] { width: 100%; }
.bayes-anywidget .bayes-value { font-variant-numeric: tabular-nums; color: #555; }
.bayes-anywidget .bayes-posterior {
  margin: 10px 0 6px;
  font-size: 14px;
  color: #222;
}
.bayes-anywidget .bayes-chart { width: 100%; height: auto; }
"""


class BayesAnywidgetInput(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, frozen=True)

    settings: Settings = Settings()
    initial_prevalence: float = 0.01
    initial_sensitivity: float = 0.99
    initial_specificity: float = 0.95


class BayesAnywidget(anywidget.AnyWidget):
    _esm = _ESM
    _css = _CSS
    prevalence = traitlets.Float(0.01).tag(sync=True)
    sensitivity = traitlets.Float(0.99).tag(sync=True)
    specificity = traitlets.Float(0.95).tag(sync=True)


def build_bayes_anywidget(input_data: BayesAnywidgetInput) -> BayesAnywidget:
    return BayesAnywidget(
        prevalence=input_data.initial_prevalence,
        sensitivity=input_data.initial_sensitivity,
        specificity=input_data.initial_specificity,
    )
