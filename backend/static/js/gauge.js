// Classifies a predicted logS value and positions the gauge needle.
// Thresholds follow the common medicinal-chemistry solubility bands.

function classifySolubility(value) {
  if (value >= -0.5) return { label: "VERY SOLUBLE", color: "#7FBF6B" };
  if (value >= -2)   return { label: "SOLUBLE",      color: "#9FCB6B" };
  if (value >= -4)   return { label: "MODERATE",     color: "#FFB238" };
  if (value >= -6)   return { label: "POOR",         color: "#E3925A" };
  return                  { label: "INSOLUBLE",   color: "#E3675A" };
}

// Maps a logS value in [-11, 2] onto a 2%-98% gauge position.
function gaugePosition(value) {
  const clamped = Math.max(-11, Math.min(2, value));
  return ((clamped - -11) / (2 - -11)) * 96 + 2;
}

function updateGauge(value) {
  const cls = classifySolubility(value);
  const badge = document.getElementById("pred-badge");
  badge.textContent = cls.label;
  badge.style.color = cls.color;
  badge.style.borderColor = cls.color;
  badge.style.background = cls.color + "1a";

  document.getElementById("gauge-needle").style.left = gaugePosition(value) + "%";
  return cls;
}
