function hexToRgb(hex) {
    const m = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
    return m ? { r: parseInt(m[1], 16), g: parseInt(m[2], 16), b: parseInt(m[3], 16) } : null;
}

function relativeLuminance(r, g, b) {
    return [r, g, b].reduce((acc, c, i) => {
        c /= 255;
        const lin = c <= 0.03928 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4);
        return acc + lin * [0.2126, 0.7152, 0.0722][i];
    }, 0);
}

function contrastRatio(hex1, hex2) {
    const c1 = hexToRgb(hex1);
    const c2 = hexToRgb(hex2);
    if (!c1 || !c2) return 21;
    const l1 = relativeLuminance(c1.r, c1.g, c1.b);
    const l2 = relativeLuminance(c2.r, c2.g, c2.b);
    const lighter = Math.max(l1, l2);
    const darker = Math.min(l1, l2);
    return (lighter + 0.05) / (darker + 0.05);
}

const darkInput = document.getElementById('color');
const lightInput = document.getElementById('bg_color');
const contrastWarning = document.getElementById('contrast-warning');
const imageInput = document.getElementById('image');
const imageWarning = document.getElementById('image-warning');

function updateContrastWarning() {
    contrastWarning.classList.toggle('d-none', contrastRatio(darkInput.value, lightInput.value) >= 3);
}

darkInput.addEventListener('input', updateContrastWarning);
lightInput.addEventListener('input', updateContrastWarning);

imageInput.addEventListener('change', () => {
    imageWarning.classList.toggle('d-none', imageInput.files.length === 0);
});
